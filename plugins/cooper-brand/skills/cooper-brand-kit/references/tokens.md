# Cooper Labs — tokens and block specs

Pixel values; the CSS class in the last column is the one in
`assets/css/cooper.css`. The social section is transcribed from the Figma
file *Brand Identity* (page *Twitter*); the documents, the deck and the fact
sheet are the design of the plugin on the same tokens. "Label" means Roboto
Condensed 500 UPPERCASE with 0.12 em letter-spacing (the role JetBrains Mono
holds in the Parallel kit; there is no mono here).

## Page

| Item | Value | CSS |
|---|---|---|
| Sheet | 794 × 1123, `paper`, clip | `.page` |
| Padding | 40 / 56 / 36 / 56 | `.page` |
| Running head | label 8, `muted`; 12 below, hairline `line` | `.pagehead` |
| Footer | hairline `line`, 12 above, label 8 `muted`; left `COOPER LABS · INTERNAL · NOT FOR DISTRIBUTION`, right `NN / NN`: every sheet counts, the cover is 01 (unnumbered), the interior runs from 02, the total includes the back cover | `.pagefoot` |
| Content | vertical stack, gap 34, starts 34 under the head, max 939 high | `.content` |
| Block | row: margin 128 + gap 24 + main fill | `.block`, `.block__margin`, `.block__main` |

## Cover

Light by default: the render full-bleed under a fade to `paper`, ink type.
`cover: "dark"` is the typographic cover: plain `ink`, white type, no
picture (`.cover--dark`).

| Item | Value | CSS |
|---|---|---|
| Ground | `paper` (dark: `ink`) | `.cover`, `.cover--dark` |
| Image | full-bleed, cover-fit, centred; one of the six renders | `.cover__img` |
| Fade | linear 180°: transparent to 35%, `paper` 85% at 72%, `paper` at 100% (dark: the same to `ink`) | `.cover__fade` |
| Top row | y 44, wordmark 22 high left (`cooper_horizontal_b.svg`; `_w` on dark), `CONFIDENTIAL · vX.X` label 9 `muted` right | `.cover__top`, `.cover__logo`, `.cover__conf` |
| Masthead | bottom 44, left 56, width 682 | `.cover__bottom` |
| Kicker | label 9, ls 0.14 em, `accent-deep` (dark: `accent-soft`) | `.cover__kicker` |
| Title | PP Eiko 500, 60 / 1.02, ls −0.05 em, `ink` (dark: `white`), 14 under kicker; Title Case; one phrase in `accent` (`<em>`) | `.cover__title`, `.cover__title em` |
| Standfirst | Roboto Condensed 13 / 1.5, `ink-soft` (dark: white at 72%), max 520, 18 under title | `.cover__stand` |
| Hairline | `line` (dark: `line-inv`), 26 under standfirst | `.cover__rule` |
| Meta strip | 4 columns gap 24, 16 under hairline; key label 8 `muted`, value Roboto Condensed 11 `ink` 8 below | `.cover__meta` |
| Notice | label 8 ls 0.10 em `muted`, 22 under meta | `.cover__notice` |

Back cover: `ink` ground, the white wordmark, a radial orange glow at 16%
bottom-left, tagline PP Eiko 500, 34 / 1.15, ls −0.04 em, `white`, the
closing phrase in `accent` ("We turn Web3 ideas *into products people
use.*"), then hairline, a four-column colophon (WEBSITE · X · TELEGRAM ·
THIS DOCUMENT) and the notice. THIS DOCUMENT reads on two lines: the class,
then `vX.Y · D Mon YYYY`. `.back`, `.back__glow`, `.back__tagline`.

## Blocks

