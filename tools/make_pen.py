#!/usr/bin/env python3
"""Write cooper.pen: the Object system as a Pencil (pen.dev) document, from the same tokens as cooper.css.

    python3 tools/make_pen.py            # -> cooper.pen at the repository root (image fills point into plugins/cooper-brand/assets/)

The document carries the tokens as variables, the pieces of the system as reusable components (the mark, the
wordmark, the running head and the footer, the label, the figures strip, the table, the recommendation) and one
frame per page of the system: the cover, a section page, a part divider, the hero page, the back cover, the deck's
title and content slides, the fact sheet and the meeting note. Open it in Pencil to edit; the CSS stays the source
the builders use, the .pen is the source a designer edits. Paths are relative to the .pen file.
"""
import json, pathlib, itertools

_R = pathlib.Path(__file__).resolve().parents[1]
OUT = _R / "cooper.pen"
A = "./plugins/cooper-brand/assets"      # relative to the .pen
_ids = itertools.count(1)


def nid(prefix="n"):
    return f"{prefix}{next(_ids)}"


# ---------------------------------------------------------------- tokens
VARS = {
    "paper": {"type": "color", "value": "#F5F5F5"}, "card": {"type": "color", "value": "#FFFFFF"}, "ink": {"type": "color", "value": "#1E1E1E"},
    "ink-soft": {"type": "color", "value": "#383838"}, "muted": {"type": "color", "value": "#848484"}, "line": {"type": "color", "value": "#DDDDDD"},
    "hair": {"type": "color", "value": "#EBEBEB"}, "accent": {"type": "color", "value": "#FF9E42"}, "white": {"type": "color", "value": "#FAFAFA"},
    "display": {"type": "string", "value": "PP Eiko"}, "sans": {"type": "string", "value": "Roboto Condensed"},
    "margin": {"type": "number", "value": 72}, "measure": {"type": "number", "value": 650}, "column": {"type": "number", "value": 200}, "gap": {"type": "number", "value": 36},
}

EI = {"fontFamily": "$display", "fontWeight": "500"}
RC = {"fontFamily": "$sans", "fontWeight": "400"}
LAB = {"fontFamily": "$sans", "fontWeight": "500", "fontSize": 7.5, "letterSpacing": 0.75, "lineHeight": 1.3, "fill": "$muted"}
MARK_D = "M302.863 66.6665V233.333H66.667V66.6665H302.863ZM255.901 78.8638C216.608 78.8638 184.765 110.707 184.765 150C184.765 189.293 216.608 221.136 255.901 221.136H291.835V78.8638H255.901Z"
MARK_VB = [66.667, 66.6665, 236.196, 166.6665]


def text(name, content, size, style, fill="$ink", width=None, **kw):
    t = {"type": "text", "id": nid("t"), "name": name, "content": content, "fontSize": size, "fill": fill, **style, **kw}
    if width is not None:
        t["textGrowth"] = "fixed-width"; t["width"] = width
    return t


def label(name, content, fill="$muted", width=None, **kw):
    return text(name, content.upper(), 7.5, {**LAB, "fill": fill}, fill=fill, width=width, **kw)


def frame(name, children=None, layout="vertical", **kw):
    f = {"type": "frame", "id": nid("f"), "name": name, "layout": layout, **kw}
    if children:
        f["children"] = children
    return f


def rule(name, color="$ink", h=1, width="fill_container"):
    return {"type": "rectangle", "id": nid("r"), "name": name, "width": width, "height": h, "fill": color}


def mark(h=8.5, fill="$ink", name="Mark"):
    return {"type": "path", "id": nid("p"), "name": name, "geometry": MARK_D, "viewBox": MARK_VB, "width": round(h * 236.196 / 166.6665, 2), "height": h, "fill": fill}


def image(name, url, w, h, **kw):
    return {"type": "frame", "id": nid("i"), "name": name, "width": w, "height": h, "fill": {"type": "image", "url": url, "mode": "fill"}, "layout": "none", **kw}


def pair(k, v, kw_width=None):
    return frame(k, [label(k, k), text(v, v, 8.5, RC, lineHeight=1.3)], layout="horizontal", gap=6, alignItems="center")


# ---------------------------------------------------------------- components
C = {}


def component(node):
    node["reusable"] = True
    C[node["name"]] = node["id"]
    return node


