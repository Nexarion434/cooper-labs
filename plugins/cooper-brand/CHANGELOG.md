# Changelog

## 0.4.1 · 15 Sep 2026

Type never sits on a render (Nicolas, on pages 5 and 9 of the 0.4.0
proposal). A divider's render and the back cover's are now **plates**, 700
and 620 high from the top, and the words sit on white under them, exactly
as on the cover; the deck's closing slide takes the render on its left
half, like the title slide. Decision 18 amended: a render is a picture,
the page carries the words.

## 0.4.0 · 15 Sep 2026

The documents rebuilt on **Object**, direction 1 of the second design
canvas of 15 September ("Cooper Labs Document Directions, Round Two":
Object, Broadsheet, Orange, Ink, Editorial), chosen by Nicolas. The
poster-and-block system of 0.3 is gone. Same engine, same descriptions
(three new optional keys), same checks; `tools/doc.css` rewritten.

### The idea
The block is an object and the document is its catalogue. The six renders
do the work; the type is small and precise; the page is white with wide
margins and hairlines. No box, no band, no tile, no big number in colour,
no orange in the type: the orange lives in the renders.

### The pages
- **Cover**: the render as a plate across the top 620 px (`cover: "01"`
  is the default), the wordmark on it; under it the kicker, the title at
  46, the standfirst; the meta as key-value pairs at the bottom.
- **Section page**: margins 72, measure 650; the running head and the
  footer as 7.5 px muted labels without rules; each block a row of a grid,
  the **margin column** (200: the label, the source, a specimen) beside
  the reading column; a block without a label spans the measure. Headings
  24, body 11 on 400, bullets as terms in a row, tables on hairlines with
  one ink line under the head, the figures as one strip on an ink line,
  the recommendation as a title and a paragraph.
- **Back cover**: a render across the page (`back: "05"`), the tagline at
  the bottom left, the colophon as pairs.
- **Dividers** fill the page with a render (`render` on the page; 04 or
  05 for a full page); the number is kept for the Contents page and no
  longer shown. A **hero** page takes a plate above the number
  (`render`, `caption`); a block takes a **specimen** in its margin
  (`specimen`, `caption`). Statement, steps, timeline, matrix, glossary,
  checklist, code and the rest follow (see `tokens.md`).
- **Deck**: the plate on the left half of the title slide, the margin
  column beside the block, no rules; the closing slide a render across.
- **Fact sheet**: an optional plate at the top (`render`), the same
  blocks at smaller sizes.
- Docs: `tokens.md` rewritten; the four document skills and the brand kit
  updated; `build_doc.py`, `build_deck.py`, `build_fact_sheet.py` take
  the new keys.

### Design decisions (0.4.0)
18. **The renders carry the identity, the type stays quiet.** One render
    at most per page; 01 and 02 read as texture, 03 to 06 show the block.
19. **No colour in the type.** The `*phrase*` convention stays in the
    descriptions (portable, and the social cards use it) and renders in
    ink in the documents.
20. **The margin column is the structure.** Labels, sources and specimens
    live there; nothing is boxed. A block without a label spans the
    measure, which is how the figures strip and the tables breathe.
21. **A divider is a picture.** The part number is data for the Contents
    page, not a display element.

## 0.3.1 · 15 Sep 2026

