# Cooper Labs — tokens and block specs

Pixel values; the CSS class in the last column is the one in
`assets/css/cooper.css`. The social section is transcribed from the Figma
file *Brand Identity* (page *Twitter*); the documents, the deck and the fact
sheet are the design of the plugin on the same tokens. "Label" means Roboto
Condensed 500 UPPERCASE with 0.1 em letter-spacing (the role JetBrains Mono
holds in the Parallel kit; there is no mono here).

## Page

Chosen on the design canvas of 14 September 2026: the **poster cover** (the
posts' typography on white) and the **block interior** (the block as a
device: the ruled grid of a spec sheet, labels in boxes, figure cells with
the first number orange, fully ruled tables, the recommendation as an orange
and ink band). PP Eiko at line-height 0.9 to 1.0, tracked −0.045 to
−0.07 em.

| Item | Value | CSS |
|---|---|---|
| Sheet | 794 × 1123, `paper`, clip | `.page` |
| Padding | 40 / 56 / 36 / 56; measure 682 | `.page` |
| Running head | the mark 16 wide + label 8 `ink` left, the page number label 11 right, on a 1 px `ink` rule | `.pagehead`, `.pagehead__meta`, `.pagehead__num` |
| Footer | 1 px `ink` rule, 10 above, label 8 `ink`; left `COOPER LABS · INTERNAL · NOT FOR DISTRIBUTION`, right `NN / NN`: every sheet counts, the cover is 01 (unnumbered), the interior runs from 02, the total includes the back cover | `.pagefoot` |
| Content | vertical stack, gap 28, starts 28 under the head, max 939 high | `.content` |
| Block | column: the label row (the boxed label, the source at the right), then the content, 12 under | `.block`, `.block__margin`, `.block__main` |
| Prose block | a block whose content starts with a heading and a body splits in two: the heading in a 230 column at the left, the body at the right on a `line` hairline, 20 in; what follows (a table, tiles, cells) spans the measure | `.block__main:has(> .heading + .body)` |

## Cover

The poster: a white page (`card`), the halftone (`cover: "02"`,
`.cover--texture`) at 55% fading to white from 22% to 68%, or another
render in the top 60% under the fade; everything centred. `cover: "dark"`:
`ink`, white type, the orange mark.

