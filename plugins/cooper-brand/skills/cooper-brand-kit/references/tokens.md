# Cooper Labs — tokens and block specs

Pixel values; the CSS class in the last column is the one in
`assets/css/cooper.css`. The social section is transcribed from the Figma
file *Brand Identity* (page *Twitter*); the documents, the deck and the fact
sheet are the design of the plugin on the same tokens. "Label" means Roboto
Condensed 500 UPPERCASE with 0.1 em letter-spacing (the role JetBrains Mono
holds in the Parallel kit; there is no mono here).

## Page

The language of cooperlabs.xyz on A4: a light grey page, white cards with a
12 radius and a soft shadow (`0 1px 8px rgba(0,0,0,.06)`), the orange dash
(19 × 5, radius 39) as the mark, PP Eiko at line-height 0.9 to 1.0 with
−0.04 em tracking. No margin column, no ink rules: prose sits on the page,
the structured blocks (figures, tables, bullets, recommendation) are cards.

| Item | Value | CSS |
|---|---|---|
| Sheet | 794 × 1123, `paper`, clip | `.page` |
| Padding | 40 / 56 / 36 / 56; measure 682 | `.page` |
| Running head | the mark 16 wide + label 8 `muted` left, the page number label 11 `ink` right; no rule | `.pagehead`, `.pagehead__meta`, `.pagehead__num` |
| Footer | hairline `line`, 12 above, label 8 `muted`; left `COOPER LABS · INTERNAL · NOT FOR DISTRIBUTION`, right `NN / NN`: every sheet counts, the cover is 01 (unnumbered), the interior runs from 02, the total includes the back cover | `.pagefoot` |
| Content | vertical stack, gap 30, starts 36 under the head, max 939 high | `.content` |
| Block | column: the section head row (dash + label, source at the right), then the main | `.block`, `.block__margin`, `.block__main` |

## Cover

Light: the render in the top 72% under a fade to `paper`, the masthead at
the bottom with the meta strip as a card. `cover: "02"` lays the halftone
at 60% (`.cover--texture`, as on the posts). `cover: "dark"`: plain `ink`,
white type, no picture.

| Item | Value | CSS |
|---|---|---|
| Ground | `paper` (dark: `ink`) | `.cover`, `.cover--dark` |
| Image | top 72% (texture: 64%), cover-fit, centred; one of the six renders | `.cover__img` |
| Fade | linear 180° over the same height: transparent to 40%, `paper` 90% at 82%, `paper` at 100% (dark: the same to `ink`) | `.cover__fade` |
| Top row | y 44, wordmark 22 high left, `CONFIDENTIAL · vX.X` label 9 `ink-soft` right | `.cover__top`, `.cover__logo`, `.cover__conf` |
| Masthead | bottom 44, left 56, width 682 | `.cover__bottom` |
| Kicker | the dash, then label 9 `ink-soft` (dark: `grey-6`) | `.cover__kicker` |
| Title | PP Eiko 500, 72 / .92, ls −0.045 em, `ink` (dark: `white`), 18 under kicker, max 640; Title Case; one phrase in `accent` (`<em>`) | `.cover__title`, `.cover__title em` |
| Standfirst | Roboto Condensed 13 / 1.5, ls −0.01 em, `ink-soft` (dark: white at 72%), max 480, 20 under title | `.cover__stand` |
| Meta card | 28 under; white card radius 12, 4 cells on `hair` rules, padding 14 18; key label 8 `muted`, value 11 `ink` (dark: white at 6% ground) | `.cover__meta` |
| Notice | label 8 ls 0.08 em `muted`, 20 under | `.cover__notice` |

