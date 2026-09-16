---
name: cooper-brand-kit
description: >
  This skill should be used for anything involving Cooper Labs' visual
  identity in a document or a visual: "Cooper brand", "Cooper Labs look",
  "on-brand", "which colours", "which font", "the orange", "the block", or
  when checking whether a page, deck, PDF or card follows the Cooper Labs
  brand. It is the foundation loaded by cooper-internal-document,
  cooper-deck, cooper-fact-sheet and cooper-social.
metadata:
  version: "0.5.2"
  source: "Figma file Brand Identity (S5Lg16aM47EGiGOYCDxl9a), page Twitter; cooperlabs.xyz"
---

# Cooper Labs — brand kit

Cooper Labs is a product studio: design and engineering in one team, from the
first spec to production. The leitmotiv, written the same way everywhere:
**"We turn ideas into products people use."** The studio is not described by
a sector, so "Web3" and "crypto" say what a client does, never what Cooper
Labs is (`references/voice.md`). The identity is white, grey and orange: one display
face with a single weight, a condensed sans for everything else, a black
square-and-crescent mark ("the block"), and six renders of that block in
white 3D, halftone, pixels and orange. Documents are the **catalogue of
the object**: the renders do the work (a plate across the top of the
cover, of a part divider and of the back cover, a specimen in a margin),
the type is small and precise, the page is white with wide
margins and hairlines. No boxes, no bands, no tiles.

Source of truth: the Figma file *Brand Identity* (page *Twitter*: the posts,
the X covers, the social preview, the logos, the palette) and cooperlabs.xyz
(the tokens and the type of the site). The social section of the plugin
transcribes the Figma file pixel for pixel; the documents, the deck and the
fact sheet are the design of the plugin (there is no Cooper Labs Pencil or
Figma document system yet, see `references/pencil.md`). Treat everything
below as rules. When a request conflicts with a rule, say so and propose the
on-brand version.

## Intake, in one round

Never build from a bare request; never ask more than once. Use
`AskUserQuestion`, four questions maximum, defaults pre-selected. Anything
readable from a source is read, not asked. If the session is unattended,
take the defaults, build, and list the assumptions at the top of the reply.

The cover render is one of the questions for documents: offer three by
number and scene from `assets/img/catalogue.json` (or the plain dark cover),
and say which one was used. A post picks between the white render (01) and
the halftone at 60% (02); the other four carry the block itself.

## Colour

