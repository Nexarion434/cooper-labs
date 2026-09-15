#!/usr/bin/env python3
"""Build a Cooper Labs deck (16:9, 1280 x 720) from a description.

    python3 build_deck.py deck.json deck.html            # writes the HTML and prints the PDF name to use
    python3 build_deck.py deck.json deck.html --pdf      # ... and renders the PDF next to it, one slide per page, then checks it
    python3 build_deck.py deck.json deck.html --png out/ # ... one PNG per slide
    python3 build_deck.py --example > deck.json          # a description to start from

The same grid as the A4 page, scaled x1.6: one block per slide (a margin
column of 180 with the tag and the source, a reading column with the heading,
body, bullets, table, figures or recommendation). Slide numbers, `NN / NN`,
the version in the title slide, every running head and the closing slide, and
the file name are computed. Titles get Title Case and their `*italic phrase*`.

The description (JSON):

    class          proposal | case-study | spec | post-mortem | memo | briefing | update | pitch
    subject        "Parallel MCP server"               -> running head, file name
    title          "One server, *thirty-six tools,* one URL."   (*...* is the accent, set in orange)
    standfirst     one sentence; kicker (optional, default "<Class> · <subject>")
    version        "v0.1"; classification Confidential | Internal | Public; status Draft | Final
    date           "2026-09-10"; owner "Noah, Protocol"
    render         "01" (one of the six renders, full-bleed on the title slide, ink type) | "dark" (plain ink ground, white type)
    closing        true (default): the dark closing slide with the tagline and the links
    slides         [ ... ] one object per slide:
        {"tag": "Summary", "source": "...", "heading": "...", "body": "...", "bullets": [...], "table": {...}, "figures": [...], "reco": [...]}
            a content slide: one block, the keys of build_doc.py (or "main" for another order)
        {"kind": "divider", "n": "02", "kicker": "Part two · Assessment", "title": "What the numbers say *under stress.*"}
        {"kind": "statement", "text": "A fee that is zero on a normal day ... *turns a bank run into a queue.*", "who": "Summary · Protocol review"}
"""
import sys, os, re, json, html, pathlib, subprocess

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE.parent
sys.path.insert(0, str(HERE))
import brand   # noqa: E402
from build_doc import CLASSES, E, EM, title_case, long_date, short_date, slug, item_html, ORDER, cover_ground   # noqa: E402

LABELS = brand.DECK_LABELS


def title_slide(d, A):
    meta = [("Date", long_date(d["date"])), ("Classification", d["classification"]), ("Status", d["status"]), ("Owner", d["owner"])]
    m = "".join(f'<div><div class="k">{E(k)}</div><div class="v">{E(v)}</div></div>' for k, v in meta)
    raw = str(d.get('render', d.get('illustration', 1)))
    plain_dark = raw.lower() in ("dark", "none")
    n = "" if plain_dark else f"{int(raw):02d}"
    dark = plain_dark or cover_ground(n) == "dark"
    img = "" if plain_dark else f'''  <div class="canvas__bg" style="background-image:url('{A}{brand.RENDERS}/{n}.jpg')"></div>
  <div class="cover__fade"></div>
'''
    return f'''<!-- ========================= 01 · TITLE ========================= -->
<section class="canvas canvas--deck deck--title{" cover--dark" if dark else ""}{" cover--texture" if n == "02" else ""}" data-name="{E(d['stem'])}-01-title">
{img}
  <div class="cover__top">
    <img class="cover__logo" src="{A}{brand.LOGO_W if dark else brand.LOGO_B}" alt="{brand.NAME}">
    <div class="cover__conf">{E(d["classification"])} · {E(d["version"])}</div>
  </div>
  <div class="cover__bottom">
    <div class="cover__kicker">{E(d["kicker"])}</div>
    <div class="cover__title">{EM(title_case(d["title"]))}</div>
    <div class="cover__stand">{E(d["standfirst"])}</div>
    <div class="cover__rule"></div>
    <div class="cover__meta">{m}</div>
  </div>
</section>
'''


def closing_slide(d, A, n, total):
    m = "".join(f'<div><div class="k">{E(k)}</div><div class="v">{E(v)}</div></div>' for k, v in brand.LINKS)
    m += f'<div><div class="k">This deck</div><div class="v">{E(d["class_label"])} · {E(d["version"])} · {E(short_date(d["date"]))}</div></div>'
    return f'''<!-- ========================= {n:02d} · CLOSING ========================= -->
<section class="canvas canvas--deck deck--back cover--dark" data-name="{E(d['stem'])}-{n:02d}-closing">
  <div class="back__glow"></div>
  <div class="cover__top" style="left:72px;right:72px;top:56px">
    <img class="cover__logo" src="{A}{brand.LOGO_W}" alt="{brand.NAME}" style="height:30px">
    <div class="cover__conf" style="font-size:12px">{E(d["classification"])} · {E(d["version"])}</div>
  </div>
  <div class="cover__bottom" style="left:72px;right:72px;bottom:56px">
    <div class="back__tagline">{brand.TAGLINE_HTML}</div>
    <div class="cover__rule"></div>
    <div class="cover__meta">{m}</div>
    <div class="cover__notice" style="font-size:11px">{E(d["notice"])} · © {d["date"][:4]} {brand.COPYRIGHT}</div>
  </div>
</section>
'''


