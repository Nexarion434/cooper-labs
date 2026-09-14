#!/usr/bin/env python3
"""Framing of a render on a social canvas (the zoom on a detail).

Every render in ../img/catalogue.json carries `frames`: for each canvas
size, the `<img>` geometry inside `.canvas__bg`, in percent of the canvas
(`w`, `h`, `left`, `top`), plus the `focus` (point of the image put at the
centre, in percent of the image) and `zoom` they were computed from.

    python3 frame.py 26                    # CSS for the three sizes + the Pencil override
    python3 frame.py 26 x                  # one size: 1200 | x | para | li | sq | story | xhead | forum | mail | notion, or any WxH
    python3 frame.py 26 --focus 69 41 --zoom 1.6      # compute new frames from a focus and a zoom
    python3 frame.py 26 --focus 69 41 --zoom 1.6 --write   # ... and store them in the catalogue
    python3 frame.py 26 --preview check.png            # the three crops with the text zones drawn

Rule of thumb: h% = w% x (canvas ratio / image ratio); the renders are 16:10
(1841 x 1151), so x1.111 on 1200 x 675, x1.563 on 2000 x 800, x1.25 on
2400 x 1200, x1.196 on 1200 x 627, x1.191 on 1200 x 630, x0.625 on 1080 x 1080,
x0.352 on 1080 x 1920 (there the window is taller than the image: it is widened
instead), x1.875 on 1500 x 500, x2.5 on 1600 x 400, x1.25 on 600 x 300,
x1.563 on 1500 x 600.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOGUE = os.path.join(HERE, "..", "img", "catalogue.json")
IMG = os.path.join(HERE, "..", "img", "renders")
IMAGE_RATIO = 1841 / 1151          # the renders are 16:10 (1841 x 1151)
SIZES = {"1200x675": (1200, 675), "1200x630": (1200, 630), "1500x500": (1500, 500), "2000x800": (2000, 800), "2400x1200": (2400, 1200), "1200x627": (1200, 627), "1080x1080": (1080, 1080), "1080x1920": (1080, 1920),
         "1600x400": (1600, 400), "600x300": (600, 300), "1500x600": (1500, 600), "2560x1440": (2560, 1440)}
ALIAS = {"1200": "1200x675", "post": "1200x675", "thread": "1200x675", "preview": "1200x630", "og": "1200x630", "cover": "1500x500", "wallpaper": "2560x1440", "x": "2000x800", "para": "2400x1200", "paragraph": "2400x1200", "li": "1200x627", "linkedin": "1200x627",
         "sq": "1080x1080", "square": "1080x1080", "story": "1080x1920", "xhead": "1500x500", "forum": "1600x400", "mail": "600x300", "newsletter": "600x300", "notion": "1500x600"}
# text zones per size, in percent of the canvas height (where the type sits); other sizes get the middle third
TEXT_ZONE = {"1200x675": (30, 70), "1200x630": (40, 60), "1500x500": (30, 70), "2000x800": (34, 66), "2400x1200": (36, 64), "1200x627": (30, 70), "1080x1080": (38, 62), "1080x1920": (40, 60),
             "1600x400": (36, 64), "600x300": (30, 72), "1500x600": (62, 90), "2560x1440": (40, 60)}


def size_of(key):
    """(w, h) for a stored key or any WxH."""
    if key in SIZES:
        return SIZES[key]
    m = re.match(r"^(\d+)x(\d+)$", key)
    if not m:
        sys.exit(f"unknown size {key}: use WxH, e.g. 1200x627")
    return int(m.group(1)), int(m.group(2))


def frames_from(focus, zoom, sizes=None):
    """CSS percentages per size from a focus (fx, fy in % of the image) and a zoom; any WxH works."""
    fx, fy = focus
    out = {}
    for key in (sizes or SIZES):
        w, h = size_of(key)
        canvas_ratio = w / h
        wc = 100 / zoom                              # window width, % of the image width
        hc = wc * IMAGE_RATIO / canvas_ratio         # window height, % of the image height (same ratio as the canvas)
        if hc > 100:                                 # narrow canvas: the window is taller than the image, so it is narrowed
            hc, wc = 100, 100 * canvas_ratio / IMAGE_RATIO
        left = min(max(fx - wc / 2, 0), 100 - wc)
        top = min(max(fy - hc / 2, 0), 100 - hc)
        out[key] = {"w": round(100 / wc * 100, 1), "h": round(100 / hc * 100, 1),
                    "left": round(-left / wc * 100, 1), "top": round(-top / hc * 100, 1)}
    return out


def css(f):
    return f"width:{f['w']}%;height:{f['h']}%;left:{f['left']}%;top:{f['top']}%"


def pencil(f, size):
    w, h = size_of(size)
    return {"x": round(w * f["left"] / 100), "y": round(h * f["top"] / 100), "width": round(w * f["w"] / 100), "height": round(h * f["h"] / 100)}


def load():
    with open(CATALOGUE, encoding="utf-8") as fh:
        return json.load(fh)


def entry(cat, n):
    for e in cat["images"]:
        if e["id"] == f"{int(n):02d}":
            return e
    sys.exit(f"no render {n}")


def preview(n, frames, path):
    from PIL import Image, ImageDraw
    im = Image.open(os.path.join(IMG, f"{int(n):02d}.jpg")).convert("RGB")
    tiles = []
    for key in frames:
        w, h = size_of(key)
        f = frames[key]
        scale = 600 / w
        cw, ch = 600, round(h * scale)
        iw, ih = round(cw * f["w"] / 100), round(ch * f["h"] / 100)
        canvas = Image.new("RGB", (cw, ch), "black")
        canvas.paste(im.resize((iw, ih)), (round(cw * f["left"] / 100), round(ch * f["top"] / 100)))
        d = ImageDraw.Draw(canvas, "RGBA")
        a, b = TEXT_ZONE.get(key, (33, 67))
        d.rectangle((round(cw * 0.06), round(ch * a / 100), round(cw * 0.94), round(ch * b / 100)), outline=(255, 80, 80, 230), width=2)
        d.rectangle((round(cw * 0.47), round(ch * 0.04), round(cw * 0.53), round(ch * 0.16)), outline=(255, 255, 255, 180), width=1)
        d.text((8, 6), f"{int(n):02d}  {key}  {css(f)}", fill="white")
        tiles.append(canvas)
    sheet = Image.new("RGB", (600, sum(t.height for t in tiles) + 8 * (len(tiles) - 1)), (30, 30, 30))
    y = 0
    for t in tiles:
        sheet.paste(t, (0, y)); y += t.height + 8
    sheet.save(path)
    print("preview ->", path)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(1)
    n = args.pop(0)
    cat = load(); e = entry(cat, n)
    frames = e.get("frames")
    if "--focus" in args:
        i = args.index("--focus"); focus = (float(args[i + 1]), float(args[i + 2])); del args[i:i + 3]
        zoom = 1.0
        if "--zoom" in args:
            i = args.index("--zoom"); zoom = float(args[i + 1]); del args[i:i + 2]
        frames = frames_from(focus, zoom)
        if "--write" in args:
            e["focus"] = [focus[0], focus[1]]; e["zoom"] = zoom; e["frames"] = frames; e.pop("x_focus", None)
            with open(CATALOGUE, "w", encoding="utf-8") as fh:
                json.dump(cat, fh, indent=1, ensure_ascii=False)
            print("catalogue updated for", e["id"])
    if not frames:
        sys.exit("no frames for this render; pass --focus fx fy --zoom z")
    if "--preview" in args:
        i = args.index("--preview")
        want = [ALIAS.get(a, a) for a in args if not a.startswith("--") and a != args[i + 1]]
        shown = {k: frames.get(k) or frames_from(tuple(e["focus"]), e["zoom"], [k])[k] for k in (want or list(frames))}
        preview(n, shown, args[i + 1]); return
    sizes = [ALIAS.get(a, a) for a in args if not a.startswith("--")] or list(frames)
    for key in sizes:
        if key not in frames:                                   # any WxH, computed from the stored focus and zoom
            frames[key] = frames_from(tuple(e["focus"]), e["zoom"], [key])[key]
        f = frames[key]
        print(f"{key:9s}  css:    {css(f)}")
        print(f"{'':9s}  pencil: {json.dumps(pencil(f, key))}")


if __name__ == "__main__":
    main()
