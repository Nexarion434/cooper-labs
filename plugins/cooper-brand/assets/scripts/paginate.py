#!/usr/bin/env python3
"""Flow the blocks of a document across sheets instead of one sheet per described page.

A description names pages; a reader sees sheets. Without this module the two are
the same thing, so a part that ends a third of the way down leaves the rest of
the sheet white and the next part starts overleaf. Here the blocks are measured
in Chromium with the real CSS and the real fonts, then poured: each sheet is
filled to the footer, the next block follows on the same sheet, and a block that
does not fit is cut at an item boundary with its label repeated as `· cont.`.

    from paginate import measure, pack
    m = measure([block_html, ...], css_path)        # None when Playwright is missing
    sheets = pack(units, m["avail"], m["gap"])      # -> [[unit, ...], ...]

Dividers, statements, heroes, prose, plates and wide tables keep a sheet of
their own: they are compositions, not stacks. A page described with
`"break": true` starts a new sheet, so an author can still say "this part
begins overleaf".

Needs Playwright and a Chromium build (the same pair render_pdf.py needs).
Without them `measure` returns None and the caller keeps one sheet per page.
"""
import os, json, pathlib, tempfile, asyncio

BREATH = 28          # px kept clear above the footer, so no block sits on it
MIN_PIECE = 150      # a cut piece is worth a cut only above this height
MIN_REST = 110       # ... and what follows it must be worth a continuation

JS = """() => {
  const ref = document.getElementById('ref');
  const rc = ref.querySelector('.content').getBoundingClientRect();
  const rf = ref.querySelector('.pagefoot').getBoundingClientRect();
  const mc = document.getElementById('mc');
  const cs = getComputedStyle(mc);
  const gap = parseFloat(cs.rowGap || cs.gap) || 0;
  const blocks = [...mc.children].map(b => {
    const br = b.getBoundingClientRect();
    const main = b.querySelector('.block__main');
    const margin = b.querySelector('.block__margin');
    const mr = main ? main.getBoundingClientRect() : null;
    return {
      h: br.height,
      margin_h: margin ? margin.getBoundingClientRect().height : 0,
      kids: mr ? [...main.children].map(c => ({top: c.getBoundingClientRect().top - mr.top, html: c.outerHTML})) : []
    };
  });
  return {avail: rf.top - rc.top, gap: gap, blocks: blocks};
}"""


def _doc(blocks_html, css_url, head_html, foot_html, W, H):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><link rel="stylesheet" href="{css_url}"></head>
<body style="margin:0">
<section class="page" id="ref" style="height:{H}px">
{head_html}  <div class="content"></div>
{foot_html}</section>
<section class="page" id="m" style="height:auto;overflow:visible">
{head_html}  <div class="content" id="mc">
{"".join(blocks_html)}  </div>
</section>
</body></html>
"""


async def _run(path, W, H):
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        return None
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch()
        except Exception:
            return None
        page = await browser.new_page(viewport={"width": W, "height": H})
        await page.goto(pathlib.Path(path).resolve().as_uri(), wait_until="networkidle")
        await page.evaluate("document.fonts.ready")
        await page.wait_for_timeout(200)
        out = await page.evaluate(JS)
        await browser.close()
        return out


def measure(blocks_html, css_path, head_html, foot_html, W=794, H=1123, where=None):
    """Heights of every block, and the height a sheet has for them. None without Playwright."""
    if not blocks_html:
        return None
    css_url = pathlib.Path(css_path).resolve().as_uri()
    d = tempfile.mkdtemp(prefix="measure-", dir=where)
    f = pathlib.Path(d) / "measure.html"
    f.write_text(_doc(blocks_html, css_url, head_html, foot_html, W, H), encoding="utf-8")
    try:
        out = asyncio.run(_run(f, W, H))
    except Exception:
        out = None
    finally:
        try:
            f.unlink(); os.rmdir(d)
        except OSError:
            pass
    if not out or not out.get("blocks"):
        return None
    out["avail"] = out["avail"] - BREATH
    return out


class Unit:
    """One block on its way to a sheet: its HTML, its height, and where it can be cut."""

    def __init__(self, html, h, kids, margin_h=0, meta=None, make=None, cont=False):
        self.html, self.h, self.kids, self.margin_h = html, h, kids, margin_h
        self.meta, self.make, self.cont = meta or {}, make, cont

    def split(self, room):
        """Cut at the last item boundary that fits in `room`. None when no cut is worth it."""
        if not self.make or len(self.kids) < 2:
            return None
        best = None
        for k in range(1, len(self.kids)):
            top = self.kids[k]["top"]
            if k == 1 and self.kids[0]["html"].startswith('<div class="heading"'):
                continue                                   # a heading never stays alone at the foot of a sheet
            piece = max(top, self.margin_h)
            rest = self.h - top
            if piece <= room and piece >= MIN_PIECE and rest >= MIN_REST:
                best = k
        if best is None:
            return None
        top = self.kids[best]["top"]
        first_html = self.make(self.meta, "".join(k["html"] for k in self.kids[:best]), self.cont)
        rest_html = self.make(self.meta, "".join(k["html"] for k in self.kids[best:]), True)
        first = Unit(first_html, max(top, self.margin_h), self.kids[:best], self.margin_h, self.meta, self.make, self.cont)
        rest_kids = [{"top": k["top"] - top, "html": k["html"]} for k in self.kids[best:]]
        rest = Unit(rest_html, self.h - top, rest_kids, 0, self.meta, self.make, True)
        return first, rest


def _heading_only(u):
    """A block that is nothing but a sub-heading: it belongs to what follows, never to the foot of a sheet."""
    return len(u.kids) == 1 and u.kids[0]["html"].startswith('<div class="heading"')


def pack(units, avail, gap):
    """Pour the units into sheets: fill each one, cut a block when the room is worth it."""
    sheets, cur, used = [], [], 0.0

    def add(u):
        nonlocal used
        used = used + u.h + (gap if cur else 0)
        cur.append(u)

    def close():
        nonlocal cur, used
        if cur:
            sheets.append(cur); cur, used = [], 0.0

    queue, i = list(units), 0
    while i < len(queue):
        j = i
        while j + 1 < len(queue) and _heading_only(queue[j]):
            j += 1
        group = queue[i:j + 1]                              # a heading and what it heads travel together
        if group[0].meta.get("break"):
            close()
        head_h = sum(u.h for u in group[:-1]) + gap * (len(group) - 1)   # the heads and the gap before the last block
        if used + (gap if cur else 0) + head_h + group[-1].h <= avail + 0.5:
            for u in group:
                add(u)
            i = j + 1; continue
        if cur:                                             # no room: cut the last block if the rest of the sheet is worth it
            room = avail - used - gap - head_h
            cut = group[-1].split(room) if room >= MIN_PIECE else None
            if cut:
                for u in group[:-1]:
                    add(u)
                add(cut[0]); close()
                queue[j] = cut[1]; i = j; continue
            close()
        for u in group[:-1]:                                # a fresh sheet
            add(u)
        u = group[-1]
        while True:
            if used + u.h + (gap if cur else 0) <= avail + 0.5:
                add(u); break
            room = avail - used - (gap if cur else 0)
            cut = u.split(room) if room >= MIN_PIECE else None
            if not cut:
                if cur:
                    close(); continue
                add(u); break                               # taller than a sheet and nowhere to cut: render_pdf warns
            add(cut[0]); close(); u = cut[1]
        i = j + 1
    close()
    return sheets
