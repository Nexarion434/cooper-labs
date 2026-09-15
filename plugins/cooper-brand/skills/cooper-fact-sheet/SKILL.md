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
  version: "0.5.0"
  source: "cooper-brand 0.5.0 — the parallel-brand fact sheet with the Cooper Labs identity"
---

# Cooper Labs — fact sheet

One A4 page, no cover, on the catalogue page: the wordmark and the
running head, an optional plate (`render`), a small label, a title, a
standfirst, the figures strip, two columns, an optional table on
hairlines, the contact pairs on an ink line, the footer. The blocks are
those of the internal document at smaller sizes (title 34, headings 18,
text 10), so a fact sheet and a proposal read as the same
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

The description carries `subject`, `title` (a `*phrase*` may mark the
claim; it renders in ink), `standfirst`, `render` (optional, `"01"` to
`"06"`), `date`, `version` (file name only), `classification`,
`figures` ([[number, key], ...]), `columns` (two objects with `heading` and
`bullets` or `body`), an optional `table` (`heading`, `cols`, `rows`,
`mono`, `strong`), `contact` ([[key, value], ...], default: the four studio
links) and `footer` (default `Cooper Labs · <Classification> · Figures as
of <Month YYYY>`). `kicker` (the running head) and `tag` (the label above
the title) are computed from the subject and the date unless given.

## Composition

| Item | Value | CSS |
|---|---|---|
| Running head | wordmark in ink, 16 high, left; label 7.5 muted `FACT SHEET · SUBJECT · MONTH YYYY` right; no rule | `.page--fact .pagehead`, `.pagehead__logo` |
| Plate | `render`: the render 180 high across the measure, 32 under the head | `.fact__img` |
| Label | 7.5 muted uppercase | `.tag` |
| Title | PP Eiko 500, 34 / 1, max 480, 12 under the label | `.fact__title` |
| Standfirst | Roboto Condensed 10.5 / 1.55 `ink-soft`, max 400 | `.fact__stand` |
| Figures | the strip on an ink line, numbers at 32, keys under | `.fact .figures` |
| Columns | two columns, gap 32; heading 18, bullets as a list on hairlines, body at 10 | `.fact__cols` |
| Table | the table on hairlines, with its heading | `.table` |
| Contact | four pairs on an ink line: key label 7.5, value 10 | `.fact__contact` |
| Footer | `COOPER LABS · PUBLIC · COOPERLABS.XYZ · MONTH YYYY` and `01 / 01` | `.pagefoot` |

Stack: 22 between the groups, 28 under the running head. Everything must fit
above the footer: a figures row, two columns of three bullets and a
four-row table do; a longer table means a second sheet, not a smaller type.

## Rules specific to the fact sheet

- **Title Case on the title and the headings**; sentence case on the
  standfirst, bullets and cells. A `*phrase*` renders in ink.
- **Figures carry a date** when they are measurements; a figure that
  describes the offer (`6` weeks, `Weekly` demos) needs none.
- **Public means public**: no client names without their agreement, no
  ticket numbers, no "TBD"; `check_pdf.py` greps the text layer.
- **One render at most**, as the plate at the top (`render`); the white
  3D (01) is the quiet default, a block render when the sheet is about the
  studio.
- Contact values are the four studio links unless told otherwise.

## Before delivering

1. Figures match the source; nothing invented.
2. Title and headings in Title Case.
3. Everything above the footer, nothing cut (look at the PNG).
4. `check_pdf.py` passes; the classification in the footer is the one
   intended.

## References

- `cooper-brand-kit/references/tokens.md` — the Fact sheet section
- `cooper-internal-document/SKILL.md` — the blocks and the writing rules
- `../../assets/examples/fact-sheet-cooper-labs.json` and `.html` — the studio one-pager
- `../../assets/scripts/build_fact_sheet.py` — the builder
