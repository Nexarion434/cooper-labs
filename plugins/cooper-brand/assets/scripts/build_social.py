#!/usr/bin/env python3
"""Build a set of Cooper Labs social canvases from a description, not by hand.

    python3 build_social.py posts.json posts.html          # writes the HTML; then render_png.py + check_png.py
    python3 build_social.py posts.json posts.html --png out/   # ... and renders the PNGs, then checks them
    python3 build_social.py --example > posts.json          # the canvases of the template, to start from

The builder applies the Figma file: the post (kicker, title, the mark or the
wordmark at the bottom, on a render or on the halftone at 60%), the partner
card (the mark, a line, the partner's symbol), the X cover (one line, the
wordmark), the social preview (the wordmark alone), and the extra sizes,
banners and thread cards on the same rules. One canvas is one object of
`canvases`:

    name           the PNG file name (without .png)
    kind           post | partner | xcover | preview | banner | thread
    render         "01" (the render behind, 01-06; 02 is the halftone); frame omitted: the catalogue framing for
                   the size | "cover": plain cover fit | {"w", "h", "left", "top"} in % of the canvas (frame.py)
    texture        true: render 02 at 60% over white (Template02 and 04), the wordmark at the bottom
    dark           true: ink ground, white type and logos (no render)
    subject_ok     true when the text over the render's block was looked at and accepted

    post     kicker "NEW POST"; title "2026 Roadmap / for Parallel published" (" / " breaks the line; *...* is the orange accent);
             logo "mark" | "word" (default: mark on a render, word on the texture);
             size 1200x675 (default) | 1200x627 (li) | 1080x1080 (sq) | 1080x1920 (story) | 600x300 (mail) | 2000x800 (x) | 2400x1200 (para) | 2560x1440 (wallpaper)
    partner  icon "path/to/partner-icon.svg" (their symbol, 80 x 80, black on the light render)
    xcover   line "We turn ideas / into products people use."; variant "centre" (default) | "right" (the block at the right, as We Are Cooper)
    preview  (nothing else: the wordmark centred on the render)
    banner   size 1600x400 (forum) | 1500x600 (notion); tag "..." (PP Eiko line); kicker "..." (condensed uppercase); logo true|false
    thread   n 1; total 3; body "One sentence with *the accent.*"; kicker "Why we ship in weeks · thread"

Titles keep their capitalisation as written; the kicker is set in uppercase by the CSS.
"""
import sys, os, re, json, html, pathlib, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_text

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE.parent
sys.path.insert(0, str(HERE))
import brand                                     # noqa: E402
from frame import frames_from                    # noqa: E402

E = html.escape
POST_CLASS = {"1200x675": "", "1200x627": " canvas--li", "1080x1080": " canvas--sq", "1080x1920": " canvas--story", "600x300": " canvas--mail",
              "2000x800": " canvas--x", "2400x1200": " canvas--para", "2560x1440": " canvas--wallpaper"}
BANNER_CLASS = {"1600x400": " canvas--forum", "1500x600": " canvas--notion"}
ALIAS = {"li": "1200x627", "linkedin": "1200x627", "sq": "1080x1080", "square": "1080x1080", "story": "1080x1920", "mail": "600x300", "newsletter": "600x300",
         "x": "2000x800", "para": "2400x1200", "paragraph": "2400x1200", "1200": "1200x675", "post": "1200x675", "wallpaper": "2560x1440",
         "forum": "1600x400", "notion": "1500x600"}


def EM(s):
    """Escape, then *phrase* -> <em>phrase</em> (the orange accent) and " / " -> a line break."""
    return "<br>".join(re.sub(r"\*(.+?)\*", r"<em>\1</em>", E(part)) for part in s.split(" / "))


def load_catalogue():
    with open(ASSETS / "img" / "catalogue.json", encoding="utf-8") as fh:
        return {e["id"]: e for e in json.load(fh)["images"]}


