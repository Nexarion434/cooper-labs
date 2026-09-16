#!/usr/bin/env python3
"""Build a Cooper Labs internal document from a description, not by hand.

    python3 build_doc.py doc.json out.html            # writes the HTML and prints the PDF name to use
    python3 build_doc.py doc.json out.html --pdf      # ... and renders the PDF next to it, then checks it
    python3 build_doc.py --example > doc.json         # an annotated description to start from

Everything that repeats is computed: page numbers and `NN / NN`, the Contents
page (from the block tags, when the document has five content pages or more,
or `"contents": true`), the version, classification and subject in the cover,
every running head, the back cover and the file name. Titles and headings get
Title Case and their `*italic phrase*`.

The description (JSON, or a Python dict passed to `build()`):

    class          proposal | case-study | spec | post-mortem | memo | guide | report
    subject        "Parallel MCP server"                      -> running head, file name
    title          "Ship the MCP server *before the CLI.*"   (*...* marks the accent phrase; in the Object system it stays in ink)
    standfirst     one sentence; kicker (optional, default "<Class> · <subject>")
    version        "v0.1"; classification Confidential | Internal; status Draft | Final
    date           "2026-09-09"; owner "Noah, Cooper Labs"; cover "01" (the render as a plate across the top of the cover, the default; "02" the halftone) | "dark" (plain ink, white type)
    back           "05" (the render as the plate of the back cover, the default) | "dark" (plain ink)
    contents       "auto" (default) | true | false; contents_intro (the "How to read" text, optional)
    versions       [["v0.1", "2026-09-09", "First draft"], ...]   -> the Versions table on the Contents page
    pages          [{"name": "Analysis", "blocks": [ ... ]}]
    flow           true (default) | false

The blocks flow (0.6.0): a page in the description is a group of blocks, not a
sheet. Every block is measured in Chromium and the sheets are filled to the
footer, so a part that ends a third of the way down is followed by the next one
on the same sheet instead of leaving the rest white; a block that does not fit
is cut at an item boundary and its label repeated with `· cont.`. Pages of
their own (divider, statement, hero, prose, plate, wide) keep a sheet to
themselves, `"break": true` on a page starts a new sheet, and `"flow": false`
restores one sheet per described page. Without Playwright the flow is skipped.

A block is a row of the margin grid: `tag` and `source` in the margin column
(200 wide), the rest in the reading column; a block without a tag spans the
measure. `specimen` ("03") puts a square crop of that render in the margin,
with `caption` under it. `toc` (false to keep the block out of the Contents
page, or a string to name its entry). In this order when given as keys: heading
(string, or {"text", "suffix"}), body (string or list), bullets ([[term,
text], ...]), table ({"cols": [[label, width | null], ...], "rows": [[...]],
"mono": [col indexes], "strong": [...], "highlight": row index | null, "head":
true}), figures ([[number, key], ...]), reco ([title, body]). For another
order, give `main` as a list of one-key objects.

Page styles (0.5.0). More block items, in the reading column:
    cols       {"columns": [{"head": "B · Convex fee", "bullets": [...] | "body": "...", "verdict": "Recommended."}, ...]}
    timeline   {"steps": [{"date": "10 Sep", "title": "...", "text": "...", "past": true}, ...], "phases": ["Review", ...]}
    chart      {"type": "bar", "labels": [...], "series": [{"name": "...", "values": [...], "soft": true}], "max": 100, "unit": "%"}
               {"type": "line", "labels": [...], "values": [...], "max": 100, "unit": "%", "last": "71.2%"}
    matrix     {"cols": ["Low impact", ...], "rows": [{"key": "Likely", "cells": [{"title": "...", "text": "...", "hot": true}, ...]}]}
    defs       [[term, definition], ...]                       (glossary, two columns)
    flow       {"boxes": [{"x", "y", "w", "h", "title", "sub", "soft"}], "arrows": [{"from": [x, y], "to": [x, y], "label"}], "caption": "One module, *four states.*", "height": 400}
    checklist  [{"text": "...", "who": "Risk · 24 Sep", "done": true}, ...]
    signoff    [["Owner", "Noah, Protocol"], ...]
    code       {"text": "...", "keywords": ["uint256", "function"]}   (// comments are muted)
A block with `"step": "01"` shows the number in the margin instead of a tag.
Pages of their own, with `style` instead of `blocks` (`toc` names their line on the Contents page):
    divider    {"n": "02", "kicker": "Part two · Assessment", "title": "...", "standfirst": "...", "list": [["Sections", "..."], ...], "render": "04", "dark": false}
               (`render` lays that render as a plate across the top 700 px; `n` is kept for the Contents page and not shown)
    statement  {"text": "... *turns a bank run into a queue.*", "who": "Summary · Protocol review"}
    hero       {"n": "38", "unit": "%", "kicker": "...", "body": "...", "figures": [[n, k], ...], "render": "03", "caption": "..."}   (`render`: a plate above the number)
    prose      {"lede": "...", "body": ["...", "..."], "signature": ["Noah, Protocol", "10 September 2026"]}
    plate      {"render": "03", "caption": "...", "blocks": [...]}      (the picture, then blocks)
    wide       {"heading": "...", "suffix": "...", "table": {...}, "foot": ["Source ...", "Values ..."]}
"""
import sys, os, re, json, html, pathlib, datetime, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brand, paginate, check_text

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE.parent
E = html.escape
CLASSES = brand.CLASSES
SMALL = {"a", "an", "the", "and", "but", "or", "nor", "for", "so", "yet", "as", "at", "by", "in", "of", "on", "to", "up", "vs", "via", "per", "from", "into", "onto", "over", "with", "under", "than", "that", "its"}


