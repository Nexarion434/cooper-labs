#!/usr/bin/env python3
"""Check the social canvases of a run before the PNGs go out.

    python3 check_png.py posts.html out/          # the HTML the PNGs were rendered from, and their folder
    python3 check_png.py posts.html out/ --only "blog-*"

Sibling of check_pdf.py. Opens the source HTML in Chromium and, for every
`.canvas` (or the ones matching --only):
  1. the PNG exists in the folder and its size matches the canvas class
     (1200 x 675, .canvas--x 2000 x 800, .canvas--para 2400 x 1200, .canvas--li,
     --sq, --story, --xhead, --forum, --mail, --notion, --deck, or a 2x of it);
  2. the post title stays on two lines at most at 1200 x 675 and 1200 x 627, a
     cover line on two, a thread sentence on three;
  3. no text block overlaps the logo;
  4. the logo under the title is centred (+-2 px);
  5. every text block is inside the canvas.
One line per canvas, `ok` or the list of failures; exit code 1 on any failure.
"""
import sys, os, fnmatch, pathlib, asyncio, struct

SIZES = {"canvas--x": (2000, 800), "canvas--para": (2400, 1200), "canvas--li": (1200, 627), "canvas--sq": (1080, 1080), "canvas--story": (1080, 1920), "canvas--preview": (1200, 630), "canvas--cover": (1500, 500),
         "canvas--xhead": (1500, 500), "canvas--forum": (1600, 400), "canvas--mail": (600, 300), "canvas--notion": (1500, 600), "canvas--deck": (1280, 720), "canvas--wallpaper": (2560, 1440)}
TEXT_SELECTORS = ".post__kicker, .post__title, .post__logo, .xcover__line, .xcover__logo, .partner, .preview__logo, .thread__n, .thread__body, .thread__k, .banner__tag, .banner__k"

JS = """(el) => {
  const c = el.getBoundingClientRect();
  const rel = (r) => ({x: r.left - c.left, y: r.top - c.top, w: r.width, h: r.height});
  const boxes = Array.from(el.querySelectorAll('%s')).filter(t => t.getClientRects().length).map(t => {
    const cs = getComputedStyle(t);
    return Object.assign(rel(t.getBoundingClientRect()), {sel: t.className.split(' ')[0], lh: parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.1, lines: t.getClientRects().length});
  });
  const icon = el.querySelector('.post__logo, .xcover__logo, .preview__logo');
  const badge = el.querySelector('.post__logo, .xcover__logo, .preview__logo');
  return {w: c.width, h: c.height, cls: el.className, boxes,
          icon: icon ? rel(icon.getBoundingClientRect()) : null,
          badge: badge ? rel(badge.getBoundingClientRect()) : null};
}""" % TEXT_SELECTORS


def png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


def intersects(a, b, pad=0):
    return not (a["x"] + a["w"] <= b["x"] - pad or b["x"] + b["w"] <= a["x"] - pad or a["y"] + a["h"] <= b["y"] - pad or b["y"] + b["h"] <= a["y"] - pad)


def check_canvas(name, info, outdir):
    fails = []
    expected = (1200, 675)
    for cls, size in SIZES.items():
        if cls in info["cls"].split():
            expected = size
    if (round(info["w"]), round(info["h"])) != expected:
        fails.append(f"canvas is {round(info['w'])} x {round(info['h'])}, class says {expected[0]} x {expected[1]}")
    png = os.path.join(outdir, f"{name}.png")
    if not os.path.exists(png):
        fails.append("PNG missing")
    else:
        size = png_size(png)
        if size and size not in (expected, (expected[0] * 2, expected[1] * 2)):
            fails.append(f"PNG is {size[0]} x {size[1]}, expected {expected[0]} x {expected[1]} (or 2x)")
    for b in info["boxes"]:
        if b["sel"] == "post__title" and expected in ((1200, 675), (1200, 627)) and b["h"] > b["lh"] * 2.5:
            fails.append(f"post title runs on {round(b['h'] / b['lh'])} lines: two at most")
        if b["sel"] == "xcover__line" and b["h"] > b["lh"] * 2.5:
            fails.append(f"cover line runs on {round(b['h'] / b['lh'])} lines: two at most")
        if b["sel"] == "thread__body" and b["h"] > b["lh"] * 3.5:
            fails.append(f"thread sentence runs on {round(b['h'] / b['lh'])} lines: three at most")
        if b["x"] < -1 or b["y"] < -1 or b["x"] + b["w"] > info["w"] + 1 or b["y"] + b["h"] > info["h"] + 1:
            fails.append(f".{b['sel']} runs outside the canvas")
        if info["icon"] and b["sel"] not in ("post__logo", "xcover__logo", "preview__logo") and intersects(b, info["icon"], pad=4):
            fails.append(f".{b['sel']} overlaps the logo")
    if info["badge"]:
        centre = info["badge"]["x"] + info["badge"]["w"] / 2
        if abs(centre - info["w"] / 2) > 2 and "xcover--right" not in info["cls"]:
            fails.append(f"logo centre is {round(centre - info['w'] / 2, 1)} px off")
    return fails


async def run(src, outdir, only):
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        sys.exit("playwright is required:  pip install playwright  &&  playwright install chromium")
    failures = 0
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 2600, "height": 2000})
        await page.goto(pathlib.Path(src).resolve().as_uri(), wait_until="networkidle")
        await page.evaluate("document.fonts.ready")
        await page.wait_for_timeout(300)
        n = 0
        for node in await page.query_selector_all(".canvas"):
            name = await node.get_attribute("data-name") or f"canvas-{n + 1}"
            if only and not any(fnmatch.fnmatch(name, pat) for pat in only):
                continue
            n += 1
            info = await node.evaluate(JS)
            fails = check_canvas(name, info, outdir)
            print(f"{'FAIL' if fails else 'ok':4s} {name}" + ("" if not fails else "\n" + "\n".join(f"  ! {f}" for f in fails)))
            failures += bool(fails)
        await browser.close()
    if n == 0:
        sys.exit("no canvas found")
    return failures


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__); sys.exit(1)
    only = []
    while "--only" in args:
        i = args.index("--only"); only.append(args[i + 1]); del args[i:i + 2]
    sys.exit(1 if asyncio.run(run(args[0], args[1], only)) else 0)


if __name__ == "__main__":
    main()
