#!/usr/bin/env python3
"""Render a new picture of the block and add it to the catalogue.

    python3 render_block.py --out preview.png --scale 0.25                       # a quick look, 460 x 288
    python3 render_block.py --material orange --ground grey --effect grain,chroma --yaw 28 --pitch 18 --out 07.jpg
    python3 render_block.py --material grey --ground grey --effect pixel:6,dither --yaw -30 --pitch 24 --zoom 1.8 --out 08.jpg
    python3 render_block.py --preset pixel --yaw 40 --catalogue 09 --name block-pixel-right     # renders/09.jpg + catalogue.json
    python3 render_block.py --list                                                 # presets, materials, grounds, effects

The block is the mark in three dimensions: a box in the proportion of the
mark (236 x 167, depth 104) with a cylinder of radius 71 cut through it,
centred at 80% of the width, so the hole opens on the right face. The
picture is ray-cast here, with no dependency beyond numpy and Pillow: a
perspective camera orbits the block (`--yaw`, `--pitch`, `--roll`,
`--zoom`), one key light and one fill light shade it (`--light`), the
ground is a flat tone with an optional soft shadow, and the post effects
give the families of the six masters:

    material   white | orange | grey | ink            (the albedo; `white` reads as render 01's matte)
    ground     white | paper | grey | dark | ink      (the flat tone behind the block)
    effect     grain[:amount]   film grain over everything (render 05)
               chroma[:px]      red and blue channels shifted (render 05)
               pixel[:size]     the picture in big pixels (render 03, 06)
               dither           one-bit ordered dither, like the pixel masters (render 03, 06)
               halftone[:cell]  round-dot halftone of the luminance (render 02)
               lines[:px]       horizontal scanlines
               dots[:cell]      a dotted ground, as in render 04 (drawn behind the block)
               soft             a wide blur of the whole picture (render 01's macro softness)
    preset     clean | orange | pixel | halftone | noise | macro   (a material, a ground, effects and a camera, then your flags on top)

Masters are 1841 x 1151 (16:10); `--scale` renders a fraction of that for
previews. `--catalogue NN` writes renders/NN.jpg, measures the block's box
and writes the catalogue entry (name, ground, busy, subject, frames) so
build_social.py, frame.py and the documents can use it by number at once.
Renders 01 to 06 are the masters from the Figma file and are never
overwritten.
"""
import sys, os, json, math, argparse, pathlib
import numpy as np
from PIL import Image, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE.parent
CATALOGUE = ASSETS / "img" / "catalogue.json"
RENDERS = ASSETS / "img" / "renders"
sys.path.insert(0, str(HERE))

W0, H0 = 1841, 1151                       # the masters
# the block: the mark's box (236.196 x 166.6665 in the SVG), a depth of 90, the hole of radius 71.136 at (189.23, 83.33)
BW, BH, BD = 236.196, 166.6665, 104.0
HOLE_X, HOLE_Y, HOLE_R = 255.901 - 66.667, 150.0 - 66.6665, 71.136

MATERIALS = {"white": (0.96, 0.96, 0.95), "orange": (1.0, 0.62, 0.26), "grey": (0.62, 0.62, 0.62), "ink": (0.12, 0.12, 0.12)}
GROUNDS = {"white": (1.0, 1.0, 1.0), "paper": (0.96, 0.96, 0.96), "grey": (0.85, 0.85, 0.85), "dark": (0.30, 0.30, 0.30), "ink": (0.118, 0.118, 0.118)}
PRESETS = {
    "clean": dict(material="white", ground="paper", effect="", yaw=28, pitch=16, roll=-6, zoom=1.0),
    "orange": dict(material="orange", ground="grey", effect="dots:14", yaw=-32, pitch=14, roll=-4, zoom=0.55),
    "pixel": dict(material="grey", ground="grey", effect="pixel:7,dither", yaw=-34, pitch=22, roll=-10, zoom=0.95),
    "halftone": dict(material="ink", ground="white", effect="soft:34,halftone:11", yaw=0, pitch=0, roll=0, zoom=1.5),
    "noise": dict(material="orange", ground="paper", effect="grain:0.18,chroma:5", yaw=-30, pitch=12, roll=-6, zoom=0.5),
    "macro": dict(material="white", ground="white", effect="soft:5", yaw=24, pitch=10, roll=-14, zoom=2.4, light=(0.15, 0.55, 1.0)),
}


