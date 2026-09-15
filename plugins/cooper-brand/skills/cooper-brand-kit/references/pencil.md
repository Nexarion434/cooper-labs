# The design source, and a Pencil file when there is one

There is **no `cooper.pen` yet**. The HTML route is the only route: every
document, deck, fact sheet and card comes from the JSON descriptions,
`assets/css/cooper.css` and the builders. This note says where the numbers
come from and what a Pencil (or Figma) document system would need to carry
so that the two routes stay identical, as they do in `parallel-brand`.

## Where the numbers come from

| Part | Source | Status |
|---|---|---|
| Social: post (Template01, 02, 04), partner (Template03), X covers, social preview, wallpaper, logos, palette | Figma file *Brand Identity*, page *Twitter* (`S5Lg16aM47EGiGOYCDxl9a`, node `135:15`) | transcribed pixel for pixel; the rendered PNGs differ from the Figma exports by a few pixels of glyph rendering only |
| Tokens (greys, oranges, `paper`), Roboto Condensed as the text face | cooperlabs.xyz | transcribed |
| Internal document (cover, blocks, back cover, sixteen page styles), deck, fact sheet | the engine of `parallel-brand` with the Cooper Labs tokens, on the **Object** system chosen on the design canvas of 15 Sep 2026 (the renders as plates, small precise type, a margin column, hairlines, no colour in the type) | designed in the plugin, not in a design file; the canvas *Cooper Labs Document Directions, Round Two* holds the five directions |
| Extra social sizes, banners, thread, animation | the same rules as the Figma posts, at the sizes of `parallel-brand` 0.5.0 | designed in the plugin |

The design decisions taken in the plugin are listed in `CHANGELOG.md`
under *Design decisions*, so that a designer can accept or overrule them in
the design file when one exists.

## What a `cooper.pen` would carry

The `parallel.pen` structure, with the Cooper Labs components: *Internal
Document · Blocks Library* (the eight blocks and the sixteen page styles),
*Internal Document · Guide*, *Social · Blocks Library* (post, partner, X
cover, preview, banners, thread, per size), *Deck*, *Fact sheet*, and a
*Cooper · Renders* page with the six renders by number. Component names
should match the CSS classes in `tokens.md`, so that `frame.py` can print
the Pencil override for a render and the builders' descriptions map onto
instances one to one.

When that file exists, the Pencil route of `parallel-brand` applies as it
stands (duplicate, never rebuild; never detach; `placeholder: true` while
working; save with Ctrl+S; re-resolve IDs by name before every build), and
`references/pencil.md` here becomes the ID table for the Cooper components.
Until then, a request for "the Pencil version" gets the HTML build and a
note that the design file does not exist.
