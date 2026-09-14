# Changelog

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
