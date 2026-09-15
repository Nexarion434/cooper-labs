---
name: cooper-note
description: >
  This skill should be used for a Cooper Labs meeting note: "meeting note",
  "compte rendu", "CR", "the notes of the weekly", "write up what we decided",
  "who does what after the call", "minutes" (the note is shorter than
  minutes), or when a call, a weekly, a workshop or a demo has to leave one
  page with the decisions and the actions. One A4 page, delivered as a PDF.
metadata:
  version: "0.5.0"
  source: "cooper-brand 0.5.0 — the meeting note on the Object system"
---

# Cooper Labs — meeting note

One A4 page, no cover, on the catalogue page of the internal document: the
wordmark and the running head, the facts of the meeting in the margin
column (date, where, attendees, note by), the title beside them, then the
blocks: **Context** (one or two sentences), **Decisions** (a numbered
list), **Actions** (a table: action, owner, due), **Next** (one sentence
and the next meeting). What was decided and who does what, not what was
said. **English throughout.** Load `cooper-brand-kit` first if the tokens
are not already in context.

## Intake, in one round

| Question | Options |
|---|---|
| Which meeting? | subject (`Parallel weekly`), date, where, who was there |
| What was decided? | each decision in one line, with its one-sentence reason |
| Who does what? | action, owner, due date; an action without an owner is a decision, not an action |
| Classification | Internal (default) · Confidential |

Read a transcript, a chat log or the user's own notes when given; ask only
for what is missing. Never invent a decision or an owner.

## Build

```bash
S=${CLAUDE_PLUGIN_ROOT}/assets/scripts
python3 $S/build_note.py --example > note.json          # a description to start from
# edit note.json
python3 $S/build_note.py note.json note.html --pdf      # HTML, CooperLabs-Note-<Subject>-<date>.pdf, check_pdf.py
python3 $S/render_pdf.py note.html note.pdf --png review/
```

The description carries `subject`, `title` (a `*phrase*` may mark the
claim; it renders in ink), `date` (ISO), `where`, `attendees` (a list),
`owner` (who wrote it), `classification`, `context`, `decisions`
(`[[title, one sentence], ...]`), `actions` (`[[action, owner, due], ...]`),
`next` and `next_meeting`. The running head reads `MEETING NOTE · SUBJECT ·
D MONTH YYYY`; the file is named by the date, not by a version.

## Composition

| Item | Value | CSS |
|---|---|---|
| Running head | wordmark 16 high left, label 7.5 muted right; no rule | `.page--note .pagehead` |
| Facts | key-value pairs in the margin column: key 7.5 muted, value 9.5 | `.note__facts`, `.note__pair` |
| Title | the label `MEETING NOTE · INTERNAL` 7.5 muted, then PP Eiko 30 / 1.02, max 420 | `.note__title` |
| Blocks | the margin grid of the document, 40 under the head, gap 36 | `.content`, `.block` |
| Decisions | a numbered list: `01` in PP Eiko 13 in a 40 column, the title 11 500, the sentence 10 `ink-soft`; hairlines, the first line in ink | `.nlist` |
| Actions | the table on hairlines: action (strong), owner 110, due 70 | `.table` |
| Next | a sentence, then `NEXT MEETING` and its value on an ink line | `.note__next` |
| Footer | `COOPER LABS · INTERNAL · NOT FOR DISTRIBUTION` and `01 / 01` | `.pagefoot` |

Everything must fit on the page: three to five decisions, four to six
actions. More than that is two meetings or a memo (`cooper-internal-document`).

## Rules specific to the note

- **A decision is one line and one reason.** The title says what was
  decided; the sentence says why or what changes. No discussion.
- **An action has an owner and a date.** First names for the owner (the
  attendees list gives the surname and the side); dates as `16 Sep`.
- **Title Case on the title**; sentence case everywhere else. No em dash;
  the middle dot separates meta items.
- **Written the same day**, dated the day of the meeting; the file name
  carries the date.

## Before delivering

1. Every decision and action comes from the source; nothing added.
2. Every action has an owner and a date.
3. One page, nothing cut (look at the PNG).
4. `check_pdf.py` passes.

## References

- `cooper-brand-kit/references/tokens.md` — the Note and quote section
- `cooper-internal-document/SKILL.md` — the blocks and the writing rules
- `../../assets/examples/note-parallel-weekly.json` and `.html`
- `../../assets/scripts/build_note.py` — the builder
