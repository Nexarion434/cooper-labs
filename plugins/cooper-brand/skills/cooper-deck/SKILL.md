---
name: cooper-deck
description: >
  This skill should be used for a Cooper Labs slide deck: "deck", "slides",
  "presentation", "a few slides for the client", "turn this proposal into
  slides", "pitch the MCP server", "present the case study", or when a
  document, a proposal or a set of figures has to be shown on a screen
  rather than read on paper. 16:9, 1280 x 720, the same grid and blocks as
  the internal document, one block per slide, delivered as a PDF and as PNG
  per slide.
metadata:
  version: "0.4.1"
  source: "cooper-brand 0.4.1 — the parallel-brand deck with the Cooper Labs identity"
---

# Cooper Labs — deck

The internal document, on a screen. Every slide is the A4 page on 16:9:
the margin column (the label, the source) beside one block (heading,
body, bullets, a table on hairlines, the figures strip or the
recommendation), the running head above, the footer below, no rules. A
title slide opens it with the render as a plate on the left half, a
closing slide ends it the same way, with the tagline and the links at the
right. **English
throughout.** Load `cooper-brand-kit` first if the tokens are not already in
context.

## When a deck, when a document

A deck carries one idea per slide and is read aloud; a document carries the
evidence and is read alone. Write the proposal first when there is a
decision to record; make the deck from it (same subject, same version) for
the meeting. A deck never replaces the decision log.

## Intake, in one round

| Question | Options |
|---|---|
| What does it present, and to whom? | one line, free text; the kicker carries the audience and the date (`Proposal · Parallel MCP server · Parallel team, 14 September 2026`) |
| Which class? | proposal · case study · spec · post-mortem · memo · briefing · update · pitch |
| Classification and status? | Confidential · Draft (default) · Internal · Public · Final |
| Render for the title slide? | three of the six by number and scene from `assets/img/catalogue.json`, the plain dark slide, plus "pick for me" |

Owner is the person asking unless told otherwise. Date is today. Version
follows the document it presents, or `v0.1` for a draft.

## Build

```bash
S=${CLAUDE_PLUGIN_ROOT}/assets/scripts
python3 $S/build_deck.py --example > deck.json               # a description to start from (or new_doc.py deck-parallel-mcp --demo deck.html)
# edit deck.json: meta, then slides
python3 $S/build_deck.py deck.json deck.html --pdf --png out/   # HTML, CooperLabs-Deck-<Subject>-vX.X.pdf (one slide per page), one PNG per slide, check_pdf.py
```

The description carries `class`, `subject`, `title` (a `*phrase*` may
mark the claim; it renders in ink), `standfirst`, `kicker`, `version`,
`classification`, `status`, `date`, `owner`, `render` (`"01"` to `"06"`
for the plate on the title slide, or `"dark"`), `back` (`"05"` default,
or `"dark"`) and `slides`. A
slide is either a content slide (`tag`, `source`, then `heading`, `body`,
`bullets`, `table`, `figures`, `reco`, the keys of `build_doc.py`, or
`main` for another order), a `divider` (`n`, `kicker`, `title`) or a
`statement` (`text`, `who`). Slide numbers, `NN / NN`, the version in the
title slide, every running head and the closing slide, and the file name
are computed; `closing: false` drops the closing slide.

`check_pdf.py deck.pdf --html deck.html --size 1280x720` verifies the page
size, the copy hygiene, the version and the numbering. `render_png.py` gives
the PNGs (for a chat, a Telegram message, a thumbnail); `check_png.py`
accepts the `canvas--deck` size.

## Slides

| Slide | Use | Composition |
|---|---|---|
| Title | first | the render at cover fit on the left half, wordmark and `CLASSIFICATION · vX.X` at the top; at the right: kicker, title 56, standfirst, the meta pairs at the bottom |
| Content | the argument | the margin column (label 11, source 12) beside the block: heading 40, body 17, bullets (22 / 15), table 15 on hairlines, the figures strip at 72, the recommendation 30 |
| Divider | a new part | kicker and title 64 at the bottom left; no number; footer only |
| Statement | the one sentence to remember | text 48 at the left, vertically centred, the source line under it |
| Closing | last | the render on the left half (`back`), the wordmark; at the right, bottom-aligned: the tagline 48, the studio links and `This deck · Class · vX.Y · date` as pairs |

One block per content slide. When a block does not fit (a table longer than
five rows, more than four bullets, a body over four lines), split it over
two slides rather than shrinking the type: the footer numbers follow.

## Rules specific to the deck

- **Title Case on titles and headings**, sentence case elsewhere (rules in
  `cooper-brand-kit/references/voice.md`); a `*phrase*` renders in ink.
- **Numbers alone in a figure cell** (`6`, `74%`); figures in tables are
  tabular. Never bold a figure.
- **No em dash** anywhere on a slide; the middle dot separates meta items.
- The running head reads `CLASS · SUBJECT · CLASSIFICATION · vX.X`, the
  footer `COOPER LABS · INTERNAL · NOT FOR DISTRIBUTION` and `NN / NN`;
  `Public` decks get `COOPER LABS · COOPERLABS.XYZ`.
- A render appears on the title slide and the closing slide only; a
  content slide has no picture and no colour. Dividers and statements sit
  on the white ground.
- Deliver the PDF; the PNGs are for a message or a preview, never for
  printing.

## Before delivering

1. Version, subject and classification identical on the title slide, in
   every running head, on the closing slide and in the file name.
2. Every slide fits: nothing runs into the footer (look at the PNGs).
3. Every table has a source line in the margin, with a date.
4. `check_pdf.py ... --size 1280x720` passes and the title slide was looked
   at in a real viewer.

## References

- `cooper-brand-kit/references/tokens.md` — the Deck section, sizes and CSS classes
- `cooper-internal-document/SKILL.md` — the blocks, the classes, the writing rules the deck borrows
- `../../assets/examples/deck-parallel-mcp.json` and `.html` — the seven-slide example
- `../../assets/scripts/build_deck.py` — the builder