| # | Block | Spec | CSS |
|---|---|---|---|
| 01 | Section label | margin column. 20 × 2 `accent` mark, 10 gap, label 9 / 1.3, `accent-deep` | `.tag` |
| 02 | Sub-heading | PP Eiko 500, 26 / 1.15, ls −0.03 em, `ink`, Title Case; optional accent phrase (`<em>`, `accent`); optional suffix `muted`, same size, one space | `.heading`, `.heading em`, `.heading__suffix` |
| 03 | Body | Roboto Condensed 10.5 / 1.6, `ink`, 10 under a heading, 8 between paragraphs | `.body` |
| 04 | Bullet | 6 px `accent` dot at y 6, gap 12; term Roboto Condensed 500 10.5 / 1.5 `ink`; text 10.5 / 1.55 `ink-soft`; bullets 10 apart | `.bullets`, `.bullet`, `.bullet__dot`, `.bullet__term`, `.bullet__text` |
| 05 | Table | head: label 8 ls 0.10 em `muted`, 9 below, 1 px `ink` rule; rows: 9 / 10 / 9 / 0 padding, 1 px `line` rule; text Roboto Condensed 10 / 1.4 `ink`; figure cells Roboto Condensed 10 tabular `ink-soft` (`td.mono`, the name kept from the engine); strong 500; one `tint` row allowed | `.table`, `td.mono`, `td.strong`, `tr.highlight`, `.table--plain` |
| 06 | Headline figures | row with `line` rule top and bottom; cells fill, 14 / 0 / 14 / 14 padding, `line` left rule except the first; number PP Eiko 500 40 / 1 ls −0.04 em `ink`, key label 8 `muted` 10 below. Numbers only in the number cell (`6`, `74%`, `T+1`): a word wraps | `.figures`, `.figure`, `.figure__n`, `.figure__k` |
| 07 | Recommendation | 2 px `accent` left rule, 18 padding; title PP Eiko 500 21 / 1.25 ls −0.02 em `ink`; body 10.5 / 1.6 `ink-soft` 10 below | `.reco`, `.reco__title`, `.reco__body` |
| 08 | Source line | margin column, under the label, gap 10; label-face 8 / 1.5 `muted`, not uppercase | `.source` |
| — | Meta item | key label 8 `muted`; value Roboto Condensed 11 / 1.3, 8 below | `.cover__meta .k`, `.v` |
| — | Logo | the horizontal wordmark, 22 high on the cover, 18 in a fact-sheet running head, 30 on a deck title slide; `_b` on paper, `_w` on dark. Never redrawn | `.cover__logo`, `.pagehead__logo` |

Shipped table shapes: 4 columns 190 / 60 / 110 / fill (options), 3 columns
70 / fill / 190 (decision log), 3 columns 60 / 80 / fill (timeline), 2
columns 130 / fill (glossary), 3 columns 48 / fill / 60 without a head row
(contents). Any other shape is built from the same cells with one fill column.

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

The A4 page scaled ×1.6 on 1280 × 720, one block per slide.

| Item | Value | CSS |
|---|---|---|
| Slide | 1280 × 720 `paper`, padding 56 / 72 | `.canvas--deck`, `.deck` |
| Running head | label 11 `muted`, 16 above a `line` rule; number right | `.deck__head` |
| Footer | rule, 14, label 11: `COOPER LABS · INTERNAL · NOT FOR DISTRIBUTION` and `NN / NN`; 44 from the bottom | `.deck__foot` |
| Grid | margin 180 + gap 40 + reading column, 44 under the head | `.deck__grid`, `.deck__margin`, `.deck__main` |
| Blocks | tag 12 (mark 28 × 3), source 11, heading 44 / 1.1, body 17 / 1.55 max 760, bullets 17 (dot 9), table 15 (figures 14, head 11), figures 72 (key 11), recommendation title 32 body 16 (rule 3) | `.deck .tag` … |
| Title slide | the render full-bleed under the light fade (or `render: "dark"`, plain ink); wordmark 30 high; conf 12; kicker 12; title 76 max 900 ls −0.05 em; standfirst 18 max 640; meta k 11 v 15 | `.deck--title` |
| Divider | number 200 `accent`, kicker label 12 `accent-deep`, title 72 / 1.02 max 900; bottom-aligned, padding 56 / 72 / 120 | `.deck--divider` |
| Statement | padding 0 160, centred; mark 28 × 3 `accent`; text 60 / 1.15; source label 12 | `.deck--statement` |
| Closing | `ink`, glow, tagline 44 max 700, the links, THIS DECK | `.deck--back` |

## Fact sheet

One A4 page, the document blocks at smaller sizes.

| Item | Value | CSS |
|---|---|---|
| Running head | wordmark `ink` 18 high left, meta right, items centred | `.page--fact .pagehead`, `.pagehead__logo` |
| Stack | column, gap 28, 28 under the head | `.fact` |
| Title | PP Eiko 500 44 / 1.05 ls −0.04 em max 600, 14 under the tag; one `accent` phrase | `.fact__title` |
| Standfirst | Roboto Condensed 12 / 1.5 `ink-soft` max 520, 12 under the title | `.fact__stand` |
| Columns | two, gap 24; heading 18; body and bullets 10 | `.fact__cols` |
| Figures | the figures row, numbers 34 | `.fact .figure__n` |
| Contact | four columns on a 1 px `ink` rule, 12 above; key label 8, value 10.5 | `.fact__contact` |

