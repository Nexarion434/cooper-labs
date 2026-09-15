#!/usr/bin/env python3
"""Build a Cooper Labs quote (two A4 pages) from a description.

    python3 build_quote.py quote.json quote.html          # writes the HTML and prints the PDF name to use
    python3 build_quote.py quote.json quote.html --pdf    # ... and renders the PDF next to it, then checks it
    python3 build_quote.py --example > quote.json         # a description to start from

Two pages, no cover, on the catalogue page of the internal document. Page
one is the offer: the parties and the quote's facts in the margin column,
the title, the introduction, the phases as a table across the measure with
the total. Page two is the agreement: the payment schedule, the terms as a
numbered list, the acceptance block for both signatures. Prices are written
as given (`"24 000"`), the currency once (`currency`).

The description (JSON):

    subject        "Parallel MCP server"                 -> running head, file name
    number         "Q-2026-014"; date "2026-09-14"; valid_until "2026-10-14"
    currency       "EUR" (default) ; vat "VAT not applicable, art. 293 B CGI" | "excl. VAT" (the note under the total)
    client         {"name": "Parallel Protocol", "lines": ["Noah Levy, Protocol lead", "noah@parallel.fi"]}
    from           {"name": "Cooper Labs", "lines": [...]}   (default: the studio's lines from brand.py)
    title          "Parallel MCP server, six weeks"
    intro          ["one or two paragraphs: what is proposed, from the brief", ...]
    phases         [{"name": "Phase one · Server", "what": "...", "weeks": "3", "price": "24 000"}, ...]
    total          "42 000"
    schedule       [["On signature", "20 September", "30%", "12 600"], ...]   (milestone, when, share, amount)
    terms          ["Fixed price per phase; the next phase starts on a demo, not on a plan.", ...]
    signatories    [["For Cooper Labs", "Jean Brasse, Founder"], ["For Parallel Protocol", "Noah Levy, Protocol lead"]]
    classification Confidential (default)
"""
import sys, os, json, pathlib, subprocess

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE.parent
sys.path.insert(0, str(HERE))
import brand   # noqa: E402
from build_doc import E, EM, title_case, slug, long_date, body, table, block_html   # noqa: E402

FROM_LINES = ["Jean Brasse, Founder", "contact@cooperlabs.xyz", "cooperlabs.xyz"]


def party(k, name, lines):
    ls = "".join(f"<div>{E(x)}</div>" for x in lines)
    return f'<div class="quote__party"><div class="k">{E(k)}</div><div class="v"><div class="quote__name">{E(name)}</div>{ls}</div></div>'


def facts(items):
    return "".join(f'<div class="note__pair"><div class="k">{E(k)}</div><div class="v">{E(v)}</div></div>' for k, v in items)


def numbered(items):
    rows = "".join(f'<div class="nlist__row"><div class="nlist__n">{i:02d}</div><div><div class="nlist__x">{E(t)}</div></div></div>\n' for i, t in enumerate(items, 1))
    return f'        <div class="nlist">\n{rows}        </div>\n'


def phases_table(d):
    cur = d.get("currency", "EUR")
    rows = [[p["name"], p.get("what", ""), str(p.get("weeks", "")), p["price"]] for p in d["phases"]]
    out = f'        <table class="table table--quote">\n          <tr><th>Phase</th><th>What is delivered</th><th style="width:60px">Weeks</th><th style="width:100px">Price, {E(cur)}</th></tr>\n'
    for r in rows:
        out += f'          <tr><td class="strong">{E(r[0])}</td><td>{E(r[1])}</td><td class="mono">{E(r[2])}</td><td class="mono">{E(r[3])}</td></tr>\n'
    if d.get("total"):
        out += f'          <tr class="total"><td class="strong">Total</td><td>{E(d.get("vat", "excl. VAT"))}</td><td class="mono"></td><td class="mono">{E(d["total"])}</td></tr>\n'
    return out + "        </table>\n"


def sheet(A, head, n, total, inner, foot):
    return f'''<section class="page page--quote">
  <div class="pagehead"><img class="pagehead__logo" src="{A}{brand.LOGO_B}" alt="{brand.NAME}"><div class="pagehead__meta">{E(head)}</div></div>
{inner}  <div class="pagefoot"><div class="pagefoot__meta">{E(foot)}</div><div class="pagefoot__page">{n:02d} / {total:02d}</div></div>
</section>
'''


