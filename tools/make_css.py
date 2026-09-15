"""Assemble cooper.css: fonts and tokens, the document design (doc.css), the social section transcribed from Figma (social.css)."""
import pathlib

HERE = pathlib.Path(__file__).resolve().parent

head = '''/* Cooper Labs · documents and social
   The engine of parallel-brand with the Cooper Labs identity. Documents: the OBJECT system (the block is an object, the
   document is its catalogue: the renders as plates, small precise type, wide margins, a 200 px margin column, hairlines).
   Social: the Figma file Brand Identity, page Twitter, transcribed. A4 at 96 dpi: 794 x 1123. Margins 72 (sides),
   48 (top), 44 (bottom). Measure 650. There is no cooper.pen yet (see CHANGELOG). */

/* ---------- fonts ---------- */
/* PP Eiko is the display face (Pangram Pangram, commercial): used from the machine when installed, or from
   assets/fonts/private/ when the licensee has dropped the files there (private copies of the plugin only).
   Medium (500) is the brand weight, the one every document and card uses; Thin, Light Italic, Heavy and Black
   Italic are declared for the designer's use. Otherwise "Display Fallback" (Instrument Serif, OFL) stands in.
   Roboto Condensed (OFL) is the text face and the label face; there is no mono in this identity. */
@font-face{font-family:"PP Eiko";src:local("PP Eiko Medium"),local("PPEiko-Medium"),url("../fonts/private/pp-eiko-500.woff2") format("woff2");font-weight:500;font-style:normal}
@font-face{font-family:"PP Eiko";src:local("PP Eiko Thin"),local("PPEiko-Thin"),url("../fonts/private/pp-eiko-100.woff2") format("woff2");font-weight:100;font-style:normal}
@font-face{font-family:"PP Eiko";src:local("PP Eiko Heavy"),local("PPEiko-Heavy"),url("../fonts/private/pp-eiko-800.woff2") format("woff2");font-weight:800;font-style:normal}
@font-face{font-family:"PP Eiko";src:local("PP Eiko Light Italic"),local("PPEiko-LightItalic"),url("../fonts/private/pp-eiko-300-italic.woff2") format("woff2");font-weight:300;font-style:italic}
@font-face{font-family:"PP Eiko";src:local("PP Eiko Black Italic"),local("PPEiko-BlackItalic"),url("../fonts/private/pp-eiko-900-italic.woff2") format("woff2");font-weight:900;font-style:italic}
@font-face{font-family:"Display Fallback";src:url("../fonts/instrument-serif-latin-400-normal.woff2") format("woff2");font-weight:400 500;font-style:normal}
@font-face{font-family:"Roboto Condensed";src:url("../fonts/roboto-condensed-latin-wght-normal.woff2") format("woff2");font-weight:100 900;font-style:normal}
@font-face{font-family:"Roboto Condensed";src:url("../fonts/roboto-condensed-latin-wght-italic.woff2") format("woff2");font-weight:100 900;font-style:italic}

/* ---------- tokens ---------- */
:root{
  --paper:#F5F5F5;          /* page (cooperlabs.xyz) */
  --white:#FAFAFA;          /* type on dark */
  --card:#FFFFFF;           /* the cards, and the social cards' ground, as in the Figma file */
  --black:#000000;          /* type on the social cards, as in the Figma file */
  --ink:#1E1E1E;            /* primary text, the dark ground, the dark cards */
  --ink-soft:#383838;       /* secondary text */
  --muted:#848484;          /* labels, meta, sources */
  --line:#DDDDDD;           /* the hairline on paper (footer) */
  --hair:#EBEBEB;           /* the hairline inside a card */
  --line-inv:rgba(250,250,250,.16); /* hairline on dark */
  --paper-72:rgba(250,250,250,.72);
  --accent:#FF9E42;         /* the orange: the dash, the accent phrase, the hot cell */
  --accent-deep:#C77012;    /* orange text at small sizes on paper */
  --accent-soft:#FFB261;    /* orange on dark */
  --tint:rgba(255,158,66,.14); /* one highlighted table row */
  --shadow:0 1px 8px rgba(0,0,0,.06); /* the cards' shadow, as on the site */
  --grey-1:#4B4B4B;--grey-2:#5E5E5E;--grey-3:#727272;--grey-4:#868686;--grey-5:#9B9B9B;--grey-6:#B0B0B0;--grey-7:#C6C6C6;--grey-8:#DDDDDD;--grey-9:#F3F3F3;
  --orange-1:#FFE29C;--orange-2:#FFCA7E;--orange-3:#FFB261;--orange-4:#FF9E42;--orange-5:#C77012;--orange-6:#AF5D00;--orange-7:#954A00;--orange-8:#7C3800;--orange-9:#632800;
  --display:"PP Eiko","Display Fallback",serif;
  --sans:"Roboto Condensed",sans-serif;
  --label:"Roboto Condensed",sans-serif;
  --w:794px; --h:1123px;
}

*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{font-family:var(--sans);color:var(--ink);-webkit-font-smoothing:antialiased;-webkit-print-color-adjust:exact;print-color-adjust:exact}
@page{size:794px 1123px;margin:0}

'''

doc = (HERE / 'doc.css').read_text(encoding='utf-8')
social = (HERE / 'social.css').read_text(encoding='utf-8')
_R = HERE.parent
out = (_R / 'plugins' / 'cooper-brand' if (_R / 'plugins' / 'cooper-brand').exists() else _R / 'plugin') / 'assets' / 'css' / 'cooper.css'   # the marketplace repo, or the scratch tree
# social before the documents: `.canvas` must not override `.canvas--deck` and `.deck--back`
out.write_text(head + social.rstrip() + '\n\n' + doc.rstrip() + '\n', encoding='utf-8')
print('->', out.resolve(), sum(1 for _ in open(out)), 'lines')
