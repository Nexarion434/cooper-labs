"""Whether PP Eiko Medium, the display face, was actually served, and the one-line
report the render scripts print. Imported by render_pdf.py, render_png.py and
render_anim.py.

PP Eiko comes in one weight here, Medium (500), upright only: the documents and
the cards use it as it is. The report says whether it was served or what
stood in.
"""

JS_WEIGHTS = """async () => {
    const w = {};
    for (const [k, spec] of [["500", "500 20px 'PP Eiko'"]]) {
        try { const f = await document.fonts.load(spec); w[k] = f.length > 0 && f.every(x => x.status === 'loaded'); } catch (e) { w[k] = false; }
    }
    return w; }"""


def font_report(weights, design="500"):
    """One line. `weights` is the JS_WEIGHTS result."""
    if weights.get("500"):
        return "font: PP Eiko Medium, as in the Figma file."
    return "font: PP Eiko not available (neither installed nor in assets/fonts/private/); Instrument Serif stood in for the display type: letterforms differ, line breaks may move."
