#!/usr/bin/env python3
"""Render a social canvas as a short MP4: the animated card.

    python3 render_anim.py posts.html out/ --only blog-mcp-article          # out/blog-mcp-article.mp4, 4 s
    python3 render_anim.py posts.html out/ --only "thread-*" --seconds 5 --fps 30
    python3 render_anim.py posts.html out/ --only blog-mcp-article --gif    # a GIF next to the MP4 (bigger, for chats)

Four seconds by default: a slow zoom out on the render (1.08 to 1), the
grain drifting, then the symbol, the category, the title and the subtitle
fading in one after the other, 0.25 s apart, each rising 14 px. The same
sequence applies to every kind of card (the text children fade in in their
order). Frames are screenshots taken by Playwright at each 1/fps, assembled by
ffmpeg (H.264, yuv420p, even dimensions, so X and LinkedIn accept it).

Needs Playwright with Chromium and ffmpeg on the PATH. `--only` takes a glob,
repeatable; `--scale 2` doubles the pixel size (slower).
"""
import sys, os, re, fnmatch, pathlib, asyncio, shutil, subprocess, tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from fontcheck import JS_WEIGHTS, font_report          # noqa: E402

# Runs once per canvas: prepares the layers and returns a setter; the page keeps it on window.__setT
JS_PREPARE = """(el) => {
  const bg = el.querySelector('.canvas__bg'); const noise = el.querySelector('.canvas__noise');
  const items = [];
  const icon = null;
  for (const sel of ['.post > *', '.post__logo', '.xcover__line', '.xcover__logo', '.partner > *', '.preview__logo', '.thread > *', '.banner > *']) el.querySelectorAll(sel).forEach(n => { if (!items.includes(n)) items.push(n); });
  const base = items.map(n => getComputedStyle(n).transform);
  if (bg) { bg.style.transformOrigin = 'center'; bg.style.willChange = 'transform'; }
  items.forEach(n => { n.style.willChange = 'transform, opacity'; });
  const ease = t => t < 0 ? 0 : t > 1 ? 1 : 1 - Math.pow(1 - t, 3);
  window.__setT = (t, total) => {
    if (bg) bg.style.transform = 'scale(' + (1.08 - 0.08 * Math.min(t / total, 1)) + ')';
    if (noise) noise.style.backgroundPosition = (Math.floor(t * 30) % 7 * 13) + 'px ' + (Math.floor(t * 30) % 5 * 17) + 'px';
    items.forEach((n, i) => {
      const k = ease((t - (0.2 + 0.25 * i)) / 0.8);
      n.style.opacity = k;
      const b = base[i] === 'none' ? '' : base[i] + ' ';
      n.style.transform = b + 'translateY(' + (14 * (1 - k)).toFixed(2) + 'px)';
    });
  };
  return items.length;
}"""


async def run(src, outdir, only, seconds, fps, scale, gif):
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        sys.exit("playwright is required:  pip install playwright  &&  playwright install chromium")
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg is required on the PATH (apt install ffmpeg / brew install ffmpeg)")
    os.makedirs(outdir, exist_ok=True)
    frames_n = int(round(seconds * fps))
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 2600, "height": 2000}, device_scale_factor=scale)
        await page.goto(pathlib.Path(src).resolve().as_uri(), wait_until="networkidle")
        await page.evaluate("document.fonts.ready")
        await page.wait_for_timeout(400)
        weights = await page.evaluate(JS_WEIGHTS)
        done = 0
        for node in await page.query_selector_all(".canvas"):
            name = await node.get_attribute("data-name") or f"canvas-{done + 1}"
            if only and not any(fnmatch.fnmatch(name, pat) for pat in only):
                continue
            n_items = await node.evaluate(JS_PREPARE)
            tmp = tempfile.mkdtemp(prefix="anim-")
            for i in range(frames_n):
                await page.evaluate("([t, total]) => window.__setT(t, total)", [i / fps, seconds])
                await node.screenshot(path=os.path.join(tmp, f"f{i:04d}.png"))
            mp4 = os.path.join(outdir, f"{name}.mp4")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", os.path.join(tmp, "f%04d.png"),
                            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", mp4], check=True)
            print(f"MP4 -> {mp4}  ({seconds:g} s, {fps} fps, {n_items} elements)")
            if gif:
                g = os.path.join(outdir, f"{name}.gif")
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", os.path.join(tmp, "f%04d.png"),
                                "-vf", "fps=15,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer", g], check=True)
                print(f"GIF -> {g}")
            shutil.rmtree(tmp, ignore_errors=True)
            done += 1
        await browser.close()
    print(font_report(weights))
    if done == 0:
        sys.exit("no canvas matched")


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__); sys.exit(1)
    only, seconds, fps, scale, gif = [], 4.0, 30, 1, False
    while "--only" in args:
        i = args.index("--only"); only.append(args[i + 1]); del args[i:i + 2]
    if "--seconds" in args:
        i = args.index("--seconds"); seconds = float(args[i + 1]); del args[i:i + 2]
    if "--fps" in args:
        i = args.index("--fps"); fps = int(args[i + 1]); del args[i:i + 2]
    if "--scale" in args:
        i = args.index("--scale"); scale = int(args[i + 1]); del args[i:i + 2]
    if "--gif" in args:
        gif = True; args.remove("--gif")
    asyncio.run(run(args[0], args[1], only, seconds, fps, scale, gif))


if __name__ == "__main__":
    main()