| Item | Value | CSS |
|---|---|---|
| Ground | `card` #FFF (dark: `ink`) | `.cover`, `.cover--dark` |
| Image | the halftone full page at 55%, or a render in the top 60%, cover-fit | `.cover__img` |
| Fade | to white: 22% → 50% at 85% → 68% (a render: 30% → 72% → 100%); to `ink` on the dark cover | `.cover__fade` |
| Top row | y 44, wordmark 22 high left, `CONFIDENTIAL · vX.X` label 9 `black` right | `.cover__top`, `.cover__logo`, `.cover__conf` |
| Block | from y 120 to the bottom, centred both ways, text centred; the meta line at the bottom | `.cover__bottom` |
| Kicker | Roboto Condensed 400 14 / 1.1, ls −0.06 em, UPPERCASE (the posts' kicker) | `.cover__kicker` |
| Title | PP Eiko 500, 92 / .9, ls −0.07 em (the posts' tracking), `black`, 22 under, max 660; Title Case; one phrase in `accent` | `.cover__title`, `.cover__title em` |
| Standfirst | Roboto Condensed 14 / 1.45, ls −0.02 em, `ink-soft`, max 440, 28 under | `.cover__stand` |
| The mark | 53.3 × 37.6 (the Figma post size), 40 under; orange on dark | `.cover__rule` |
| Meta line | one centred line: the four values as label 9 ls 0.08 em `black`, middle dots in `grey-6`, 40 above | `.cover__meta`, `.cover__meta .v` |
| Notice | label 8 ls 0.08 em `muted`, 12 under | `.cover__notice` |

Back cover: the poster on `ink`: the white wordmark, the tagline centred in
PP Eiko 500, 56 / .92, ls −0.06 em, `white`, the closing phrase in
`accent`, the orange mark under it, the colophon as one line (website, X,
Telegram, then `Class · vX.Y · D Mon YYYY`) and the notice. `.back`,
`.back__tagline`.

## Blocks

| # | Block | Spec | CSS |
|---|---|---|---|
| 01 | Section label | the boxed label: an `ink` box 26 wide with the white mark (14), then the label 9 `ink` in a 1 px `ink` outline, 22 high | `.tag`, `.tag::before` |
| 08 | Source line | at the right of the label row, label-face 8.5 / 1.4 `muted`, not uppercase, right-aligned, max 300 | `.source` |
| 02 | Sub-heading | PP Eiko 500, 30 / .95, ls −0.045 em, `ink`, max 600, Title Case; optional accent phrase (`<em>`); optional suffix `muted` | `.heading`, `.heading em`, `.heading__suffix` |
| 03 | Body | Roboto Condensed 10.5 / 1.55, ls −0.005 em, `ink`, max 560; 12 under a heading, 8 between paragraphs; in a prose block, at the right on the hairline | `.body` |
| 04 | Bullets | ruled cells (1 px `line`, white, padding 14, `auto-fit` from 150 wide, sharing borders): a counter `01` label 8 `muted`, the term PP Eiko 16 / 1.05 ls −0.03 em, the text 10 / 1.5 `ink-soft` | `.bullets`, `.bullet`, `.bullet__term`, `.bullet__text` |
| 05 | Table | fully ruled, 1 px `line` on every cell; head label 8 `muted` on `paper`, padding 10 12; cells white, padding 10 12; text 10.5 / 1.4 `ink`; figure cells tabular 10 `ink-soft` (`td.mono`); strong 500; one `tint` row | `.table`, `td.mono`, `td.strong`, `tr.highlight`, `.table--plain` |
| 06 | Headline figures | ruled cells 150 high sharing borders (1 px `line`, white, padding 14): the key label 8 at the top, the number PP Eiko 500 56 / .85 ls −0.05 em at the bottom; **the first number is `accent`** (and any `<em>`), the others `ink`. Numbers only in the number cell | `.figures`, `.figure`, `.figure__n`, `.figure__k` |
| 07 | Recommendation | the band: an `accent` cell 120 wide with the ink mark 40 wide at its bottom left, then `ink`: title PP Eiko 500 22 / 1.05 ls −0.03 em `white` (padding 18 22 0), body 10.5 / 1.5 white at 72% (10 22 18) | `.reco`, `.reco::before`, `.reco__title`, `.reco__body` |
| — | Logo | the horizontal wordmark, 22 high on the cover, 18 in a fact-sheet running head, 30 on a deck title slide; the mark 16 wide in a running head, 14 in a label box, 40 in the recommendation band, 53 on the cover; `_b` on paper, `_w` in a box, `_o` on ink. Never redrawn | `.cover__logo`, `.pagehead__logo`, `.tag::before`, `.cover__rule` |

Shipped table shapes: 4 columns 190 / 60 / 110 / fill (options), 3 columns
70 / fill / 190 (decision log), 3 columns 60 / 80 / fill (timeline), 2
columns 130 / fill (glossary), 3 columns 48 / fill / 60 without a head row
(contents, rows 5.5 / 12). Any other shape is built from the same cells
with one fill column.

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

The page scaled ×1.6 on 1280 × 720, one block per slide; the title and the
closing slides are the poster.

| Item | Value | CSS |
|---|---|---|
| Slide | 1280 × 720 `paper`, padding 56 / 72 | `.canvas--deck`, `.deck` |
| Running head | the mark 22 wide + label 11 left, the number label 14 right, on a 1 px `ink` rule | `.deck__head` |
| Footer | 1 px `ink` rule, 14, label 11: `COOPER LABS · INTERNAL · NOT FOR DISTRIBUTION` and `NN / NN`; 44 from the bottom | `.deck__foot` |
| Stack | the label row, then the block, 40 under the head, gap 22 | `.deck__grid`, `.deck__margin`, `.deck__main` |
| Blocks | boxed label 12 (box 38, mark 20), source 12, heading 48 / .92 max 980 (prose split at 380), body 17 / 1.5 max 860, cells from 260 wide (term 24, text 15), ruled table 15 (head 11, figures 14), figure cells 220 high (88, key 11), the band with a 180 cell (title 34, body 16) | `.deck .tag` … |
| Title slide | the poster on white: the render (or the halftone) at 55% under a fade to white 20% → 60% → 80%, wordmark 30 high; kicker 16; title 96 / .9 ls −0.07 em max 980; standfirst 17 max 600; the mark 64 wide; the meta line 11 | `.deck--title` |
| Divider | number 220 / .85 ls −0.06 em `ink`, bare (no block), 36 over the kicker label 12; title 76 / .92 max 960; bottom-aligned, padding 56 / 72 / 120 | `.deck--divider` |
| Statement | centred, padding 0 140; the mark 64 wide; text 64 / .98 ls −0.05 em; source label 12 | `.deck--statement` |
| Closing | the poster on `ink`: tagline 72 max 900, the orange mark 64, the colophon line | `.deck--back` |

## Fact sheet

One A4 page, the document blocks at smaller sizes, ruled.

| Item | Value | CSS |
|---|---|---|
| Running head | wordmark `ink` 18 high left, meta right, on the `ink` rule | `.page--fact .pagehead`, `.pagehead__logo` |
| Stack | column, gap 22, 28 under the head | `.fact` |
| Title | PP Eiko 500 46 / .92 ls −0.05 em max 600, 14 under the boxed label; one `accent` phrase | `.fact__title` |
| Standfirst | Roboto Condensed 12 / 1.5 ls −0.01 em `ink-soft` max 520, 14 under the title | `.fact__stand` |
| Figures | the ruled cells at 110 high, numbers 40, the first number orange | `.fact .figure` |
| Columns | two ruled cells sharing a border, padding 16 18 18; heading 20; bullets as a list on `line` rules (term 10 500, text 9.5) | `.fact__cols` |
| Contact | four ruled cells: key label 8, value 10.5 | `.fact__contact` |

## Page styles

Sixteen compositions on the block grid; the table in
`cooper-internal-document/SKILL.md` says what each is for. Sizes beyond the
scale: 22 (lede), 46 (statement), 130 (hero figure), 180 (divider number).

| Style | Values | CSS |
|---|---|---|
| A / B · Divider | fills the page, bottom-aligned; the number PP Eiko 500 180 / .85 ls −0.06 em `ink`, bare (white on the dark page); kicker label 9 `ink` 32 under; title 60 / .92 ls −0.05 em max 560, 16 under; standfirst 13 / 1.5 `ink-soft` max 440; the list as four ruled cells, 28 under. Dark: `ink` page, white type, the cells on `line-inv` | `.divider`, `.page--dark` |
| C · Statement | the poster, centred, padding 0 40: the mark 53 wide; text 46 / .98 ls −0.05 em, one `accent` phrase, 32 under; source label 9 `muted` 32 under | `.statement` |
| D · Hero figure | centred; number 130 / .85 ls −0.06 em, unit in `accent`; kicker label 9 `ink` 22 under; 1 px `ink` rule 34 under; row of body + tiles 24 under | `.hero` |
| E · Two columns | two ruled cells sharing a border, padding 16 18 18; head as an outlined label box; heading 22; bullets as a list on `line` rules; verdict PP Eiko 16 `accent-deep` on a 1 px `ink` rule, pushed to the bottom | `.cols`, `.cols__head`, `.verdict` |
| F · Timeline | a ruled box padding 22 20 20; 1 px `ink` rule, 7 × 7 `accent` squares (`line` when past); date label 9, title 500 10.5, text 10 / 1.5; phases row label 8 on a `line` rule | `.tl`, `.tl__step`, `.tl__phase` |
| G · Data page | the ruled table across 682, 9.5, cells 7 / 10; foot label-face 8.5 `muted` | `.wide`, `.wide__foot` |
| H · Chart | SVG in a ruled box padding 16; axes `hair`, base `ink`, bars `accent` / `grey-8`, line 1.5 `accent`; labels 8; legend 8 with 10 × 10 squares | `.chart`, `.legend` |
| I · Matrix | a ruled grid 96 + 3 columns, cells sharing borders, white, padding 12; heads and keys on `paper` (label 8 / 9); cell title PP Eiko 13, text 9.5 `ink-soft`; the hot cell `accent` with `ink` type | `.matrix` |
| J · Plate | 420 high across the measure, 1 px `ink` border; caption as an `ink` box bottom left (label 8 white) | `.plate`, `.plate__cap` |
| K · Prose | padding 0 24; lede PP Eiko 500 22 / 1.2 ls −0.04 em with an `accent` phrase; body in two columns gap 24, 22 under; signature row label 8 on a 1 px `ink` rule | `.prose`, `.prose__lede`, `.prose__sig` |
| L · Steps | the block turns into a row: the number PP Eiko 500 22 white in a 44 × 44 `ink` box, then the step (heading 22, body, meta label 8 `muted`) | `.step__n`, `.step`, `.step__meta` |
| M · Glossary | ruled cells in two columns, padding 10 12 12; term PP Eiko 15 / 1.1, definition 9.5 / 1.5 `ink-soft` | `.defs`, `.def` |
| N · Flow | SVG 530 wide; white boxes on a 1 px `ink` stroke, square (soft: `grey-6`, dashed); arrows `ink` with an `accent` dot; text 10 500, label 8, caption PP Eiko 14 with an `accent` span | `.flow` |
| O · Checklist | ruled rows padding 10 14 sharing borders; box 10 × 10 1 px `ink`, ticked `accent`; text 10.5; owner label 9 110 wide; sign-off as four ruled cells, min 88 high | `.check`, `.sign` |
| P · Code | the `ink` panel: Roboto Condensed 9 / 1.6 `white`, padding 18 20; comments `grey-5`, keywords `accent` | `.code` |

## Fonts

| Family | File | Licence |
|---|---|---|
| PP Eiko Medium | not shipped; `local("PP Eiko Medium")` when installed, else `assets/fonts/private/pp-eiko-500.woff2` in a private copy | Pangram Pangram, commercial |
| Instrument Serif | `assets/fonts/instrument-serif-latin-400-*.woff2` | SIL OFL 1.1 (display fallback) |
| Roboto Condensed | `assets/fonts/roboto-condensed-latin-wght-{normal,italic}.woff2` | SIL OFL 1.1 |
