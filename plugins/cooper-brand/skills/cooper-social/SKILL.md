---
name: cooper-social
description: >
  This skill should be used for Cooper Labs' visuals on X / Twitter,
  LinkedIn and the site: "a post for the roadmap", "the card for the
  Parallel report", "a Cooper post", "the X cover", "a new X header",
  "social preview", "OG image", "a partner card with Parallel", "a 1200 by
  675 visual", "LinkedIn image", "a square", "a story", "newsletter header",
  "forum banner", "Notion cover", "a wallpaper", "a thread of three cards",
  "an animated version of the card", or when a title, a partner, a line or
  a series has to become the branded PNG or MP4. Covers the HTML to PNG /
  MP4 build.
metadata:
  version: "0.1.0"
  source: "Figma file Brand Identity (S5Lg16aM47EGiGOYCDxl9a), page Twitter; the extra sizes designed in the plugin"
---

# Cooper Labs — social

Four formats transcribed from the Figma file *Brand Identity*, page
*Twitter*, and the sizes the plugin adds on the same rules. Load
`cooper-brand-kit` first if the tokens are not already in context.

| Format | In the Figma file | Variable content | Ground |
|---|---|---|---|
| **Post** | Template01 (render 01 + the mark), Template02 and 04 (halftone at 60% + the wordmark) | kicker, title on one or two lines | render 01 at cover fit, or the halftone (02) at 60% over white |
| **Partner** | Template03 | the partner's symbol (an SVG, black) | render 01 |
| **X cover** | the tagline cover, the *We Are Cooper* cover | one line (two at most); the `right` variant with the block | render 01; 04 or 06 for the right variant |
| **Social preview** | the OG image | nothing: the wordmark alone | render 01 |

The post is 1200 × 675 (the X card); the X cover 1500 × 500; the preview
1200 × 630. Type on the cards is `black` on a white ground, as in the file,
in PP Eiko Medium with −0.09 em tracking, vertically trimmed to the cap
height (`text-box: trim-both`), so the PNGs match the Figma exports to a
few pixels.

The plugin adds, on the same rules and the sizes of `parallel-brand`: the
post on **LinkedIn 1200 × 627**, **square 1080 × 1080**, **story 1080 ×
1920**, **newsletter header 600 × 300**, **X header image 2000 × 800**,
**paragraph image 2400 × 1200** and **wallpaper 2560 × 1440**; two
**banners** (forum header 1600 × 400, Notion cover 1500 × 600); a
**thread** as a numbered series of 1200 × 675 cards; and any card as a
four-second **animated MP4**. `dark: true` puts any canvas on the ink
ground with white type and no render.

| Format | Size | Class | Block |
|---|---|---|---|
| LinkedIn | 1200 × 627 | `canvas--li` | post; the wordmark 36 from the bottom |
| Square | 1080 × 1080 | `canvas--sq` | post, kicker 26, title 80, width 900 |
| Story | 1080 × 1920 | `canvas--story` | post, kicker 30, title 96, width 900, wordmark 50 high |
| Newsletter header | 600 × 300 | `canvas--mail` | post, kicker 14, title 40, width 540, wordmark 20 |
| X header image | 2000 × 800 | `canvas--x` | post, kicker 39, title 116, width 1140 |
| Paragraph image | 2400 × 1200 | `canvas--para` | post, kicker 52, title 155, width 1520 |
| Wallpaper | 2560 × 1440 | `canvas--wallpaper` | post, kicker 60, title 178, width 1600; the halftone as it is (*The Space Between*) |
| Forum header | 1600 × 400 | `canvas--forum` | banner: wordmark left, kicker right |
| Notion cover | 1500 × 600 | `canvas--notion` | banner at the bottom: line 64 with an orange phrase left, kicker right, no wordmark |
| Thread card | 1200 × 675 | `canvas` | `n/N` 61 top left (the `/N` in orange), sentence 58 max 1000 with one orange phrase, kicker 18 + the mark at the bottom |

## Intake, in one round

| Question | Options |
|---|---|
| Which card? | post · partner · X cover · social preview · banner · thread |
| The content | post: kicker and title (as the author writes them; `" / "` for the line break). Partner: the symbol file. X cover: the line, centred or right. Banner: line and kicker. Thread: the sentences, one per card |
| The ground | post: render 01 (Template01, the mark) pre-selected · the halftone at 60% (Template02, the wordmark) · dark. X cover: 01 · 04 or 06 with the block at the right |
| Which sizes? | 1200 × 675 pre-selected · LinkedIn · square · story · newsletter · X header · paragraph · wallpaper. Scale 1x pre-selected · 2x |

Nothing is invented: if a title or a partner symbol is missing, ask for it
or stop. Never pick a picture outside the six renders.

## Build

Describe the canvases, let the builder apply the rules (the render or the
texture, the mark or the wordmark, the framing per size), render, check:

```bash
S=${CLAUDE_PLUGIN_ROOT}/assets/scripts
python3 $S/build_social.py --example > posts.json        # the canvases of the template, to start from
# edit posts.json: keep the canvases you need, fill the content, name them
python3 $S/build_social.py posts.json posts.html --png out/   # HTML, one PNG per canvas, then check_png.py
# or step by step:
python3 $S/render_png.py posts.html out/                 # one PNG per .canvas, at the canvas size
python3 $S/render_png.py posts.html out/ --scale 2       # twice the size
python3 $S/render_png.py posts.html out/ --only "post-*" # a glob, repeatable
python3 $S/check_png.py posts.html out/                  # ok / FAIL per canvas, exit 1 on failure
```

One canvas is one object of `canvases`: `name` (the PNG file name), `kind`
(`post`, `partner`, `xcover`, `preview`, `banner`, `thread`), `render`
(`"01"` to `"06"`), `texture` (true: the halftone at 60%, and the wordmark
by default), `dark`, `frame` (omitted: the catalogue framing for the size;
`"cover"`: the plain cover fit, what the Figma file does; or a `{w, h,
left, top}` from `frame.py`), `subject_ok`, and the content of the kind:
`kicker`, `title`, `logo` (`mark` | `word`), `size` (post; `size` one of
`1200x675`, `li`, `sq`, `story`, `mail`, `x`, `para`, `wallpaper`); `icon`
(partner, a path relative to the description); `line`, `variant`
(`centre` | `right`) (xcover); `size`, `tag`, `kicker`, `logo` (banner,
`size` one of `forum`, `notion`); `n`, `total`, `body`, `kicker` (thread).
Titles are written plain, `" / "` for the line break, `*...*` for an orange
phrase when one is wanted: the Figma posts carry none.

```bash
python3 $S/render_anim.py posts.html out/ --only post-2026-roadmap        # the animated card: out/post-2026-roadmap.mp4, 4 s
python3 $S/render_anim.py posts.html out/ --only "thread-*" --gif         # ... and a GIF next to it
```

The animated card is the same canvas over four seconds: a slow zoom out on
the render (1.08 to 1), then the kicker, the title and the logo rising in
one after the other, 0.25 s apart. H.264, even dimensions, 30 fps;
`--seconds`, `--fps` and `--scale 2` adjust it. One card takes about a
minute to render.

Raw HTML remains possible: `new_doc.py social posts.html` copies the
template to edit by hand. `new_doc.py social --demo posts.html` writes the
description and the HTML built from it, so the whole pipeline is one line:

```bash
python3 $S/new_doc.py social --demo posts.html && python3 $S/render_png.py posts.html out/ && python3 $S/check_png.py posts.html out/
```

`render_png.py` warns, after each canvas, when a text block lands on the
render's `subject` (the block, as boxed in the catalogue for 03 to 06) and
prints the `frame.py --preview` command that shows the crop; a warning, not
a failure. It ends with the font line: `PP Eiko Medium, as in the Figma
file`, or `Instrument Serif stood in`. `check_png.py` fails on: a PNG
missing or not at the size of its class, a post title on three lines at
1200 × 675 or 627, a cover line on three lines, a text block over the logo
or outside the canvas, a logo off centre (except the right-variant cover).

Names carry the slug, and the size when there is more than one:
`post-2026-roadmap`, `post-2026-roadmap-li-1200x627`,
`post-2026-roadmap-sq-1080`, `post-2026-roadmap-story-1080x1920`,
`post-2026-roadmap-mail-600x300`, `partner-parallel`,
`x-cover-tagline-1500x500`, `x-cover-we-are-cooper-1500x500`,
`social-preview-1200x630`, `wallpaper-the-space-between-2560x1440`,
`forum-header-1600x400`, `notion-cover-<slug>-1500x600`,
`thread-<slug>-1of3`.

## Post

Template01: render 01 at cover fit, the kicker in Roboto Condensed 28
UPPERCASE and the title in PP Eiko 83.48 centred on a 684-wide column,
24 apart, the **mark alone** 37.633 high, 69 from the bottom. Template02 and
04: the halftone (02) at 60% over white, the same text, the **wordmark**
40.1 high, 42 from the bottom. The title keeps the author's capitalisation
("2026 Roadmap / for Parallel published", "Seventeenth / Parallel Report",
"Flash Loans / Explained"): two lines at most at 1200 × 675, broken with
`" / "` where the author breaks it. A title that needs three lines is
shortened with the author. `logo` overrides the default (the mark on a
render, the wordmark on the texture). The kicker is optional (the wallpaper
has none).

## Partner

Template03: the mark 113.375 × 80, a 2 × 482 black line, the partner's
symbol 80 × 80, centred with a 254 gap, on render 01. The symbol is an SVG
in black (`icon`, a path relative to the description); the plugin ships
`assets/logo/partners/parallel_icon_b.svg`. Ask for the file rather than
redrawing a partner's mark.

## X cover and social preview