# ---------------------------------------------------------------- the ray cast
def rot(yaw, pitch, roll):
    y, p, r = (math.radians(a) for a in (yaw, pitch, roll))
    ry = np.array([[math.cos(y), 0, math.sin(y)], [0, 1, 0], [-math.sin(y), 0, math.cos(y)]])
    rp = np.array([[1, 0, 0], [0, math.cos(p), -math.sin(p)], [0, math.sin(p), math.cos(p)]])
    rr = np.array([[math.cos(r), -math.sin(r), 0], [math.sin(r), math.cos(r), 0], [0, 0, 1]])
    return rr @ rp @ ry


def cast(w, h, yaw, pitch, roll, zoom, fov, light, material, ground, shadow=True, offset=(0.0, 0.0)):
    """Return an RGB float image (h, w, 3) and the block's mask (h, w)."""
    # the camera looks down -z at the block centred on the origin; the block is rotated instead of the camera
    R = rot(yaw, pitch, roll)                                    # world <- block
    Ri = R.T                                                     # block <- world
    dist = 3.2 * BW / zoom
    aspect = w / h
    fy = math.tan(math.radians(fov) / 2)
    xs = (np.arange(w) + 0.5) / w * 2 - 1
    ys = 1 - (np.arange(h) + 0.5) / h * 2
    px, py = np.meshgrid(xs * fy * aspect, ys * fy)
    d = np.stack([px + offset[0], py + offset[1], -np.ones_like(px)], -1)
    d /= np.linalg.norm(d, axis=-1, keepdims=True)
    o = np.array([0.0, 0.0, dist])
    # into block space (the block spans [-BW/2, BW/2] x [-BH/2, BH/2] x [-BD/2, BD/2]; the hole's axis is z)
    ob = Ri @ o
    db = d @ Ri.T
    eps = 1e-9
    inv = 1.0 / np.where(np.abs(db) < eps, eps, db)
    lo = np.array([-BW / 2, -BH / 2, -BD / 2]); hi = -lo
    t1 = (lo - ob) * inv; t2 = (hi - ob) * inv
    tmin = np.minimum(t1, t2); tmax = np.maximum(t1, t2)
    tb0 = tmin.max(-1); tb1 = tmax.min(-1)
    box_hit = (tb1 > tb0) & (tb1 > 0)
    face_axis = tmin.argmax(-1)                                    # which slab gave the entry
    # the cylinder along z, centre (cx, cy)
    cx, cy = HOLE_X - BW / 2, HOLE_Y - BH / 2
    ox, oy = ob[0] - cx, ob[1] - cy
    dx, dy = db[..., 0], db[..., 1]
    a = dx * dx + dy * dy
    b = 2 * (ox * dx + oy * dy)
    c = ox * ox + oy * oy - HOLE_R * HOLE_R
    disc = b * b - 4 * a * c
    cyl = disc > 0
    sq = np.sqrt(np.where(cyl, disc, 0))
    tc0 = np.where(cyl, (-b - sq) / (2 * a), np.inf)
    tc1 = np.where(cyl, (-b + sq) / (2 * a), -np.inf)
    # the solid is the box minus the cylinder
    enters_face = box_hit & (~cyl | (tb0 < tc0) | (tb0 > tc1))     # the ray meets a box face outside the hole
    through_hole = box_hit & ~enters_face & (tc1 < tb1)              # it enters inside the hole and meets the hole's wall
    t = np.where(enters_face, tb0, np.where(through_hole, tc1, np.inf))
    hit = np.isfinite(t)
    p = ob + db * np.where(hit, t, 0.0)[..., None]
    # normals in block space
    n_face = np.zeros_like(p)
    sign = -np.sign(db)
    for ax in range(3):
        m = face_axis == ax
        n_face[..., ax] = np.where(m, sign[..., ax], 0)
    radial = np.stack([p[..., 0] - cx, p[..., 1] - cy, np.zeros_like(t)], -1)
    radial /= np.maximum(np.linalg.norm(radial, axis=-1, keepdims=True), eps)
    n = np.where(enters_face[..., None], n_face, -radial)
    n_world = n @ R.T
    # lights (world space): a key from the upper left front, a fill from the right, a rim from behind
    key = np.array(light); key = key / np.linalg.norm(key)
    fill = np.array([0.8, 0.2, 0.5]); fill /= np.linalg.norm(fill)
    ndl = np.clip(n_world @ key, 0, 1)
    ndf = np.clip(n_world @ fill, 0, 1)
    view = -d
    half = key + view; half /= np.maximum(np.linalg.norm(half, axis=-1, keepdims=True), eps)
    spec = np.clip((n_world * half).sum(-1), 0, 1) ** 40 * 0.12
    inside = through_hole.astype(float)                              # the hole's wall is in the block's own shade
    shade = 0.52 + 0.46 * ndl + 0.12 * ndf - 0.2 * inside
    alb = np.array(MATERIALS[material])
    col = alb[None, None, :] * shade[..., None] + spec[..., None]
    g = np.array(GROUNDS[ground])
    img = np.broadcast_to(g, (h, w, 3)).astype(float).copy()
    if shadow:
        # a soft ellipse of shadow under the block, in screen space, from the block's footprint
        yy, xx = np.mgrid[0:h, 0:w]
        ys_hit = np.where(hit, yy, -1)
        if hit.any():
            cxs, cys = xx[hit].mean(), yy[hit].mean()
            rx = (xx[hit].max() - xx[hit].min()) * 0.62 + 1
            ry = (yy[hit].max() - yy[hit].min()) * 0.26 + 1
            sy = ys_hit.max() + ry * 0.35
            e = ((xx - cxs) / rx) ** 2 + ((yy - sy) / ry) ** 2
            sh = np.clip(1 - e, 0, 1) ** 1.6 * 0.22
            img *= (1 - sh)[..., None]
    img = np.where(hit[..., None], col, img)
    return np.clip(img, 0, 1), hit