def pct(v):
    s = f"{float(v):.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def bg(c, A, cat, size="1200x675"):
    """The picture layer: an <img> framed inline, or the plain cover fit; the halftone at 60% when `texture`."""
    if c.get("dark"):
        return ""
    n = "02" if c.get("texture") else f"{int(c.get('render', 1)):02d}"
    src = f"{A}{brand.RENDERS}/{n}.jpg"
    cls = "canvas__bg canvas__bg--texture" if c.get("texture") else "canvas__bg"
    f = c.get("frame")
    if f == "cover" or (c.get("texture") and f is None):
        return f'  <div class="{cls}" style="background-image:url(\'{src}\')"></div>\n'
    if not isinstance(f, dict):
        e = cat.get(n) or {}
        f = (e.get("frames") or {}).get(size)
        if f is None and e.get("focus"):
            f = frames_from(tuple(e["focus"]), e.get("zoom", 1), [size])[size]
        if f is None:
            return f'  <div class="{cls}" style="background-image:url(\'{src}\')"></div>\n'
    style = f"width:{pct(f['w'])}%;height:{pct(f['h'])}%;left:{pct(f['left'])}%;top:{pct(f['top'])}%"
    return f'  <div class="{cls}"><img src="{src}" style="{style}" alt=""></div>\n'


def logos(c, A):
    dark = c.get("dark")
    return (f"{A}{brand.ICON_W if dark else brand.ICON_B}", f"{A}{brand.LOGO_W if dark else brand.LOGO_B}")