def foot(d, n, total):
    return f'<div class="deck__foot"><span>{E(d["footer"])}</span><span>{n:02d} / {total:02d}</span></div>'


def content_slide(d, sl, head, n, total):
    if "main" in sl:
        main = "".join(item_html(k, v) for item in sl["main"] for k, v in item.items())
    else:
        main = "".join(item_html(k, sl[k]) for k in ORDER if k in sl)
    margin = (f'<div class="tag">{E(sl["tag"])}</div>' if sl.get("tag") else "") + (f'<div class="source">{E(sl["source"])}</div>' if sl.get("source") else "")
    label = sl.get("name") or sl.get("tag") or f"slide {n}"
    return f'''<!-- ========================= {n:02d} · {E(label.upper())} ========================= -->
<section class="canvas canvas--deck" data-name="{E(d['stem'])}-{n:02d}-{slug(label).lower()}">
  <div class="deck">
    <div class="deck__head"><span>{E(head)}</span><span>{n:02d}</span></div>
    <div class="deck__grid">
      <div class="deck__margin">{margin}</div>
      <div class="deck__main">
{main}      </div>
    </div>
  </div>
  {foot(d, n, total)}
</section>
'''


def divider_slide(d, sl, n, total):
    return f'''<!-- ========================= {n:02d} · DIVIDER ========================= -->
<section class="canvas canvas--deck" data-name="{E(d['stem'])}-{n:02d}-divider">
  <div class="deck--divider">
    <div class="divider__n">{E(str(sl["n"]))}</div>
    <div class="divider__kicker">{E(sl["kicker"])}</div>
    <div class="divider__title">{EM(title_case(sl["title"]))}</div>
  </div>
  {foot(d, n, total)}
</section>
'''


def statement_slide(d, sl, n, total):
    return f'''<!-- ========================= {n:02d} · STATEMENT ========================= -->
<section class="canvas canvas--deck" data-name="{E(d['stem'])}-{n:02d}-statement">
  <div class="deck--statement">
    <div class="statement__mark"></div>
    <div class="statement__text">{EM(sl["text"])}</div>
    <div class="statement__who">{E(sl.get("who", d["kicker"]))}</div>
  </div>
  {foot(d, n, total)}
</section>
'''


def build(d, out_html, relative=False):
    d = dict(d)
    d["class_label"] = LABELS.get(d.get("class", "deck"), d.get("class", "Deck").replace("-", " ").capitalize())
    d.setdefault("kicker", f"{d['class_label']} · {d['subject']}")
    d.setdefault("notice", brand.NOTICE)
    d.setdefault("footer", brand.FOOTER if d.get("classification", "Internal") != "Public" else brand.FOOTER_PUBLIC)
    d["stem"] = slug(d["subject"]).lower()
    A = "../" if relative else ASSETS.as_posix() + "/"
    head = f"{d['class_label']} · {d['subject']} · {d['classification']} · {d['version']}"
    slides = d["slides"]
    closing = d.get("closing", True)
    total = 1 + len(slides) + (1 if closing else 0)
    out = [title_slide(d, A)]
    n = 2
    for sl in slides:
        kind = sl.get("kind", "content")
        if kind == "divider":
            out.append(divider_slide(d, sl, n, total))
        elif kind == "statement":
            out.append(statement_slide(d, sl, n, total))
        elif kind == "content":
            out.append(content_slide(d, sl, head, n, total))
        else:
            sys.exit(f"slide {n}: unknown kind {kind!r} (content | divider | statement)")
        n += 1
    if closing:
        out.append(closing_slide(d, A, n, total))
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{brand.NAME} · Deck · {E(d["subject"])}</title>
<link rel="stylesheet" href="{A}{brand.CSS}">
<style>@page{{size:1280px 720px;margin:0}}</style>
</head>
<body>

{"".join(out)}
</body>
</html>
'''
    p = pathlib.Path(out_html)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(doc, encoding="utf-8")
    pdf_name = f"{brand.FILE_PREFIX}-Deck-{slug(d['subject'])}-{d['version']}.pdf"
    return p, pdf_name, total


def _example():
    with open(ASSETS / "examples" / "deck-parallel-mcp.json", encoding="utf-8") as fh:
        return json.load(fh)


EXAMPLE = _example()


def main():
    args = sys.argv[1:]
    if "--example" in args:
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False)); return
    if len(args) < 2:
        print(__doc__); sys.exit(1)
    with open(args[0], encoding="utf-8") as fh:
        d = json.load(fh)
    out, pdf_name, total = build(d, args[1], relative="--relative" in args)
    print(f"-> {out}  ({total} slides)  PDF name: {pdf_name}")
    code = 0
    if "--png" in args:
        folder = args[args.index("--png") + 1]
        subprocess.run([sys.executable, str(HERE / "render_png.py"), str(out), folder], check=True)
    if "--pdf" in args:
        pdf = out.with_name(pdf_name)
        subprocess.run([sys.executable, str(HERE / "render_pdf.py"), str(out), str(pdf), "--size", "1280x720", "--sheets", ".canvas--deck"], check=True)
        code = subprocess.run([sys.executable, str(HERE / "check_pdf.py"), str(pdf), "--html", str(out), "--size", "1280x720"]).returncode
    sys.exit(code)


if __name__ == "__main__":
    main()
