# cooper-brand

Cooper Labs' brand kit for documents and social: the A4 internal-document
template and its sixteen page styles, the monthly report, the deck, the
fact sheet, the meeting note, the quote, the social cards of the Figma file
and the sizes around them, the brand renders and the script that makes new
ones. Seven skills:

| Skill | Use it for |
|---|---|
| `cooper-brand-kit` | tokens, type, the logo, the renders, voice, the build route. Loaded by every other skill. |
| `cooper-internal-document` | proposal, case study, spec, post-mortem, memo, guide, monthly report, as a branded A4 PDF; sixteen page styles (divider, statement, hero figure, two columns, timeline, data page, chart, matrix, plate, prose, steps, glossary, flow, checklist, code) |
| `cooper-deck` | the same document on a screen: 16:9, one block per slide, title, divider, statement and closing slides, PDF and PNG |
| `cooper-fact-sheet` | one A4 page on the studio, a service or a product shipped: figures, two columns, a table, a contact strip |
| `cooper-note` | a one-page meeting note: the facts, the decisions numbered, the actions with owner and date, the next meeting |
| `cooper-quote` | a two-page quote: the parties, the phases with their prices, the schedule, the terms, the signatures |
| `cooper-social` | the cards of the Figma file (post on the render or on the halftone, partner card, X cover in two variants, social preview) and the plugin's sizes (LinkedIn, square, story, newsletter, X header, paragraph, wallpaper), the forum header and Notion cover banners, thread cards, and the animated MP4 of any card |

Everything is in English, whatever the language of the request. The engine
is the one of `parallel-brand` (same scripts, same checks); the identity is
in `assets/css/cooper.css`, `assets/scripts/brand.py`, `assets/logo/` and
`assets/img/`.

## Produce a document

```bash
S=${CLAUDE_PLUGIN_ROOT}/assets/scripts
python3 $S/build_doc.py --example > work.json         # a description to start from (or new_doc.py <class> --demo work.html)
# edit work.json: cover meta, pages, blocks
python3 $S/build_doc.py work.json work.html --pdf     # HTML, CooperLabs-<Class>-<Subject>-vX.X.pdf, check_pdf.py
```

Page numbers, the Contents page and the version in its four places are
computed. Raw HTML still works: `new_doc.py internal-doc work.html`, edit,
`render_pdf.py work.html out.pdf --png review/`, `check_pdf.py out.pdf --html work.html`.

## Produce social cards

```bash
python3 $S/build_social.py --example > posts.json     # the canvases of the template (or new_doc.py social --demo posts.html)
# edit posts.json: keep the canvases you need, fill the content, name them
python3 $S/build_social.py posts.json posts.html --png out/   # HTML, one PNG per canvas, check_png.py
```

The builder lays the render or the halftone, the mark or the wordmark, and
frames the render for the size; `render_png.py` warns when text lands on
the block of a render and prints the `frame.py` command that shows the
crop; `check_png.py` fails on a title on three lines, text over the logo,
a logo off centre, a PNG at the wrong size. `--only "post-*"` renders a
subset; `--scale 2` doubles the size.

## Produce a deck, a fact sheet, a note, a quote, a render

```bash
python3 $S/build_deck.py --example > deck.json && python3 $S/build_deck.py deck.json deck.html --pdf --png out/      # 16:9, one slide per page + PNGs
python3 $S/build_fact_sheet.py --example > sheet.json && python3 $S/build_fact_sheet.py sheet.json sheet.html --pdf   # one A4 page
python3 $S/build_note.py --example > note.json && python3 $S/build_note.py note.json note.html --pdf               # a one-page meeting note
python3 $S/build_quote.py --example > quote.json && python3 $S/build_quote.py quote.json quote.html --pdf           # a two-page quote
python3 $S/new_doc.py report --demo september.html && python3 $S/build_doc.py september.json september.html --pdf  # the monthly report
python3 $S/render_anim.py posts.html out/ --only post-2026-roadmap                                                   # the animated card, MP4
python3 $S/render_block.py --preset orange --yaw 30 --scale 0.25 --out look.png                                       # a new render of the block, a look
python3 $S/render_block.py --preset orange --yaw 30 --catalogue 09 --name block-orange-right                          # ... the master and its catalogue entry
```

The smoke test of the whole pipeline, one line each:

```bash
python3 $S/new_doc.py social --demo posts.html && python3 $S/render_png.py posts.html out/ && python3 $S/check_png.py posts.html out/
python3 $S/new_doc.py internal-doc --demo work.html && python3 $S/build_doc.py work.json work.html --pdf
python3 $S/new_doc.py page-styles --demo styles.html && python3 $S/build_doc.py styles.json styles.html --pdf
python3 $S/new_doc.py deck-parallel-mcp --demo deck.html && python3 $S/build_deck.py deck.json deck.html --pdf
python3 $S/new_doc.py fact-sheet-cooper-labs --demo sheet.html && python3 $S/build_fact_sheet.py sheet.json sheet.html --pdf
```

Needs Python with Playwright and Chromium: `pip install playwright && playwright install chromium`
(poppler or pypdf for the PDF text layer, and ffmpeg for the animated card, optional).
Fonts, logos and renders ship with the plugin; nothing is fetched at render
time. PP Eiko does not ship: see `assets/fonts/private/README.md`.

The example content (the Parallel MCP server proposal, Atlas Wallet, the
launch-day post-mortem, the Friday-demos memo) is illustrative; the figures
are placeholders, not records.

## Layout

```
skills/cooper-brand-kit/            SKILL.md + references/ (tokens, voice, pencil: the design source)
skills/cooper-internal-document/    SKILL.md
skills/cooper-deck/                 SKILL.md
skills/cooper-fact-sheet/           SKILL.md
skills/cooper-social/               SKILL.md
assets/css/cooper.css               the stylesheet: the document engine with the Cooper Labs tokens, the social section transcribed from the Figma file
assets/templates/internal-doc.json  the 24-sheet skeleton (a proposal on every page style), description and built .html
assets/templates/social.json        every social canvas (17): post (3), partner, X cover (2), preview, the extra sizes (5), banners (2), thread (3), and the built .html
assets/examples/*.json              case study, spec, post-mortem, memo, page-styles (19 sheets), deck (7 slides), fact sheet, and the built .html
assets/scripts/                     build_doc.py · build_social.py · build_deck.py · build_fact_sheet.py · new_doc.py · render_pdf.py · render_png.py · render_anim.py · check_pdf.py · check_png.py · frame.py · fontcheck.py · brand.py
assets/logo/                        the horizontal and vertical wordmarks, the mark (black, white, orange), the avatars; partners/ for the partner cards
assets/img/renders/                 the six Figma masters, 1841 x 1151, numbered 01-06; new ones from render_block.py from 07
assets/img/catalogue.json           every render by number: ground, busy, subject, focus, zoom, frames per size
assets/fonts/                       Roboto Condensed and Instrument Serif (OFL); private/ for PP Eiko (not shipped)
```