def canvas(c, A, cat):
    kind = c["kind"]
    name = E(c["name"])
    attrs = (" data-subject-ok" if c.get("subject_ok") else "")
    dark = " canvas--dark" if c.get("dark") else ""
    mark, word = logos(c, A)
    if kind == "post":
        size = ALIAS.get(str(c.get("size", "1200x675")), str(c.get("size", "1200x675")))
        if size not in POST_CLASS:
            sys.exit(f"{c['name']}: post size {size} is not one of {', '.join(POST_CLASS)}")
        logo = c.get("logo") or ("word" if c.get("texture") else "mark")
        logo_html = (f'  <img class="post__logo post__logo--mark" src="{mark}" alt="">\n' if logo == "mark" else f'  <img class="post__logo post__logo--word" src="{word}" alt="{brand.NAME}">\n')
        kicker = f'    <div class="post__kicker">{E(c["kicker"])}</div>\n' if c.get("kicker") else ""
        return (f'<section class="canvas{POST_CLASS[size]}{dark}" data-name="{name}"{attrs}>\n' + bg(c, A, cat, size) +
                f'  <div class="post">\n{kicker}    <div class="post__title">{EM(c["title"])}</div>\n  </div>\n' + logo_html + "</section>\n")
    if kind == "partner":
        icon = c["icon"]
        if not re.match(r"^(https?:|/|[A-Za-z]:)", icon):
            icon = (pathlib.Path(c.get("_base", ".")) / icon).as_posix()
        return (f'<section class="canvas{dark}" data-name="{name}"{attrs}>\n' + bg(c, A, cat) +
                f'  <div class="partner"><img class="partner__mark" src="{mark}" alt="{brand.NAME}"><div class="partner__line"></div><img class="partner__icon" src="{E(icon)}" alt=""></div>\n</section>\n')
    if kind == "xcover":
        right = c.get("variant") == "right"
        inner = f'<div class="xcover__line">{EM(c["line"])}</div><img class="xcover__logo" src="{word}" alt="{brand.NAME}">'
        if right:
            inner = f'<div class="xcover__block">{inner}</div>'
        return (f'<section class="canvas canvas--cover{" xcover--right" if right else ""}{dark}" data-name="{name}"{attrs}>\n' + bg(c, A, cat, "1500x500") +
                f'  {inner}\n</section>\n')
    if kind == "preview":
        return (f'<section class="canvas canvas--preview{dark}" data-name="{name}"{attrs}>\n' + bg(c, A, cat, "1200x630") +
                f'  <img class="preview__logo" src="{word}" alt="{brand.NAME}">\n</section>\n')
    if kind == "banner":
        size = ALIAS.get(str(c.get("size", "1600x400")), str(c.get("size", "1600x400")))
        if size not in BANNER_CLASS:
            sys.exit(f"{c['name']}: banner size {size} is not one of {', '.join(BANNER_CLASS)}")
        inner = (f'<img class="banner__logo" src="{word}" alt="{brand.NAME}">' if c.get("logo", size != "1500x600") else "")
        inner += (f'<div class="banner__tag">{EM(c["tag"])}</div>' if c.get("tag") else "")
        inner += (f'<div class="banner__k">{E(c["kicker"])}</div>' if c.get("kicker") else "")
        return (f'<section class="canvas{BANNER_CLASS[size]}{dark}" data-name="{name}"{attrs}>\n' + bg(c, A, cat, size) + f'  <div class="banner">{inner}</div>\n</section>\n')
    if kind == "thread":
        n, total = int(c["n"]), int(c["total"])
        return (f'<section class="canvas{dark}" data-name="{name}"{attrs}>\n' + bg(c, A, cat) +
                '  <div class="thread">\n'
                f'    <div class="thread__n">{n}<span>/{total}</span></div>\n    <div class="thread__body">{EM(c["body"])}</div>\n'
                f'    <div class="thread__foot"><div class="thread__k">{E(c.get("kicker", ""))}</div><img class="thread__icon" src="{mark}" alt=""></div>\n'
                '  </div>\n</section>\n')
    sys.exit(f"{c.get('name')}: unknown kind {kind!r} (post | partner | xcover | preview | banner | thread)")


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Cooper Labs · Social</title>
<link rel="stylesheet" href="{A}css/cooper.css">
<style>body{{background:#333;display:flex;flex-direction:column;gap:40px;padding:40px;align-items:flex-start}}</style>
</head>
<body>

<!-- Built by build_social.py from {src}. Edit the description and rebuild rather than this file.
     Renders: {A}img/renders/NN.jpg, 01-06 (see img/catalogue.json). -->

"""

KINDS = {"post": "POST · 1200 × 675 (and li, sq, story, mail, x, para, wallpaper): kicker, title, the mark or the wordmark",
         "partner": "PARTNER · 1200 × 675: the mark, a line, the partner's symbol", "xcover": "X COVER · 1500 × 500",
         "preview": "SOCIAL PREVIEW · 1200 × 630", "banner": "BANNERS · forum header 1600 × 400, Notion cover 1500 × 600", "thread": "THREAD · a numbered series of 1200 × 675 cards"}


def build(d, out_html, relative=False, src="a description", base=None):
    A = "../" if relative else ASSETS.as_posix() + "/"
    cat = load_catalogue()
    names = [c["name"] for c in d["canvases"]]
    dup = {n for n in names if names.count(n) > 1}
    if dup:
        sys.exit(f"duplicate canvas names: {', '.join(sorted(dup))}")
    parts = [HEAD.format(A=A, src=src)]
    last = None
    for c in d["canvases"]:
        c = dict(c, _base=base or ".")
        if c["kind"] != last:
            parts.append(f"<!-- ============ {KINDS.get(c['kind'], c['kind'].upper())} ============ -->\n")
            last = c["kind"]
        parts.append(canvas(c, A, cat) + "\n")
    parts.append("</body>\n</html>\n")
    out = pathlib.Path(out_html)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(parts), encoding="utf-8")
    return out, len(names)


EXAMPLE = {"canvases": [
    {"name": "post-2026-roadmap", "kind": "post", "render": "01", "frame": "cover", "kicker": "New post", "title": "2026 Roadmap / for Parallel published"},
    {"name": "post-seventeenth-parallel-report", "kind": "post", "texture": True, "kicker": "January 2026", "title": "Seventeenth / Parallel Report"},
    {"name": "post-flash-loans-explained", "kind": "post", "texture": True, "kicker": "Parallel", "title": "Flash Loans / Explained"},
    {"name": "partner-parallel", "kind": "partner", "render": "01", "frame": "cover", "icon": "../logo/partners/parallel_icon_b.svg"},
    {"name": "x-cover-tagline-1500x500", "kind": "xcover", "render": "01", "frame": "cover", "line": "We turn ideas / into products people use."},
    {"name": "x-cover-we-are-cooper-1500x500", "kind": "xcover", "render": "04", "frame": "cover", "variant": "right", "line": "We Are Cooper"},
    {"name": "social-preview-1200x630", "kind": "preview", "render": "01", "frame": "cover"},
    {"name": "post-2026-roadmap-li-1200x627", "kind": "post", "render": "01", "frame": "cover", "size": "1200x627", "kicker": "New post", "title": "2026 Roadmap / for Parallel published"},
    {"name": "post-2026-roadmap-sq-1080", "kind": "post", "texture": True, "size": "1080x1080", "kicker": "New post", "title": "2026 Roadmap / for Parallel published"},
    {"name": "post-2026-roadmap-story-1080x1920", "kind": "post", "render": "01", "frame": "cover", "size": "1080x1920", "kicker": "New post", "title": "2026 Roadmap / for Parallel published"},
    {"name": "post-2026-roadmap-mail-600x300", "kind": "post", "texture": True, "size": "600x300", "kicker": "Newsletter · January", "title": "2026 Roadmap / for Parallel published"},
    {"name": "wallpaper-the-space-between-2560x1440", "kind": "post", "texture": True, "size": "2560x1440", "title": "The Space Between", "logo": "word"},
    {"name": "forum-header-1600x400", "kind": "banner", "size": "1600x400", "render": "01", "kicker": "Builders · cooperlabs.xyz"},
    {"name": "notion-cover-parallel-mcp-1500x600", "kind": "banner", "size": "1500x600", "render": "01", "tag": "Proposal · Parallel *MCP server*", "kicker": "Internal · Draft v0.1"},
    {"name": "thread-ship-in-weeks-1of3", "kind": "thread", "render": "01", "frame": "cover", "n": 1, "total": 3, "kicker": "How we ship · thread",
     "body": "Every project starts with one question: what does the user *do on day one?*"},
    {"name": "thread-ship-in-weeks-2of3", "kind": "thread", "render": "01", "frame": "cover", "n": 2, "total": 3, "kicker": "How we ship · thread",
     "body": "We build alongside the team, in the open, and *demo every Friday.*"},
    {"name": "thread-ship-in-weeks-3of3", "kind": "thread", "render": "01", "frame": "cover", "n": 3, "total": 3, "kicker": "How we ship · thread",
     "body": "Launch is not the end. *We stay* to iterate, harden and scale."}]}


def main():
    args = [a for a in sys.argv[1:] if a != "--no-lint"]
    if "--example" in args:
        print(json.dumps(EXAMPLE, indent=1, ensure_ascii=False)); return
    if len(args) < 2:
        print(__doc__); sys.exit(1)
    with open(args[0], encoding="utf-8") as fh:
        d = json.load(fh)
    check_text.gate(d, args[0], "--no-lint" in sys.argv)
    out, n = build(d, args[1], relative="--relative" in args, src=os.path.basename(args[0]), base=os.path.dirname(os.path.abspath(args[0])))
    print(f"-> {out}  ({n} canvas{'es' if n != 1 else ''})")
    if "--png" in args:
        folder = args[args.index("--png") + 1]
        subprocess.run([sys.executable, str(HERE / "render_png.py"), str(out), folder], check=True)
        sys.exit(subprocess.run([sys.executable, str(HERE / "check_png.py"), str(out), folder]).returncode)


if __name__ == "__main__":
    main()