# ---------------------------------------------------------------- text helpers
def _cap(w):
    lead = re.match(r"^[*(\"']*", w).group(0)
    rest = w[len(lead):]
    if not any(c.isupper() for c in rest):
        rest = rest[:1].upper() + rest[1:]
    rest = re.sub(r"([-‑])([a-z])", lambda m: m.group(1) + m.group(2).upper(), rest)
    return lead + rest


def title_case(s):
    """Title Case as Noah likes it: every word capitalised except short connectors; first and last always."""
    words = s.split(" ")
    out = []
    for i, w in enumerate(words):
        core = w.strip("*()?.,:;!\"'")
        edge = i == 0 or i == len(words) - 1 or (i > 0 and words[i - 1].endswith((":", ".", "?", "!")))
        out.append(w if core.lower() in SMALL and not edge else _cap(w))
    return " ".join(out)


def EM(s):
    """Escape, then turn *phrase* into <em>phrase</em>: the italic signature."""
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", E(s))


def long_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


def short_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%b %Y')}"


def slug(s):
    return "-".join(w for w in re.sub(r"[^A-Za-z0-9]+", " ", title_case(s.replace("*", ""))).split())


# ---------------------------------------------------------------- HTML pieces
def cover_ground(n):
    """light or dark, from the catalogue of renders."""
    try:
        with open(ASSETS / "img" / "catalogue.json", encoding="utf-8") as fh:
            return {e["id"]: e.get("ground", "light") for e in json.load(fh)["images"]}.get(f"{int(n):02d}", "light")
    except Exception:
        return "light"


def cover(d, A):
    meta = [("Date", long_date(d["date"])), ("Classification", d["classification"]), ("Status", d["status"]), ("Owner", d["owner"])]
    m = "".join(f'<div><div class="k">{E(k)}</div><div class="v">{E(v)}</div></div>' for k, v in meta)
    plain_dark = str(d["cover"]).lower() in ("dark", "none")      # the typographic cover: plain ink ground, no render
    dark = plain_dark or cover_ground(d["cover"]) == "dark"
    logo = brand.LOGO_W if dark else brand.LOGO_B
    img = "" if plain_dark else f'''  <div class="cover__img" style="background-image:url('{A}{brand.RENDERS}/{int(d["cover"]):02d}.jpg')"></div>
  <div class="cover__fade"></div>
'''
    return f'''<!-- ========================= COVER ========================= -->
<section class="cover{" cover--dark" if dark else ""}{" cover--texture" if not plain_dark and int(d["cover"]) == 2 else ""}">
{img}
  <div class="cover__top">
    <img class="cover__logo" src="{A}{logo}" alt="{brand.NAME}">
    <div class="cover__conf">{E(d["classification"])} · {E(d["version"])}</div>
  </div>
  <div class="cover__bottom">
    <div class="cover__kicker">{E(d["kicker"])}</div>
    <div class="cover__title">{EM(title_case(d["title"]))}</div>
    <div class="cover__stand">{E(d["standfirst"])}</div>
    <div class="cover__rule"></div>
    <div class="cover__meta">{m}</div>
    <div class="cover__notice">{E(d["notice"])}</div>
  </div>
</section>
'''