def wordmark(h=18, fill="$ink"):
    return component(frame("Wordmark", [mark(h * 0.706, fill), text("Cooper Labs", "Cooper Labs", h, EI, fill=fill, lineHeight=1, letterSpacing=-0.36)], layout="horizontal", gap=8, alignItems="center"))


def running_head():
    return component(frame("Running head", [
        frame("Left", [mark(8.5), label("Kicker", "Proposal · Parallel MCP server · Confidential · v0.1")], layout="horizontal", gap=10, alignItems="center"),
        label("Folio", "03")], layout="horizontal", justifyContent="space_between", alignItems="center", width="$measure"))


def footer():
    return component(frame("Footer", [label("Meta", "Cooper Labs · Internal · Not for distribution"), label("Page", "03 / 24")],
                           layout="horizontal", justifyContent="space_between", alignItems="center", width="$measure"))


def figure(n="6", k="Weeks, brief to release"):
    return component(frame("Figure", [text("Number", n, 40, EI, lineHeight=0.9, letterSpacing=-1.6), label("Key", k, width="fill_container")], layout="vertical", gap=10, width="fill_container"))


def figures_strip(items):
    return frame("Figures", [rule("Rule top"), frame("Row", [{"type": "ref", "id": nid("g"), "ref": C["Figure"], "name": f"Figure {n}", "width": "fill_container",
                                                                  "descendants": {C["Figure/Number"]: {"content": n}, C["Figure/Key"]: {"content": k.upper()}}} for n, k in items],
                                                  layout="horizontal", gap=24, padding=[16, 0], width="fill_container"), rule("Rule bottom", "$hair")],
                 layout="vertical", width="fill_container")


def table(cols, rows, widths):
    def cell(txt, w, style, fill):
        c = text(txt, txt, style[0], style[1], fill=fill, lineHeight=1.4)
        if w == "fill":
            c["textGrowth"] = "fixed-width"; c["width"] = "fill_container"
        else:
            c["textGrowth"] = "fixed-width"; c["width"] = w
        return c
    head = frame("Head", [cell(c.upper(), w, (7.5, LAB), "$muted") for c, w in zip(cols, widths)], layout="horizontal", gap=12, padding=[0, 12, 8, 0], width="fill_container")
    out = [head, rule("Head rule")]
    for i, r in enumerate(rows):
        out.append(frame(f"Row {i + 1}", [cell(v, w, (10, {**RC, "fontWeight": "500" if j == 0 else "400"}), "$ink") for j, (v, w) in enumerate(zip(r, widths))],
                         layout="horizontal", gap=12, padding=[8, 12, 8, 0], width="fill_container"))
        out.append(rule(f"Rule {i + 1}", "$hair"))
    return frame("Table", out, layout="vertical", width="fill_container")


def block(tag, main_children, source=None, specimen=None, caption=None, span=False):
    margin = []
    if specimen:
        margin.append(image("Specimen", specimen, 140, 140))
        if caption:
            margin.append(text("Caption", caption, 8, RC, fill="$muted", width=140, lineHeight=1.45))
    if tag:
        margin.append(label("Tag", tag, width=140))
    if source:
        margin.append(text("Source", source, 8, RC, fill="$muted", width=140, lineHeight=1.45))
    main = frame("Main", main_children, layout="vertical", width="fill_container")
    if span or not margin:
        return frame(tag or "Block", [main], layout="horizontal", width="fill_container")
    return frame(tag, [frame("Margin", margin, layout="vertical", gap=8, width="$column", padding=[0, 32, 0, 0]), main], layout="horizontal", width="fill_container", alignItems="start")


def heading(t, suffix=None, size=24):
    return text("Heading", t + (f" {suffix}" if suffix else ""), size, EI, lineHeight=1.05, letterSpacing=-size * 0.03, width=420)


def body(t, width=400, size=11):
    return text("Body", t, size, RC, lineHeight=1.6, width=width)


def bullets(items):
    return frame("Bullets", [frame(t, [text("Term", t, 13, EI, lineHeight=1.1, letterSpacing=-0.26, width="fill_container"), text("Text", x, 9.5, RC, fill="$ink-soft", lineHeight=1.5, width="fill_container")],
                                   layout="vertical", gap=6, width="fill_container") for t, x in items], layout="horizontal", gap=24, width="fill_container")


def reco(t, b):
    return frame("Recommendation", [text("Title", t, 18, EI, lineHeight=1.1, letterSpacing=-0.45, width=400), text("Body", b, 10, RC, fill="$ink-soft", lineHeight=1.5, width=400)], layout="vertical", gap=8)


