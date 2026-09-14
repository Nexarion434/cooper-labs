#!/usr/bin/env python3
"""Render a Cooper Labs HTML document to a true A4 PDF (794 x 1123 px @ 96 dpi).

    python3 render_pdf.py input.html [output.pdf]
    python3 render_pdf.py input.html output.pdf --png review/   # one PNG per page
    python3 render_pdf.py deck.html deck.pdf --size 1280x720 --sheets .canvas--deck   # a deck: 16:9 pages (build_deck.py does this)

Every .cover / .page element becomes exactly one PDF page. Fonts, images and
logos load from the plugin's assets/ directory through the paths new_doc.py
wrote into the file.

Needs Python with Playwright and a Chromium build:
    pip install playwright && playwright install chromium

PP Eiko is not shipped (commercial). Chromium picks it up when it is
installed on the machine (the local() rules in cooper.css) or dropped into
assets/fonts/private/ as woff2; otherwise the shipped Instrument Serif stands
in. The last line of the run says which weight was served (fontcheck.py, the
same report as render_png.py).

Chromium embeds JPEG covers byte for byte but tags them `/ColorTransform 0`
("already RGB") while the data is YCbCr; strict PDF readers then render the
covers magenta. The flag is repaired in place after writing, same byte length,
so the xref table stays valid. (Repair adapted from 1212-Capital/claude-plugins,
MIT.)
"""
import sys, os, re, struct, pathlib, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fontcheck import JS_WEIGHTS, font_report

W, H = 794, 1123


def _jpeg_is_ycbcr(buf):
    i, n = 2, len(buf)
    while i + 4 <= n and buf[i] == 0xFF:
        marker = buf[i + 1]
        if marker in (0xD8, 0xD9):
            i += 2
            continue
        ln = struct.unpack(">H", buf[i + 2:i + 4])[0]
        seg = buf[i + 4:i + 2 + ln]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3):
            ncomp = seg[5]
            ids = [seg[6 + 3 * k] for k in range(ncomp)]
            return ncomp == 3 and ids != [ord("R"), ord("G"), ord("B")]
        if marker == 0xDA:
            return False
        i += 2 + ln
    return False


def fix_jpeg_colortransform(path):
    data = bytearray(pathlib.Path(path).read_bytes())
    fixed = 0
    for m in re.finditer(rb"/ColorTransform\s+0", bytes(data)):
        s = data.find(b"stream", m.end())
        if s == -1:
            continue
        j = s + 6
        while j < len(data) and data[j] in (0x0D, 0x0A):
            j += 1
        if data[j:j + 2] != b"\xff\xd8" or not _jpeg_is_ycbcr(data[j:j + 4096]):
            continue
        zero = data.rfind(b"0", m.start(), m.end())
        data[zero:zero + 1] = b"1"
        fixed += 1
    if fixed:
        pathlib.Path(path).write_bytes(bytes(data))
    return fixed


async def run(src, out, png_dir, size=None, sheets=".cover, .page"):
    W, H = size or (794, 1123)
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        sys.exit("playwright is required:  pip install playwright  &&  playwright install chromium")

    url = pathlib.Path(src).resolve().as_uri()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        await page.goto(url, wait_until="networkidle")
        await page.evaluate("document.fonts.ready")
        await page.wait_for_timeout(400)

        weights = await page.evaluate(JS_WEIGHTS)
        n_pages = await page.evaluate(f"document.querySelectorAll('{sheets}').length")
        overflow = await page.evaluate("""() => [...document.querySelectorAll('.page')].map((p, i) => {
            const c = p.querySelector('.content'); const f = p.querySelector('.pagefoot');
            if (!c || !f) return null;
            const over = c.getBoundingClientRect().bottom - f.getBoundingClientRect().top;
            return over > 0 ? `page ${i + 2}: content overflows the footer by ${Math.round(over)} px` : null;
        }).filter(Boolean)""")

        if png_dir:
            os.makedirs(png_dir, exist_ok=True)
            nodes = await page.query_selector_all(sheets)
            for i, node in enumerate(nodes, 1):
                await node.screenshot(path=os.path.join(png_dir, f"p{i:02d}.png"))
            print(f"{len(nodes)} PNG -> {png_dir}")

        await page.pdf(path=out, width=f"{W}px", height=f"{H}px", print_background=True,
                       margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}, prefer_css_page_size=True)
        await browser.close()

    n = fix_jpeg_colortransform(out)
    print(f"PDF -> {out}  ({n_pages} pages" + (f", {n} JPEG colour flags repaired" if n else "") + ")")
    print(font_report(weights))
    for line in overflow:
        print("warning:", line)


def main():
    args = list(sys.argv[1:])
    if not args:
        print(__doc__)
        sys.exit(1)
    png_dir, size, sheets = None, None, ".cover, .page"
    if "--size" in args:
        i = args.index("--size"); m = re.match(r"^(\d+)x(\d+)$", args[i + 1]); size = (int(m.group(1)), int(m.group(2))); del args[i:i + 2]
    if "--sheets" in args:
        i = args.index("--sheets"); sheets = args[i + 1]; del args[i:i + 2]
    if "--png" in args:
        i = args.index("--png")
        png_dir = args[i + 1]
        args = args[:i] + args[i + 2:]
    src = args[0]
    out = args[1] if len(args) > 1 else os.path.splitext(src)[0] + ".pdf"
    asyncio.run(run(src, out, png_dir, size, sheets))


if __name__ == "__main__":
    main()