| Token | Hex | Role |
|---|---|---|
| `paper` | `#F5F5F5` | page ground (the site's ground) |
| `card` | `#FFFFFF` | the social cards' ground, as in the Figma file |
| `white` | `#FAFAFA` | type on dark |
| `black` | `#000000` | type on the social cards, as in the Figma file |
| `ink` | `#1E1E1E` | primary text; the dark ground (back cover, closing slide, dark cover) |
| `ink-soft` | `#383838` | secondary text: bullet explanations, recommendation body, table figures |
| `muted` | `#848484` | labels, meta lines, sources, page furniture |
| `line` | `#DDDDDD` | a hairline on paper (social) |
| `hair` | `#EBEBEB` | the hairlines of a document: table rows, lists, the figures strip |
| `line-inv` | white at 16% | every hairline on dark |
| `accent` | `#FF9E42` | the orange: the renders, the orange mark and avatar, the `/N` of a thread card; not the type of a document |
| `accent-deep` | `#C77012` | orange text at small sizes on paper, when a social card needs it |
| `accent-soft` | `#FFB261` | orange text on dark: the cover kicker, the `/N` of a thread card |
| `paper` | `#F5F5F5` | the grey of one highlighted table row, the hot matrix cell, the code panel |

Greys 1 to 9 (`#4B4B4B` … `#F3F3F3`) and oranges 1 to 9 (`#FFE29C` …
`#632800`) are the scales of the site; the tokens above are the ones a
document uses. Not brand colours: any blue, green or violet; pure black on
paper (the cards use `#000` because the Figma file does; documents use `ink`).
`accent` on paper fails contrast below 14 px: small orange text is always
`accent-deep`.

## Type

| Family | Weight | Role |
|---|---|---|
| **PP Eiko** | Medium (500), upright: the brand weight | display: cover title, sub-headings, headline figures, recommendation title, tagline, every social title and line |
| PP Eiko, other cuts | Thin 100, Light Italic 300, Heavy 800, Black Italic 900 | declared in the CSS for the designer's exploration; nothing shipped uses them, and a document does not use them without a design decision recorded in the CHANGELOG |
| **Roboto Condensed** | 400, 500 | body, bullets, table text, cover values; **and** labels, kickers, meta lines, table heads, figures in tables (there is no mono in this identity) |

PP Eiko is commercial (Pangram Pangram). The identity uses **one weight,
Medium, upright**; the studio holds five cuts (Thin, Light Italic, Medium,
Heavy, Black Italic), all declared. It is **not** in the public plugin:
the HTML route picks it up through `local()` when installed, then from
`assets/fonts/private/` when the licensee has put the woff2 files there
(private copy of the plugin, for cloud sessions without the designer's
computer), and otherwise falls back to Instrument Serif, which ships. The
render scripts say which case applied. Roboto Condensed ships as woff2
(OFL).

The documents set no italic, and the orange lives in
the renders, not in the type: a phrase written with `*...*` in a
description ("Ship the MCP Server *Before the CLI.*") is kept in the source
and **renders in ink**, so the descriptions stay portable. The orange
phrase remains the signature of the social cards that ask for it (a thread
card's `/N`). Titles are **Title Case** (short connectors stay lowercase,
see `references/voice.md`). Social posts keep the capitalisation of the
Figma file, with no accent unless asked.

Display type is tracked tight and set close: line-height 0.85 to 1.05,
−0.03 to −0.05 em on the titles, the headings, the figures and the hero
number, **−0.09 em on the social titles and kickers** (the Figma value). Labels are UPPERCASE Roboto
Condensed 500 with 0.1 em letter-spacing.

## Geometry

A4 at 96 dpi, 794 × 1123. Margins 48 top, 72 sides, 44 bottom. Measure
650. One language, **Object**, chosen on the design canvas of 15 September
2026 (round two, direction 1) after the poster-and-block system of 0.3 was
set aside:

- **The plate.** The cover is a render across the top 620 px with the
  wordmark on it, then the kicker, the title at 46, the standfirst, the
  meta row at the bottom. A part divider is the same plate (700 high) with
  the title small under it at the bottom left; the back cover the same
  with the tagline. A hero figure gets a plate above the number; a block
  can carry a square **specimen** in its margin. Type never sits on a
  render: the plate is a picture, the page carries the words.
- **The catalogue page.** White. The running head and the footer are
  7.5 px labels in `muted`, no rules. Each block is a row of a grid: the
  **margin column** (200 wide: the label, the source, a specimen) and the
  reading column; a block without a label spans the measure. Headings at
  24, body at 11 on a 400 measure, bullets as terms and texts in a row,
  tables on hairlines with one ink line under the head, the figures as
  one strip on an ink line, the recommendation as a title and a
  paragraph. No box, no band, no tile, no big number in colour. Radius 0
  everywhere. Blocks stack with a 36 gap.

## The logo

`assets/logo/`: the horizontal wordmark (`cooper_horizontal_b.svg` ink,
`_w` white; the mark, then "Cooper Labs" in PP Eiko outlined), the vertical
lock-up, the mark alone (`cooper_icon_b/w/o.svg`, black, white, orange) and
the avatars (square and round, black, white, orange). The mark is 53.333 ×
37.633 in the Figma file at post size; the wordmark on a post is 40 high.
Never redraw it, never recolour it outside black, white and orange, never
put it on a busy part of a render.

## Imagery

**Six renders**, numbered as in the plugin and shipped 16:10 (1841 × 1151)
in `assets/img/renders/NN.jpg`: 01 *space-between* (soft white volumes, the
render behind the posts, the X cover, the social preview and the wallpaper),
02 *halftone* (the block as a rain of dots, laid at 60% over white on the
texture posts), 03 *block-grey* (the pixel block, large, left of centre),
04 *block-orange-dots*, 05 *block-orange-noise*, 06 *block-orange-grey* (the
orange block, small, centred). All six take ink type on top. Always refer to
a render **by its number**; `assets/img/catalogue.json` describes each one
(ground, what is visible, where it is loaded, the `subject` box that must
not sit under text) and carries a default framing per social size (`frames`,
read and recomputed for any size by `assets/scripts/frame.py`).

On a document the renders carry the identity: `cover: "01"` (the default)
puts that render as the plate across the top of the cover (`"02"` the
halftone, any number works, `"dark"` a plain ink cover); `back: "05"` is
the plate of the back cover; `render` on a divider is its plate (the top
700 px), on a hero page a plate above the number, on a plate page the
plate; `specimen` on a block puts a 140 × 140 crop in the margin. The
white 3D (01) and the halftone (02) read as texture; 03 to 06 show the
block itself. Never more than one render per page.

Nothing outside the catalogue goes on Cooper Labs material: no stock, no
generated image, no photograph. **New renders are made with
`assets/scripts/render_block.py`**: the block in three dimensions (the
mark's box with the cylinder cut through it), ray-cast with numpy, a
camera (`--yaw`, `--pitch`, `--roll`, `--zoom`, `--dx`, `--dy`), a material
(white, orange, grey, ink), a ground (white, paper, grey, dark, ink) and
the effects of the six families (`grain`, `chroma`, `pixel`, `dither`,
`halftone`, `lines`, `dots`, `soft`); six presets (`clean`, `orange`,
`pixel`, `halftone`, `noise`, `macro`) give the masters' looks. `--scale
0.25` for a look, then `--catalogue NN --name … --desc …` writes
`renders/NN.jpg` at 1841 × 1151 and its catalogue entry (subject box,
busy, frames), so every builder can use it by number at once. A render
made this way goes into the catalogue only once the designer has looked
at it and kept it; none ships beyond the six. Renders 01 to 06 are the
Figma masters and are never overwritten.

## Social

Transcribed from the Figma file, page *Twitter*: the **post** 1200 × 675
(kicker, title, the mark or the wordmark at the bottom; on render 01 or on
the halftone at 60%), the **partner** card (the mark, a line, the partner's
symbol), the **X cover** 1500 × 500 (one line and the wordmark, centred, or
the block at the right as *We Are Cooper*), the **social preview** 1200 ×
630 (the wordmark alone). The plugin adds, on the same rules: the post on
LinkedIn, square, story, newsletter, X header and paragraph sizes, the
wallpaper 2560 × 1440, the forum header and Notion cover banners, thread
cards and the animated MP4. Specs in `references/tokens.md`, build in the
`cooper-social` skill.

## Documents, deck, fact sheet

The internal document (`cooper-internal-document`: proposal, case study,
spec, post-mortem, memo, guide; sixteen page styles), the deck
(`cooper-deck`: 16:9, 1280 × 720, one block per slide) and the fact sheet
(`cooper-fact-sheet`: one A4 page) share the tokens, the blocks and the
rules. The engine is the one of `parallel-brand`, with the Cooper Labs
identity in `assets/css/cooper.css` and `assets/scripts/brand.py`.

## One route, HTML → PDF / PNG

A description in JSON, a builder that applies the rules, a renderer, a
checker:

```bash
S=${CLAUDE_PLUGIN_ROOT}/assets/scripts
python3 $S/build_doc.py --example > work.json && python3 $S/build_doc.py work.json work.html --pdf      # documents
python3 $S/build_social.py --example > posts.json && python3 $S/build_social.py posts.json posts.html --png out/   # social
python3 $S/build_deck.py --example > deck.json && python3 $S/build_deck.py deck.json deck.html --pdf --png out/    # deck
python3 $S/build_fact_sheet.py --example > sheet.json && python3 $S/build_fact_sheet.py sheet.json sheet.html --pdf   # fact sheet
python3 $S/check_text.py work.json                    # the copy lint alone (the builders run it anyway)
python3 $S/new_doc.py internal-doc work.html          # raw HTML instead, to edit by hand (or case-study, spec, post-mortem, memo, social)
python3 $S/new_doc.py social --demo posts.html        # description + HTML in one go: the smoke test of the pipeline
```

Two passes run on their own, without being asked. **The flow**
(`paginate.py`): a described page is a group of blocks, the blocks are
measured in Chromium and poured into sheets, so no part starts overleaf
while half a sheet stands empty (`"flow": false`, or `"break": true` on a
page, when a break is wanted). **The copy lint** (`check_text.py`): an em
dash, an en dash between words, trailing dots, an emoji or a "lorem" in the
description stops the build; the words that mark machine prose are printed
as tells. Rewrite rather than pass `--no-lint`.

`render_pdf.py` and `render_png.py` end with the same font line (`PP Eiko
Medium, as in the Figma file`, or what stood in); `check_pdf.py` and
`check_png.py` refuse what would embarrass the brand (numbering, version,
em dash, a title on three lines, text over the logo).

`assets/css/cooper.css` carries the numbers of the Figma file (social) and
of the plugin's design (documents). Do not invent CSS values; change the
Figma file or the CSS, and record the decision in the CHANGELOG. Requires
Python with Playwright and Chromium (`pip install playwright && playwright
install chromium`).

## Before delivering anything

1. Every colour is in the table above; in a document the orange is in the
   renders only (the social cards keep their orange where the Figma file
   has it).
2. Display type is PP Eiko Medium, everything else Roboto Condensed; nothing
   is bolder than 500; no italic anywhere; no box, band or tile around a
   figure or a label.
3. No em dash and nothing else on the `check_text.py` list; the middle dot `·` separates
   meta items. Document titles are Title Case; standfirst, body and
   recommendation titles are sentence case; social titles as written.
4. Every image is one of the six renders, named by number; the logo is one
   of the shipped files.
5. `check_pdf.py` or `check_png.py` passes and the cover or the card has
   been looked at in a real viewer.

## References

- `references/tokens.md` — every token, block spec and CSS class
- `references/voice.md` — tone, naming and mechanics
- `references/pencil.md` — the design source, and what a Pencil file would need
- `../../assets/img/catalogue.json` — the six renders by number, with ground, scene, subject and frames