# ---------------------------------------------------------------- pages
def page(name, children, x, y, w=794, h=1123, fill="$card"):
    return frame(name, children, layout="none", x=x, y=y, width=w, height=h, fill=fill, clip=True)


def at(node, x, y, **kw):
    node["x"] = x; node["y"] = y; node.update(kw)
    return node


def ref(name, x, y, **kw):
    return {"type": "ref", "id": nid("g"), "ref": C[name], "name": name, "x": x, "y": y, **kw}


def cover(x, y):
    meta = frame("Meta", [pair("Date", "14 September 2026"), pair("Classification", "Confidential"), pair("Status", "Draft"), pair("Owner", "Jean, Cooper Labs")], layout="horizontal", gap=24, alignItems="center")
    return page("Doc · Cover", [
        at(image("Plate", f"{A}/img/renders/01.jpg", 794, 620), 0, 0),
        at(frame("Top", [ref("Wordmark", 0, 0), label("Conf", "Confidential · v0.1", fill="$ink")], layout="horizontal", justifyContent="space_between", alignItems="center", width="$measure"), 72, 56),
        at(frame("Title block", [label("Kicker", "Proposal · Parallel MCP server"), text("Title", "Ship the MCP Server Before the CLI.", 46, EI, lineHeight=1, letterSpacing=-1.84, width=500),
                                 text("Standfirst", "Proposes a six-week build of an MCP server that exposes Parallel's positions, rates and governance to AI agents, read-only, for a start on 28 September 2026.", 11, RC, fill="$ink-soft", lineHeight=1.55, width=360)],
                 layout="vertical", gap=0, width="$measure"), 72, 684),
        at(frame("Bottom", [meta, label("Notice", "Internal document · Not for distribution outside Cooper Labs")], layout="vertical", gap=12), 72, 1010)], x, y)


def summary_page(x, y):
    content = frame("Content", [
        block("Summary", [heading("One Server, Every Agent.", "(six weeks)"), body("Agents already answer questions about Parallel from stale documentation and guessed numbers. An MCP server gives every assistant the same read-only view of the protocol: positions, rates, backing and governance, straight from the chain and the indexer. It holds no keys, signs nothing, and ships in six weeks. The CLI the team asked for is a thin client of the same server, and comes after.")],
              specimen=f"{A}/img/renders/03.jpg", caption="Fig. 1 · The block, rendered. From the Brand Identity file."),
        block(None, [figures_strip([("6", "Weeks, brief to release"), ("7", "Tools, read-only"), ("3", "Chains covered"), ("0", "Keys held")])], span=True),
        block("Assessment", [heading("What Exists, What Is Missing"), table(["Area", "Today", "Gap"], [["Protocol data", "Subgraph and a REST indexer, per chain", "No single entry point"], ["Documentation", "Public docs site, versioned", "Not machine-readable"], ["Governance", "Snapshot and the forum", "Tallies only via the UI"], ["Agents", "Ad-hoc prompts with pasted numbers", "No source of truth"]], [110, "fill", 140])],
              source="Reviewed with the Parallel protocol team on 10 Sep 2026."),
        block("Risks & mitigants", [bullets([("Stale data", "Every answer carries the block number and the age of the indexer; past 300 s the tool says so."), ("Misuse as advice", "Read-only tools, a fixed disclaimer in every schema, no rates projected forward."), ("Maintenance", "The server is generated from the tool schemas; a new protocol module is one file.")])]),
        block("Recommendation", [reco("Build the server first, read-only, and derive the CLI from it in week five.", "Start on 28 September; a public beta on 6 November, announced with the Seventeenth Parallel Report.")])],
        layout="vertical", gap="$gap", width="$measure")
    # the heading + body stack inside Main gets its gaps from a vertical Main with gap 16
    for b in content["children"]:
        for m in b["children"]:
            if m["name"] == "Main":
                m["gap"] = 16
    return page("Doc · Section page", [ref("Running head", 72, 48), at(content, 72, 104), ref("Footer", 72, 1123 - 44 - 10)], x, y)


