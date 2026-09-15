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
  version: "0.3.1"
  source: "cooper-brand 0.3.1 — the parallel-brand deck with the Cooper Labs identity"
---

# Cooper Labs — deck

The internal document, on a screen. Every slide is the A4 page scaled ×1.6:
the label row (the boxed label, the source) over one block (heading, body,
ruled cells, a ruled table, the tiles or the recommendation band), the
running head above, the footer below, both on ink rules. A title slide
opens it as a poster (the halftone, the title centred, the mark), a
closing slide ends it as the poster on ink with the tagline and the links. **English
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

The description carries `class`, `subject`, `title` with its `*orange
phrase*`, `standfirst`, `kicker`, `version`, `classification`, `status`,
`date`, `owner`, `render` (`"01"` to `"06"`, `"02"` for the halftone at 60%, or `"dark"`) and `slides`. A
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
| Title | first | the poster: the halftone (or the render) at 55% under the fade, wordmark and `CLASSIFICATION · vX.X` at the top, centred kicker, title (96 at −0.07 em, one orange phrase), standfirst, the mark, the meta line |
| Content | the argument | label row: boxed label 12, source 12; then heading 48 (split from the body at 380), body 17, ruled cells (24 / 15), ruled table 15, tiles 88, the band 34 |
| Divider | a new part | the number bare at 220, kicker, title 76; footer only |
| Statement | the one sentence to remember | the poster: the mark, text 64 centred with its orange phrase, source line |
| Closing | last | the poster on ink: the tagline, the orange mark, one line with the studio links and `Class · vX.Y · date` |

One block per content slide. When a block does not fit (a table longer than
five rows, more than four bullets, a body over four lines), split it over
two slides rather than shrinking the type: the footer numbers follow.

## Rules specific to the deck

- **Title Case on titles and headings**, sentence case elsewhere; **one
  orange phrase** per title, heading, divider title or statement, none on
  labels (rules in `cooper-brand-kit/references/voice.md`).
- **Numbers alone in a figure cell** (`6`, `74%`); figures in tables are
  tabular. Never bold a figure.
- **No em dash** anywhere on a slide; the middle dot separates meta items.
- The running head reads `CLASS · SUBJECT · CLASSIFICATION · vX.X`, the
  footer `COOPER LABS · INTERNAL · NOT FOR DISTRIBUTION` and `NN / NN`;
  `Public` decks get `COOPER LABS · COOPERLABS.XYZ`.
- The render appears **only on the title slide**; a content slide has no
  picture and no colour beyond the orange figure, phrase or band. Dividers
  and statements sit on the paper ground.
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