## Page styles

Sixteen compositions inside the document grid; the table in
`cooper-internal-document/SKILL.md` says what each is for. Sizes beyond the
scale: 18 (lede), 44 (statement), 120 (hero figure), 160 (divider number).

| Style | Values | CSS |
|---|---|---|
| A / B · Divider | fills the page, bottom-aligned; number PP Eiko 500 160 ls −0.02 em `accent` (dark: `accent-soft`); kicker label 9 `accent-deep` 28 under; title 60 / 1.02 max 560, 14 under; standfirst 13 / 1.5 `ink-soft` max 440; rule; list of four k/v | `.divider`, `.page--dark` |
| C · Statement | centred, padding 0 64; mark 20 × 2 `accent`; text 44 / 1.15, one `accent` phrase; source label 9 `muted` 28 under | `.statement` |
| D · Hero figure | centred; number 120 ls −0.02 em, unit in `accent`; kicker label 9 `accent-deep` 16 under; rule 34; row of body + figures (no outer rule) | `.hero` |
| E · Two columns | gap 24; head label 9 `accent-deep` on a 1 px `ink` rule; heading 21; verdict PP Eiko 16 `accent-deep` on a `line` rule | `.cols`, `.cols__head`, `.verdict` |
| F · Timeline | 1 px `ink` rule, dots 6 `accent` (`line` when past); date label 9, title 500 10.5, text 10 / 1.5; phases row label 8 on a `line` rule | `.tl`, `.tl__step`, `.tl__phase` |
| G · Data page | the table across 682, 9.5, cells 7 / 10; foot label-face 8 `muted` | `.wide`, `.wide__foot` |
| H · Chart | SVG on the reading column; axes `line`, base `ink`, bars `accent` / `line`, line 1.5 `accent`; labels 8; legend 8 with 12 × 2 swatches | `.chart`, `.legend` |
| I · Matrix | grid 110 + 3 columns on a 1 px `ink` rule; heads label 8; keys label 9 `accent-deep`; cells 10 / 1.5 `ink-soft`, title 500 `ink`; one `tint` cell | `.matrix` |
| J · Plate | 420 high, full bleed (margin −56), 34 under the head; caption label 8 bottom left | `.plate`, `.plate__cap` |
| K · Prose | padding 0 64; lede PP Eiko 500 18 / 1.4 with an `accent` phrase; body in two columns gap 24; signature row label 8 on a `line` rule | `.prose`, `.prose__lede`, `.prose__sig` |
| L · Steps | number PP Eiko 500 40 `accent` in the margin; heading 21; meta label-face 8 `muted` 10 under | `.step__n`, `.step`, `.step__meta` |
| M · Glossary | two columns gap 24; term PP Eiko 500 16, definition 10 / 1.5 `ink-soft`, `line` rule under each | `.defs`, `.def` |
| N · Flow | SVG 530 wide; boxes 1 px `ink` (soft: `line`), radius 0; arrows `muted` with an `accent` dot 2.5; text 10, label 8, caption PP Eiko 14 with an `accent` span | `.flow` |
| O · Checklist | rows 9 / 0 on `line` rules; box 9 × 9 1 px `ink`, ticked `accent`; text 10.5; owner label 9 110 wide; sign-off columns on a 1 px `ink` rule, 44 padding | `.check`, `.sign` |
| P · Code | Roboto Condensed 9 / 1.6, padding 14, `ink` rule above, `line` rule under; comments `muted`, keywords `accent-deep` | `.code` |

## Fonts

| Family | File | Licence |
|---|---|---|
| PP Eiko Medium | not shipped; `local("PP Eiko Medium")` when installed, else `assets/fonts/private/pp-eiko-500.woff2` in a private copy | Pangram Pangram, commercial |
| Instrument Serif | `assets/fonts/instrument-serif-latin-400-*.woff2` | SIL OFL 1.1 (display fallback) |
| Roboto Condensed | `assets/fonts/roboto-condensed-latin-wght-{normal,italic}.woff2` | SIL OFL 1.1 |
