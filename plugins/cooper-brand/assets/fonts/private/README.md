# Private fonts (not in the public repository)

PP Eiko is a commercial face (Pangram Pangram). The plugin does not ship it.
Every display line, in the documents and on the cards, uses **Medium
(500)**, upright: that is the brand weight. Four more cuts are declared in
the CSS for the designer's use (Thin, Light Italic, Heavy, Black Italic);
nothing shipped uses them. Two ways to render with the face:

1. **On a machine where it is installed**: nothing to do, the CSS picks it
   up with `local("PP Eiko Medium")`.
2. **In a cloud session (Cowork / Claude Code without your computer)**: drop
   your licensed woff2 file in this folder, in a **private** copy of the
   plugin only, named:

   ```
   pp-eiko-500.woff2          Medium            the brand weight, the only one the builders need
   pp-eiko-100.woff2          Thin              optional
   pp-eiko-300-italic.woff2   Light Italic      optional
   pp-eiko-800.woff2          Heavy             optional
   pp-eiko-900-italic.woff2   Black Italic      optional
   ```

   The CSS loads each as a second source after `local()`. When Medium is
   missing, Instrument Serif (OFL, shipped) stands in, and `render_png.py`
   / `render_pdf.py` say so in their last line; a missing optional cut
   falls back to Medium.

   To make the woff2 from the OTF: `python3 -c "from fontTools.ttLib import
   TTFont; f=TTFont('PPEiko-Medium.otf'); f.flavor='woff2';
   f.save('pp-eiko-500.woff2')"` (`pip install fonttools brotli`).

Check your licence before copying the file here: a desktop licence usually
does not cover web-font use, and none allows redistribution. Keep the
repository that carries it **private**. For a public copy, uncomment the
font line in the `.gitignore` at the marketplace root before the first
commit, so the file never enters the history.
