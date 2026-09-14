---
name: cooper-fact-sheet
description: >
  This skill should be used for a Cooper Labs fact sheet or one-pager: "fact
  sheet", "one-pager", "the studio on one page", "a page on what we do", "a
  recto for a prospect", "summarise the offer on one page", "a one-pager for
  the Atlas launch", or when the studio, a service, a product shipped for a
  client or a figure set has to fit on one A4 page for someone outside the
  team. One page, recto, delivered as a PDF.
metadata:
  version: "0.1.0"
  source: "cooper-brand 0.1.0 — the parallel-brand fact sheet with the Cooper Labs identity"
---

# Cooper Labs — fact sheet

One A4 page, no cover: the wordmark and the running head at the top, a
section label, a title with its orange phrase, a standfirst, the headline
figures, two columns, an optional table, the contact strip, the footer. The
blocks are those of the internal document at smaller sizes (title 44,
headings 18, text 10), so a fact sheet and a proposal read as the same
family. **English throughout.** Load `cooper-brand-kit` first if the tokens
are not already in context.

## Intake, in one round

| Question | Options |
|---|---|
| What is on the sheet? | the studio, a service, a product shipped (subject), one line on who reads it |
| The figures | three or four, with their date; if a figure is missing, ask, never invent |
| Classification | Public (default) · Internal |
| Contact strip | the four links pre-selected: website, X, Telegram, email |

The date is the as-of date of the sheet; it appears in the running head
(`Fact sheet · Cooper Labs · September 2026`) and in the footer.

## Build

```bash
S=${CLAUDE_PLUGIN_ROOT}/assets/scripts
python3 $S/build_fact_sheet.py --example > sheet.json          # a description to start from (or new_doc.py fact-sheet-cooper-labs --demo sheet.html)
# edit sheet.json
python3 $S/build_fact_sheet.py sheet.json sheet.html --pdf     # HTML, CooperLabs-Fact-Sheet-<Subject>-vX.X.pdf, check_pdf.py
python3 $S/render_pdf.py sheet.html sheet.pdf --png review/    # a PNG of the page when needed
```

The description carries `subject`, `title` with its `*orange phrase*`,
`standfirst`, `date`, `version` (file name only), `classification`,
`figures` ([[number, key], ...]), `columns` (two objects with `heading` and
`bullets` or `body`), an optional `table` (`heading`, `cols`, `rows`,
`mono`, `strong`), `contact` ([[key, value], ...], default: the four studio
links) and `footer` (default `Cooper Labs · <Classification> · Figures as
of <Month YYYY>`). `kicker` (the running head) and `tag` (the label above
the title) are computed from the subject and the date unless given.

## Composition

| Item | Value | CSS |
|---|---|---|
| Running head | wordmark in ink, 18 high, left; label 8 `FACT SHEET · SUBJECT · MONTH YYYY` right; hairline | `.page--fact .pagehead`, `.pagehead__logo` |
| Label | the section label with its orange mark, 28 under the head | `.tag` |
| Title | PP Eiko 500, 44 / 1.05, max 600, one orange phrase, 14 under the label | `.fact__title` |
| Standfirst | Roboto Condensed 12 / 1.5 `ink-soft`, max 520 | `.fact__stand` |
| Figures | the headline-figures row, numbers at 34 | `.fact .figure__n` |
| Columns | two, gap 24; heading 18, bullets or body at 10 | `.fact__cols` |
| Table | the document table, with its heading | `.table` |
| Contact | four columns on a 1 px `ink` rule: key label 8, value 10.5 | `.fact__contact` |
| Footer | `COOPER LABS · PUBLIC · COOPERLABS.XYZ · MONTH YYYY` and `01 / 01` | `.pagefoot` |

Stack: 28 between the groups, 28 under the running head. Everything must fit
above the footer: a figures row, two columns of three bullets and a
four-row table do; a longer table means a second sheet, not a smaller type.

## Rules specific to the fact sheet

- **Title Case on the title and the headings, one orange phrase each**;
  sentence case on the standfirst, bullets and cells.
- **Figures carry a date** when they are measurements; a figure that
  describes the offer (`6` weeks, `Weekly` demos) needs none.
- **Public means public**: no client names without their agreement, no
  ticket numbers, no "TBD"; `check_pdf.py` greps the text layer.
- **No render** on a fact sheet: the wordmark is the only brand mark. The
  page is paper, the type does the work.
- Contact values are the four studio links unless told otherwise.

## Before delivering

1. Figures match the source; nothing invented.
2. Title and headings in Title Case with one orange phrase each.
3. Everything above the footer, nothing cut (look at the PNG).
4. `check_pdf.py` passes; the classification in the footer is the one
   intended.

## References

- `cooper-brand-kit/references/tokens.md` — the Fact sheet section
- `cooper-internal-document/SKILL.md` — the blocks and the writing rules
- `../../assets/examples/fact-sheet-cooper-labs.json` and `.html` — the studio one-pager
- `../../assets/scripts/build_fact_sheet.py` — the builder