def back(d, A):
    """The back cover: the render as a plate (`back: "05"`; `back: "dark"` for plain ink), the tagline and the links under it."""
    m = "".join(f'<div><div class="k">{E(k)}</div><div class="v">{E(v)}</div></div>' for k, v in brand.LINKS)
    m += f'<div><div class="k">This document</div><div class="v">{E(d["class_label"])} · {E(d["version"])} · {E(short_date(d["date"]))}</div></div>'
    r = str(d.get("back", "05")).lower()
    dark = r in ("dark", "none")
    img = "" if dark else f'''  <div class="cover__img" style="background-image:url('{A}{brand.RENDERS}/{int(r):02d}.jpg')"></div>
'''
    return f'''<!-- ======================= BACK COVER ======================= -->
<section class="cover back{" cover--dark" if dark else ""}">
{img}  <div class="cover__top">
    <img class="cover__logo" src="{A}{brand.LOGO_W if dark else brand.LOGO_B}" alt="{brand.NAME}">
    <div class="cover__conf">{E(d["classification"])} · {E(d["version"])}</div>
  </div>
  <div class="cover__bottom">
    <div class="back__tagline">{brand.TAGLINE_HTML}</div>
    <div class="cover__rule"></div>
    <div class="cover__meta">{m}</div>
    <div class="cover__notice">{E(d["notice"])} · © {d["date"][:4]} {brand.COPYRIGHT}</div>
  </div>
</section>
'''


def head_html(head, n):
    return f'  <div class="pagehead"><div class="pagehead__meta">{E(head)}</div><div class="pagehead__num">{n:02d}</div></div>\n'


def foot_html(n, total):
    return f'  <div class="pagefoot"><div class="pagefoot__meta">{brand.FOOTER}</div><div class="pagefoot__page">{n:02d} / {total:02d}</div></div>\n'


def page(name, head, n, total, blocks, raw=None, dark=False, before=""):
    """A sheet: the running head, either a stack of blocks or a raw composition, the footer."""
    inner = f'  <div class="content">\n{"".join(blocks)}  </div>\n' if raw is None else raw
    return f'''<!-- ===================== PAGE · {E(name.upper())} ===================== -->
<section class="page{" page--dark" if dark else ""}">
{'  <div class="back__glow"></div>' + chr(10) if dark else ""}{head_html(head, n)}{before}{inner}{foot_html(n, total)}</section>
'''


def block_html(tag, main, source=None, step=None, specimen=None, caption=None, A=""):
    spec = (f'<div class="specimen" style="background-image:url(\'{A}{brand.RENDERS}/{int(specimen):02d}.jpg\')"></div>' if specimen else "") + (f'<div class="specimen__cap">{E(caption)}</div>' if specimen and caption else "")
    margin = (f'<div class="step__n">{E(str(step))}</div>' if step else "") + spec + (f'<div class="tag">{E(tag)}</div>' if tag else "") + (f'<div class="source">{E(source)}</div>' if source else "")
    return f'''    <div class="block">
      <div class="block__margin">{margin}</div>
      <div class="block__main">
{main}      </div>
    </div>
'''


def heading(t, suffix=None):
    s = f'<span class="heading__suffix">{E(suffix)}</span>' if suffix else ""
    return f'        <div class="heading">{EM(title_case(t))}{s}</div>\n'


def body(t):
    return "".join(f'        <div class="body">{E(p)}</div>\n' for p in ([t] if isinstance(t, str) else t))


def bullets(items):
    rows = "".join(f'          <div class="bullet"><div class="bullet__dot"></div><div><div class="bullet__term">{E(t)}</div><div class="bullet__text">{E(x)}</div></div></div>\n' for t, x in items)
    return f'        <div class="bullets">\n{rows}        </div>\n'


def table(cols, rows, mono=(), strong=(), highlight=None, head=True):
    def w(c):
        return f' style="width:{c[1]}px"' if isinstance(c[1], int) else ""
    out = f'        <table class="table{"" if head else " table--plain"}">\n'
    if head:
        out += "          <tr>" + "".join(f"<th{w(c)}>{E(c[0])}</th>" for c in cols) + "</tr>\n"
    for i, r in enumerate(rows):
        tds = ""
        for j, v in enumerate(r):
            cls = " ".join(x for x in [("mono" if j in mono else ""), ("strong" if j in strong else "")] if x)
            tds += f'<td{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}{w(cols[j]) if i == 0 and not head else ""}>{E(v)}</td>'
        out += f'          <tr{" class=%shighlight%s" % (chr(34), chr(34)) if highlight == i else ""}>{tds}</tr>\n'
    return out + "        </table>\n"


