# Private fonts (not in the public repository)

PP Eiko is a commercial face (Pangram Pangram). The plugin does not ship it.
Every display line, in the documents and on the cards, uses **Medium
(500)**, upright; there is no italic in this identity. Two ways to render
with it:

1. **On a machine where it is installed**: nothing to do, the CSS picks it
   up with `local("PP Eiko Medium")`.
2. **In a cloud session (Cowork / Claude Code without your computer)**: drop
   your licensed woff2 file in this folder, in a **private** copy of the
   plugin only, named:

   ```
   pp-eiko-500.woff2          Medium
   ```

   The CSS loads it as a second source after `local()`. When it is missing,
   Instrument Serif (OFL, shipped) stands in, and `render_png.py` /
   `render_pdf.py` say so in their last line.

Check your licence before copying the file here: a desktop licence usually
does not cover web-font use, and none allows redistribution. Keep the
repository that carries it **private**. For a public copy, uncomment the
font line in the `.gitignore` at the marketplace root before the first
commit, so the file never enters the history.
