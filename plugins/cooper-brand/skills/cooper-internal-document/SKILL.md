---
name: cooper-internal-document
description: >
  This skill should be used for any long-form Cooper Labs document:
  "proposal", "statement of work", "case study", "spec", "post-mortem",
  "incident report", "memo", "guide", "write this up as a Cooper doc", or
  when turning a brief, a project or a decision into the branded A4 PDF.
  Covers the HTML to PDF build.
metadata:
  version: "0.3.1"
  source: "cooper-brand 0.3.1 — the parallel-brand engine with the Cooper Labs identity"
---

# Cooper Labs — internal document

One skeleton for every long document: a poster cover, as many section
pages as the argument needs on the block grid, a poster back cover. A4 at
96 dpi (794 × 1123): the cover reads like a post (the halftone, the title
centred, the mark), the inside like a spec sheet (ruled cells, boxed
labels, one orange figure, the orange band). **English throughout**, whatever language the request
is in. Load `cooper-brand-kit` first if the tokens are not already in
context.

## Document classes

| Class | Kicker | Default sections |
|---|---|---|
| Proposal | `PROPOSAL · <subject>` | Summary + figures → statement → Part one (divider, context & scope, prose, chart) → Part two (divider, options, two columns, timeline, hero figure, steps, flow, data page) → Part three (dark divider, decision + decision log, matrix, checklist + sign-off) → appendices (plate, tools, glossary, code). The 24-sheet template; a short proposal keeps the summary, context, options and decision pages |
| Case study | `CASE STUDY · <client>` | Client → figures → What we did → Outcome (table) → What we would change |
| Spec | `SPEC · <feature>` | Summary → Requirements (ID / requirement / priority) → Interface → Open questions |
| Post-mortem | `POST-MORTEM · <date>` | Incident → Timeline → Root cause → Actions |
| Memo | `MEMO · <subject>` | Rule or proposal → figures → Impact → Next steps |
| Guide | `GUIDE · <subject>` | whatever the guide needs; the page-styles example is one |

The skeleton is not a checklist. Add, reorder or drop sections to fit the
argument; the Contents page is only worth having from five pages up, and
past twelve entries it lists one line per page, named after the page. A
proposal to a client is `Confidential`; a case study or a memo is
`Internal`; either can be `Public` when it goes out.

## Intake, before anything else

One round, `AskUserQuestion`, defaults pre-selected:

| Question | Options |
|---|---|
| Which class? | proposal · case study · spec · post-mortem · memo · guide |
| What does it decide or record, and for whom? | one line, free text. If it cannot be answered the document is not ready |
| Classification and status? | Confidential · Draft (default) · Internal · Public · Final |
| Cover? | three of the six renders (`assets/img/renders/`, 01 to 06), named by number and scene from `assets/img/catalogue.json`, the plain dark cover, plus "pick for me" |

Owner is the person asking unless told otherwise. Date is today. Version is
`v0.1` for a draft, `v1.0` for a final.

## Build

Describe the document, let the builder lay it out. Nothing that repeats is
typed twice: page numbers, the Contents page, the version in its four places.

```bash
S=${CLAUDE_PLUGIN_ROOT}/assets/scripts
python3 $S/build_doc.py --example > work.json            # an annotated description to start from
# or copy a class: python3 $S/new_doc.py case-study --demo study.html  (writes study.json + study.html)
# edit work.json: cover meta, then pages, each a list of blocks
python3 $S/build_doc.py work.json work.html --pdf       # HTML, PDF named CooperLabs-<Class>-<Subject>-vX.X.pdf, check_pdf.py
python3 $S/render_pdf.py work.html CooperLabs-Proposal-Subject-v0.1.pdf --png review/   # review PNGs when needed
```

The description (`build_doc.py --example` prints one) carries `class`,
`subject`, `title` with its `*orange phrase*`, `standfirst`, `version`,
`classification`, `status`, `date` (ISO), `owner`, `cover` (`"01"` to
`"06"`, or `"dark"`), `versions` (the rows of the Versions table) and
`pages`, each a `name` and a list of blocks. A block is one row of the
margin grid: `tag` and `source` in the margin, then `heading`, `body`,
`bullets`, `table`, `figures`, `reco` in the reading column (or `main` as
an ordered list of one-key objects). Headings get Title Case; `toc` names
or hides a block's line on the Contents page. The Contents page is
generated from the tags when the document has five content pages or more
(`"contents": true | false` to force it).

Raw HTML remains possible for people who prefer it: `new_doc.py
internal-doc work.html` copies the skeleton, `render_pdf.py` renders it,
and `check_pdf.py work.pdf --html work.html` verifies the numbering by
hand. `new_doc.py <class> --demo out.html` writes both the description and
the HTML built from it, the one-command smoke test of the pipeline.