def figures(items):
    f = "".join(f'          <div class="figure"><div class="figure__n">{E(str(n))}</div><div class="figure__k">{E(k)}</div></div>\n' for n, k in items)
    return f'        <div class="figures">\n{f}        </div>\n'


def reco(t, b):
    return f'        <div class="reco"><div class="reco__title">{E(t)}</div><div class="reco__body">{E(b)}</div></div>\n'


# ---------------------------------------------------------------- page styles (0.5.0)
def cols(v):
    out = '        <div class="cols">\n'
    for c in v["columns"]:
        out += "          <div>\n" + (f'            <div class="cols__head">{E(c["head"])}</div>\n' if c.get("head") else "")
        out += (heading(c["heading"]) if c.get("heading") else "") + (body(c["body"]) if c.get("body") else "") + (bullets(c["bullets"]) if c.get("bullets") else "")
        out += (f'            <div class="verdict">{E(c["verdict"])}</div>\n' if c.get("verdict") else "") + "          </div>\n"
    return out + "        </div>\n"


def timeline(v):
    steps = "".join(f'            <div class="tl__step{" tl__step--past" if st.get("past") else ""}"><div class="tl__date">{E(st["date"])}</div><div class="tl__title">{E(st["title"])}</div><div class="tl__text">{E(st.get("text", ""))}</div></div>\n' for st in v["steps"])
    phases = ("          <div class=\"tl__phase\">" + "".join(f"<div>{E(x)}</div>" for x in v["phases"]) + "</div>\n") if v.get("phases") else ""
    return f'        <div class="tl">\n          <div class="tl__row">\n{steps}          </div>\n{phases}        </div>\n'


def chart(v):
    W, x0, y0 = 530, 30, 10
    mx = v.get("max", 100); unit = v.get("unit", "")
    labels = v["labels"]
    if v.get("type", "bar") == "bar":
        H = v.get("height", 220); ph = H - y0 - 24; pw = W - x0 - 10
        out = f'<svg class="chart" viewBox="0 0 {W} {H}">'
        for g in (0, 25, 50, 75):
            y = y0 + ph - ph * g / 100
            out += f'<line class="axis" x1="{x0}" y1="{y:.1f}" x2="{W - 10}" y2="{y:.1f}"/><text x="0" y="{y + 3:.1f}">{round(mx * g / 100)}{E(unit)}</text>'
        bw = pw / len(labels); series = v["series"]
        for i, lab in enumerate(labels):
            x = x0 + i * bw + 6
            for k, sr in enumerate(series):
                val = sr["values"][i]; h = ph * val / mx
                w = (bw - 12) if sr.get("soft") else (bw - 12) / 2
                out += f'<rect class="bar{" bar--soft" if sr.get("soft") else ""}" x="{x:.1f}" y="{y0 + ph - h:.1f}" width="{w:.1f}" height="{h:.1f}"/>'
            out += f'<text x="{x + (bw - 12) / 2:.1f}" y="{H - 6}" text-anchor="middle">{E(str(lab))}</text>'
        out += f'<line class="base" x1="{x0}" y1="{y0 + ph}" x2="{W - 10}" y2="{y0 + ph}"/></svg>\n'
        legend = "".join(f'<span><i{" class=%ssoft%s" % (chr(34), chr(34)) if sr.get("soft") else ""}></i>{E(sr["name"])}</span>' for sr in series)
        return f"        {out}        <div class=\"legend\">{legend}</div>\n"
    H = v.get("height", 150); ph = H - y0 - 30; pw = W - x0 - 10
    out = f'<svg class="chart" viewBox="0 0 {W} {H}">'
    for g in (0, 50, 100):
        y = y0 + ph - ph * g / 100
        out += f'<line class="axis" x1="{x0}" y1="{y:.1f}" x2="{W - 10}" y2="{y:.1f}"/><text x="0" y="{y + 3:.1f}">{round(mx * g / 100)}{E(unit)}</text>'
    vals = v["values"]; pts = []
    for i, val in enumerate(vals):
        x = x0 + i * pw / max(len(vals) - 1, 1); y = y0 + ph - ph * val / mx; pts.append((x, y))
    out += '<polyline class="line" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>'
    x, y = pts[-1]
    out += f'<circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="3"/><text class="val" x="{x - 4:.1f}" y="{y - 8:.1f}" text-anchor="end">{E(v.get("last", str(vals[-1]) + unit))}</text>'
    for i, lab in enumerate(labels):
        out += f'<text x="{pts[i][0]:.1f}" y="{H - 6}" text-anchor="middle">{E(str(lab))}</text>'
    out += f'<line class="base" x1="{x0}" y1="{y0 + ph}" x2="{W - 10}" y2="{y0 + ph}"/></svg>\n'
    return f"        {out}"


