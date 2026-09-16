# Cooper Labs — voice and mechanics

## Positioning

> **We turn Web3 ideas into products people use.**

Cooper Labs is a product studio for Web3 teams: a designer and an engineer on
every project, from the brief to the stores, working software shown every
Friday. The studio's material speaks as a builder speaks: what was made, for
whom, in how many weeks, and what the numbers said afterwards.

Documents let the renders carry the identity (the cover plate, a part
divider, the back cover, a specimen). Inside, the voice is precise, calm
and specific; a headline carries one claim, in ink.

## Tone

- **Lead with the decision.** The standfirst says what the document decides
  or records, and for whom. The summary says what was found and what is
  recommended. The rest is evidence.
- **Figures carry the emphasis.** No "cutting-edge", "seamless",
  "best-in-class". Weeks, demos, tools, users, ratings. If there is no number,
  say so.
- **Name the risk and the mitigant together.** A risk without a mitigant is
  written as accepted or unmitigated, never left implicit.
- **Short sentences, one idea each.** Two clauses maximum.
- **A proposal names its demos.** Every phase ends on a Friday demo; the next
  phase starts on one. Dates are commitments, so they are written as dates.
- **A case study says what would change.** The last block of a case study is
  what the studio would do differently, not a testimonial.
- **A post-mortem is blameless.** Actors are roles or first names; every
  action has an owner and a date.

## Naming

- The studio is "Cooper Labs", two words, both capitalised; "Cooper" alone
  only in the fixed line *We Are Cooper*. Never "CooperLabs" in prose (the
  file prefix is the one exception).
- Clients and products are named as they name themselves: "Parallel",
  "USDp", "Atlas Wallet". Product names keep their own case in Title Case.
- Engagement phases are "Product", "Build", "Release", "Care". The weekly
  demo is "the Friday demo".
- Tickets are `ATL-140`, `PAR-12`, `DES-122`, as in Linear.

## The marked phrase

PP Eiko exists here in one weight and no italic. A headline still carries
one claim, and the descriptions mark it with `*...*` (`<em>` in HTML):

- one phrase per headline, two or three words, never a single noun and never
  the whole line;
- the verb or the qualifier, the part that carries the claim: "Ship the MCP
  Server *Before the CLI.*", "One Server, *Every Agent.*", "*Fifty-Two
  Minutes* on the Wrong RPC.";
- never on kickers, labels, meta lines, table heads or body copy.

In the **documents** (0.4.0, the Object system) the mark renders in ink:
the phrase is written for whoever reads the description and for a future
system, not seen. On the **social cards** that ask for it (`.thread__body`,
`.banner__tag`) the CSS renders it upright and `accent`.

**Social posts are the exception**: the titles of the Figma file carry no
accent ("2026 Roadmap / for Parallel published", "Seventeenth / Parallel
Report", "Flash Loans / Explained"). Add one only when asked, and keep the
capitalisation as the author wrote it.

## Nothing that reads like a model wrote it

A client can tell. The em dash is the first tell, and it is never the only
one: where there is one, there is usually an adjective doing the work of a
figure. `check_text.py` holds the list and every builder runs it on the
description before it writes a line, so the copy is caught while it can still
be rewritten (`python3 check_text.py doc.json`, or `--text "one sentence"`).

Faults, which stop the build:

| Written | Write instead |
|---|---|
| `—` | a period when what follows is a sentence, a comma for an aside, a colon when it explains, `·` in a meta line |
| `–` between words | "to" in a range (2023 to 2026), a comma elsewhere |
| `...` for a trailing thought | the end of the sentence |
| an emoji | words |

Tells, which are printed and left to the writer: *seamless, robust,
cutting-edge, best-in-class, game-changing, transformative, holistic, synergy,
landscape, realm, myriad, plethora, vibrant, a testament to, underscores,
pivotal, crucial, unlock, empower, streamline, harness, foster, delve,
leverage, utilise, deep dive, embark, our journey, in today's, ever-evolving,
fast-paced, it's worth noting, when it comes to, more than just, at the end of
the day, boasts, comprehensive, ensures that, truly, really, significantly*,
"Moreover" or "Overall" opening a sentence, and the shape *"not just X, it's
Y."*

The rewrite is the same move every time: **put the figure where the adjective
was**, and cut the rest. "A robust, seamless integration that empowers the
team" is "Two endpoints, one schema; the team shipped in six weeks." If there
is no figure, say the fact plainly, or say there is no figure yet.

## Mechanics

- **No em dash** anywhere a reader will see it: copy, headings, table cells,
  the PDF title. Use a period, a comma, or the middle dot.
- Middle dot `·` separates meta items: `PROPOSAL · PARALLEL MCP SERVER ·
  CONFIDENTIAL · v0.1`.
- Kickers, labels and meta lines are UPPERCASE Roboto Condensed 500 with
  0.12 em letter-spacing. Table head cells the same.
- **Document titles are Title Case** (cover title, sub-headings, tagline):
  every word capitalised except short connectors (a, an, the, and, but, or,
  nor, for, so, yet, as, at, by, in, of, on, to, up, vs, via, per, from,
  into, onto, over, with, under, than, that, its); first and last words
  always, and the word after a colon or a question mark. Hyphenated words
  capitalise both parts (Fifty-Two, Read-Only). Product names keep their own
  case (USDp, MCP, PIP-14). `build_doc.py` applies it.
- Sentence case stays for the standfirst, body copy, bullets, table cells,
  the recommendation title (it is a sentence) and the muted parenthetical
  suffix of a sub-heading ("(six weeks)").
- Dates: `14 September 2026` in prose and on the cover, `14 Sep` in tables
  and timelines, `09:52 UTC` for times.
- Versions: `v0.1` draft, `v1.0` final, bumped on every material revision
  and identical on the cover, in every running head and in the file name.
- Figures: numbers alone in a headline-figure cell (`6`, `74%`, `4.7`); the
  word goes in the key (`WEEKS, BRIEF TO RELEASE`). Percentages with one
  decimal when it matters, none when it does not.
- Classification is one of `Confidential`, `Internal`, `Public`. Status is
  one of `Draft`, `Final`. Both appear on the cover meta strip.
- **English throughout**, whatever the language of the conversation.

## Fixed lines

- Cover notice: `INTERNAL DOCUMENT · NOT FOR DISTRIBUTION OUTSIDE COOPER LABS`
- Footer: `COOPER LABS · INTERNAL · NOT FOR DISTRIBUTION`; a `Public` fact
  sheet or deck: `COOPER LABS · COOPERLABS.XYZ`
- Back cover notice: `INTERNAL DOCUMENT · NOT FOR DISTRIBUTION OUTSIDE COOPER
  LABS · © 2026 COOPER LABS`
- Back cover colophon: `cooperlabs.xyz`, `@cooperlabs`, `@jeanbrasse`, then
  the document's class, version and date. The contact strip of a fact sheet
  adds `contact@cooperlabs.xyz`.
- Tagline, on the back cover and the closing slide: `We turn Web3 ideas
  *into products people use.*`

Do not invent clients, figures, ratings, dates or team members. The examples
shipped with the plugin (Atlas Wallet, the Parallel MCP server proposal, the
launch-day post-mortem) are illustrative: their figures are placeholders,
not records. When a figure is missing, leave a visible `TBD` and say so in
the reply.
