# tools

The sources of what the plugin ships, kept next to it so a change is made
here and regenerated, not edited in the output.

| File | Writes |
|---|---|
| `make_css.py` | `plugins/cooper-brand/assets/css/cooper.css` from `doc.css` (the documents, the deck, the fact sheet, the page styles) and `social.css` (the Figma transcription), with the fonts and tokens head |
| `make_examples.py` | the descriptions: `assets/templates/internal-doc.json`, `assets/templates/report.json` and every `assets/examples/*.json` |
| `make_pen.py` | `cooper.pen` at the repository root: the Object system as a Pencil document (variables, components, one frame per page), from the same numbers as `doc.css` |

After a change, rebuild the HTML with the builders (`build_doc.py`,
`build_deck.py`, `build_fact_sheet.py`, `build_note.py`, `build_quote.py`,
`build_social.py` with `--relative`) and run the smoke test in the plugin
README.
