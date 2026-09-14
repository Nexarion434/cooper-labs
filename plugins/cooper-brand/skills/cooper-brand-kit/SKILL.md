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
  version: "0.2.0"
  source: "Figma file Brand Identity (S5Lg16aM47EGiGOYCDxl9a), page Twitter; cooperlabs.xyz"
---

# Cooper Labs — brand kit

Cooper Labs is a product studio for Web3 teams: design and engineering in one
team, from the brief to the stores. Tagline: **"We turn Web3 ideas into
products people use."** The identity is white, grey and orange: one display
face with a single weight, a condensed sans for everything else, a black
square-and-crescent mark ("the block"), the orange dash, white cards on a
light grey ground, and six renders of that block in white 3D, halftone,
pixels and orange. Documents borrow a render for the cover and the site's
cards for their structure.

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
| `line` | `#DDDDDD` | every hairline on paper |
| `line-inv` | white at 16% | every hairline on dark |
| `accent` | `#FF9E42` | the orange: the accent phrase in a headline, marks, bullet dots, rules, the unit of a hero figure |
| `accent-deep` | `#C77012` | orange text at small sizes on paper: section labels, kickers, verdicts |
| `accent-soft` | `#FFB261` | orange text on dark: the cover kicker, the `/N` of a thread card |
| `tint` | orange at 14% | one highlighted table row, one matrix cell |

Greys 1 to 9 (`#4B4B4B` … `#F3F3F3`) and oranges 1 to 9 (`#FFE29C` …
`#632800`) are the scales of the site; the tokens above are the ones a
document uses. Not brand colours: any blue, green or violet; pure black on
paper (the cards use `#000` because the Figma file does; documents use `ink`).
`accent` on paper fails contrast below 14 px: small orange text is always
`accent-deep`.

## Type

| Family | Weight | Role |
|---|---|---|
| **PP Eiko** | Medium (500), upright only | display: cover title, sub-headings, headline figures, recommendation title, tagline, every social title and line |
| **Roboto Condensed** | 400, 500 | body, bullets, table text, cover values; **and** labels, kickers, meta lines, table heads, figures in tables (there is no mono in this identity) |

PP Eiko is commercial (Pangram Pangram) and exists here in **one weight, no
italic**. It is **not** in the public plugin: the HTML route picks it up
through `local()` when installed, then from `assets/fonts/private/` when
the licensee has put the woff2 there (private copy of the plugin, for cloud
sessions without the designer's computer), and otherwise falls back to
Instrument Serif, which ships. The render scripts say which case applied.
Roboto Condensed ships as woff2 (OFL).

Because the display face has no italic, **the brand signature is an orange
phrase**: one phrase per headline set in `accent` ("Ship the MCP Server
*Before the CLI.*", "We turn Web3 ideas *into products people use.*"),
the verb or the qualifier, two or three words, never on a label. In HTML it
is `<em>` (rendered upright and orange by the CSS); in a description it is
`*...*`. Titles are **Title Case** (short connectors stay lowercase, see
`references/voice.md`). Social posts keep the capitalisation of the Figma
file, with no accent unless asked.

Display type is tracked tight and set close, as on the site: line-height
0.9 to 1.0 and −0.04 to −0.05 em on the cover title, the headings, the
figures and the big numbers, **−0.09 em on the social titles and kickers**
(the Figma value). Labels are UPPERCASE Roboto Condensed 500 with 0.1 em
letter-spacing.

## Geometry

A4 at 96 dpi, 794 × 1123. Margins 40 top, 56 sides, 36 bottom. Measure 682.
The page is the language of cooperlabs.xyz: a light grey ground, **white
cards with a 12 radius and a soft shadow** for everything structured
(figures, tables, bullets, the two columns, the timeline, the matrix cells,
the checklist, the contact strip), the **dark card** (`ink`) for the
recommendation and the code, and prose straight on the page. No margin
column and no ink rules: a section is a row with the **orange dash** (19 ×
5, radius 39) and its label, the source at the right, then the content.
Blocks stack with a 30 gap. Radius 12 on cards, 16 on a deck card or a
plate, 39 on the dash and the pills.

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

On a document a render appears **only on the cover**, in the top 72% under
a fade to `paper` so the masthead and its meta card sit on a plain ground;
`cover: "02"` lays the halftone at 60% as on the posts; `cover: "dark"`
gives the typographic cover (plain `ink`, white type, no picture). Inside a
document an image must carry information; the plate page style is the one
exception.

Nothing outside the six goes on Cooper Labs material: no stock, no generated
image, no photograph. New renders come from the 3D file and enter the
catalogue by number.

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
python3 $S/new_doc.py internal-doc work.html          # raw HTML instead, to edit by hand (or case-study, spec, post-mortem, memo, social)
python3 $S/new_doc.py social --demo posts.html        # description + HTML in one go: the smoke test of the pipeline
```

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

1. Every colour is in the table above; small orange text is `accent-deep`.
2. Display type is PP Eiko Medium, everything else Roboto Condensed; nothing
   is bolder than 500; no italic anywhere. Every cover title and most
   sub-headings carry one orange phrase; kickers and labels carry none.
3. No em dash anywhere a reader will see it; the middle dot `·` separates
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