def matrix(v):
    out = '        <div class="matrix">\n          <div class="matrix__h"></div>' + "".join(f'<div class="matrix__h">{E(c)}</div>' for c in v["cols"]) + "\n"
    for r in v["rows"]:
        out += f'          <div class="matrix__k">{E(r["key"])}</div>' + "".join(f'<div class="matrix__cell{" hot" if c.get("hot") else ""}"><b>{E(c["title"])}</b>{E(c.get("text", ""))}</div>' for c in r["cells"]) + "\n"
    return out + "        </div>\n"


def defs(v):
    return '        <div class="defs">\n' + "".join(f'          <div class="def"><div class="def__t">{E(t)}</div><div class="def__d">{E(x)}</div></div>\n' for t, x in v) + "        </div>\n"


def flow(v):
    out = f'<svg class="flow" viewBox="0 0 530 {v.get("height", 400)}">'
    for b in v["boxes"]:
        out += f'<rect class="{"soft" if b.get("soft") else ""}" x="{b["x"]}" y="{b["y"]}" width="{b["w"]}" height="{b["h"]}"/><text x="{b["x"] + 12}" y="{b["y"] + 22}">{E(b["title"])}</text>'
        if b.get("sub"):
            out += f'<text class="m" x="{b["x"] + 12}" y="{b["y"] + 38}">{E(b["sub"])}</text>'
    for a in v.get("arrows", ()):
        (x1, y1), (x2, y2) = a["from"], a["to"]
        out += f'<path d="M{x1},{y1} L{x2},{y2}"/><circle class="dot" cx="{x2}" cy="{y2}" r="2.5"/>'
        if a.get("label"):
            out += (f'<text class="m" x="{(x1 + x2) / 2}" y="{y1 - 6}" text-anchor="middle">{E(a["label"])}</text>' if y1 == y2 else f'<text class="m" x="{x1 + 8}" y="{(y1 + y2) / 2 + 3}">{E(a["label"])}</text>')
    if v.get("caption"):
        cap = re.sub(r"\*(.+?)\*", r"<tspan>\1</tspan>", E(v["caption"]))
        out += f'<text class="em" x="0" y="{v.get("height", 400) - 20}">{cap}</text>'
    return f"        {out}</svg>\n"


def checklist(v):
    return "".join(f'        <div class="check"><div class="check__box{" on" if c.get("done") else ""}"></div><div class="check__t">{E(c["text"])}</div><div class="check__who">{E(c.get("who", ""))}</div></div>\n' for c in v)


def signoff(v):
    return '        <div class="sign">' + "".join(f'<div><div class="k">{E(k)}</div><div class="v">{E(x) if x else "&nbsp;"}</div></div>' for k, x in v) + "</div>\n"


def code(v):
    text = v["text"] if isinstance(v, dict) else v
    kws = v.get("keywords", ()) if isinstance(v, dict) else ()
    lines = []
    for line in text.split("\n"):
        head, sep, comment = line.partition("//")
        head = E(head)
        for k in kws:
            head = re.sub(r"(?<![\w])" + re.escape(k) + r"(?![\w])", f'<span class="k">{k}</span>', head)
        lines.append(head + (f'<span class="c">//{E(comment)}</span>' if sep else ""))
    return '        <div class="code">' + "\n".join(lines) + "</div>\n"


def item_html(key, v):
    if key == "cols":
        return cols(v)
    if key == "timeline":
        return timeline(v)
    if key == "chart":
        return chart(v)
    if key == "matrix":
        return matrix(v)
    if key == "defs":
        return defs(v)
    if key == "flow":
        return flow(v)
    if key == "checklist":
        return checklist(v)
    if key == "signoff":
        return signoff(v)
    if key == "code":
        return code(v)
    if key == "meta":
        return f'        <div class="step__meta">{E(v)}</div>\n'
    if key == "space":
        return f'        <div style="height:{int(v)}px"></div>\n'
    if key == "heading":
        return heading(v["text"], v.get("suffix")) if isinstance(v, dict) else heading(v)
    if key == "body":
        return body(v)
    if key == "bullets":
        return bullets(v)
    if key == "table":
        return table(v["cols"], v["rows"], mono=tuple(v.get("mono", ())), strong=tuple(v.get("strong", ())), highlight=v.get("highlight"), head=v.get("head", True))
    if key == "figures":
        return figures(v)
    if key == "reco":
        return reco(v[0], v[1])
    raise ValueError(f"unknown block item: {key}")


