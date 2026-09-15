# Cooper Labs — tokens and block specs

Pixel values; the CSS class in the last column is the one in
`assets/css/cooper.css`. The social section is transcribed from the Figma
file *Brand Identity* (page *Twitter*); the documents, the deck and the fact
sheet are the design of the plugin on the same tokens. "Label" means Roboto
Condensed 500 UPPERCASE with 0.1 em letter-spacing (the role JetBrains Mono
holds in the Parallel kit; there is no mono here).

## Page

Chosen on the design canvas of 15 September 2026 (round two, direction 1,
**Object**): the block is an object and the document is its catalogue. The
six renders do the work (a plate across the top of the cover, of a part
divider and of the back cover, a plate above a hero figure, a square
specimen in the margin of a block); the type is small and precise;
the page is white with wide margins, a 200 margin column and hairlines. No
boxes, no bands, no tiles; the orange lives in the renders, not in the type
(an accent phrase written with `*…*` renders in ink).

| Item | Value | CSS |
|---|---|---|
| Sheet | 794 × 1123, `card` (#FFF), clip | `.page` |
| Padding | 48 / 72 / 44 / 72; measure 650 | `.page` |
| Running head | the mark 12 wide + label 7.5 `muted` left, the page number label 7.5 `muted` right; no rule | `.pagehead`, `.pagehead__meta`, `.pagehead__num` |
| Footer | label 7.5 `muted`, 44 from the bottom; left `COOPER LABS · INTERNAL · NOT FOR DISTRIBUTION`, right `NN / NN`; no rule | `.pagefoot` |
| Content | vertical stack, gap 36, starts 56 under the head | `.content` |
| Block | a grid row: the margin column 200 wide (the label, the source, a specimen), the reading column beside it; a block without a label spans the measure | `.block`, `.block__margin`, `.block__main` |
| Divider plate | `render` on a divider: the render across the top 700 px; the running head is dropped on that page (the folio stays in the footer) | `.page__img` |

## Cover

The plate: the render (`cover: "01"`, the default; `"02"` the halftone) at
cover fit across the top 620, no fade, the wordmark on it; below, the
kicker, the title, the standfirst at the left; the meta as one row at the
bottom, the notice under it. `cover: "dark"`: plain `ink`, white type.

| Item | Value | CSS |
|---|---|---|
| Ground | `card` #FFF (dark: `ink`) | `.cover`, `.cover--dark` |
| Plate | the render, cover fit, 620 high from the top, position 50% 40% | `.cover__img` |
| Top row | y 56, wordmark 18 high left, `CONFIDENTIAL · vX.X` label 8 `ink` right | `.cover__top`, `.cover__logo`, `.cover__conf` |
| Block | from y 684 to 56 above the bottom, left-aligned | `.cover__bottom` |
| Kicker | label 8 `muted` | `.cover__kicker` |
| Title | PP Eiko 500, 46 / 1, ls −0.04 em, `ink`, 18 under, max 500; Title Case | `.cover__title` |
| Standfirst | Roboto Condensed 11 / 1.55, `ink-soft`, max 360, 22 under | `.cover__stand` |
| Meta row | at the bottom: four `key value` pairs, key label 7.5 `muted`, value 8.5 `ink`, gap 24 | `.cover__meta`, `.k`, `.v` |
| Notice | label 7.5 `muted`, 12 under the meta | `.cover__notice` |

Back cover: the plate again (`back: "05"`, the default; `"dark"` for
plain ink), the wordmark on it, and under it at the bottom left the
tagline PP Eiko 500 40 / 1 ls −0.04 em `ink` max 380, the colophon as
key-value pairs (website, X, Telegram, `This document`), the notice.
`.back`, `.back__tagline`.

## Blocks

| # | Block | Spec | CSS |
|---|---|---|---|
| 01 | Section label | label 7.5 `muted` at the top of the margin column, wrapping | `.tag` |
| 08 | Source line | under the label in the margin, Roboto Condensed 8 / 1.45 `muted`, max 140 | `.source` |
| — | Specimen | `specimen: "03"` on a block: a 140 × 140 crop of the render (cover fit at 42% 50%) above the label, its `caption` 8 / 1.45 `muted` under it | `.specimen`, `.specimen__cap` |
| 02 | Sub-heading | PP Eiko 500, 24 / 1.05, ls −0.03 em, `ink`, max 420, Title Case; optional suffix `muted` | `.heading`, `.heading__suffix` |
| 03 | Body | Roboto Condensed 11 / 1.6, ls −0.005 em, `ink`, max 400; 16 under a heading, 8 between paragraphs | `.body` |
| 04 | Bullets | a grid, `auto-fit` from 130 wide, gap 20 / 24, nothing around them: the term PP Eiko 13 / 1.1 ls −0.02 em, the text 9.5 / 1.5 `ink-soft` 6 under | `.bullets`, `.bullet`, `.bullet__term`, `.bullet__text` |
| 05 | Table | head label 7.5 `muted` on a 1 px `ink` line; rows on `hair` lines, padding 8 12 8 0, text 10 / 1.4 `ink`; figure cells tabular 9.5 `ink-soft` (`td.mono`); strong 500; one row on `paper` (`tr.highlight`); no vertical rules | `.table`, `td.mono`, `td.strong`, `tr.highlight`, `.table--plain` |
| 06 | Headline figures | one strip: a 1 px `ink` line above, a `hair` line below, padding 16 0, gap 24; the number PP Eiko 500 40 / .9 ls −0.04 em `ink`, the key label 7.5 `muted` 10 under. Numbers only in the number cell | `.figures`, `.figure`, `.figure__n`, `.figure__k` |
| 07 | Recommendation | a title PP Eiko 500 18 / 1.1 ls −0.025 em `ink` and a paragraph 10 / 1.5 `ink-soft`, max 400, nothing around them | `.reco`, `.reco__title`, `.reco__body` |
| — | Logo | the horizontal wordmark, 18 high on the cover and the back, 16 in a fact-sheet running head, 26 on a deck title slide; the mark 12 wide in a running head, 18 in a deck head; `_b` on paper, `_w` on ink. Never redrawn | `.cover__logo`, `.pagehead__logo` |

Shipped table shapes: 4 columns 190 / 60 / 110 / fill (options), 3 columns
70 / fill / 190 (decision log), 3 columns 60 / 80 / fill (timeline), 2
columns 130 / fill (glossary), 3 columns 48 / fill / 60 without a head row
(contents, rows 5.5 / 12). Any other shape is built from the same rows with
one fill column.

## Social

Transcribed from the Figma file, page *Twitter*. Type on the cards is
`black` (`#000`) on a `card` (`#FFF`) ground with the render at cover fit,
as in the file; the halftone (02) is laid at 60% opacity. Renders by number,
`assets/img/renders/NN.jpg`. Every text box carries `text-box: trim-both
cap alphabetic`, the Figma vertical trim, so the positions below are
measured from the cap height and the baseline.

### Common

| Item | Value | CSS |
|---|---|---|
| Canvas | 1200 × 675, `card`, `black` type, clip; `--dark` is `ink` with white type and no render | `.canvas`, `.canvas--dark` |
| Ground | the render at cover fit (`background-image`), or an `<img>` sized and offset inline to frame a detail (`frames` of `catalogue.json`, `frame.py`) | `.canvas__bg`, `.canvas__bg img` |
| Texture | render 02 at 60% opacity over white | `.canvas__bg--texture` |
| Display | PP Eiko 500, letter-spacing −0.09 em on titles, kickers and cover lines | |
| Sizes | 1200 × 630 preview, 1500 × 500 cover, 2000 × 800 x, 2400 × 1200 para, 1200 × 627 li, 1080 × 1080 sq, 1080 × 1920 story, 600 × 300 mail, 1600 × 400 forum, 1500 × 600 notion, 2560 × 1440 wallpaper | `.canvas--preview`, `--cover`, `--x`, `--para`, `--li`, `--sq`, `--story`, `--mail`, `--forum`, `--notion`, `--wallpaper` |

### Post · Template01 (render + the mark), Template02 and 04 (halftone + the wordmark)

| Item | Value | CSS |
|---|---|---|
| Block | padding 69, column, centred both ways, text centred | `.post` |
| Kicker | Roboto Condensed 400 28 / 1.1, ls −0.09 em, UPPERCASE, width 684 | `.post__kicker` |
| Title | PP Eiko 500 83.48 / 1.1, ls −0.09 em, width 684, 24 under the kicker; `" / "` breaks the line; an optional `*phrase*` in `accent` | `.post__title`, `.post__title em` |
| Logo | centred; the mark 37.633 high, 69 from the bottom (Template01) **or** the wordmark 40.1 high, 42 from the bottom (Template02 / 04) | `.post__logo--mark`, `.post__logo--word` |
| Other sizes | li: wordmark 36 from the bottom · sq: kicker 26, title 80, width 900, wordmark 60 · story: kicker 30, title 96, width 900, wordmark 50 high at 120 · mail: padding 30, kicker 14, title 40, width 540, wordmark 20 at 20 · x: kicker 39, title 116, width 1140, wordmark 56 at 60 · para: kicker 52, title 155, width 1520, wordmark 72 at 100 · wallpaper: kicker 60, title 178, width 1600, wordmark 60 at 100 | `.canvas--<size> .post__*` |

### Partner · Template03

| Item | Value | CSS |
|---|---|---|
| Row | centred both ways, gap 254 | `.partner` |
| Mark | 113.375 × 80 | `.partner__mark` |
| Line | 2 × 482, `black` | `.partner__line` |
| Partner symbol | 80 × 80, contained, black on the light render | `.partner__icon` |

### X cover · 1500 × 500

| Item | Value | CSS |
|---|---|---|
| Line | PP Eiko 500 66 / 0.9, ls −0.09 em, centred at the middle, one or two lines (`" / "`) | `.xcover__line` |
| Wordmark | centred, 24.68 high, top 380.3 | `.xcover__logo` |
| Right variant (*We Are Cooper*) | block at left 977, width 411, vertically centred, gap 15; line left-aligned, wordmark 7.11 in from the left; render 04 or 06 | `.xcover--right .xcover__block` |

### Social preview · 1200 × 630

| Item | Value | CSS |
|---|---|---|
| Wordmark | centred, 69.42 high, top 285.14 (the mark 70.859 × 50, "Cooper Labs" 65) | `.preview__logo` |

### Banners, thread, animation (the plugin's additions)

| Item | Value | CSS |
|---|---|---|
| Forum header | 1600 × 400; row space-between, padding 0 80; wordmark 44 high left; kicker Roboto Condensed 500 16 UPPERCASE ls 0.06 em right | `.canvas--forum .banner`, `.banner__logo`, `.banner__k` |
| Notion cover | 1500 × 600; the row aligned at the bottom, padding 0 100 70; line PP Eiko 500 64 / 1.1 ls −0.06 em with an `accent` phrase left, kicker right, no wordmark | `.canvas--notion .banner`, `.banner__tag` |
| Thread card | 1200 × 675; padding 70 80, column space-between; `n/N` PP Eiko 500 61 ls −0.06 em (`/N` in `accent`); sentence 58 / 1.08 ls −0.06 em max 1000, one `accent` phrase; foot row: kicker Roboto Condensed 500 18 UPPERCASE + the mark 79 × 56 | `.thread`, `.thread__n`, `.thread__body`, `.thread__foot`, `.thread__k`, `.thread__icon` |
| Animated card | 4 s at 30 fps: render scale 1.08 → 1, then the logo and each text child rising in 0.25 s apart, 14 px rise, cubic ease-out; H.264, even dimensions | `render_anim.py` |

## Deck

The page on 1280 × 720, one block per slide; the title slide is the plate on
the left half, the closing slide a render across the slide.

| Item | Value | CSS |
|---|---|---|
| Slide | 1280 × 720 `card`, padding 56 / 80 | `.canvas--deck`, `.deck` |
| Running head | the mark 18 wide + label 11 `muted` left, the number label 11 right; no rule | `.deck__head` |
| Footer | label 11 `muted`: `COOPER LABS · INTERNAL · NOT FOR DISTRIBUTION` and `NN / NN`; 48 from the bottom; no rule | `.deck__foot` |
| Grid | the margin column 320 (label 11, source 12), the block beside it, 64 under the head; a slide without a label spans the width | `.deck__grid`, `.deck__margin`, `.deck__main` |
| Blocks | heading 40 / 1.02 max 760, body 17 / 1.55 max 680, bullets from 220 wide (term 22, text 15), table 15 (head 11, figures 14), figures 72 (key 11) in the strip, recommendation 30 + 16 max 680 | `.deck .heading` … |
| Title slide | the render at cover fit on the left 640; at the right (x 720 to 1200, from y 150): kicker 11, title 56 / 1 ls −0.04 em max 480, standfirst 15 max 400, the meta pairs at the bottom (key 10, value 12), the notice 10 | `.deck--title` |
| Divider | bottom-aligned, padding 56 / 80 / 120: kicker label 11 `muted`, title 64 / 1 ls −0.04 em max 720; no number | `.deck--divider` |
| Statement | left-aligned, padding 0 200, vertically centred: text 48 / 1.05 ls −0.04 em max 820, source label 11 `muted` 32 under; no mark | `.deck--statement` |
| Closing | the render on the left 640 (`back: "05"`), the wordmark; at the right, bottom-aligned: the tagline 48 / 1 max 480, the colophon pairs, the notice | `.deck--back` |

## Fact sheet

One A4 page, the document blocks at smaller sizes.

| Item | Value | CSS |
|---|---|---|
| Running head | wordmark `ink` 16 high left, meta label 7.5 `muted` right; no rule | `.page--fact .pagehead`, `.pagehead__logo` |
| Stack | column, gap 22, 32 under the head | `.fact` |
| Plate | `render`: the render 180 high across the measure at the top | `.fact__img` |
| Title | PP Eiko 500 34 / 1 ls −0.04 em max 480, 12 under the label | `.fact__title` |
| Standfirst | Roboto Condensed 10.5 / 1.55 `ink-soft` max 400, 12 under the title | `.fact__stand` |
| Figures | the strip, padding 12 0, numbers 32 | `.fact .figures` |
| Columns | two columns gap 32; heading 18; bullets as a list on `hair` lines (term 10.5 500, text 9.5) | `.fact__cols` |
| Contact | four pairs on a 1 px `ink` line: key label 7.5, value 10 | `.fact__contact` |

## Note and quote

One and two A4 pages on the catalogue page: the wordmark in the running
head, the facts (or the parties) in the margin column, the title beside
them, then the blocks of the document.

| Item | Value | CSS |
|---|---|---|
| Head | a grid 200 + fill, 56 under the running head: the pairs at the left (key 7.5 `muted`, value 9.5 `ink`, gap 14), the label and the title PP Eiko 500 30 / 1.02 ls −0.035 em max 420 at the right | `.note__head`, `.quote__head`, `.note__facts`, `.quote__parties`, `.note__title` |
| Blocks | the document's stack, 40 under the head | `.note .content`, `.quote .content` |
| Numbered list | rows on `hair` lines (the first on `ink`), padding 10 0: the number PP Eiko 13 in a 40 column, the title 11 500, the text 10 `ink-soft` max 400 | `.nlist`, `.nlist__row`, `.nlist__n`, `.nlist__t`, `.nlist__x` |
| Next meeting | a pair on a 1 px `ink` line, 14 under the sentence | `.note__next` |
| Quote table | the table across the measure; figure cells 10 `ink`; the total row on a 1 px `ink` line, 500, the amount 12 | `.table--quote`, `tr.total` |
| Signatures | the sign-off columns with `DATE, SIGNATURE` on a `hair` line 28 under the name | `.sign`, `.sign__line` |

## Page styles

Sixteen compositions; the table in `cooper-internal-document/SKILL.md` says
what each is for. Sizes beyond the scale: 20 (lede), 36 (statement), 96
(hero figure).

| Style | Values | CSS |
|---|---|---|
| A / B · Divider | `render` as a plate across the top 700; on white under it, the title block at the bottom left (bottom 80, width 380): kicker label 7.5 `muted`, title PP Eiko 500 40 / 1 ls −0.04 em `ink` 16 under, standfirst 11 / 1.55 `ink-soft` max 320; the list at the bottom right (x 522, width 200) as key-value pairs (key 7.5, value 8.5); the number is not shown. Dark: `ink` page, white type, no render | `.divider`, `.divider__list`, `.page--dark` |
| C · Statement | left-aligned, vertically centred: text PP Eiko 500 36 / 1.05 ls −0.04 em max 480; source label 7.5 `muted` 28 under; no mark | `.statement` |
| D · Hero figure | `render`: a plate 406 high across the measure with its `caption` 8 `muted` 10 under; then the number PP Eiko 500 96 / .85 ls −0.05 em in the margin column with the unit (`<em>`) in Roboto Condensed 300 22, the kicker label 7.5 `muted` under; the body beside it in the reading column; the figures strip across the measure 40 under | `.hero`, `.hero__img`, `.hero__cap`, `.hero__n` |
| E · Two columns | two columns gap 32, nothing around them; head label 7.5 `muted`; heading 18; bullets as a list on `hair` lines; verdict PP Eiko 14 `ink` on a 1 px `ink` line, pushed to the bottom | `.cols`, `.cols__head`, `.verdict` |
| F · Timeline | a 1 px `ink` line, 5 × 5 `ink` squares (`grey-7` when past); date label 7.5, title 500 10.5, text 9.5 / 1.5; phases row label 7.5 on a `hair` line | `.tl`, `.tl__step`, `.tl__phase` |
| G · Data page | the table across 650, 9.5, rows 7 / 10 | `.wide`, `.wide__foot` |
| H · Chart | SVG on the page; axes `hair`, base `ink`, bars `ink` / `grey-8`, line 1.5 `ink`; labels 7.5; legend 7.5 with 8 × 8 squares | `.chart`, `.legend` |
| I · Matrix | a grid 96 + 3 columns on `hair` lines, heads on a 1 px `ink` line (label 7.5); cell title PP Eiko 13, text 9.5 `ink-soft`; the hot cell on `paper` | `.matrix` |
| J · Plate | the render 406 high across the measure, the caption 8 `muted` under it | `.plate`, `.plate__cap` |
| K · Prose | lede PP Eiko 500 20 / 1.25 ls −0.03 em max 560; body in two columns gap 32, 28 under; signature row label 7.5 on a 1 px `ink` line | `.prose`, `.prose__lede`, `.prose__sig` |
| L · Steps | the number PP Eiko 500 22 `ink` in the margin column; the step beside it (heading 18, body, meta label 7.5 `muted`) | `.step__n`, `.step`, `.step__meta` |
| M · Glossary | two columns gap 32 of entries on `hair` lines, padding 10 0 12; term PP Eiko 14 / 1.1, definition 9.5 / 1.5 `ink-soft` | `.defs`, `.def` |
| N · Flow | SVG 530 wide; white boxes on a 0.75 px `ink` stroke, square (soft: `grey-6`, dashed); arrows `ink` with an `ink` square; text 10 500, label 7.5, caption PP Eiko 14 | `.flow` |
| O · Checklist | rows on `hair` lines (the first on `ink`), padding 10 0; box 9 × 9 1 px `ink`, ticked `ink`; text 10.5; owner label 8 110 wide; sign-off as four columns gap 24 on a 1 px `ink` line, min 72 high | `.check`, `.sign` |
| P · Code | a `paper` panel: Roboto Condensed 9 / 1.6 `ink`, padding 18 20; comments `muted`, keywords 700 | `.code` |

## Fonts

| Family | File | Licence |
|---|---|---|
| PP Eiko Medium | not shipped; `local("PP Eiko Medium")` when installed, else `assets/fonts/private/pp-eiko-500.woff2` in a private copy | Pangram Pangram, commercial |
| Instrument Serif | `assets/fonts/instrument-serif-latin-400-*.woff2` | SIL OFL 1.1 (display fallback) |
| Roboto Condensed | `assets/fonts/roboto-condensed-latin-wght-{normal,italic}.woff2` | SIL OFL 1.1 |