# ---------------------------------------------------------------- the effects
BAYER8 = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26], [12, 44, 4, 36, 14, 46, 6, 38], [60, 28, 52, 20, 62, 30, 54, 22],
                   [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25], [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]]) / 64.0


def lum(a):
    return a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114


def fx_grain(a, amount=0.14, seed=7):
    rng = np.random.default_rng(seed)
    return np.clip(a + rng.normal(0, amount, a.shape[:2])[..., None] * np.array([1, 0.9, 1.1]), 0, 1)


def fx_chroma(a, px=4):
    out = a.copy()
    out[..., 0] = np.roll(a[..., 0], int(px), axis=1)
    out[..., 2] = np.roll(a[..., 2], -int(px), axis=1)
    return out


def fx_pixel(a, size=6):
    h, w = a.shape[:2]; s = max(1, int(size))
    small = a[:h - h % s, :w - w % s].reshape(h // s, s, w // s, s, 3).mean((1, 3))
    return np.repeat(np.repeat(small, s, 0), s, 1)[:h, :w] if (h % s == 0 and w % s == 0) else np.pad(np.repeat(np.repeat(small, s, 0), s, 1), ((0, h % s), (0, w % s), (0, 0)), mode="edge")


def fx_dither(a, cell=1):
    h, w = a.shape[:2]
    l = lum(a)
    thr = np.tile(BAYER8, (h // 8 + 1, w // 8 + 1))[:h, :w]
    if cell > 1:                                                     # coarse: one threshold per cell
        thr = np.repeat(np.repeat(np.tile(BAYER8, (h // (8 * cell) + 1, w // (8 * cell) + 1)), cell, 0), cell, 1)[:h, :w]
    dark = np.array(GROUNDS["ink"]); light = np.array([1.0, 1.0, 1.0])
    return np.where((l > thr)[..., None], light, dark)


def fx_halftone(a, cell=12):
    h, w = a.shape[:2]; c = max(2, int(cell))
    l = lum(a)
    out = np.ones_like(a)
    yy, xx = np.mgrid[0:h, 0:w]
    cy = (yy // c) * c + c / 2; cx = (xx // c) * c + c / 2
    # the dot radius follows the darkness of the cell's mean
    small = l[:h - h % c, :w - w % c].reshape(h // c, c, w // c, c).mean((1, 3))
    m = np.repeat(np.repeat(small, c, 0), c, 1)
    m = np.pad(m, ((0, h - m.shape[0]), (0, w - m.shape[1])), mode="edge")
    r = (1 - m) * c * 0.62
    dot = ((xx - cx) ** 2 + (yy - cy) ** 2) < r * r
    out[dot] = np.array([0.18, 0.18, 0.18])
    return out


def fx_lines(a, px=3):
    h = a.shape[0]; s = max(2, int(px))
    mask = (np.arange(h) % s == 0)
    out = a.copy(); out[mask] *= 0.82
    return out


def fx_dots(a, cell=14, mask=None):
    h, w = a.shape[:2]; c = max(4, int(cell))
    yy, xx = np.mgrid[0:h, 0:w]
    d = ((xx % c) - c / 2) ** 2 + ((yy % c) - c / 2) ** 2 < 1.6
    out = a.copy()
    keep = d if mask is None else (d & ~mask)
    out[keep] *= 0.55
    return out


def fx_soft(a, radius=None):
    im = Image.fromarray((a * 255).astype(np.uint8))
    r = radius or max(2, a.shape[1] // 90)
    return np.asarray(im.filter(ImageFilter.GaussianBlur(r))).astype(float) / 255


def apply(a, mask, spec):
    for item in [x.strip() for x in spec.split(",") if x.strip()]:
        name, _, arg = item.partition(":")
        v = float(arg) if arg else None
        if name == "grain": a = fx_grain(a, v if v is not None else 0.14)
        elif name == "chroma": a = fx_chroma(a, v if v is not None else 4)
        elif name == "pixel": a = fx_pixel(a, v if v is not None else 6)
        elif name == "dither": a = fx_dither(a, int(v) if v is not None else 1)
        elif name == "halftone": a = fx_halftone(a, v if v is not None else 12)
        elif name == "lines": a = fx_lines(a, v if v is not None else 3)
        elif name == "dots": a = fx_dots(a, v if v is not None else 14, mask)
        elif name == "soft": a = fx_soft(a, v)
        else: sys.exit(f"unknown effect {name!r}")
    return a


# ---------------------------------------------------------------- the catalogue
def subject_box(mask):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    h, w = mask.shape
    x0, x1, y0, y1 = xs.min() / w * 100, xs.max() / w * 100, ys.min() / h * 100, ys.max() / h * 100
    return {"x": round(x0), "y": round(y0), "w": round(x1 - x0), "h": round(y1 - y0), "what": "the block"}


def busy_of(box):
    if box is None:
        return "all"
    cx = box["x"] + box["w"] / 2
    if box["w"] > 60: return "all"
    return "left" if cx < 40 else "right" if cx > 60 else "centre"


def write_catalogue(n, name, desc, ground, box, material, effect, camera):
    import frame
    with open(CATALOGUE, encoding="utf-8") as fh:
        cat = json.load(fh)
    nid = f"{int(n):02d}"
    if int(n) <= 6:
        sys.exit("renders 01 to 06 are the masters from the Figma file; pick a number from 07")
    fx, fy = (box["x"] + box["w"] / 2, box["y"] + box["h"] / 2) if box else (50, 50)
    entry = {"id": nid, "file": f"renders/{nid}.jpg", "name": name, "ground": "dark" if GROUNDS[ground][0] < 0.5 else "light",
             "desc": desc, "busy": busy_of(box), "subject": box, "focus": [50, 50], "zoom": 1.0, "used_by": [],
             "made_with": {"script": "render_block.py", "material": material, "ground": ground, "effect": effect, **camera},
             "frames": frame.frames_from([50, 50], 1.0)}
    cat["images"] = [e for e in cat["images"] if e["id"] != nid] + [entry]
    cat["images"].sort(key=lambda e: e["id"])
    with open(CATALOGUE, "w", encoding="utf-8") as fh:
        json.dump(cat, fh, indent=1, ensure_ascii=False); fh.write("\n")
    return entry


# ---------------------------------------------------------------- main
def render(args):
    w, h = int(round(W0 * args.scale)), int(round(H0 * args.scale))
    ss = 2 if args.scale >= 0.5 else 1                              # supersample the masters
    img, mask = cast(w * ss, h * ss, args.yaw, args.pitch, args.roll, args.zoom, args.fov, args.light, args.material, args.ground,
                     shadow=not args.no_shadow, offset=(args.dx, args.dy))
    if ss > 1:
        img = img.reshape(h, ss, w, ss, 3).mean((1, 3))
        mask = mask.reshape(h, ss, w, ss).mean((1, 3)) > 0.5
    img = apply(img, mask, args.effect)
    return Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)), mask


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--preset", choices=sorted(PRESETS))
    ap.add_argument("--material", choices=sorted(MATERIALS))
    ap.add_argument("--ground", choices=sorted(GROUNDS))
    ap.add_argument("--effect", help="comma-separated, see the list above")
    ap.add_argument("--yaw", type=float); ap.add_argument("--pitch", type=float); ap.add_argument("--roll", type=float)
    ap.add_argument("--zoom", type=float, help="1 fills about a third of the width; 3 is a macro")
    ap.add_argument("--fov", type=float, default=28)
    ap.add_argument("--dx", type=float, default=0.0, help="shift the block in the frame, in view units (−0.5 left … 0.5 right)")
    ap.add_argument("--dy", type=float, default=0.0)
    ap.add_argument("--light", type=float, nargs=3, metavar=("X", "Y", "Z"), help="the key light's direction (default −0.55 0.75 0.6: upper left, in front)")
    ap.add_argument("--no-shadow", action="store_true")
    ap.add_argument("--scale", type=float, default=1.0, help="fraction of 1841 x 1151")
    ap.add_argument("--out", help="PNG or JPG to write (default: renders/NN.jpg with --catalogue)")
    ap.add_argument("--catalogue", metavar="NN", help="write renders/NN.jpg and the catalogue entry")
    ap.add_argument("--name", help="the catalogue name (block-orange-left)")
    ap.add_argument("--desc", help="one line for the catalogue")
    ap.add_argument("--quality", type=int, default=88)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if args.list:
        print("presets:  " + ", ".join(f"{k} ({v['material']} on {v['ground']}, {v['effect'] or 'no effect'})" for k, v in PRESETS.items()))
        print("materials:", ", ".join(MATERIALS)); print("grounds:  ", ", ".join(GROUNDS))
        print("effects:   grain[:amount] chroma[:px] pixel[:size] dither[:cell] halftone[:cell] lines[:px] dots[:cell] soft[:radius]")
        return
    base = dict(PRESETS[args.preset]) if args.preset else dict(PRESETS["clean"])
    for k in ("material", "ground", "effect", "yaw", "pitch", "roll", "zoom"):
        if getattr(args, k) is None:
            setattr(args, k, base[k])
    if args.light is None:
        args.light = base.get("light", (-0.55, 0.75, 0.6))
    if args.preset == "macro" and args.dx == 0.0 and args.dy == 0.0:
        args.dx, args.dy = -0.16, 0.02                                   # the crescent in the frame
    if args.catalogue and int(args.catalogue) <= 6:
        sys.exit("renders 01 to 06 are the masters from the Figma file; pick a number from 07")
    if args.catalogue and args.scale != 1.0:
        print("note: a catalogued render is a master; rendering at full scale")
        args.scale = 1.0
    im, mask = render(args)
    out = pathlib.Path(args.out) if args.out else (RENDERS / f"{int(args.catalogue):02d}.jpg" if args.catalogue else pathlib.Path("block.png"))
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix.lower() in (".jpg", ".jpeg"):
        im.convert("RGB").save(out, "JPEG", quality=args.quality, optimize=True, progressive=True)
    else:
        im.save(out)
    box = subject_box(mask)
    print(f"-> {out}  {im.size[0]} x {im.size[1]}  block at {box}" if box else f"-> {out}  (no block in frame)")
    if args.catalogue:
        camera = {"yaw": args.yaw, "pitch": args.pitch, "roll": args.roll, "zoom": args.zoom, "fov": args.fov, "dx": args.dx, "dy": args.dy}
        name = args.name or f"block-{args.material}-{args.preset or 'custom'}"
        desc = args.desc or f"The block in {args.material} on a {args.ground} ground" + (f", {args.effect.replace(',', ' and ').replace(':', ' ')}" if args.effect else "")
        e = write_catalogue(args.catalogue, name, desc, args.ground, box, args.material, args.effect, camera)
        print(f"-> catalogue.json  {e['id']} {e['name']}  ground {e['ground']}, busy {e['busy']}")


if __name__ == "__main__":
    main()