ORDER = ("heading", "body", "bullets", "table", "figures", "reco", "cols", "timeline", "chart", "matrix", "defs", "flow", "checklist", "signoff", "code", "meta")


_A = [""]      # the asset prefix, set by build() before the blocks are written
LAST = {}      # what the last build did: flowed, described pages, sheets


def block_from(b, main=None, cont=False):
    """The HTML of one block. `main` re-uses measured items; `cont` is a piece carried over to the next sheet."""
    if main is None:
        if "main" in b:
            main = "".join(item_html(k, v) for item in b["main"] for k, v in item.items())
        else:
            main = "".join(item_html(k, b[k]) for k in ORDER if k in b)
        if b.get("step"):
            main = f'        <div class="step">\n{main}        </div>\n'
    if cont:
        tag = b.get("tag")
        return block_html(f"{tag} · cont." if tag else None, main, A=_A[0])
    return block_html(b.get("tag"), main, b.get("source"), b.get("step"), b.get("specimen"), b.get("caption"), A=_A[0])


def style_page(pg, head, n, total, A):
    """A page of its own: divider, statement, hero, prose, plate, wide."""
    st = pg["style"]
    if st == "divider":
        lst = ("          <div class=\"divider__list\">" + "".join(f'<div><div class="k">{E(k)}</div><div class="v">{E(v)}</div></div>' for k, v in pg["list"]) + "</div>\n") if pg.get("list") else ""
        raw = (f'  <div class="divider">\n    <div class="divider__n">{E(str(pg["n"]))}</div>\n    <div class="divider__kicker">{E(pg["kicker"])}</div>\n'
               f'    <div class="divider__title">{EM(title_case(pg["title"]))}</div>\n' + (f'    <div class="divider__stand">{E(pg["standfirst"])}</div>\n' if pg.get("standfirst") else "") +
               ('    <div class="divider__rule"></div>\n' + lst if lst else "") + "  </div>\n")
        before = f'''  <div class="page__img" style="background-image:url('{A}{brand.RENDERS}/{int(pg["render"]):02d}.jpg')"></div>
''' if pg.get("render") else ""
        return page(pg["name"], head, n, total, None, raw=raw, dark=pg.get("dark", False), before=before)
    if st == "statement":
        raw = (f'  <div class="statement">\n    <div class="statement__mark"></div>\n    <div class="statement__text">{EM(pg["text"])}</div>\n'
               f'    <div class="statement__who">{E(pg.get("who", ""))}</div>\n  </div>\n')
        return page(pg["name"], head, n, total, None, raw=raw)
    if st == "hero":
        row = ""
        if pg.get("body") or pg.get("figures"):
            row = '    <div class="hero__row">\n' + (f'      <div class="body">{E(pg["body"])}</div>\n' if pg.get("body") else "") + (("      " + figures(pg["figures"]).strip() + "\n") if pg.get("figures") else "") + "    </div>\n"
        plate = (f'''    <div class="hero__img" style="background-image:url('{A}{brand.RENDERS}/{int(pg["render"]):02d}.jpg')"></div>
''' + (f'    <div class="hero__cap">{E(pg["caption"])}</div>\n' if pg.get("caption") else "")) if pg.get("render") else ""
        raw = (f'  <div class="hero">\n' + plate + f'    <div class="hero__n">{E(str(pg["n"]))}<em>{E(pg.get("unit", ""))}</em></div>\n    <div class="hero__k">{E(pg["kicker"])}</div>\n'
               '    <div class="hero__rule"></div>\n' + row + "  </div>\n")
        return page(pg["name"], head, n, total, None, raw=raw)
    if st == "prose":
        paras = "<br><br>".join(E(x) for x in ([pg["body"]] if isinstance(pg["body"], str) else pg["body"]))
        sig = (f'    <div class="prose__sig"><span>{E(pg["signature"][0])}</span><span>{E(pg["signature"][1])}</span></div>\n') if pg.get("signature") else ""
        raw = f'  <div class="prose">\n    <div class="prose__lede">{EM(pg["lede"])}</div>\n    <div class="body">{paras}</div>\n{sig}  </div>\n'
        return page(pg["name"], head, n, total, None, raw=raw)
    if st == "plate":
        before = (f'  <div class="plate"><img src="{A}{brand.RENDERS}/{int(pg.get("render", pg.get("illustration", 1))):02d}.jpg" alt="">'
                  + (f'<div class="plate__cap">{E(pg["caption"])}</div>' if pg.get("caption") else "") + "</div>\n")
        return page(pg["name"], head, n, total, [block_from(b) for b in pg.get("blocks", [])], before=before)
    if st == "wide":
        t = pg["table"]
        foot = ('    <div class="wide__foot">' + "".join(f"<span>{E(x)}</span>" for x in pg["foot"]) + "</div>\n") if pg.get("foot") else ""
        raw = ('  <div class="wide">\n' + (heading(pg["heading"], pg.get("suffix")).replace("        ", "    ") if pg.get("heading") else "") + '    <div style="height:14px"></div>\n' +
               table(t["cols"], t["rows"], mono=tuple(t.get("mono", ())), strong=tuple(t.get("strong", ())), highlight=t.get("highlight"), head=t.get("head", True)).replace("        ", "    ") + foot + "  </div>\n")
        return page(pg["name"], head, n, total, None, raw=raw)
    sys.exit(f"page {n}: unknown style {st!r}")


