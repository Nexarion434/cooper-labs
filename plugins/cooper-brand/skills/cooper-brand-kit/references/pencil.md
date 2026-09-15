# The design source: `cooper.pen`

Since 0.5.0 the repository root carries **`cooper.pen`**, the Object system
as a Pencil (pen.dev) document, written by `tools/make_pen.py` from the
same tokens as `cooper.css`. Two sources, one system: the CSS is what the
builders use, the `.pen` is what a designer opens, edits and extends.
Image fills point into `plugins/cooper-brand/assets/` by relative path, so
the file must stay at the repository root (or its `A` prefix in the script
be changed).

## What is in the file

- **Variables**: the tokens (`paper`, `card`, `ink`, `ink-soft`, `muted`,
  `line`, `hair`, `accent`, `white`; `display` = PP Eiko, `sans` = Roboto
  Condensed; `margin` 72, `measure` 650, `column` 200, `gap` 36).
- **Components** (the *Components* frame at the top): *Wordmark* (the mark
  as a path + "Cooper Labs" in PP Eiko), *Running head*, *Footer*,
  *Figure* (number + key). The mark is a path with the SVG geometry of
  `cooper_icon_b.svg`, never a picture.
- **Pages**, one frame each, at the sizes of the builders: *Doc · Cover*,
  *Doc · Section page* (specimen, heading and body, the figures strip, a
  table, bullets, the recommendation), *Doc · Divider*, *Doc · Hero
  figure*, *Doc · Back cover*, *Deck · Title*, *Deck · Content slide*,
  *Fact sheet*, *Meeting note*. Frame names match the CSS sections in
  `tokens.md`; node names match the class names (`Tag`, `Source`,
  `Specimen`, `Heading`, `Body`, `Figures`, `Table`, `Recommendation`).

Regenerate it after a change to the tokens or the layout numbers:

```bash
python3 tools/make_pen.py        # -> cooper.pen (overwrites; edits made in Pencil are lost, so commit them or fold them into the script)
```

## Working in Pencil through the MCP

`execute` acts on the **active editor**, whatever `filePath` says: the
designer opens `cooper.pen` in Pencil first (`get_app_state` shows which
file is active; if it is not `cooper.pen`, ask rather than building in the
wrong file). Then the rules of `parallel-brand` apply:

1. **Duplicate, never rebuild.** `Copy` a page frame, then override text.
2. **Never detach an instance.** Override a descendant's `content`; for a
   component that *is* a text node, set `content` on the ref itself.
3. Emulate deleting a descendant with `enabled: false`.
4. `placeholder: true` on a copied frame while you work on it; clear it at
   the end.
5. Pencil does not autosave through the MCP: ask the designer to save
   (Ctrl+S) before reading the `.pen` from disk or ending the session.
6. PP Eiko must be installed on the machine for the display type to render
   (it is not shipped; `local("PP Eiko Medium")`); Roboto Condensed comes
   from Google Fonts. A weight that is not installed stalls the frame.
7. Verify with `Get(page, (n, c) => c.problems && Print(n.name, c.problems))`
   before a screenshot; zero problems is the bar.
8. IDs are a cache: re-resolve by name before every build,
   `Get(n => n.reusable && Print(n.id, "=", n.name))`.

## Where the numbers come from

| Part | Source | Status |
|---|---|---|
| Social: post (Template01, 02, 04), partner (Template03), X covers, social preview, wallpaper, logos, palette | Figma file *Brand Identity*, page *Twitter* (`S5Lg16aM47EGiGOYCDxl9a`, node `135:15`) | transcribed pixel for pixel; the rendered PNGs differ from the Figma exports by a few pixels of glyph rendering only |
| Tokens (greys, oranges, `paper`), Roboto Condensed as the text face | cooperlabs.xyz | transcribed |
| Internal document, report, deck, fact sheet, note, quote | the engine of `parallel-brand` with the Cooper Labs tokens, on the **Object** system chosen on the design canvas of 15 Sep 2026 (*Cooper Labs Document Directions, Round Two*) | designed in the plugin; `cooper.pen` mirrors it |
| Extra social sizes, banners, thread, animation | the same rules as the Figma posts, at the sizes of `parallel-brand` 0.5.0 | designed in the plugin; not in `cooper.pen` yet |
| Renders 07 and up | `assets/scripts/render_block.py` | made in the plugin, catalogued by number |

The design decisions taken in the plugin are listed in `CHANGELOG.md`
under *Design decisions*, so that a designer can accept or overrule them in
the design file. The social section is not in `cooper.pen`: its source is
the Figma file.