`render_pdf.py` warns when a page's content runs into the footer and ends
with the font line: `PP Eiko Medium, as in the Figma file`, or `Instrument
Serif stood in` (line breaks may then move by a word). `check_pdf.py` fails
on any inconsistency listed under *Before delivering*.

## Structure

**Cover.** The poster: a white page, the halftone at 55% fading to white
behind the title (`cover: "02"`, the default; another number puts that
render in the top 60%; `cover: "dark"`: ink, white type, the orange mark).
Wordmark top left, `CONFIDENTIAL · vX.X` (or `INTERNAL · vX.X`) top
right. Centred: the kicker (the class and the subject, in the posts'
condensed uppercase), the title in PP Eiko 92 at −0.07 em with one phrase
in orange (the brand signature: the verb or the qualifier, two or three
words), a standfirst that says **what the document decides and for whom**,
the mark alone; at the bottom, the meta as one line (date · classification
· status · owner) and the notice.

**Section pages.** Running head on an ink rule: the mark and `CLASS ·
SUBJECT · CLASSIFICATION · vX.X` left, page number right. Content is a
stack of blocks with a 28 gap; each block is a label row, then the content:

| Block | Label row | Content | CSS |
|---|---|---|---|
| Section label | the boxed label: an ink box with the white mark, then the label in an outline | | `.tag` |
| Source line | at the right of the label row, muted | | `.source` |
| Sub-heading | | PP Eiko 30 at 0.95, one orange phrase when the heading makes a claim, optional muted suffix; with a body after it, the heading takes the left column and the body the right, on a hairline | `.heading` |
| Body | | Roboto Condensed 10.5, max 560 | `.body` |
| Bullets | | ruled cells sharing borders: a counter, the term in PP Eiko 16, the text | `.bullets` |
| Table | | fully ruled: label head on paper, white cells; tabular cells for figures; one `tint` row allowed | `.table` |
| Headline figures | | ruled cells: the key at the top, the number in PP Eiko 56 at the bottom, the first number orange | `.figures` |
| Recommendation | | the band: an orange cell with the mark, then the ink panel with the title in white PP Eiko 22 and one or two paragraphs | `.reco` |

The first figure is the one that matters: its number is orange. A
block with figures alone has no label row. Sections are marked by the
boxed label, not by numbered headings; inside a section the sub-heading
marks the sub-part.

**Back cover.** The poster on ink: the tagline centred with its orange
phrase, the orange mark under it, the colophon as one line (the studio
links, then `Class · vX.Y · D Mon YYYY`) and the notice. Keep it; it is
what makes a printed copy read as finished.

## Page styles

Beyond the block stack, sixteen compositions inside the same grid, every
one a block or a page of `build_doc.py` and shown one per page in
`assets/examples/page-styles.json`. Use them where the argument needs them,
not to decorate: a long proposal opens each part with a divider, puts its
one sentence on a statement page, its one number on a hero page.

| Style | What it is for | In the description | Bends a rule |
|---|---|---|---|
| A · Divider | opens a part: the number bare at 180, kicker, title, standfirst, four ruled cells | page `style: divider` (`n`, `kicker`, `title`, `standfirst`, `list`) | |
| B · Divider, dark | the same on the ink ground, for the decision part | `style: divider`, `dark: true` | dark ground inside |
| C · Statement | the one sentence to remember, the poster: the mark, the sentence at 46 centred, one orange phrase | `style: statement` (`text`, `who`) | |
| D · Hero figure | one number at 130, its unit in orange, a body and the tiles | `style: hero` (`n`, `unit`, `kicker`, `body`, `figures`) | |
| E · Two columns | two ruled cells side by side, a boxed head, bullets as a list, a verdict at the bottom | block `cols` (`columns`: `head`, `bullets` or `body`, `verdict`) | |
| F · Timeline | a ruled box: steps on an ink rule with orange squares, past steps in the light hairline, phases under | block `timeline` (`steps`, `phases`) | |
| G · Data page | the ruled table across the whole measure, a foot line | page `style: wide` (`heading`, `table`, `foot`) | no margin column |
| H · Chart | bar (two series, one soft) or line, inline SVG in a ruled box, a legend | block `chart` (`type`, `labels`, `series` or `values`, `max`, `unit`) | |
| I · Matrix | likelihood against impact as a ruled grid, the hot cell in orange | block `matrix` (`cols`, `rows` with `key` and `cells`, `hot`) | a tinted cell, not a row |
| J · Plate | one render across the measure in an ink frame, on the opening page of a part | page `style: plate` (`render`, `caption`, then `blocks`) | imagery inside |
| K · Prose | a lede at 18, two columns of running text, a signature | page `style: prose` (`lede`, `body`, `signature`) | no margin column |
| L · Steps | numbered steps, the number in an ink box at the left, a meta line | blocks with `step`, `heading`, `body`, `meta` | |
| M · Glossary | terms as ruled cells in two columns, PP Eiko 15 | block `defs` | |
| N · Flow | square white boxes on an ink stroke, an orange dot at every arrow head, a caption | block `flow` (`boxes`, `arrows`, `caption`, `height`) | |
| O · Checklist | ruled rows, ticked boxes in orange, owner and date, four sign-off cells | blocks `checklist`, `signoff` | |
| P · Code | the ink panel, Roboto Condensed 9, comments muted, keywords in orange | block `code` (`text`, `keywords`) | |

