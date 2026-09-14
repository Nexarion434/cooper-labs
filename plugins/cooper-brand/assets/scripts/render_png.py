#!/usr/bin/env python3
"""Render every social canvas of a Cooper Labs HTML file to PNG.

    python3 render_png.py social.html outdir/            # one PNG per .canvas, at the canvas size (1200 x 675, 2000 x 800, 2400 x 1200...)
    python3 render_png.py social.html outdir/ --scale 2  # twice the size
    python3 render_png.py social.html outdir/ --only dao-treasury-report-2026-08
    python3 render_png.py social.html outdir/ --only "governance-*"      # --only takes a glob, repeatable

Each `.canvas` element is written as `<outdir>/<data-name>.png`. After each
canvas the script maps the render's `subject` box (catalogue.json) through
the frame in use and warns when a text block lands on it: a warning, not a
failure, with the `frame.py` command that shows the crop; a canvas carrying
`data-subject-ok` is not checked (the overlap was looked at and accepted).
Needs Python with
Playwright and Chromium (`pip install playwright && playwright install chromium`).
"""
import sys, os, re, json, fnmatch, pathlib, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fontcheck import JS_WEIGHTS, font_report

HERE = pathlib.Path(__file__).resolve().parent
CATALOGUE = HERE.parent / "img" / "catalogue.json"
TEXT_SELECTORS = ".post__kicker, .post__title, .xcover__line, .partner, .preview__logo, .thread__body, .banner__tag, .banner__k"
SIZE_KEYS = {(1200, 675): "1200x675", (1200, 630): "1200x630", (1500, 500): "1500x500", (2000, 800): "2000x800", (2400, 1200): "2400x1200", (1200, 627): "1200x627", (1080, 1080): "1080x1080",
             (1080, 1920): "1080x1920", (1600, 400): "1600x400", (600, 300): "600x300", (1500, 600): "1500x600", (2560, 1440): "2560x1440"}

# Runs in the page for one canvas: the geometry of the picture, the text boxes, the render number.
JS_INSPECT = """(el) => {
  const c = el.getBoundingClientRect();
  const rel = (r) => ({x: r.left - c.left, y: r.top - c.top, w: r.width, h: r.height});
  const bg = el.querySelector('.canvas__bg');
  let img = null, number = null;
  if (bg) {
    const im = bg.querySelector('img');
    let src = im ? (im.getAttribute('src') || '') : (getComputedStyle(bg).backgroundImage || '');
    const m = src.match(/renders\\/(\\d\\d)\\.jpg/);
    if (m) number = m[1];
    if (im) { img = rel(im.getBoundingClientRect()); }
    else if (number) {
      // background-size: cover, centred: the renders are 1841 x 1151
      const s = Math.max(c.width / 1841, c.height / 1151);
      const w = 1841 * s, h = 1151 * s;
      img = {x: (c.width - w) / 2, y: (c.height - h) / 2, w: w, h: h};
    }
  }
  // the bounds of the glyphs themselves (a Range), not of the box, which for a centred line spans the canvas
  const texts = Array.from(el.querySelectorAll('%s')).filter(t => t.offsetParent !== null || t.getClientRects().length).map(t => {
    const r = document.createRange(); r.selectNodeContents(t); const b = r.getBoundingClientRect();
    return Object.assign(rel(b.width && b.height ? b : t.getBoundingClientRect()), {sel: t.className.split(' ')[0]}); });
  return {w: c.width, h: c.height, number, img, texts};
}""" % TEXT_SELECTORS


def load_catalogue():
    try:
        with open(CATALOGUE, encoding="utf-8") as fh:
            return {e["id"]: e for e in json.load(fh)["images"]}
    except Exception:
        return {}


def overlap(a, b):
    """Intersection area of two boxes {x, y, w, h}."""
    x0, y0 = max(a["x"], b["x"]), max(a["y"], b["y"])
    x1, y1 = min(a["x"] + a["w"], b["x"] + b["w"]), min(a["y"] + a["h"], b["y"] + b["h"])
    return max(0, x1 - x0) * max(0, y1 - y0)


def text_zone_warnings(info, catalogue):
    """Warn when a text block covers the render's subject (the block), using the frame actually rendered."""
    if not info["number"] or not info["img"]:
        return []
    entry = catalogue.get(info["number"])
    if not entry or not entry.get("subject"):
        return []
    s, im = entry["subject"], info["img"]
    subj = {"x": im["x"] + im["w"] * s["x"] / 100, "y": im["y"] + im["h"] * s["y"] / 100, "w": im["w"] * s["w"] / 100, "h": im["h"] * s["h"] / 100}
    out = []
    for t in info["texts"]:
        if t["w"] < 4 or t["h"] < 4:
            continue
        inner = {"x": t["x"] + t["w"] * 0.02, "y": t["y"], "w": t["w"] * 0.96, "h": t["h"]}
        a = overlap(inner, subj)
        if a > 0.10 * subj["w"] * subj["h"] or a > 0.08 * inner["w"] * inner["h"]:
            key = SIZE_KEYS.get((round(info["w"]), round(info["h"])), f"{round(info['w'])}x{round(info['h'])}")
            out.append(f"text block .{t['sel']} sits on {s.get('what', 'the subject')} of render {info['number']} "
                       f"(overlap {round(100 * a / (subj['w'] * subj['h']))}% of it). Reframe or pick another number:\n"
                       f"      python3 {HERE / 'frame.py'} {info['number']} {key} --preview check-{info['number']}.png")
            break
    return out


async def run(src, outdir, scale, only):
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        sys.exit("playwright is required:  pip install playwright  &&  playwright install chromium")
    os.makedirs(outdir, exist_ok=True)
    catalogue = load_catalogue()
    warnings = 0
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 2600, "height": 2000}, device_scale_factor=scale)
        await page.goto(pathlib.Path(src).resolve().as_uri(), wait_until="networkidle")
        await page.evaluate("document.fonts.ready")
        await page.wait_for_timeout(400)
        weights = await page.evaluate(JS_WEIGHTS)
        n = 0
        for node in await page.query_selector_all(".canvas"):
            name = await node.get_attribute("data-name") or f"canvas-{n + 1}"
            if only and not any(fnmatch.fnmatch(name, pat) for pat in only):
                continue
            await node.screenshot(path=os.path.join(outdir, f"{name}.png"))
            print("PNG ->", os.path.join(outdir, f"{name}.png"))
            n += 1
            if await node.get_attribute("data-subject-ok") is not None:
                continue                                   # the overlap was looked at and accepted
            info = await node.evaluate(JS_INSPECT)
            for w in text_zone_warnings(info, catalogue):
                warnings += 1
                print(f"  ! {name}: {w}")
        await browser.close()
    print(font_report(weights))
    if n == 0:
        sys.exit("no canvas rendered")
    if warnings:
        print(f"{warnings} text-zone warning{'s' if warnings > 1 else ''}: look at the PNG before posting.")



def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)
    scale, only = 1, []
    if "--scale" in args:
        i = args.index("--scale"); scale = int(args[i + 1]); del args[i:i + 2]
    while "--only" in args:
        i = args.index("--only"); only.append(args[i + 1]); del args[i:i + 2]
    asyncio.run(run(args[0], args[1], scale, only))


if __name__ == "__main__":
    main()