def divider(x, y):
    lst = frame("List", [pair("Sections", "Options · Plan · Method"), pair("Pages", "10 to 16"), pair("Estimate", "12 Sep 2026, one designer and one engineer"), pair("Phase gate", "16 October")], layout="vertical", gap=6, width=200)
    return page("Doc · Divider", [
        at(image("Plate", f"{A}/img/renders/04.jpg", 794, 700), 0, 0),
        at(frame("Title block", [label("Kicker", "Part two · The build"), text("Title", "Six Weeks, Six Demos.", 40, EI, lineHeight=1, letterSpacing=-1.6, width=380),
                                 text("Standfirst", "The four options, the one recommended, the plan by week, and how the work runs from Monday to Friday.", 11, RC, fill="$ink-soft", lineHeight=1.55, width=320)], layout="vertical", gap=16, width=380), 72, 900),
        at(lst, 522, 960),
        ref("Footer", 72, 1123 - 44 - 10)], x, y)


def hero(x, y):
    return page("Doc · Hero figure", [
        ref("Running head", 72, 48),
        at(image("Plate", f"{A}/img/renders/06.jpg", 650, 406), 72, 104),
        at(text("Caption", "Fig. 2 · The block, dithered. Six weeks from the brief to the public beta.", 8, RC, fill="$muted", lineHeight=1.45, width=650), 72, 520),
        at(frame("Number", [text("N", "6", 96, EI, lineHeight=0.85, letterSpacing=-4.8), text("Unit", "weeks", 22, {**RC, "fontWeight": "300"}, lineHeight=1)], layout="horizontal", gap=8, alignItems="end"), 68, 596),
        at(label("Kicker", "From the brief to the public beta", width=150), 72, 700),
        at(body("Six weeks, six Friday demos. The server answers on Base at the end of week one and on three chains at the end of week two; the CLI is derived from it in week five and the public beta ships with the Seventeenth Parallel Report on 6 November."), 272, 596),
        at(figures_strip([("6", "Demos"), ("3", "Chains"), ("2", "Phases")]), 72, 760, width=650),
        ref("Footer", 72, 1123 - 44 - 10)], x, y)


def back(x, y):
    links = frame("Colophon", [pair("Website", "cooperlabs.xyz"), pair("X", "@cooperlabs"), pair("Telegram", "@jeanbrasse"), pair("This document", "Proposal · v0.1 · 14 Sep 2026")], layout="horizontal", gap=24, alignItems="center")
    return page("Doc · Back cover", [
        at(image("Plate", f"{A}/img/renders/05.jpg", 794, 620), 0, 0),
        at(frame("Top", [ref("Wordmark", 0, 0), label("Conf", "Confidential · v0.1", fill="$ink")], layout="horizontal", justifyContent="space_between", alignItems="center", width="$measure"), 72, 56),
        at(frame("Bottom", [text("Tagline", "We turn Web3 ideas into products people use.", 40, EI, lineHeight=1, letterSpacing=-1.6, width=380), links, label("Notice", "Internal document · Not for distribution outside Cooper Labs · © 2026 Cooper Labs")], layout="vertical", gap=16), 72, 880)], x, y)


def deck_title(x, y):
    return page("Deck · Title", [
        at(image("Plate", f"{A}/img/renders/01.jpg", 640, 720), 0, 0),
        at(frame("Top", [ref("Wordmark", 0, 0, descendants={}), label("Conf", "Confidential · v0.1", fill="$ink", fontSize=11)], layout="horizontal", justifyContent="space_between", alignItems="center", width=1120), 80, 56),
        at(frame("Title block", [label("Kicker", "Proposal · Parallel MCP server · Parallel team, 14 September 2026", fontSize=11), text("Title", "Ship the MCP Server Before the CLI.", 56, EI, lineHeight=1, letterSpacing=-2.24, width=480),
                                 text("Standfirst", "Proposes a six-week, read-only MCP server for Parallel's positions, rates and governance, for a start on 28 September.", 15, RC, fill="$ink-soft", lineHeight=1.5, width=400)], layout="vertical", gap=22, width=480), 720, 150),
        at(frame("Meta", [pair("Date", "14 September 2026"), pair("Classification", "Confidential"), pair("Status", "Draft"), pair("Owner", "Jean, Cooper Labs")], layout="vertical", gap=10), 720, 560)], x, y, 1280, 720)


