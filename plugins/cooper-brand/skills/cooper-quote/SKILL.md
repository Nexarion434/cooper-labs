---
name: cooper-quote
description: >
  This skill should be used for a Cooper Labs quote or proposal letter:
  "quote", "devis", "estimate", "how much for", "send them the price", "the
  offer for", "proposal letter", "a two-pager with the phases and the
  price", or when a scope, a price per phase, a payment schedule and the
  terms have to go to a client for signature. Two A4 pages, delivered as a
  PDF.
metadata:
  version: "0.5.0"
  source: "cooper-brand 0.5.0 — the quote on the Object system"
---

# Cooper Labs — quote

Two A4 pages, no cover, on the catalogue page of the internal document.
**Page one is the offer**: the parties (to, from) and the quote's facts
(number, date, valid until) in the margin column, the title and the
introduction beside them, then the phases as a table across the measure
with the total on an ink line. **Page two is the agreement**: the payment
schedule, the terms as a numbered list, the acceptance paragraph and the
two signature blocks. **English throughout** (the legal mention can be
French, `art. 293 B CGI`). Load `cooper-brand-kit` first if the tokens are
not already in context.

## Intake, in one round

| Question | Options |
|---|---|
| For whom, for what? | client (name, contact, email), subject, the brief or the proposal it follows |
| The phases | name, what is delivered, weeks, price; two or three phases, a fixed price each |
| Money | currency (EUR default), VAT mention, the payment schedule (30 / 40 / 30 on signature, mid demo, delivery, by default) |
| Number and dates | `Q-YYYY-NNN`, the date, valid for 30 days by default |

A quote follows a proposal when there is one: the phases are the
proposal's phases, the prices are not invented. Ask for the prices; never
estimate them.

## Build

```bash
S=${CLAUDE_PLUGIN_ROOT}/assets/scripts
python3 $S/build_quote.py --example > quote.json          # a description to start from
# edit quote.json
python3 $S/build_quote.py quote.json quote.html --pdf     # HTML, CooperLabs-Quote-<Subject>-<number>.pdf, check_pdf.py
python3 $S/render_pdf.py quote.html quote.pdf --png review/
```

The description carries `subject`, `number`, `date`, `valid_until`,
`currency`, `vat` (the note on the total line), `client` (`name`,
`lines`), `from` (default: the studio), `title`, `intro` (paragraphs),
`phases` (`name`, `what`, `weeks`, `price`), `total`, `schedule`
(`[[milestone, when, share, amount], ...]`), `terms` (a list),
`acceptance` (optional paragraph) and `signatories`
(`[[for whom, name and role], ...]`). Prices are strings, written as they
should print (`24 000`); the currency appears once, in the table head.

## Composition

| Item | Value | CSS |
|---|---|---|
| Running head | wordmark 16 high left, label 7.5 muted `QUOTE · SUBJECT · NUMBER · DATE` right | `.page--quote .pagehead` |
| Parties | `TO`, `FROM`, then the facts, as key-value pairs in the margin column; the name 500 | `.quote__parties`, `.quote__party` |
| Title | the label `QUOTE · CONFIDENTIAL`, PP Eiko 30, the introduction under it at 11 | `.note__title`, `.body` |
| Phases | a table across the measure: phase (strong), what, weeks, price; the total row on an ink line, the amount at 12 | `.table--quote` |
| Schedule | the table on hairlines: milestone, when, share, amount | `.table` |
| Terms | the numbered list | `.nlist` |
| Acceptance | one paragraph, then two columns on an ink line: for whom, name and role, `DATE, SIGNATURE` on a hairline | `.sign`, `.sign__line` |
| Footer | `COOPER LABS · CONFIDENTIAL · QUOTE Q-YYYY-NNN` and `NN / 02` | `.pagefoot` |

## Rules specific to the quote

- **Fixed price per phase, and the next phase starts on a demo.** The
  first term says so; do not remove it.
- **Nothing that signs.** A quote for read-only work says it; anything
  that holds keys is a separate quote.
- **Amounts add up**: the phases sum to the total, the schedule sums to
  the total; `check_pdf.py` does not check arithmetic, so do it.
- **Title Case on the title**; sentence case everywhere else; no em dash.
- The quote is confidential by default; the footer says so.

## Before delivering

1. Prices and dates come from the user; the sums are right.
2. The client's name and contact are spelled as they spell them.
3. Two pages, nothing cut (look at the PNGs).
4. `check_pdf.py` passes.

## References

- `cooper-brand-kit/references/tokens.md` — the Note and quote section
- `cooper-internal-document/SKILL.md` — the blocks and the writing rules
- `../../assets/examples/quote-parallel-mcp.json` and `.html`
- `../../assets/scripts/build_quote.py` — the builder