No big number in an orange box any more (Nicolas, on the 0.3.0 pages).
- **Dividers** (the document's page style A / B and the deck slide): the
  part number stands bare in ink at 180 (220 on a slide), white on the
  dark page, 32 over the kicker.
- **Headline figures**: ruled cells sharing borders like every other
  structured block (no gap, no orange ground); the first number is set in
  `accent`, the others in `ink`; an `<em>` in a number is `accent` too.
  The deck and the fact sheet follow.
- Docs: `tokens.md`, the four document skills and decision 14 updated.

### Design decisions (0.3.1)
14. **The first figure is the one that matters**: its number is orange,
    the cell stays white. Write the figures in that order. (Replaces the
    orange tile of 0.3.0.)
17. **The orange is type, the mark and the band.** It never fills a box
    around a big number: the divider number and the figures are bare.

## 0.3.0 · 15 Sep 2026

The documents on the two directions Nicolas picked on the design canvas
of 14 September: the **poster cover** (direction B) and the **block
interior** (direction C). Same engine, same descriptions, same checks;
`tools/doc.css` rewritten.

### The poster (cover, back cover, statement, title and closing slides)
- A white page; the halftone at 55% fading to white behind the title
  (`cover: "02"`, now the default of the template and the deck), or a
  render in the top 60%; `cover: "dark"` on ink with the orange mark.
- Everything centred: the posts' condensed uppercase kicker at −0.06 em,
  the title in PP Eiko 92 at −0.07 em (the posts' tracking), the
  standfirst, the mark alone; the meta as one line at the bottom. The
  back cover and the closing slide mirror it on ink; the colophon's
  "This document" cell is one line (`Proposal · v0.1 · 14 Sep 2026`).

### The block (every section page, the deck slides, the fact sheet)
- Ink rules under the running head and over the footer. The section
  label is a **box**: an ink cell with the white mark, then the label in
  an outline. A prose block splits heading left, body right on a
  hairline (`:has()`).
- **Ruled cells** sharing 1 px `line` borders for everything structured:
  bullets (numbered by a counter), tables (head on paper), the two
  columns, the matrix, the glossary, the checklist and sign-off, the
  contact strip, the divider's list; ruled boxes for the timeline and the
  chart; the plate in an ink frame with an ink caption box.
- **Tiles** for the figures, 150 high, the key at the top and the number
  in PP Eiko 56 at the bottom, **the first tile orange**. The
  recommendation is the **band**: an orange cell with the mark, then the
  ink panel. The code is an ink panel. The divider number sits in an
  orange block; the step number in an ink box.
- Docs: `tokens.md` rewritten again; the four document skills updated.

### Design decisions (0.3.0)
13. **The cover is a post.** Same kicker, title tracking, mark and
    halftone as the Figma posts, so a document and the feed read as one
    thing. The site's cards (0.2.0) are gone from the documents.
14. **The first figure is the one that matters**: it takes the orange
    tile. Write the figures in that order. *(0.3.1: the number is orange,
    not the tile.)*
15. **The label box carries the mark**, not a number: sections are not
    numbered inside a page (the Contents page numbers them).
16. **No shadows, no radius**: the block is square and ruled; nothing is
    rasterised in the PDF any more.

## 0.2.0 · 14 Sep 2026

The documents redesigned on the language of cooperlabs.xyz, so that a
Cooper Labs page no longer reads as a recoloured Parallel page. Same
engine, same descriptions, same checks; `assets/css/cooper.css` is now
written by hand (`tools/doc.css` + `tools/social.css`, assembled by
`tools/make_css.py` at the repository root; `tools/make_examples.py`
writes the descriptions), not derived from `parallel.css`.

### The page
- **Cards.** A light grey page (`paper`); everything structured is a white
  card with a 12 radius and the site's soft shadow: the figures row, every
  table, the bullets (one card each, in a row), the two columns, the
  timeline, the matrix cells, the chart, the glossary, the checklist and
  sign-off, the contact strip, the meta strips of the cover, the dividers
  and the back cover. The recommendation and the code are the **dark card**
  (`ink`). Prose sits straight on the page.
- **No margin column, no ink rules.** A section is a row with the **orange
  dash** (the site's 19 × 5, radius 39 mark) and its label, the source at
  the right, then the content. The running head carries the mark and no
  rule; the footer keeps its hairline and `NN / NN`.
- **Type set like the site.** PP Eiko at line-height 0.9 to 1.0 and
  −0.04 / −0.05 em: cover 72, headings 28, figures 44, hero 130, dividers
  180, deck dividers 220. Labels at 0.1 em.
- **Cover.** The render in the top 72% under the fade, the masthead below
  with the meta card; `cover: "02"` lays the halftone at 60% as on the
  posts (`.cover--texture`, also on the deck title with `render: "02"`).
  The back cover and the closing slide carry the orange mark.
- The page styles, the deck and the fact sheet follow (rounded plate with a
  pill caption, white-filled rounded flow boxes, the hot matrix cell in
  orange, checklist rows in a card, bullet cards on slides).
- Docs: `tokens.md` rewritten for the page, the cover, the blocks, the
  deck, the fact sheet and the sixteen styles; the four document skills
  updated.

### Design decisions (0.2.0)
9. **Cards, not columns.** The site's white-card-on-grey is the structure
   of the page; the Parallel margin grid is gone. Tables, figures, bullets,
   two columns, timeline, matrix, glossary, checklist are cards; prose is
   not.
10. **The dash is the mark.** Every section label, kicker and bullet
    carries the site's 19 × 5 orange dash instead of a 20 × 2 rule or a
    dot.
11. **Dark cards for the verdict.** The recommendation and the code sit on
    `ink`, the one place the page goes dark inside.
12. **Box shadows in the PDF.** Chromium rasterises the cards' shadows
    (`check_pdf.py` counts them as JPEG images); at 0.06 alpha they print
    clean. Set `--shadow: none` in the tokens for a flat print.

## 0.1.1 · 14 Sep 2026

- The proposal template (`assets/templates/internal-doc.json`) is the long
  form: 24 sheets, three parts on dividers, every one of the sixteen page
  styles in use on the Parallel MCP server proposal (statement, prose,
  chart, two columns, timeline, hero figure, steps, flow, data page,
  matrix, checklist and sign-off, plate, glossary, code). The Contents page
  lists one line per page past twelve entries.
- `cooper-internal-document` 0.1.1: the proposal class describes the long
  form.

## 0.1.0 · 14 Sep 2026

First release: the `parallel-brand` 0.5.0 engine with the Cooper Labs
identity, from the Figma file *Brand Identity* (page *Twitter*) and
cooperlabs.xyz. Everything in English.

### Identity
- Tokens: `paper` #F5F5F5, `card` #FFF and `black` #000 (the cards, as in
  the file), `ink` #1E1E1E, `ink-soft`, `muted`, `line`, the orange
  `accent` #FF9E42 with `accent-deep` and `accent-soft`, the grey and
  orange scales of the site.
- Type: PP Eiko Medium (500, one weight, no italic; not shipped, `local()`
  then `assets/fonts/private/pp-eiko-500.woff2`, Instrument Serif as the
  fallback) and Roboto Condensed for text and labels. No mono.
- Logos from the Figma file: horizontal and vertical wordmarks (ink,
  white), the mark (black, white, orange), the avatars; viewBoxes measured
  so the descenders are not clipped.
- Six renders, 1841 × 1151, in `assets/img/renders/` with the catalogue
  (ground, busy, subject box of the block, frames for twelve sizes).

### Social (transcribed from the Figma file)
- `build_social.py` kinds `post` (Template01: render 01 + the mark;
  Template02 / 04: the halftone at 60% + the wordmark), `partner`
  (Template03), `xcover` (centred, and the *We Are Cooper* right variant),
  `preview`; `text-box: trim-both cap alphabetic` reproduces Figma's
  vertical trim. The three reference cards match the Figma exports within a
  few pixels of glyph rendering (2 to 4% of pixels differ, none by position).
- The plugin's sizes on the same block: LinkedIn, square, story,
  newsletter, X header, paragraph, wallpaper; `banner` (forum, Notion) and
  `thread` kinds; `dark` option; `render_anim.py` for the MP4.
- `frame.py` on the 16:10 renders, twelve sizes with aliases (`post`,
  `preview`, `cover`, `wallpaper`…); `check_png.py` checks a post title on
  two lines at most, a cover line on two, the logo centred, nothing over it;
  `render_png.py` measures the text against the block's box.

### Documents (designed in the plugin)
- `build_doc.py`, `build_deck.py`, `build_fact_sheet.py`, `new_doc.py`,
  the render and check scripts, with `brand.py` holding every Cooper Labs
  string (names, links, tagline, notices, classes). Classes: proposal, case
  study, spec, post-mortem, memo, guide; deck labels add briefing, update,
  pitch.
- Template `internal-doc.json` (a proposal, 8 sheets); examples
  case-study, spec, post-mortem, memo, page-styles (19 sheets),
  deck-parallel-mcp (7 slides), fact-sheet-cooper-labs; all pass
  `check_pdf.py`.
- Skills `cooper-brand-kit` (tokens, voice, the design source),
  `cooper-internal-document`, `cooper-deck`, `cooper-fact-sheet`,
  `cooper-social`.

### Design decisions (taken in the plugin; to confirm in a design file)
1. **Light cover.** The render sits under a fade to `paper` with ink type,
   because the six renders are all light; `cover: "dark"` gives a plain ink
   cover with white type, no picture. The back cover and the closing slide
   are ink.
2. **The orange phrase replaces the italic.** PP Eiko exists in one weight
   and no italic, so the brand signature (one phrase per headline) is set in
   `accent`, upright. Verdicts, the hero unit and the `/N` of a thread card
   follow. Social post titles carry none, as in the Figma file.
3. **Roboto Condensed as the label face.** Where the Parallel kit uses
   JetBrains Mono (labels, kickers, meta, table figures, code), Cooper uses
   Roboto Condensed 500 UPPERCASE; figures in tables are tabular Roboto
   Condensed. The CSS class `td.mono` keeps its name.
4. **Tracking.** −0.05 em on the cover title, −0.03 em on headings, −0.04 em
   on figures and the tagline, −0.09 em on the social type (the Figma
   value).
5. **Type on the cards is #000 on #FFF**, as the Figma file has it, while
   documents use `ink` on `paper`. Kept as two tokens rather than unified.
6. **The tagline** is the Figma cover line, "We turn Web3 ideas into
   products people use.", on the back cover, the closing slide and the
   default X cover; the site's wording, when it differs, is not used.
7. **Halftone at 60%** over white for the texture posts, as measured in the
   file; the wallpaper uses the halftone as it is.
8. **Headline figures are numbers alone**: the display face at 40 wraps a
   word in a four-cell row, so the word goes in the key.

### Not done
- No Pencil or Figma document system for the documents, the deck and the
  fact sheet; the social section only has the Figma reference. See
  `cooper-brand-kit/references/pencil.md`.
- Partner symbols: only `parallel_icon_b.svg` ships; others are given as
  files.