def build(d, out_html, relative=False):
    d = dict(d)
    d.setdefault("classification", "Confidential")
    d.setdefault("currency", "EUR")
    d.setdefault("footer", f"{brand.NAME} · {d['classification']} · Quote {d['number']}")
    A = "../" if relative else ASSETS.as_posix() + "/"
    head = f"Quote · {d['subject']} · {d['number']} · {long_date(d['date'])}"
    frm = d.get("from", {"name": brand.NAME, "lines": FROM_LINES})
    f = [("Quote", d["number"]), ("Date", long_date(d["date"]))]
    if d.get("valid_until"):
        f.append(("Valid until", long_date(d["valid_until"])))
    intro = body(d["intro"]) if d.get("intro") else ""
    page1 = f'''  <div class="quote">
    <div class="quote__head">
      <div class="quote__parties">{party("To", d["client"]["name"], d["client"].get("lines", []))}{party("From", frm["name"], frm.get("lines", []))}<div class="note__facts">{facts(f)}</div></div>
      <div><div class="tag">Quote · {E(d["classification"])}</div><div class="note__title">{EM(title_case(d["title"]))}</div>{intro}</div>
    </div>
    <div class="content">
{block_html(None, phases_table(d))}    </div>
  </div>
'''
    blocks = []
    if d.get("schedule"):
        blocks.append(block_html("Payment schedule", table([["Milestone", None], ["When", 110], ["Share", 60], [f"Amount, {d['currency']}", 100]], d["schedule"], mono=(2, 3), strong=(0,))))
    if d.get("terms"):
        blocks.append(block_html("Terms", numbered(d["terms"])))
    sig = d.get("signatories", [["For " + brand.NAME, FROM_LINES[0]], ["For " + d["client"]["name"], d["client"].get("lines", [""])[0]]])
    sign = '        <div class="sign">' + "".join(f'<div><div class="k">{E(k)}</div><div class="v">{E(v)}</div><div class="sign__line">Date, signature</div></div>' for k, v in sig) + "</div>\n"
    blocks.append(block_html("Acceptance", body(d.get("acceptance", "Signed by both parties, this quote is the agreement: the scope, the price per phase and the schedule above. Anything outside it is a new quote.")) + sign))
    page2 = f'''  <div class="quote">
    <div class="content" style="margin-top:56px">
{"".join(blocks)}    </div>
  </div>
'''
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{brand.NAME} · Quote · {E(d["subject"])} · {E(d["number"])}</title>
<link rel="stylesheet" href="{A}{brand.CSS}">
</head>
<body>

<!-- ========================= QUOTE · {E(d["subject"].upper())} · 01 ========================= -->
{sheet(A, head, 1, 2, page1, d["footer"])}
<!-- ========================= QUOTE · {E(d["subject"].upper())} · 02 ========================= -->
{sheet(A, head, 2, 2, page2, d["footer"])}</body>
</html>
'''
    p = pathlib.Path(out_html)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(doc, encoding="utf-8")
    pdf_name = f"{brand.FILE_PREFIX}-Quote-{slug(d['subject'])}-{d['number']}.pdf"
    return p, pdf_name


def _example():
    with open(ASSETS / "examples" / "quote-parallel-mcp.json", encoding="utf-8") as fh:
        return json.load(fh)


def main():
    args = sys.argv[1:]
    if "--example" in args:
        print(json.dumps(_example(), indent=2, ensure_ascii=False)); return
    if len(args) < 2:
        print(__doc__); sys.exit(1)
    with open(args[0], encoding="utf-8") as fh:
        d = json.load(fh)
    out, pdf_name = build(d, args[1], relative="--relative" in args)
    print(f"-> {out}  PDF name: {pdf_name}")
    if "--pdf" in args:
        pdf = out.with_name(pdf_name)
        subprocess.run([sys.executable, str(HERE / "render_pdf.py"), str(out), str(pdf)], check=True)
        sys.exit(subprocess.run([sys.executable, str(HERE / "check_pdf.py"), str(pdf), "--html", str(out)]).returncode)


if __name__ == "__main__":
    main()
