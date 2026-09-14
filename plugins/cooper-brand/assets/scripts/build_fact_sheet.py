#!/usr/bin/env python3
"""Build a Cooper Labs fact sheet (one A4 page, recto) from a description.

    python3 build_fact_sheet.py sheet.json sheet.html          # writes the HTML and prints the PDF name to use
    python3 build_fact_sheet.py sheet.json sheet.html --pdf    # ... and renders the PDF next to it, then checks it
    python3 build_fact_sheet.py --example > sheet.json         # a description to start from

One page, no cover: the wordmark and the running head at the top, a section
label and a title with its `*italic phrase*`, a standfirst, the headline
figures, two columns of headings with bullets or body, an optional table,
the contact strip, the footer. Everything is written from the same blocks as
the internal document, at the fact-sheet sizes (title 44, headings 18, text 10).

The description (JSON):

    subject        "sEURp"                       -> running head, file name
    kicker         "Fact sheet · sEURp · September 2026" (the running head; default "Fact sheet · <subject> · <Month YYYY>")
    tag            "sEURp · Fact sheet" (the section label above the title; default "<subject> · Fact sheet")
    title          "The euro savings rate, *on-chain and at par.*"
    standfirst     one or two sentences
    date           "2026-09-01"; version "v1.0" (file name only); classification Public | Internal
    figures        [["4.2%", "Current rate"], ...]           (three or four)
    columns        [{"heading": "How it *works*", "bullets": [[term, text], ...] | "body": "..."}, {...}]   (two)
    table          {"heading": "Backing, *as of 31 August*", "cols": [...], "rows": [...], "mono": [...], "strong": [...]}   (optional)
    contact        [["Website", "cooperlabs.xyz"], ["X", "@cooperlabs"], ...]   (default: website, X, Telegram, email)
    footer         "Cooper Labs · Public · Figures as of 31 Aug 2026"
"""
import sys, os, re, json, html, pathlib, subprocess, datetime

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE.parent
sys.path.insert(0, str(HERE))
import brand   # noqa: E402
from build_doc import E, EM, title_case, slug, heading, body, bullets, table, figures   # noqa: E402


def month(iso):
    d = datetime.date.fromisoformat(iso)
    return d.strftime("%B %Y")


def column(c):
    out = heading(c["heading"], c.get("suffix")) if c.get("heading") else ""
    if c.get("body"):
        out += body(c["body"])
    if c.get("bullets"):
        out += bullets(c["bullets"])
    return f"      <div>\n{out}      </div>\n"


def build(d, out_html, relative=False):
    d = dict(d)
    d.setdefault("classification", "Public")
    d.setdefault("kicker", f"Fact sheet · {d['subject']} · {month(d['date'])}")
    d.setdefault("tag", f"{d['subject']} · Fact sheet")
    d.setdefault("footer", f"{brand.NAME} · {d['classification']} · Figures as of {month(d['date'])}")
    d.setdefault("contact", brand.CONTACT)
    A = "../" if relative else ASSETS.as_posix() + "/"
    parts = [f'''    <div>
      <div class="tag">{E(d["tag"])}</div>
      <div class="fact__title">{EM(title_case(d["title"]))}</div>
      <div class="fact__stand">{E(d["standfirst"])}</div>
    </div>
''']
    if d.get("figures"):
        parts.append(figures(d["figures"]))
    if d.get("columns"):
        parts.append('    <div class="fact__cols">\n' + "".join(column(c) for c in d["columns"]) + "    </div>\n")
    if d.get("table"):
        t = d["table"]
        parts.append("    <div>\n" + (heading(t["heading"], t.get("suffix")) if t.get("heading") else "") +
                     table(t["cols"], t["rows"], mono=tuple(t.get("mono", ())), strong=tuple(t.get("strong", ())), highlight=t.get("highlight"), head=t.get("head", True)) + "    </div>\n")
    if d.get("contact"):
        cells = "".join(f'<div><div class="k">{E(k)}</div><div class="v">{E(v)}</div></div>' for k, v in d["contact"])
        parts.append(f'    <div class="fact__contact">{cells}</div>\n')
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{brand.NAME} · Fact sheet · {E(d["subject"])}</title>
<link rel="stylesheet" href="{A}{brand.CSS}">
</head>
<body>

<!-- ========================= FACT SHEET · {E(d["subject"].upper())} ========================= -->
<section class="page page--fact">
  <div class="pagehead"><img class="pagehead__logo" src="{A}{brand.LOGO_B}" alt="{brand.NAME}"><div class="pagehead__meta">{E(d["kicker"])}</div></div>
  <div class="fact">
{"".join(parts)}  </div>
  <div class="pagefoot"><div class="pagefoot__meta">{E(d["footer"])}</div><div class="pagefoot__page">01 / 01</div></div>
</section>
</body>
</html>
'''
    p = pathlib.Path(out_html)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(doc, encoding="utf-8")
    pdf_name = f"{brand.FILE_PREFIX}-Fact-Sheet-{slug(d['subject'])}-{d.get('version', 'v1.0')}.pdf"
    return p, pdf_name


def _example():
    with open(ASSETS / "examples" / "fact-sheet-cooper-labs.json", encoding="utf-8") as fh:
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
    out, pdf_name = build(d, args[1], relative="--relative" in args)
    print(f"-> {out}  PDF name: {pdf_name}")
    if "--pdf" in args:
        pdf = out.with_name(pdf_name)
        subprocess.run([sys.executable, str(HERE / "render_pdf.py"), str(out), str(pdf)], check=True)
        sys.exit(subprocess.run([sys.executable, str(HERE / "check_pdf.py"), str(pdf)]).returncode)


if __name__ == "__main__":
    main()