Back cover: `ink` ground, the white wordmark, the orange mark 236 wide at
the top right, tagline PP Eiko 500, 40 / .95, ls −0.045 em, `white`, the
closing phrase in `accent` ("We turn Web3 ideas *into products people
use.*"), then the colophon card (WEBSITE · X · TELEGRAM · THIS DOCUMENT) and
the notice. THIS DOCUMENT reads on two lines: the class, then `vX.Y · D Mon
YYYY`. `.back`, `.back__glow` (the mark), `.back__tagline`.

## Blocks

| # | Block | Spec | CSS |
|---|---|---|---|
| 01 | Section label | the dash 19 × 5 `accent`, gap 10, label 9 `ink` | `.tag` |
| 08 | Source line | at the right of the label row, label-face 8.5 / 1.4 `muted`, not uppercase, right-aligned, max 300 | `.source` |
| 02 | Sub-heading | PP Eiko 500, 28 / .98, ls −0.04 em, `ink`, max 600, Title Case; optional accent phrase (`<em>`); optional suffix `muted` | `.heading`, `.heading em`, `.heading__suffix` |
| 03 | Body | Roboto Condensed 10.5 / 1.55, ls −0.005 em, `ink`, max 560; 12 under a heading, 8 between paragraphs | `.body` |
| 04 | Bullets | a grid of white cards (radius 12, padding 16, `auto-fit` from 150 wide, gap 10): the dash, then the term PP Eiko 14 / 1.05 ls −0.025 em, then the text 9.5 / 1.5 `ink-soft` | `.bullets`, `.bullet`, `.bullet__dot`, `.bullet__term`, `.bullet__text` |
| 05 | Table | a white card radius 12; head label 8 `muted` on a `hair` rule, padding 14 / 10 / 10; rows 9 / 10 / 9 on `hair` rules, none under the last; first cell 16 in, last 16 out; text 10 / 1.4 `ink`; figure cells tabular 10 `ink-soft` (`td.mono`); strong 500; one `tint` row | `.table`, `td.mono`, `td.strong`, `tr.highlight`, `.table--plain` |
| 06 | Headline figures | one white card; cells fill, padding 18 18 16, `hair` left rule except the first; number PP Eiko 500 44 / .9 ls −0.045 em `ink`, key label 8 `muted` 12 below. Numbers only in the number cell (`6`, `74%`, `T+1`) | `.figures`, `.figure`, `.figure__n`, `.figure__k` |
| 07 | Recommendation | the dark card: `ink` radius 12, padding 20 22 22, the dash; title PP Eiko 500 22 / 1.05 ls −0.03 em `white` max 520; body 10.5 / 1.55 white at 72% 12 below | `.reco`, `.reco__title`, `.reco__body` |
| — | Logo | the horizontal wordmark, 22 high on the cover, 18 in a fact-sheet running head, 30 on a deck title slide; the mark 16 wide in a running head; `_b` on paper, `_w` on dark. Never redrawn | `.cover__logo`, `.pagehead__logo`, `.pagehead__meta::before` |

Spacing inside a block: 12 between the label row and the main, 12 under a
heading before body, 16 before a card. Shipped table shapes: 4 columns
190 / 60 / 110 / fill (options), 3 columns 70 / fill / 190 (decision log),
3 columns 60 / 80 / fill (timeline), 2 columns 130 / fill (glossary), 3
columns 48 / fill / 60 without a head row (contents, rows 6.5 / 6.5). Any
other shape is built from the same cells with one fill column.

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

The page scaled ×1.6 on 1280 × 720, one block per slide, the same cards.

| Item | Value | CSS |
|---|---|---|
| Slide | 1280 × 720 `paper`, padding 56 / 72 | `.canvas--deck`, `.deck` |
| Running head | the mark 22 wide + label 11 `muted` left, the number label 14 `ink` right; no rule | `.deck__head` |
| Footer | rule, 14, label 11: `COOPER LABS · INTERNAL · NOT FOR DISTRIBUTION` and `NN / NN`; 44 from the bottom | `.deck__foot` |
| Stack | the label row, then the main, 48 under the head, gap 22 | `.deck__grid`, `.deck__margin`, `.deck__main` |
| Blocks | tag 12 (dash 28 × 7), source 12, heading 48 / .95 max 980, body 17 / 1.5 max 860, bullet cards radius 16 padding 24 (term 22, text 15, from 260 wide), table card radius 16 (15, head 11, figures 14), figures card (72, key 11), recommendation card radius 16 (title 34, body 16) | `.deck .tag` … |
| Title slide | the render in the top 78% under the light fade (`render: "02"` at 60%; `"dark"` plain ink); wordmark 30 high; conf 12; kicker 12 with the dash 28 × 7; title 84 / .92 max 900; standfirst 18 max 640; meta card radius 16 max 900, k 11 v 15 | `.deck--title` |
| Divider | number 220 / .85 `accent` ls −0.05 em, kicker with the dash, title 76 / .92 max 960; bottom-aligned, padding 56 / 72 / 120 | `.deck--divider` |
| Statement | padding 0 140, centred; the dash 28 × 7; text 64 / 1.02 ls −0.04 em; source label 12 | `.deck--statement` |
| Closing | `ink`, the orange mark 300 wide top right, tagline 52 max 760, the colophon card | `.deck--back` |

## Fact sheet

One A4 page, the document blocks at smaller sizes, in cards.

| Item | Value | CSS |
|---|---|---|
| Running head | wordmark `ink` 18 high left, meta right; no rule | `.page--fact .pagehead`, `.pagehead__logo` |
| Stack | column, gap 22, 30 under the head | `.fact` |
| Title | PP Eiko 500 46 / .95 ls −0.045 em max 600, 14 under the tag; one `accent` phrase | `.fact__title` |
| Standfirst | Roboto Condensed 12 / 1.5 ls −0.01 em `ink-soft` max 520, 14 under the title | `.fact__stand` |
| Columns | two white cards, gap 12, padding 16 18 18; heading 19; bullets as a list on `hair` rules (dash 12 × 4, term 10 500, text 9.5) | `.fact__cols` |
| Figures | the figures card, numbers 34, cells 14 16 12 | `.fact .figure__n` |
| Contact | a white card of four cells on `hair` rules: key label 8, value 10.5 | `.fact__contact` |

## Page styles

Sixteen compositions on the same page; the table in
`cooper-internal-document/SKILL.md` says what each is for. Sizes beyond the
scale: 20 (lede), 46 (statement), 130 (hero figure), 180 (divider number).

| Style | Values | CSS |
|---|---|---|
| A / B · Divider | fills the page, bottom-aligned; number PP Eiko 500 180 / .85 ls −0.05 em `accent`; kicker with the dash, label 9 `ink-soft` 30 under; title 60 / .92 ls −0.045 em max 560, 16 under; standfirst 13 / 1.5 `ink-soft` max 440; the list as a card of four cells, 28 under (dark: white at 6%) | `.divider`, `.page--dark` |
| C · Statement | centred, padding 0 48; the dash; text 46 / 1 ls −0.04 em, one `accent` phrase, 28 under; source label 9 `muted` 28 under | `.statement` |
| D · Hero figure | centred; number 130 / .85 ls −0.05 em, unit in `accent`; kicker with the dash 22 under; row of body + figures card, 36 under | `.hero` |
| E · Two columns | two white cards, gap 12, padding 18 20 20; head: the dash + label 9 `ink-soft`; heading 22; bullets as a list on `hair` rules; verdict PP Eiko 16 `accent-deep` on a `hair` rule, pushed to the bottom | `.cols`, `.cols__head`, `.verdict` |
| F · Timeline | a white card padding 22 20 20; 1 px `ink` rule, dashes 12 × 4 `accent` (`line` when past); date label 9, title 500 10.5, text 10 / 1.5; phases row label 8 on a `hair` rule | `.tl`, `.tl__step`, `.tl__phase` |
| G · Data page | the table card across 682, 9.5, cells 7 / 10; foot label-face 8.5 `muted` | `.wide`, `.wide__foot` |
| H · Chart | SVG in a white card padding 16; axes `hair`, base `ink`, bars `accent` / `grey-8`, line 1.5 `accent`; labels 8; legend 8 with 12 × 4 dashes | `.chart`, `.legend` |
| I · Matrix | grid 96 + 3 columns, gap 8; cells are white cards radius 10 padding 12; heads and keys sit on the page (label 8 / 9); cell title PP Eiko 12, text 9.5 `ink-soft`; the hot cell is `accent` with `ink` type | `.matrix` |
| J · Plate | 420 high, across the measure, radius 16, 36 under the head; caption as a white pill bottom left (label 8) | `.plate`, `.plate__cap` |
| K · Prose | padding 0 24; lede PP Eiko 500 20 / 1.25 ls −0.03 em with an `accent` phrase; body in two columns gap 24, 22 under; signature row label 8 on a `line` rule | `.prose`, `.prose__lede`, `.prose__sig` |
| L · Steps | the block turns into a row: the number PP Eiko 500 40 / .85 `accent` in a 64 column, then the step (heading 22, body, meta label 8 `muted`) | `.step__n`, `.step`, `.step__meta` |
| M · Glossary | a white card padding 4 20 6, two columns gap 24; term PP Eiko 15 / 1.1, definition 9.5 / 1.5 `ink-soft`, `hair` rule under each | `.defs`, `.def` |
| N · Flow | SVG 530 wide; boxes white with a `grey-7` stroke, radius 6 (soft: `line`, dashed); arrows `muted` with an `accent` dot 2.5; text 10 500, label 8, caption PP Eiko 14 with an `accent` span | `.flow` |
| O · Checklist | rows 10 / 16 on `hair` rules inside a white card (radius on the first and last); box 10 × 10 radius 3 `grey-6`, ticked `accent`; text 10.5; owner label 9 110 wide; sign-off as a card of cells, min 88 high | `.check`, `.sign` |
| P · Code | the dark card: Roboto Condensed 9 / 1.6 `white`, padding 18 20, radius 12; comments `grey-5`, keywords `accent` | `.code` |

## Fonts

| Family | File | Licence |
|---|---|---|
| PP Eiko Medium | not shipped; `local("PP Eiko Medium")` when installed, else `assets/fonts/private/pp-eiko-500.woff2` in a private copy | Pangram Pangram, commercial |
| Instrument Serif | `assets/fonts/instrument-serif-latin-400-*.woff2` | SIL OFL 1.1 (display fallback) |
| Roboto Condensed | `assets/fonts/roboto-condensed-latin-wght-{normal,italic}.woff2` | SIL OFL 1.1 |