The cover: one line in PP Eiko 66 / 0.9 centred at the middle of 1500 × 500,
the wordmark 24.68 high at y 380.3; the leitmotiv by default ("We turn ideas
/ into products people use."), a campaign line on request. `variant:
right` is the *We Are Cooper* composition: the render 04 or 06 with the
orange block at the left, the line and the wordmark in a 411-wide block at
x 977, left-aligned. The preview: the wordmark alone, 69.42 high at y
285.14 on 1200 × 630, nothing else.

## Banners and thread

The forum header carries the wordmark 44 high at the left and a kicker in
Roboto Condensed 500 16 UPPERCASE at the right (`Builders ·
cooperlabs.xyz`); the Notion cover has no wordmark, the line at 64 with its
orange phrase sits at the bottom left with a kicker at the bottom right
(`Proposal · Parallel *MCP server*` / `Internal · Draft v0.1`). A thread
is a series of 1200 × 675 cards: `n/N` top left (the `/N` in orange), one
sentence in PP Eiko 58 with one orange phrase, at most three lines, the
thread's kicker and the mark at the bottom, the same render on every card.
One sentence per card, the claim in the orange; the last card says what to
do.

## Framing the render

`assets/img/catalogue.json` carries, for each of the six, `ground`,
`busy`, `subject` (the box of the block, for 03 to 06; `null` for 01 and
02), `focus`, `zoom` and the resulting `frames` per canvas size, for the
twelve sizes in use. The Figma posts use the plain cover fit (`frame:
"cover"`), and 01 and 02 take it at every size. A framed detail is for the
block renders: `frame.py` reads and recomputes the geometry for any size:

```bash
python3 $S/frame.py 04                      # CSS for every stored size
python3 $S/frame.py 04 cover                # one size: post | li | sq | story | mail | x | para | preview | cover | forum | notion | wallpaper, or any WxH
python3 $S/frame.py 04 --preview check.png  # the crops with the text zones drawn: look at it
python3 $S/frame.py 04 --focus 50 50 --zoom 1.4 --write   # a new framing, stored in the catalogue
```

The renders are 16:10 (1841 × 1151), so the window is `100 / zoom` percent
of the image wide and `wc × (16/10) / canvas ratio` percent high; `left` and
`top` are negative offsets in percent of the canvas. The text zone per
size, in percent of the height: 30–70 on 1200 × 675, 627 and 1500 × 500;
34–66 on 2000 × 800; 36–64 on 2400 × 1200 and 1600 × 400; 38–62 on the
square; 40–60 on the story, the preview and the wallpaper; 30–72 on
600 × 300; 62–90 on the Notion cover. The block has to end up outside it,
or `subject_ok` records that the overlap was looked at and accepted.

## Rules

- **The Figma posts are the reference.** Kicker 28, title 83.48, tracking
  −0.09 em, the 684 column, the mark at 69 or the wordmark at 42: do not
  move them. New sizes scale the same block.
- **Capitalisation as written.** No Title Case pass on a post; no orange
  phrase unless asked. Banner lines and thread sentences carry one orange
  phrase, marked `*...*`.
- **Only the six renders**, by number; the post uses 01 or the halftone, the
  cover 01 (04 or 06 at the right), the partner and the preview 01. The
  block renders are for the right-variant cover and for dark-free variety
  on a thread, not for the standard post.
- **Nothing of the picture under the text**: no block, no hard edge inside
  the title column. Reframe with `frame.py`, or pick another number;
  `render_png.py` measures it and says so.
- **PP Eiko Medium** is what the Figma file uses; when it is missing,
  Instrument Serif stands in and the line breaks move. In a cloud session
  without the designer's computer, the woff2 in `assets/fonts/private/` of
  a private copy of the plugin is what makes the render identical to Figma.
- Nothing else goes on the card: no URL, no hashtag, no second logo. The
  post text carries those.
- Exports are PNG, sRGB, at the canvas size or 2x. Never JPEG for the
  halftone (it bands).

## Before delivering

1. Kicker, title, line, partner and sentences match what the author gave;
   the line break where they put it; nothing rephrased.
2. The render is one of the six and its number is in the reply.
3. File names carry the slug and the size.
4. Every size asked for, every card of a thread, both covers when the pair
   was asked for, and the MP4 when the animated version was asked for, are
   rendered.
5. `check_png.py` passes, `render_png.py` printed no subject warning (or the
   overlap was looked at and `subject_ok` set), and the PNG has been looked
   at, not only produced: two lines at most, the logo centred, nothing of
   the block under the text.

## References

- `cooper-brand-kit/references/tokens.md` — the Social section, exact geometry and CSS classes
- `../../assets/templates/social.json` and `.html` — every canvas (17), description and build
- `../../assets/img/catalogue.json` — the six renders by number, with `ground`, `subject` and the `frames` per size
- `../../assets/scripts/build_social.py` — the builder; `render_png.py`, `check_png.py` — render and checks; `render_anim.py` — the animated card
- `../../assets/scripts/frame.py` — framing: CSS, preview, recompute, any size
