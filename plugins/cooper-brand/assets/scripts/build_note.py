#!/usr/bin/env python3
"""Build a Cooper Labs meeting note (one A4 page) from a description.

    python3 build_note.py note.json note.html          # writes the HTML and prints the PDF name to use
    python3 build_note.py note.json note.html --pdf    # ... and renders the PDF next to it, then checks it
    python3 build_note.py --example > note.json        # a description to start from

One page, no cover, on the catalogue page of the internal document: the
wordmark and the running head, the title, the meeting's facts in the margin
column (date, where, who, owner), then the blocks: the context, the
decisions as a numbered list, the actions as a table (action, owner, due),
what comes next and the next meeting. Short by design: what was decided and
who does what, not minutes.

The description (JSON):

    subject        "Parallel weekly"                    -> running head, file name
    title          "Week 37: the server answers on Base"
    date           "2026-09-12"; where "Google Meet" | "Cooper Labs, Paris"
    attendees      ["Jean, Cooper Labs", "Noah, Parallel", ...]
    owner          "Jean, Cooper Labs"                  (who wrote the note)
    classification Internal (default) | Confidential
    context        one or two sentences: why the meeting, what was on the table
    decisions      [["Server first", "The CLI is derived from the server in week five; nothing else changes."], ...]
    actions        [["Confirm the three chains", "Noah", "16 Sep"], ...]
    next           one sentence on what happens before the next meeting (optional)
    next_meeting   "19 Sep 2026, 10:00, Google Meet" (optional)
"""
import sys, os, json, pathlib, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_text

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE.parent
sys.path.insert(0, str(HERE))
import brand   # noqa: E402
from build_doc import E, EM, title_case, slug, long_date, body, table, block_html   # noqa: E402


def pairs(items):
    return "".join(f'<div class="note__pair"><div class="k">{E(k)}</div><div class="v">{v}</div></div>' for k, v in items)


def numbered(items):
    rows = "".join(f'<div class="nlist__row"><div class="nlist__n">{i:02d}</div><div><div class="nlist__t">{E(t)}</div><div class="nlist__x">{E(x)}</div></div></div>\n' for i, (t, x) in enumerate(items, 1))
    return f'        <div class="nlist">\n{rows}        </div>\n'


def build(d, out_html, relative=False):
    d = dict(d)
    d.setdefault("classification", "Internal")
    d.setdefault("footer", brand.FOOTER)
    A = "../" if relative else ASSETS.as_posix() + "/"
    head = f"Meeting note · {d['subject']} · {long_date(d['date'])}"
    who = "<br>".join(E(a) for a in d.get("attendees", []))
    facts = [("Date", E(long_date(d["date"]))), ("Where", E(d.get("where", "")))] if d.get("where") else [("Date", E(long_date(d["date"])))]
    facts += [("Attendees", who)] if who else []
    facts += [("Note by", E(d["owner"]))] if d.get("owner") else []
    blocks = []
    if d.get("context"):
        blocks.append(block_html("Context", body(d["context"])))
    if d.get("decisions"):
        blocks.append(block_html("Decisions", numbered(d["decisions"])))
    if d.get("actions"):
        blocks.append(block_html("Actions", table([["Action", None], ["Owner", 110], ["Due", 70]], d["actions"], strong=(0,))))
    nxt = ""
    if d.get("next"):
        nxt += body(d["next"])
    if d.get("next_meeting"):
        nxt += f'        <div class="note__next"><span class="k">Next meeting</span><span class="v">{E(d["next_meeting"])}</span></div>\n'
    if nxt:
        blocks.append(block_html("Next", nxt))
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{brand.NAME} · Meeting note · {E(d["subject"])}</title>
<link rel="stylesheet" href="{A}{brand.CSS}">
</head>
<body>

<!-- ========================= MEETING NOTE · {E(d["subject"].upper())} ========================= -->
<section class="page page--note">
  <div class="pagehead"><img class="pagehead__logo" src="{A}{brand.LOGO_B}" alt="{brand.NAME}"><div class="pagehead__meta">{E(head)}</div></div>
  <div class="note">
    <div class="note__head">
      <div class="note__facts">{pairs(facts)}</div>
      <div><div class="tag">Meeting note · {E(d["classification"])}</div><div class="note__title">{EM(title_case(d["title"]))}</div></div>
    </div>
    <div class="content">
{"".join(blocks)}    </div>
  </div>
  <div class="pagefoot"><div class="pagefoot__meta">{E(d["footer"])}</div><div class="pagefoot__page">01 / 01</div></div>
</section>
</body>
</html>
'''
    p = pathlib.Path(out_html)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(doc, encoding="utf-8")
    pdf_name = f"{brand.FILE_PREFIX}-Note-{slug(d['subject'])}-{d['date']}.pdf"
    return p, pdf_name


def _example():
    with open(ASSETS / "examples" / "note-parallel-weekly.json", encoding="utf-8") as fh:
        return json.load(fh)


def main():
    args = [a for a in sys.argv[1:] if a != "--no-lint"]
    if "--example" in args:
        print(json.dumps(_example(), indent=2, ensure_ascii=False)); return
    if len(args) < 2:
        print(__doc__); sys.exit(1)
    with open(args[0], encoding="utf-8") as fh:
        d = json.load(fh)
    check_text.gate(d, args[0], "--no-lint" in sys.argv)
    out, pdf_name = build(d, args[1], relative="--relative" in args)
    print(f"-> {out}  PDF name: {pdf_name}")
    if "--pdf" in args:
        pdf = out.with_name(pdf_name)
        subprocess.run([sys.executable, str(HERE / "render_pdf.py"), str(out), str(pdf)], check=True)
        sys.exit(subprocess.run([sys.executable, str(HERE / "check_pdf.py"), str(pdf), "--html", str(out)]).returncode)


if __name__ == "__main__":
    main()
