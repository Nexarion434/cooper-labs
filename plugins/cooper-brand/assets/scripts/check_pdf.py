#!/usr/bin/env python3
"""Check a Cooper Labs PDF before it goes out.

    python3 check_pdf.py doc.pdf [more.pdf ...]
    python3 check_pdf.py doc.pdf --html doc.html      # also check the source it was rendered from
    python3 check_pdf.py deck.pdf --html deck.html --size 1280x720   # a deck: 16:9 pages instead of A4

Exit code 1 on any failure. On the PDF itself:
  1. JPEG colour flags: every DCTDecode image declares the transform that
     matches its data, so covers do not turn magenta in strict readers.
  2. Page size: every page is A4 (595.3 x 841.9 pt, 794 x 1123 px), or the
     `--size` given in px (a deck is 1280 x 720).
  3. Copy hygiene in the text layer (pdftotext or pypdf when available):
     no em dash, no "lorem", no unfilled "vX.X" / "DD MONTH"; "TBD" is reported
     as a note.
With the source HTML (`--html`, or `<name>.html` found next to the PDF):
  4. The version string is the same on the cover, in every running head, on
     the back cover, and in the PDF file name (`...-vX.Y.pdf`).
  5. Page numbers: every sheet counts (cover, contents, pages, back cover;
     title, slides, closing for a deck); the running head number and the
     `NN / NN` footer agree, the numbers are consecutive from 02 with no
     repeat or gap, and NN is the sheet count.
  6. The Contents page: every entry points to a page that carries the matching
     section tag (rows written by build_doc.py carry `data-tag`; hand-written
     rows are matched on their label).
"""
import sys, re, struct, pathlib, zlib, html, shutil, subprocess


# ---------------------------------------------------------------- PDF bytes
def jpeg_components(buf):
    i, n = 2, len(buf)
    while i + 4 <= n and buf[i] == 0xFF:
        marker = buf[i + 1]
        if marker in (0xD8, 0xD9):
            i += 2
            continue
        ln = struct.unpack(">H", buf[i + 2:i + 4])[0]
        seg = buf[i + 4:i + 2 + ln]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3):
            return [seg[6 + 3 * k] for k in range(seg[5])]
        if marker == 0xDA:
            return None
        i += 2 + ln
    return None


def check_colour(data):
    bad = images = 0
    for m in re.finditer(rb"/Subtype\s*/Image(.{0,600}?)stream", data, re.S):
        head = m.group(1)
        if b"DCTDecode" not in head:
            continue
        s = m.end()
        while s < len(data) and data[s] in (0x0D, 0x0A):
            s += 1
        if data[s:s + 2] != b"\xff\xd8":
            continue
        images += 1
        ids = jpeg_components(data[s:s + 4096]) or []
        ct = re.search(rb"/ColorTransform\s+(\d)", head)
        declared_rgb = ct is not None and int(ct.group(1)) == 0
        if len(ids) == 3 and declared_rgb != (ids == [ord("R"), ord("G"), ord("B")]):
            bad += 1
    return images, bad


def check_pages(data):
    sizes = set()
    for m in re.finditer(rb"/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]", data):
        w, h = float(m.group(3)) - float(m.group(1)), float(m.group(4)) - float(m.group(2))
        sizes.add((round(w, 1), round(h, 1)))
    return sizes


def page_count(path, data):
    """Pages in the PDF: pdfinfo, else pypdf, else the root of the page tree (the largest /Count)."""
    if shutil.which("pdfinfo"):
        try:
            m = re.search(r"^Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, timeout=30).stdout, re.M)
            if m:
                return int(m.group(1))
        except Exception:
            pass
    try:
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            import pypdf
            return len(pypdf.PdfReader(str(path)).pages)
    except Exception:
        pass
    counts = [int(m.group(1)) for m in re.finditer(rb"/Type\s*/Pages\b[^>]*?/Count\s+(\d+)", data, re.S)]
    return max(counts) if counts else len(re.findall(rb"/Type\s*/Page\b", data))


def text_layer(path, data):
    """The text of the PDF: pdftotext, else pypdf, else the literal strings of the content streams."""
    if shutil.which("pdftotext"):
        try:
            return subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True, timeout=60).stdout, "pdftotext"
        except Exception:
            pass
    try:
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            import pypdf
            return "\n".join((p.extract_text() or "") for p in pypdf.PdfReader(str(path)).pages), "pypdf"
    except Exception:
        pass
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", data, re.S):
        chunk = m.group(1)
        try:
            chunk = zlib.decompress(chunk)
        except Exception:
            pass
        out += [t.decode("latin-1", "ignore") for t in re.findall(rb"\((.*?)(?<!\\)\)", chunk)]
    return " ".join(out), "content streams (install poppler or pypdf for a real text layer)"