def deck_content(x, y):
    main = frame("Main", [heading("One Server, Every Agent.", "(six weeks)", 40), body("Agents already answer questions about Parallel from stale documentation. An MCP server gives every assistant the same read-only view of the protocol, straight from the chain and the indexer. It holds no keys, signs nothing, and the CLI the team asked for is a thin client of it.", 680, 17),
                          figures_strip([("6", "Weeks, brief to release"), ("7", "Tools, read-only"), ("3", "Chains covered"), ("0", "Keys held")])], layout="vertical", gap=24, width="fill_container")
    main["children"][0]["width"] = 760
    grid = frame("Grid", [frame("Margin", [label("Tag", "Summary", fontSize=11, letterSpacing=1.1)], layout="vertical", width=320, padding=[0, 48, 0, 0]), main], layout="horizontal", width=1120, alignItems="start")
    return page("Deck · Content slide", [
        at(frame("Head", [frame("Left", [mark(12.7), label("Kicker", "Proposal · Parallel MCP server · Confidential · v0.1", fontSize=11, letterSpacing=1.1)], layout="horizontal", gap=14, alignItems="center"), label("Folio", "02", fontSize=11)], layout="horizontal", justifyContent="space_between", alignItems="center", width=1120), 80, 56),
        at(grid, 80, 130),
        at(frame("Foot", [label("Meta", "Cooper Labs · Internal · Not for distribution", fontSize=11, letterSpacing=1.1), label("Page", "02 / 07", fontSize=11)], layout="horizontal", justifyContent="space_between", width=1120), 80, 720 - 48 - 12)], x, y, 1280, 720)


def fact_sheet(x, y):
    cols = frame("Columns", [frame(h, [text("Heading", h, 18, EI, lineHeight=1.05, letterSpacing=-0.5), frame("List", [frame(t, [text("Term", t, 10.5, {**RC, "fontWeight": "500"}, lineHeight=1.4), text("Text", d, 9.5, RC, fill="$ink-soft", lineHeight=1.5, width="fill_container")], layout="vertical", gap=2, width="fill_container", padding=[7, 0]) for t, d in items], layout="vertical", width="fill_container")],
                                   layout="vertical", gap=12, width="fill_container") for h, items in [("How We Work", [("One team, both crafts", "A designer and an engineer on every project from day one; the design system lives in Figma and in code."), ("Working software on Friday", "Thirty minutes, the client in the room, the decisions written the same day."), ("Phases with a gate", "Two or three fixed-price phases; the next one starts on a demo, not on a plan.")]),
                                                                                                        ("What We Don't Do", [("No custody, no keys", "We build the product; the user signs. Nothing we ship holds funds."), ("No slides for software", "A proposal names its demos; a demo shows the thing running."), ("No open-ended retainers", "Scope, price and dates per phase, written before the first week.")])]],
                 layout="horizontal", gap=32, width=650)
    contact = frame("Contact", [rule("Rule"), frame("Row", [frame(k, [label(k, k), text(v, v, 10, RC, lineHeight=1.3)], layout="vertical", gap=6, width="fill_container") for k, v in [("Website", "cooperlabs.xyz"), ("X", "@cooperlabs"), ("Telegram", "@jeanbrasse"), ("Email", "contact@cooperlabs.xyz")]], layout="horizontal", gap=24, padding=[12, 0, 0, 0], width="fill_container")], layout="vertical", width=650)
    return page("Fact sheet", [
        at(frame("Head", [ref("Wordmark", 0, 0), label("Kicker", "Fact sheet · Cooper Labs · September 2026")], layout="horizontal", justifyContent="space_between", alignItems="center", width=650), 72, 48),
        at(frame("Stack", [image("Plate", f"{A}/img/renders/01.jpg", 650, 180),
                           frame("Title block", [label("Tag", "Cooper Labs · Fact sheet"), text("Title", "We Turn Web3 Ideas into Products People Use.", 34, EI, lineHeight=1, letterSpacing=-1.36, width=480),
                                                 text("Standfirst", "Cooper Labs is a product studio for Web3 teams: design and engineering in one team, from the brief to the stores, with a demo of working software every Friday.", 10.5, RC, fill="$ink-soft", lineHeight=1.55, width=400)], layout="vertical", gap=12),
                           figures_strip([("6", "Weeks, brief to first release"), ("Weekly", "Demo, every Friday"), ("2", "Disciplines, one team"), ("Fixed", "Price per phase")]), cols, contact], layout="vertical", gap=22, width=650), 72, 96),
        at(frame("Foot", [label("Meta", "Cooper Labs · Public · cooperlabs.xyz · September 2026"), label("Page", "01 / 01")], layout="horizontal", justifyContent="space_between", width=650), 72, 1123 - 44 - 10)], x, y)