# ---------------------------------------------------------------- the sheets
def lay_out(d, head):
    """The sheets, in order. The compositions keep one each; the blocks are poured into the rest."""
    seq, runs = [], []
    for pg in d["pages"]:
        if pg.get("style"):
            seq.append({"kind": "style", "pg": pg}); continue
        if not seq or seq[-1]["kind"] != "run":
            runs.append([]); seq.append({"kind": "run", "i": len(runs) - 1})
        for j, b in enumerate(pg["blocks"]):
            runs[seq[-1]["i"]].append((pg, b, j == 0 and bool(pg.get("break"))))
    flat = [x for run in runs for x in run]
    htmls = [block_from(b) for _, b, _ in flat]
    m = paginate.measure(htmls, ASSETS / brand.CSS, head_html(head, 2), foot_html(2, 9)) if d.get("flow", True) and flat else None
    packed = []
    if m:
        units = [paginate.Unit(h, mm["h"], mm["kids"], mm["margin_h"], meta={"b": b, "name": pg["name"], "break": brk},
                               make=lambda meta, main, cont: block_from(meta["b"], main, cont))
                 for (pg, b, brk), h, mm in zip(flat, htmls, m["blocks"])]
        i = 0
        for run in runs:
            packed.append(paginate.pack(units[i:i + len(run)], m["avail"], m["gap"])); i += len(run)
    out = []
    for s in seq:
        if s["kind"] == "style":
            out.append(s); continue
        run = runs[s["i"]]
        if m:
            for sheet in packed[s["i"]]:
                out.append({"kind": "blocks", "name": sheet[0].meta["name"], "html": [u.html for u in sheet],
                            "blocks": [u.meta["b"] for u in sheet if not u.cont]})
        else:                                             # no Playwright, or "flow": false: one sheet per described page
            groups = []
            for pg, b, _ in run:
                if not groups or groups[-1]["pg"] is not pg:
                    groups.append({"pg": pg, "bs": []})
                groups[-1]["bs"].append(b)
            for g in groups:
                out.append({"kind": "blocks", "name": g["pg"]["name"], "html": [block_from(b) for b in g["bs"]], "blocks": g["bs"]})
    return out, bool(m)


def sheet_name(sh):
    return sh["name"] if sh["kind"] == "blocks" else sh["pg"].get("toc") or sh["pg"].get("name", "")


# ---------------------------------------------------------------- the document
def contents_rows(sheets, first_page_number):
    rows, n = [], 0
    for i, sh in enumerate(sheets):
        num = first_page_number + i
        if sh["kind"] == "style":
            pg = sh["pg"]
            if pg.get("toc"):
                n += 1
                rows.append([f"{n:02d}", pg["toc"], f"{num:02d}", pg.get("kicker", pg["toc"])])
            continue
        for b in sh["blocks"]:
            tag, toc = b.get("tag"), b.get("toc", True)
            if not tag or toc is False:
                continue
            label = toc if isinstance(toc, str) else tag
            m = re.match(r"Appendix\s+([A-Z])\b", tag)
            if m:
                rows.append([m.group(1), label if isinstance(toc, str) else (tag.split("·", 1)[1].strip() if "·" in tag else tag), f"{num:02d}", tag])
            else:
                n += 1
                rows.append([f"{n:02d}", label, f"{num:02d}", tag])
    return rows