# ---------------------------------------------------------------- source HTML
def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def check_source(html_path, pdf_path, problems, notes):
    src = pathlib.Path(html_path).read_text(encoding="utf-8")
    deck = 'class="canvas canvas--deck' in src
    if deck:
        sheets = re.findall(r'<section class="canvas canvas--deck[^"]*"', src)
        confs = [strip(x) for x in re.findall(r'<div class="cover__conf"[^>]*>(.*?)</div>', src, re.S)]
        heads_nums = re.findall(r'<div class="deck__head"><span>(.*?)</span><span>(.*?)</span></div>', src, re.S)
        heads = [strip(h) for h, _ in heads_nums]
        nums = [strip(n) for _, n in heads_nums]
        foots = [strip(x) for x in re.findall(r'<div class="deck__foot"><span>.*?</span><span>(.*?)</span></div>', src, re.S)]
        # divider and statement slides carry a footer but no running head: their numbers come from the footer
        nums = [f.split(" / ")[0] for f in foots]
    else:
        sheets = re.findall(r'<section class="(cover|cover back|page)[^"]*"', src)
        confs = [strip(x) for x in re.findall(r'<div class="cover__conf">(.*?)</div>', src, re.S)]
        heads = [strip(x) for x in re.findall(r'<div class="pagehead__meta">(.*?)</div>', src, re.S)]
        nums = [strip(x) for x in re.findall(r'<div class="pagehead__num">(.*?)</div>', src, re.S)]
        foots = [strip(x) for x in re.findall(r'<div class="pagefoot__page">(.*?)</div>', src, re.S)]
    total = len(sheets)
    if not deck and not confs and not nums:          # a sheet format (fact sheet, note, quote): no cover, footers only
        if len(set(heads)) > 1:
            problems.append(f"running heads differ: {sorted(set(heads))}")
        for i, f in enumerate(foots, 1):
            if f != f"{i:02d} / {total:02d}":
                problems.append(f"footer '{f}' should read {i:02d} / {total:02d}")
        return total
    versions = set()
    for s in confs + heads:
        m = re.search(r"\bv\d+\.\d+\b", s)
        versions.add(m.group(0) if m else None)
    if len(set(confs)) > 1:
        problems.append(f"cover and back cover disagree: {sorted(set(confs))}")
    if len(set(heads)) > 1:
        problems.append(f"running heads differ: {sorted(set(heads))}")
    if len(versions) != 1 or None in versions:
        problems.append(f"version string is not the same everywhere: {sorted(str(v) for v in versions)}")
    else:
        v = versions.pop()
        fm = re.search(r"-(v\d+\.\d+)\.pdf$", pathlib.Path(pdf_path).name)
        if not fm:
            problems.append(f"file name should end with -{v}.pdf")
        elif fm.group(1) != v:
            problems.append(f"file name says {fm.group(1)}, the document says {v}")
    # page numbers: every sheet counts, interior pages run from 02
    expected = [f"{i:02d}" for i in range(2, 2 + len(nums))]
    if nums != expected:
        problems.append(f"running head numbers {nums} are not consecutive from 02")
    for n, f in zip(nums, foots):
        m = re.match(r"(\d\d) / (\d\d)$", f)
        if not m:
            problems.append(f"footer '{f}' is not NN / NN")
        elif m.group(1) != n or int(m.group(2)) != total:
            problems.append(f"footer '{f}' disagrees with head {n} or the {total} sheets")
    if len(foots) != len(nums):
        problems.append(f"{len(nums)} running heads but {len(foots)} footers")
    if deck:
        for h, n in heads_nums:                      # a content slide: the head number and the footer number agree
            if strip(n) not in nums:
                problems.append(f"slide head {strip(n)} has no footer")
        return total
    # the Contents page
    pages = re.findall(r'<section class="page(?: page--dark)?">(.*?)</section>', src, re.S)
    tags_by_num = {}
    texts_by_num = {}
    for body in pages:
        n = strip(re.search(r'<div class="pagehead__num">(.*?)</div>', body, re.S).group(1))
        tags_by_num[n] = [strip(t) for t in re.findall(r'<div class="(?:tag|divider__kicker|hero__k|statement__who)">(.*?)</div>', body, re.S)]
        texts_by_num[n] = strip(body)
    for body in pages:
        if '<div class="tag">Contents</div>' not in body:
            continue
        for row in re.findall(r"<tr[^>]*>.*?</tr>", body, re.S):
            cells = [strip(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]
            if len(cells) < 3 or not re.match(r"\d\d$", cells[2]):
                continue
            target = tags_by_num.get(cells[2])
            if target is None:
                problems.append(f"Contents entry '{cells[1]}' points to page {cells[2]}, which does not exist")
                continue
            dt = re.search(r'data-tag="([^"]*)"', row)
            if dt:
                want = html.unescape(dt.group(1))
                if want not in target and want not in texts_by_num.get(cells[2], ""):
                    problems.append(f"Contents entry '{cells[1]}' points to page {cells[2]}, which has no tag '{want}'")
            elif not any(cells[1].lower()[:12] in t.lower() or t.lower() in cells[1].lower() for t in target):
                notes.append(f"Contents entry '{cells[1]}' could not be matched to a tag on page {cells[2]} (tags: {', '.join(target) or 'none'})")
    return total


def check(path, html_path=None, size=None):
    data = pathlib.Path(path).read_bytes()
    problems, notes = [], []
    images, bad = check_colour(data)
    if bad:
        problems.append(f"{bad} of {images} JPEG images declare the wrong colour transform (magenta risk)")
    sizes = check_pages(data)
    ew, eh = (size[0] * 72 / 96, size[1] * 72 / 96) if size else (595.3, 841.9)
    if any(abs(w - ew) > 1.5 or abs(h - eh) > 1.5 for w, h in sizes):
        problems.append(f"page sizes {sorted(sizes)} are not {'A4' if not size else f'{size[0]} x {size[1]} px'} ({ew:.1f} x {eh:.1f} pt)")
    text, how = text_layer(path, data)
    for pat, what in ((r"—", "em dash"), (r"\blorem\b", "lorem text"), (r"\bv[Xx]\.[Xx]\b", "unfilled version"), (r"DD MONTH", "unfilled date")):
        if re.search(pat, text, re.I):
            problems.append(f"{what} found in the text layer ({how})")
    if re.search(r"\bTBD\b", text):
        notes.append("TBD found in the text layer: fine in a versions table, not in a final document")
    if html_path is None:
        cand = pathlib.Path(path).with_suffix(".html")
        html_path = cand if cand.exists() else None
    if html_path:
        total = check_source(html_path, path, problems, notes)
        n = page_count(path, data)
        if n and total and n != total:
            problems.append(f"the PDF has {n} pages, the source has {total} sheets")
    else:
        notes.append("no source HTML given (--html): version, numbering and Contents not checked")
    status = "FAIL" if problems else "ok"
    print(f"{status:4s} {path}  ({images} JPEG image{'s' if images != 1 else ''}, {len(sizes)} page size{'s' if len(sizes) != 1 else ''}, text via {how.split(' ')[0]})")
    for p in problems:
        print("  !", p)
    for p in notes:
        print("  note:", p)
    return len(problems)


def main():
    args = sys.argv[1:]
    html_path, size = None, None
    if "--html" in args:
        i = args.index("--html"); html_path = args[i + 1]; del args[i:i + 2]
    if "--size" in args:
        i = args.index("--size"); m = re.match(r"^(\d+)x(\d+)$", args[i + 1]); size = (int(m.group(1)), int(m.group(2))); del args[i:i + 2]
    if not args:
        print(__doc__); sys.exit(1)
    sys.exit(1 if sum(check(p, html_path, size) for p in args) else 0)


if __name__ == "__main__":
    main()