def note(x, y):
    facts = frame("Facts", [frame(k, [label(k, k), text(v, v, 9.5, RC, lineHeight=1.45, width=140)], layout="vertical", gap=4) for k, v in [("Date", "12 September 2026"), ("Where", "Google Meet"), ("Attendees", "Jean, Cooper Labs\nNicolas, Design\nNoah, Parallel\nLéa, Parallel"), ("Note by", "Jean, Cooper Labs")]], layout="vertical", gap=14, width=200, padding=[0, 32, 0, 0])
    decisions = frame("Decisions", [rule("Rule")] + sum([[frame(t, [text("N", f"{i:02d}", 13, EI, lineHeight=1.2, width=40), frame("Text", [text("Title", t, 11, {**RC, "fontWeight": "500"}, lineHeight=1.4, width="fill_container"), text("Body", d, 10, RC, fill="$ink-soft", lineHeight=1.5, width="fill_container")], layout="vertical", gap=2, width="fill_container")], layout="horizontal", padding=[10, 0], width="fill_container", alignItems="start"), rule(f"Rule {i}", "$hair")] for i, (t, d) in enumerate([("Server first, CLI in week six", "The CLI is derived from the server one week later than planned; the docs dry run takes the week. The beta date does not move."), ("Two renames", "get_rate becomes get_rates, get_backing_ratio becomes get_backing. Done before the next demo."), ("Staleness rule", "Past 300 seconds an answer says its age in the first line, not in a footnote.")], 1)], []), layout="vertical", width="fill_container")
    content = frame("Content", [block("Context", [body("Second weekly of the build. The Friday demo showed the server answering on Base, Arbitrum and Ethereum with one schema per tool; the Parallel team had read the schemas cold the day before.")]),
                                block("Decisions", [decisions]),
                                block("Actions", [table(["Action", "Owner", "Due"], [["Rename the two tools and regenerate the docs", "Jean", "16 Sep"], ["Confirm the disclaimer wording with legal", "Noah", "19 Sep"], ["Send the three-chain demo recording to the DAO channel", "Léa", "13 Sep"], ["Draft the October plan for the report", "Jean", "26 Sep"]], ["fill", 110, 70])]),
                                block("Next", [body("Week 38 adds the governance tools; the demo runs the same three questions on the three chains."), frame("Next meeting", [rule("Rule"), frame("Pair", [label("K", "Next meeting"), text("V", "19 September 2026, 10:00, Google Meet", 10.5, RC, lineHeight=1.4)], layout="horizontal", gap=8, alignItems="center", padding=[12, 0, 0, 0])], layout="vertical", width=400)])],
                    layout="vertical", gap="$gap", width=650)
    for b in content["children"]:
        for m in b["children"]:
            if m["name"] == "Main":
                m["gap"] = 14
    return page("Meeting note", [
        at(frame("Head", [ref("Wordmark", 0, 0), label("Kicker", "Meeting note · Parallel weekly · 12 September 2026")], layout="horizontal", justifyContent="space_between", alignItems="center", width=650), 72, 48),
        at(frame("Note head", [facts, frame("Title", [label("Tag", "Meeting note · Internal"), text("Title", "Week 37: The Server Answers on Three Chains", 30, EI, lineHeight=1.02, letterSpacing=-1.05, width=420)], layout="vertical", gap=14, width="fill_container")], layout="horizontal", width=650, alignItems="start"), 72, 104),
        at(content, 72, 330),
        at(frame("Foot", [label("Meta", "Cooper Labs · Internal · Not for distribution"), label("Page", "01 / 01")], layout="horizontal", justifyContent="space_between", width=650), 72, 1123 - 44 - 10)], x, y)


# ---------------------------------------------------------------- the document
def main():
    comps = frame("Components", [wordmark(), running_head(), footer(), figure()], layout="vertical", gap=32, padding=48, x=0, y=-400, fill="$paper")
    # the ids of the figure's children, for the strip's overrides
    fig = comps["children"][3]
    C["Figure/Number"] = fig["children"][0]["id"]; C["Figure/Key"] = fig["children"][1]["id"]
    pages = [cover(0, 0), summary_page(894, 0), divider(1788, 0), hero(2682, 0), back(3576, 0),
             deck_title(0, 1300), deck_content(1380, 1300), fact_sheet(0, 2200), note(894, 2200)]
    doc = {"version": "2.17", "variables": VARS, "children": [comps] + pages}
    OUT.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("->", OUT, f"{OUT.stat().st_size // 1024} KB, {len(pages)} pages, {len(C)} components")


if __name__ == "__main__":
    main()