The five that bend a rule (B, G, I, J, K) are for the opening page of a part
or a single appendix, never in the flow of an argument; say in the reply
when one was used. The Contents page lists a style page by its `toc`.

## Rules specific to this document

- **Titles are Title Case.** Cover title, sub-headings, tagline: capitalise
  every word except short connectors (a, the, of, for, to, with, under…);
  first and last words always. Standfirst, body, bullets, table cells and the
  recommendation title stay in sentence case. Rules in
  `cooper-brand-kit/references/voice.md`.
- **One orange phrase per headline, none on labels.** `<em>` in HTML,
  `*...*` in the description. Two or three words, the part that carries the
  claim. No italic exists in this identity.
- **The bold lead-in is its own node.** A bullet carries the claim in the
  term and the explanation in the text.
- **Tables.** Built from the same three cells: head, text, figure. Exactly
  one column fills; the others carry pixel widths. Head cells are left
  aligned. Every table has a source line in the margin, with a date.
- **Figures.** Numbers alone in a headline-figure cell (`6`, not `6 weeks`:
  the word goes in the key); figures inside tables are tabular. Never bold a
  figure.
- **Sources on the label row.** The source line sits at the right of the
  section label of the block that owns the table, not under the table.
- **No em dashes**, no lorem, no unfilled `vX.X` or `TBD` left in a final.
  `check_pdf.py` greps the text layer for all four.
- **Numbering: every sheet counts.** The cover is sheet 01 and carries no
  number; the Contents page, when present, is 02; the interior runs on from
  there; the back cover is the last sheet and carries no number. Running head
  and footer show the same number, the footer as `NN / total` where the total
  is the sheet count, back cover included (an 8-sheet proposal reads
  `02 / 08` … `07 / 08`). `build_doc.py` computes all of it; `check_pdf.py`
  refuses a repeat, a gap, or a total that is not the sheet count.
- Footer reads `COOPER LABS · INTERNAL · NOT FOR DISTRIBUTION`, page number
  `NN / NN`.
- The version is identical on the cover, in every running head, on the back
  cover and in the filename `CooperLabs-<Class>-<Subject>-vX.X.pdf`;
  classification identical on the cover and in the running heads.

## Variable length

Keep each page's content under 939 px, measured as the sum of the block
heights plus 28 per gap. When a section overflows, **start a new page rather
than shrinking type**. A section may span pages; repeat the label only if
the reader would otherwise lose the thread. `render_pdf.py` reports any page
whose content reaches the footer.

## Writing a Cooper Labs document well

- The standfirst names the decision, the audience and the scope. If you
  cannot write it, the document is not ready.
- Lead with the conclusion. The summary says what was found and what is
  recommended; everything after it is evidence.
- A proposal names its demos and its phase gate; the timeline table is the
  contract.
- Every risk carries a mitigant or is stated as unmitigated.
- The decision log records open questions and how they were resolved.
  Supersede rows rather than deleting them.
- A case study ends with what the studio would change; a post-mortem is
  blameless and every action has an owner and a date.

## Before delivering

1. Version and date match on the cover, every running head, the back cover
   and the filename.
2. Numbering follows the convention (every sheet counts, interior from 02);
   the Contents page, if kept, points to pages that carry the tag.
3. Every table has a source line with a date.
4. Owner, classification and status reflect reality; nothing invented.
5. `check_pdf.py <pdf> --html <html>` passes (colour flags, A4, em dash /
   lorem / vX.X / DD MONTH, version in four places, numbering, Contents) and
   the cover was eyeballed in a real viewer, not only in the review PNGs.

## References

- `cooper-brand-kit/references/tokens.md` — tokens, block specs, CSS classes
- `cooper-brand-kit/references/voice.md` — tone, naming, mechanics
- `../../assets/templates/internal-doc.json` and `.html` — the full 24-sheet skeleton (a proposal that uses every page style), description and build
- `../../assets/examples/` — case-study, spec, post-mortem, memo, page-styles (`.json` + `.html`)
- `../../assets/scripts/build_doc.py` — the builder; `check_pdf.py` — the checks
