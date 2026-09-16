#!/usr/bin/env python3
"""Start a Cooper Labs document or a set of social canvases, anywhere on disk.

    python3 new_doc.py internal-doc     out/parallel-mcp-proposal.html
    python3 new_doc.py case-study       out/atlas-wallet.html
    python3 new_doc.py post-mortem      out/relayer-outage.html
    python3 new_doc.py memo             out/pricing-model.html
    python3 new_doc.py spec             out/vault-dashboard.html
    python3 new_doc.py page-styles      out/styles.html         # the sixteen page styles, one per page
    python3 new_doc.py social           out/posts.html          # the social canvases
    python3 new_doc.py deck-parallel-mcp   out/deck.html      # a 16:9 deck
    python3 new_doc.py fact-sheet-cooper-labs out/sheet.html    # an A4 fact sheet
    python3 new_doc.py report           out/september.html       # the monthly report, eight sheets
    python3 new_doc.py note-parallel-weekly out/note.html        # a one-page meeting note
    python3 new_doc.py quote-parallel-mcp   out/quote.html       # a two-page quote

    python3 new_doc.py social --demo out/posts.html            # the description + the HTML built from it
    python3 new_doc.py internal-doc --demo out/review.html

Without `--demo`: a copy of the HTML template or example, to edit by hand.
With `--demo`: the JSON description of the same document is copied next to
the output (`out/posts.json`) and built with build_social.py, build_doc.py,
build_deck.py, build_fact_sheet.py, build_note.py or build_quote.py, so the whole pipeline runs from one command:

    python3 new_doc.py social --demo posts.html && python3 render_png.py posts.html out/ && python3 check_png.py posts.html out/
    python3 new_doc.py internal-doc --demo review.html && python3 build_doc.py review.json review.html --pdf

Edit the JSON afterwards and rebuild; the builders apply the rules (page
numbers, Contents, version in four places, alternating italic, framing).

`internal-doc` is the full skeleton (cover, contents, three parts on dividers,
every page style, appendices, back cover: 24 sheets), a proposal. The four others are one-page examples of
the other document classes; they share the same blocks and stylesheet.

The copy's `../css/`, `../img/` and `../logo/` references are rewritten to
absolute paths inside the plugin, so it renders from any directory.
"""
import sys, json, pathlib, shutil

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE.parent
SOURCES = {p.stem: p for d in ("templates", "examples") for p in (ASSETS / d).glob("*.html")}  # includes "social"


def main():
    args = sys.argv[1:]
    demo = "--demo" in args
    args = [a for a in args if a != "--demo"]
    if len(args) < 2 or args[0] not in SOURCES:
        print(__doc__)
        print("available:", ", ".join(sorted(SOURCES)))
        sys.exit(1)
    src, out = SOURCES[args[0]], pathlib.Path(args[1])
    out.parent.mkdir(parents=True, exist_ok=True)
    if demo:
        desc = src.with_suffix(".json")
        if not desc.exists():
            sys.exit(f"no description for {args[0]} ({desc.name} missing)")
        json_out = out.with_suffix(".json")
        shutil.copyfile(desc, json_out)
        print("->", json_out)
        sys.path.insert(0, str(HERE))
        with open(json_out, encoding="utf-8") as fh:
            d = json.load(fh)
        import check_text
        check_text.gate(d, json_out.name, "--no-lint" in sys.argv)
        if args[0] == "social":
            from build_social import build
            built, n = build(d, out, src=json_out.name)
            print(f"-> {built}  ({n} canvases)")
        elif args[0].startswith("deck"):
            from build_deck import build
            built, pdf_name, total = build(d, out)
            print(f"-> {built}  ({total} slides)  PDF name: {pdf_name}")
        elif args[0].startswith("fact-sheet"):
            from build_fact_sheet import build
            built, pdf_name = build(d, out)
            print(f"-> {built}  PDF name: {pdf_name}")
        elif args[0].startswith("note"):
            from build_note import build
            built, pdf_name = build(d, out)
            print(f"-> {built}  PDF name: {pdf_name}")
        elif args[0].startswith("quote"):
            from build_quote import build
            built, pdf_name = build(d, out)
            print(f"-> {built}  PDF name: {pdf_name}")
        else:
            from build_doc import build
            built, pdf_name, total = build(d, out)
            print(f"-> {built}  ({total} sheets)  PDF name: {pdf_name}")
        return
    html = src.read_text(encoding="utf-8")
    for folder in ("css", "img", "logo"):
        html = html.replace(f"../{folder}/", (ASSETS / folder).as_posix() + "/")
    out.write_text(html, encoding="utf-8")
    print("->", out)


if __name__ == "__main__":
    main()