def build(d, out_html, relative=False):
    d = dict(d)
    d["class_label"] = CLASSES[d["class"]]
    d.setdefault("kicker", f"{d['class_label']} · {d['subject']}")
    d.setdefault("notice", brand.NOTICE)
    A = "../" if relative else ASSETS.as_posix() + "/"
    _A[0] = A
    head = f"{d['class_label']} · {d['subject']} · {d['classification']} · {d['version']}"
    sheets, flowed = lay_out(d, head)
    LAST.update(flowed=flowed, described=len(d["pages"]), sheets=len(sheets))
    want_contents = d.get("contents", "auto")
    want_contents = len(sheets) >= 5 if want_contents == "auto" else bool(want_contents)
    total = 1 + (1 if want_contents else 0) + len(sheets) + 1     # every sheet counts: cover, contents, pages, back
    sections = [cover(d, A)]
    n = 2
    if want_contents:
        rows = contents_rows(sheets, n + 1)
        if len(rows) > 12:
            rows = [[f"{i + 1:02d}", sheet_name(sh), f"{n + 1 + i:02d}", ""] for i, sh in enumerate(sheets)]
        toc = table([("§", 48), ("Section", None), ("Page", 60)], [r[:3] for r in rows], mono=(0, 2), head=False)
        for r in rows:                                   # data-tag lets check_pdf verify each entry
            toc = re.sub(r'<tr>(<td[^>]*>' + re.escape(E(r[0])) + r'</td><td[^>]*>' + re.escape(E(r[1])) + r'</td>)', f'<tr data-tag="{E(r[3])}">\\1', toc, count=1)
        blocks = [block_html("Contents", heading("In this document") + toc)]
        intro = d.get("contents_intro", "Read the summary and the recommendation first; they are written to stand alone. The rest is the evidence, kept for whoever needs to check a number. Every table names its source and as-of date in the margin.")
        blocks.append(block_html("How to read", body(intro)))
        if d.get("versions"):
            vrows = [[v, short_date(dt) if re.match(r"\d{4}-\d\d-\d\d", dt) else dt, ch] for v, dt, ch in d["versions"]]
            blocks.append(block_html("Versions", table([("Version", 80), ("Date", 110), ("Change", None)], vrows, mono=(0, 1)), "Versions are recorded here and on the cover."))
        sections.append(page("Contents", head, n, total, blocks))
        n += 1
    for sh in sheets:
        sections.append(style_page(sh["pg"], head, n, total, A) if sh["kind"] == "style" else page(sh["name"], head, n, total, sh["html"]))
        n += 1
    sections.append(back(d, A))
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{brand.NAME} · {E(d["class_label"])} · {E(d["subject"])}</title>
<link rel="stylesheet" href="{A}{brand.CSS}">
</head>
<body>

{"".join(sections)}
</body>
</html>
'''
    out = pathlib.Path(out_html)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    pdf_name = f"{brand.FILE_PREFIX}-{slug(d['class_label'])}-{slug(d['subject'])}-{d['version']}.pdf"
    return out, pdf_name, total


def _example():
    """The spec example shipped in assets/examples, so `--example` and the file never drift."""
    with open(ASSETS / "examples" / "spec.json", encoding="utf-8") as fh:
        return json.load(fh)


EXAMPLE = _example()


def main():
    args = [a for a in sys.argv[1:] if a != "--no-lint"]
    if "--example" in args:
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False)); return
    if len(args) < 2:
        print(__doc__); sys.exit(1)
    with open(args[0], encoding="utf-8") as fh:
        d = json.load(fh)
    check_text.gate(d, args[0], "--no-lint" in sys.argv)
    out, pdf_name, total = build(d, args[1], relative="--relative" in args)
    how = f", {LAST['described']} described pages flowed into {LAST['sheets']}" if LAST.get("flowed") else ", not flowed (no Playwright, or \"flow\": false)"
    print(f"-> {out}  ({total} sheets{how})  PDF name: {pdf_name}")
    if "--pdf" in args:
        pdf = out.with_name(pdf_name)
        subprocess.run([sys.executable, str(HERE / "render_pdf.py"), str(out), str(pdf)], check=True)
        sys.exit(subprocess.run([sys.executable, str(HERE / "check_pdf.py"), str(pdf), "--html", str(out)]).returncode)


if __name__ == "__main__":
    main()
