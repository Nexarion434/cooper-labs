#!/usr/bin/env python3
"""Write the Cooper Labs descriptions: the internal-doc template and the examples.
Illustrative content: a Cooper Labs proposal to Parallel for an MCP server, a fictional client
(Atlas Wallet), a launch-day post-mortem, a memo on Friday demos, the page-styles guide,
the deck and the studio fact sheet. Figures are examples, not records."""
import json, pathlib, sys, copy

_R = pathlib.Path(__file__).resolve().parents[1]
ROOT = (_R / "plugins" / "cooper-brand" / "assets") if (_R / "plugins" / "cooper-brand").exists() else (_R / "plugin" / "assets")   # the marketplace repo, or the scratch tree
T, X = ROOT / "templates", ROOT / "examples"

# ------------------------------------------------------------------ the template · proposal, Parallel MCP server
TOOLS = [["get_positions", "A wallet's vaults, collateral, debt and health factor", "Read"], ["get_rates", "Borrow and savings rates per asset and chain", "Read"],
         ["get_backing", "Backing ratio, sleeves and the insurance buffer", "Read"], ["get_proposals", "Open and closed governance proposals, with tallies", "Read"],
         ["get_docs", "A section of the documentation by slug", "Read"], ["simulate_borrow", "Health factor after a hypothetical borrow", "Read"],
         ["build_tx", "An unsigned transaction for the user's own wallet", "Build"]]

INTERNAL_DOC = {
    "class": "proposal", "subject": "Parallel MCP server",
    "title": "Ship the MCP server *before the CLI.*",
    "standfirst": "Proposes a six-week build of an MCP server that exposes Parallel's positions, rates and governance to AI agents, read-only, for a start on 28 September 2026.",
    "version": "v0.1", "classification": "Confidential", "status": "Draft", "date": "2026-09-14", "owner": "Jean, Cooper Labs", "cover": "01",
    "contents": "auto",
    "contents_intro": "Read the summary and the recommendation first; they stand alone. Context, options and the appendices are the evidence, kept for whoever needs to check a figure or a date. Every table names its source in the margin.",
    "versions": [["v0.1", "2026-09-14", "First draft for the Parallel team"], ["v0.2", "TBD", "Scope and dates confirmed with Noah"], ["v1.0", "TBD", "Signed statement of work"]],
    "pages": [
        {"name": "Summary", "blocks": [
            {"tag": "Summary", "heading": {"text": "One server, *every agent.*", "suffix": "(six weeks)"},
             "body": "Agents already answer questions about Parallel from stale documentation and guessed numbers. An MCP server gives every assistant the same read-only view of the protocol: positions, rates, backing and governance, straight from the chain and the indexer. It holds no keys, signs nothing, and ships in six weeks. The CLI the team asked for is a thin client of the same server, and comes after.",
             "toc": "Summary and headline figures"},
            {"tag": None, "figures": [["6", "Weeks, brief to release"], ["7", "Tools, read-only"], ["3", "Chains covered"], ["0", "Keys held"]]},
            {"tag": "Assessment", "source": "Reviewed with the Parallel protocol team on 10 Sep 2026.", "heading": "What exists, *what is missing*",
             "table": {"cols": [["Area", 150], ["Today", None], ["Gap", 190]], "strong": [0],
                       "rows": [["Protocol data", "Subgraph and a REST indexer, per chain", "No single entry point"], ["Documentation", "Public docs site, versioned", "Not machine-readable"],
                                ["Governance", "Snapshot and the forum", "Tallies only via the UI"], ["Agents", "Ad-hoc prompts with pasted numbers", "No source of truth"]]}},
            {"tag": "Risks & mitigants", "bullets": [["Stale data", "Every answer carries the block number and the age of the indexer; past 300 s the tool says so."],
                                                     ["Misuse as advice", "Read-only tools, a fixed disclaimer in every schema, no rates projected forward."],
                                                     ["Maintenance", "The server is generated from the tool schemas; a new protocol module is one file."]]},
            {"tag": "Recommendation", "reco": ["Build the server first, read-only, and derive the CLI from it in week five.",
                                               "Start on 28 September; a public beta on 6 November, announced with the Seventeenth Parallel Report."]}]},
        {"name": "Context & scope", "blocks": [
            {"tag": "Context", "heading": "Why now", "body": "Since June the support channel receives more questions from agents than from people: the same three questions about rates, backing and a wallet's health factor, answered from documentation that is two releases behind. The protocol has the data; it does not have a door for it. The team asked for a CLI. A CLI serves developers at a terminal; an MCP server serves every assistant the community already uses, and a CLI besides."},
            {"tag": "Scope", "heading": "What is *in, what is out*",
             "bullets": [["In", "Seven read tools over the indexer and the chain, an unsigned transaction builder, the documentation as a resource, one package per chain configuration."],
                         ["Out", "Signing, key custody, write access of any kind, a hosted gateway. The server runs where the user runs it."],
                         ["Later", "The CLI (week five), a hosted read-only endpoint (after the beta), governance vote drafting (a separate proposal)."]]},
            {"tag": "Timeline", "source": "Dates agreed with Noah on 12 Sep 2026; each week ends with a Friday demo.", "heading": "Six weeks, *six demos*",
             "table": {"cols": [["Week", 60], ["Ends", 80], ["Delivered", None]], "mono": [0, 1],
                       "rows": [["1", "2 Oct", "Tool schemas agreed; get_rates and get_backing on Base"], ["2", "9 Oct", "Positions and simulate_borrow, three chains"],
                                ["3", "16 Oct", "Governance and docs resources; staleness rule"], ["4", "23 Oct", "build_tx, test suite, error copy"],
                                ["5", "30 Oct", "CLI over the server; install docs"], ["6", "6 Nov", "Public beta, announcement, hand-over"]]}}]},
        {"name": "Options", "blocks": [
            {"tag": "Options", "source": "Estimates in Cooper weeks, one designer and one engineer.", "heading": "Four ways *to open the door*",
             "table": {"cols": [["Option", 190], ["Weeks", 60], ["Reach", 110], ["Verdict", None]], "mono": [1], "strong": [0], "highlight": 1,
                       "rows": [["A · CLI first", "5", "Developers", "Serves the terminal, not the assistants"], ["B · MCP server first", "6", "Every agent", "Recommended; the CLI comes free"],
                                ["C · Both in parallel", "9", "Both", "Two codebases for one set of data"], ["D · Wait for the public API", "n/a", "Unknown", "No date; the questions keep coming"]]}},
            {"tag": "Why option B", "bullets": [["One source of truth", "Tools, CLI and documentation read the same schemas; a number cannot disagree with itself."],
                                                ["Read-only by construction", "No key ever enters the process; the worst failure is a stale answer, and the answer says so."],
                                                ["Six weeks, then a thin CLI", "The CLI is a formatter over the server's tools, a week of work rather than five."]]},
            {"tag": None, "figures": [["6", "Weeks, option B"], ["1", "Week for the CLI"], ["3", "Weeks saved on C"]]},
            {"tag": "Recommendation", "reco": ["Option B. The server first, the CLI from it.", "A fixed price per phase, two phases, the second only on the demo of week three."]}]},
        {"name": "Decision & appendix", "blocks": [
            {"tag": "Decision", "heading": "What Parallel is *asked to decide*",
             "body": "Three things, by 21 September, so that the build starts on the 28th.",
             "bullets": [["The scope", "Seven tools, read-only, as listed in Appendix B; the CLI in week five."],
                         ["The chains", "Base, Arbitrum and Ethereum at launch; a fourth is one configuration file."],
                         ["The owner", "One person at Parallel who takes the Friday demo and answers within the day."]]},
            {"tag": "Appendix A · Decision log", "source": "Kept by Cooper Labs; one line per closed question.",
             "table": {"cols": [["Date", 70], ["Question", None], ["Closed as", 190]], "mono": [0],
                       "rows": [["10 Sep", "CLI or MCP server first?", "Server first, this proposal"], ["12 Sep", "Hosted or local?", "Local; hosted after the beta"],
                                ["12 Sep", "Which chains at launch?", "Three, Base first"], ["TBD", "Who owns the demo at Parallel?", "Open"]]}},
            {"tag": "Appendix B · Tools", "main": [{"heading": "Seven tools, *one schema each*"},
                                                   {"table": {"cols": [["Tool", 150], ["Returns", None], ["Kind", 60]], "mono": [0], "rows": TOOLS}}]}]},
        {"name": "Glossary", "blocks": [
            {"tag": "Appendix C · Glossary", "heading": "Terms *used here*",
             "table": {"cols": [["Term", 130], ["Meaning", None]], "strong": [0],
                       "rows": [["MCP", "Model Context Protocol: the open standard by which an assistant calls tools and reads resources."],
                                ["Tool", "One typed function the server exposes; the assistant calls it with arguments and receives JSON."],
                                ["Resource", "A document the server serves by URI; here, the documentation."],
                                ["Indexer", "Parallel's service that reads the chain and serves positions and rates over REST."],
                                ["Health factor", "Collateral value over debt, adjusted; below 1 a position can be liquidated."],
                                ["Staleness", "The age of a figure relative to the newest block the indexer has seen."],
                                ["Unsigned transaction", "Calldata the user's own wallet signs; the server never holds a key."]]}},
            {"tag": "Contact", "body": "Jean, Cooper Labs · contact@cooperlabs.xyz · Telegram @jeanbrasse. Questions on the schemas to the engineering channel; questions on the scope to Jean."}]}]}

# ------------------------------------------------------------------ examples
CASE_STUDY = {
    "class": "case-study", "subject": "Atlas Wallet",
    "title": "From a whitepaper to a wallet *in twelve weeks.*",
    "standfirst": "Records how Cooper Labs took Atlas from a twenty-page whitepaper to a shipped mobile wallet, what it cost, and what the numbers said three months after launch.",
    "version": "v1.0", "classification": "Internal", "status": "Final", "date": "2026-09-12", "owner": "Nicolas, Design", "cover": "03",
    "pages": [{"name": "Case study", "blocks": [
        {"tag": "Client", "heading": {"text": "Atlas, *a wallet for people who hold one token*", "suffix": "(fictional client)"},
         "body": "Atlas came with a whitepaper, a token and a deadline: a wallet in the stores before the token listing. No screens, no team, no name for the app. The brief was to make the wallet simple enough that a first-time holder could receive, hold and stake in one session, and to ship it in twelve weeks."},
        {"tag": None, "figures": [["12", "Weeks, brief to the stores"], ["11", "Friday demos"], ["2", "People, full time"], ["4.7", "Store rating, month three"]]},
        {"tag": "What we did", "bullets": [["Weeks 1 to 3 · Product", "Interviews with twelve holders, one flow on paper, the onboarding cut from nine screens to four."],
                                           ["Weeks 4 to 9 · Build", "React Native, one design system in Figma and in code, the staking flow tested with the protocol's testnet from week five."],
                                           ["Weeks 10 to 12 · Release", "Store listings, the audit fixes, a beta with two hundred holders, and the launch on listing day."]]},
        {"tag": "Outcome", "source": "Client analytics, 90 days after launch; figures rounded.", "heading": "What the numbers *said*",
         "table": {"cols": [["Metric", None], ["Target", 90], ["Day 90", 90]], "mono": [1, 2], "strong": [0],
                   "rows": [["Onboarding completed", "60%", "74%"], ["First stake within a session", "25%", "31%"], ["Support tickets per 100 users", "< 5", "2.1"], ["Crash-free sessions", "99%", "99.6%"]]}},
        {"tag": "What we would change", "reco": ["Start the store review in week eight, not ten; the two rounds of review cost a week we had not planned.",
                                                 "Keep the weekly demo. Every cut that made the product simpler was decided on a Friday, in front of the client."]}]}]}

SPEC = {
    "class": "spec", "subject": "Connect flow",
    "title": "*One tap* to connect, whatever the wallet.",
    "standfirst": "Defines the wallet connection flow of the Parallel app for every supported wallet, mobile and desktop, for build starting 21 September 2026.",
    "version": "v0.2", "classification": "Internal", "status": "Draft", "date": "2026-09-14", "owner": "Nicolas, Design", "cover": "04",
    "pages": [{"name": "Spec", "blocks": [
        {"tag": "Summary", "heading": "One tap to connect, *whatever the wallet*",
         "body": "The connect button opens one sheet: the wallets found on the device first, then the rest. A returning user is reconnected silently. Every error names the wallet and the next action. The sheet is one component, used on every screen that needs a wallet; no screen may build its own."},
        {"tag": "Requirements", "source": "Priorities agreed at the design review of 11 Sep 2026.",
         "table": {"cols": [["ID", 56], ["Requirement", None], ["Priority", 90]], "mono": [0, 2],
                   "rows": [["R1", "Installed and injected wallets are listed first, detected at open", "Must"], ["R2", "A returning user is reconnected without a sheet", "Must"],
                            ["R3", "Every error names the wallet and offers one next action", "Must"], ["R4", "Wrong chain is handled inside the sheet, with a switch button", "Should"],
                            ["R5", "The sheet remembers the last wallet used, per device", "Could"]]}},
        {"tag": "Interface", "bullets": [["Button", "Label \"Connect\"; once connected, the address shortened to six and four characters, the chain as a dot."],
                                         ["Sheet", "Wallet name and icon on one row each, 56 high; a section label above the second group; no search."],
                                         ["Error", "Two lines under the row: what happened, then one action. Never a modal, never red on its own."]]},
        {"tag": None, "figures": [["1", "Tap to connect"], ["6+4", "Address shortening"], ["400 ms", "Sheet open, at most"]]},
        {"tag": "Open questions", "source": "Decide before build starts on 21 Sep.",
         "table": {"cols": [["#", 48], ["Question", None], ["Owner", 110]], "mono": [0],
                   "rows": [["01", "Do we list wallets we cannot detect, or hide them behind \"Other\"?", "Nicolas"], ["02", "Silent reconnect after how many days?", "Jean"]]}}]}]}

POST_MORTEM = {
    "class": "post-mortem", "subject": "Launch day, 26 Aug", "kicker": "Post-mortem · 26 August 2026",
    "title": "*Fifty-two minutes* on the wrong RPC.",
    "standfirst": "Records what happened on the morning of the Atlas launch, why the release pointed at the testnet, and the three actions that close the gap.",
    "version": "v1.0", "classification": "Internal", "status": "Final", "date": "2026-08-28", "owner": "Jean, Cooper Labs", "cover": "dark",
    "pages": [{"name": "Post-mortem", "blocks": [
        {"tag": "Incident", "heading": {"text": "What happened", "suffix": "(52 minutes)"},
         "body": "At 09:00 UTC the release build went live in both stores with the testnet RPC in its configuration. Balances showed as zero for every user who updated. No funds were at risk; 52 minutes of a wallet that looked empty, one hotfix, and a store review that was faster than we deserved."},
        {"tag": "Timeline", "source": "Times in UTC, from the launch channel log.",
         "table": {"cols": [["Time", 70], ["Event", None], ["Actor", 120]], "mono": [0],
                   "rows": [["09:00", "Release live; first reports of zero balances", "Support"], ["09:07", "Config diff read; testnet RPC confirmed", "Jean"],
                            ["09:15", "Hotfix built from the release branch, config only", "Engineering"], ["09:31", "Expedited review requested in both stores", "Jean"],
                            ["09:52", "Hotfix live; balances correct; incident closed", "Engineering"]]}},
        {"tag": "Root cause", "bullets": [["One configuration file for two environments", "The testnet value had been committed for the beta and never reverted; the build did not know which environment it was for."],
                                          ["No check on the release build", "The release checklist verified the version and the signing, not the network the app would talk to."]]},
        {"tag": "Actions", "source": "Tracked in Linear, ATL-140 to ATL-142.",
         "table": {"cols": [["Action", None], ["Owner", 110], ["Due", 80]], "mono": [2],
                   "rows": [["Environment baked at build time, one file per target", "Engineering", "4 Sep"], ["Release checklist: a mainnet balance read from the release build", "Jean", "4 Sep"],
                            ["Launch-day rota with a named person in each store console", "Jean", "11 Sep"]]}}]}]}

MEMO = {
    "class": "memo", "subject": "Friday demos",
    "title": "Every project demos *on Friday.*",
    "standfirst": "Sets the one rule that applies to every Cooper Labs engagement from October: a demo of working software every Friday, with the client in the room.",
    "version": "v1.0", "classification": "Internal", "status": "Final", "date": "2026-09-14", "owner": "Jean, Cooper Labs", "cover": "05",
    "pages": [{"name": "Memo", "blocks": [
        {"tag": "Rule", "heading": "The rule *in one paragraph*",
         "body": "Every project demos on Friday, from the first week to the last. The demo shows software that runs, not slides; it lasts thirty minutes; the client is there; what is decided is written in the project channel before the end of the day. A week without a demo is a week we do not invoice."},
        {"tag": None, "figures": [["30", "Minutes per demo"], ["Weekly", "From week one"], ["1", "Decision log, per project"], ["Oct", "In force"]]},
        {"tag": "Impact", "bullets": [["Clients", "See the product grow every week and decide on what they see, not on a plan."],
                                      ["The team", "A fixed rhythm; scope cut on Friday rather than discovered in the last week."],
                                      ["Proposals", "Every proposal names the six or twelve demos it promises, and the phase gate sits on one of them."]]},
        {"tag": "Next steps", "source": "Owners confirmed at the studio meeting of 11 Sep 2026.",
         "table": {"cols": [["Step", None], ["Owner", 140], ["Due", 90]], "mono": [2],
                   "rows": [["Add the demo line to the proposal template", "Nicolas", "18 Sep"], ["Write the demo format, one page", "Jean", "25 Sep"],
                            ["First Friday with every project on the rule", "All", "2 Oct"]]}}]}]}

PAGE_STYLES = {
    "class": "guide", "subject": "Page styles",
    "title": "Sixteen ways to *fill a page* inside the same grid.",
    "standfirst": "The page compositions of the internal-document template beyond the block stack: each one on its own page, with what it is for and which rule of the kit it bends.",
    "kicker": "Guide · Page styles · Internal document", "version": "v0.1", "classification": "Internal", "status": "Draft", "date": "2026-09-14", "owner": "Nicolas, Design", "cover": "02",
    "contents": True,
    "contents_intro": "Every page keeps the running head, the footer, the 682 measure and the type scale. Five of the sixteen bend a rule of the kit (a dark ground inside, no margin column, a tinted cell, a render inside): keep those for the opening page of a part or a single appendix, never in the flow of an argument.",
    "versions": [["v0.1", "2026-09-14", "Built from the description; every style a block or a page of build_doc.py"]],
    "pages": [
        {"name": "A · Divider", "toc": "A · Section divider, paper", "style": "divider", "n": "02", "kicker": "Part two · Options", "title": "Four ways *to open the door.*",
         "standfirst": "Four options, one estimate each, and the two figures the Parallel team will be asked to remember.",
         "list": [["Sections", "Options · Why B · Estimate"], ["Pages", "06 to 11"], ["Source", "Estimates of 12 Sep 2026"], ["Reading time", "Six minutes"]]},
        {"name": "B · Divider, dark", "toc": "B · Section divider, dark", "style": "divider", "dark": True, "n": "03", "kicker": "Part three · Decision", "title": "What Parallel *is asked to decide.*",
         "standfirst": "The decision in one paragraph, the three things to confirm, and the log of how each open question was closed.",
         "list": [["Sections", "Decision · Log · Appendix"], ["Pages", "12 to 15"], ["Deadline", "21 September"], ["Owner", "Jean, Cooper Labs"]]},
        {"name": "C · Statement", "toc": "C · Statement", "style": "statement", "text": "An MCP server holds no keys and signs nothing; the worst it can do is give a stale answer, *and the answer says so.*", "who": "Summary · Proposal · Parallel MCP server"},
        {"name": "D · Hero figure", "toc": "D · Hero figure", "style": "hero", "n": "6", "unit": "weeks", "kicker": "From the brief to the public beta",
         "body": "Six weeks, six Friday demos. The server answers on Base at the end of week one and on three chains at the end of week two; the CLI is derived from it in week five and the public beta ships with the Seventeenth Parallel Report on 6 November.",
         "figures": [["6", "Demos"], ["3", "Chains"], ["2", "Phases"]]},
        {"name": "E · Two columns", "blocks": [
            {"tag": "Options", "toc": "E · Two columns, side by side", "source": "Estimates in Cooper weeks, 12 Sep 2026.", "heading": "MCP server *or CLI first*"},
            {"cols": {"columns": [
                {"head": "B · MCP server first", "bullets": [["Every agent, day one", "Claude, Cursor and the community's own assistants call the same tools."], ["Read-only by construction", "No key enters the process."],
                                                            ["The CLI comes free", "A formatter over the tools, one week in week five."], ["Six weeks", "Two phases, a gate on the demo of week three."]], "verdict": "Recommended."},
                {"head": "A · CLI first", "bullets": [["Developers at a terminal", "The audience the team knows best, and the smallest."], ["Five weeks", "Then the server is another five."],
                                                     ["Two codebases", "Formatting and data fetching mixed in one tool."], ["No door for agents", "The support questions keep coming."]], "verdict": "Not first."}]}},
            {"tag": "Recommendation", "toc": False, "reco": ["Option B. The server serves everyone, and the CLI is a week rather than five.", "If the beta shows the terminal is where the users are, the CLI gets its own phase."]}]},
        {"name": "F · Timeline", "blocks": [
            {"tag": "Timeline", "toc": "F · Horizontal timeline", "source": "Dates agreed with Noah on 12 Sep 2026.", "heading": {"text": "From the brief *to the beta*", "suffix": "(six weeks)"}},
            {"timeline": {"steps": [{"date": "14 Sep", "title": "Proposal sent", "text": "This document, v0.1, to the Parallel team.", "past": True},
                                    {"date": "21 Sep", "title": "Scope confirmed", "text": "Tools, chains and the owner at Parallel.", "past": True},
                                    {"date": "28 Sep", "title": "Build starts", "text": "Week one: schemas, rates and backing on Base."},
                                    {"date": "16 Oct", "title": "Phase gate", "text": "Demo of week three; phase two on approval."},
                                    {"date": "6 Nov", "title": "Public beta", "text": "Announced with the Seventeenth Parallel Report."}],
                          "phases": ["Proposal", "Scope", "Phase one", "Gate", "Phase two"]}},
            {"tag": "Owners", "toc": False, "table": {"cols": [["Phase", 110], ["Owner", 150], ["Deliverable", None]], "strong": [0],
                                                      "rows": [["Proposal", "Jean", "This document, v0.1 to v1.0"], ["Scope", "Noah", "Tool list, chains, owner"], ["Phase one", "Cooper Labs", "Weeks one to three, three demos"], ["Phase two", "Cooper Labs", "Weeks four to six, the CLI, the beta"]]}}]},
        {"name": "G · Data page", "toc": "G · Full-measure data page", "style": "wide", "heading": "The build, *every line*", "suffix": "(estimate of 12 Sep 2026)",
         "table": {"cols": [["Item", None], ["Days", 60], ["Week", 60], ["Role", 90], ["Demo", 80], ["Phase", 70]], "strong": [0], "mono": [1, 2], "highlight": 9,
                   "rows": [["Tool schemas and error copy", "3", "1", "Design", "2 Oct", "One"], ["get_rates, get_backing on Base", "2", "1", "Engineering", "2 Oct", "One"],
                            ["Indexer client, three chains", "3", "2", "Engineering", "9 Oct", "One"], ["get_positions, simulate_borrow", "2", "2", "Engineering", "9 Oct", "One"],
                            ["Governance tools", "2", "3", "Engineering", "16 Oct", "One"], ["Docs as a resource", "1", "3", "Engineering", "16 Oct", "One"],
                            ["Staleness rule and copy", "2", "3", "Design", "16 Oct", "One"], ["build_tx and its tests", "3", "4", "Engineering", "23 Oct", "Two"],
                            ["Test suite, three chains", "2", "4", "Engineering", "23 Oct", "Two"], ["Phase gate review", "1", "3", "Both", "16 Oct", "Gate"],
                            ["CLI over the server", "4", "5", "Engineering", "30 Oct", "Two"], ["Install docs and README", "1", "5", "Design", "30 Oct", "Two"],
                            ["Beta packaging, announcement", "3", "6", "Both", "6 Nov", "Two"], ["Hand-over session", "1", "6", "Both", "6 Nov", "Two"], ["Contingency", "3", "6", "Both", "n/a", "Two"]]},
         "foot": ["Source: Cooper Labs estimate of 12 Sep 2026, one designer and one engineer.", "Days are working days; the highlighted line is the phase gate."]},
        {"name": "H · Chart", "blocks": [
            {"tag": "Data", "toc": "H · Chart", "source": "Source: the support channel, weekly counts, weeks 24 to 35 of 2026.", "heading": {"text": "Questions from agents *are rising,* answers are not", "suffix": "(12 weeks)"},
             "chart": {"type": "bar", "labels": [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35], "max": 100, "unit": "",
                       "series": [{"name": "Questions from people", "values": [41, 39, 40, 37, 36, 35, 33, 34, 31, 30, 29, 28], "soft": True},
                                  {"name": "Questions from agents", "values": [12, 15, 19, 22, 27, 31, 38, 44, 51, 57, 66, 74]}]}},
            {"tag": "Accuracy", "toc": False, "heading": "Answers checked correct, share",
             "chart": {"type": "line", "labels": [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35], "values": [71, 70, 68, 66, 63, 61, 58, 55, 52, 50, 47, 44], "max": 100, "unit": "%", "last": "44%"}},
            {"figures": [["74", "Agent questions, week 35"], ["×6", "Since week 24"], ["44%", "Answered correctly"], ["-27 pts", "Accuracy since week 24"]]}]},
        {"name": "I · Matrix", "blocks": [
            {"tag": "Risks", "toc": "I · Matrix", "source": "Assessed by Cooper Labs on 12 Sep 2026; revisited at each phase gate.", "heading": "Likelihood *against impact*"},
            {"matrix": {"cols": ["Low impact", "Medium impact", "High impact"],
                        "rows": [{"key": "Likely", "cells": [{"title": "Schema churn", "text": "Tools renamed in week one; contained by the demo."}, {"title": "Indexer lag", "text": "Every answer carries its block; past 300 s the tool says so."},
                                                             {"title": "Answer read as advice", "text": "Read-only tools and a fixed disclaimer; the wording is not yet approved.", "hot": True}]},
                                 {"key": "Possible", "cells": [{"title": "Chain config drift", "text": "One file per chain, tested weekly."}, {"title": "Owner unavailable", "text": "A named backup at Parallel, asked for in the decision."},
                                                               {"title": "Rate limits on the indexer", "text": "A cache with the block number as its key."}]},
                                 {"key": "Unlikely", "cells": [{"title": "Protocol upgrade mid-build", "text": "Schemas versioned; one file per module."}, {"title": "Store or registry outage", "text": "The package installs from the repository."},
                                                               {"title": "A key in the process", "text": "Outside the design; there is no code path that holds one."}]}]}},
            {"tag": "Reading", "toc": False, "body": "One cell is tinted: the risk that is both likely and high impact, and the only one still open. Its closure, the approved disclaimer, is one of the three things asked of Parallel."}]},
        {"name": "J · Plate", "toc": "J · Render inside", "style": "plate", "render": "03", "caption": "Render 03 · The block, as used on the launch post",
         "blocks": [{"tag": "Context", "toc": False, "heading": "Why the block *is the picture*",
                     "body": ["When a document is about one product, the render that carries that product on social can open the section. It ties the internal document to what the community saw, and it gives a long document one place to breathe.",
                              "The kit reserves imagery for the cover. This page is the case for one exception: a single plate, full width, on the opening page of a part, never in the flow of an argument."]}]},
        {"name": "K · Prose", "toc": "K · Lede and prose", "style": "prose",
         "lede": "Twice this summer a Parallel user asked an assistant for their health factor and got a number that was two releases old. *That is the wrong kind of confidence,* and it is the whole reason for this proposal.",
         "body": ["The first case came in June. A holder asked which vault paid the best savings rate; the assistant quoted the documentation, which had not been updated since the March rate change, and the holder moved funds to the wrong vault. Nothing was wrong with the protocol; the only door to its numbers was a page written by hand.",
                  "The second came in August, during the Atlas launch week, when the support channel was busiest. An agent computed a health factor from a pasted screenshot and told a user their position was safe; it had been liquidated an hour before. Again the data existed on-chain and in the indexer, and again nobody had given the assistant a way to read it.",
                  "What both cases share is a gap that a server closes. An assistant with a tool asks the tool; the tool asks the indexer; the indexer answers with a block number. The number can be stale, and then it says so; it cannot be invented. The habit of pasting numbers into a prompt disappears the day the tool exists.",
                  "Other protocols shipped read-only servers this year and reported the same thing: the questions in the support channel did not go away, they became answerable. None reported an incident from a read-only tool. The mechanism is understood; the question in front of Parallel is only whether to build the door before or after the CLI."],
         "signature": ["Jean, Cooper Labs", "14 September 2026"]},
        {"name": "L · Steps", "blocks": [
            {"tag": "Procedure", "toc": "L · Numbered steps", "source": "Release checklist R-02, as revised after the post-mortem of 26 Aug 2026.", "heading": "Releasing a build *in four steps*"},
            {"step": "01", "toc": False, "heading": "Bake the environment", "body": "Build once per target from its own configuration file. The build log prints the network name and the RPC host; the engineer pastes both lines in the release thread.", "meta": "Owner Engineering · release day, 09:00 · ATL-140"},
            {"step": "02", "toc": False, "heading": "Read a balance from the release build", "body": "Install the release build on a clean device and read one mainnet balance from a known wallet. A zero is a stop.", "meta": "Owner Jean · release day, 09:30 · ATL-141"},
            {"step": "03", "toc": False, "heading": "Submit, then watch", "body": "Submit to both stores; one named person in each console until the build is live, with the hotfix branch open.", "meta": "Owner Jean · release day · ATL-142"},
            {"step": "04", "toc": False, "heading": "Close the release", "body": "Post the version, the block number of the first read and the store links in the project channel, and tag the client.", "meta": "Owner Engineering · release day, close"}]},
        {"name": "M · Glossary", "blocks": [
            {"tag": "Glossary", "toc": "M · Glossary, two columns", "heading": "Terms used *across the set*"},
            {"defs": [["Agent", "An assistant that calls tools on a user's behalf; here, any MCP client."], ["Block number", "The chain height a figure was read at; every answer carries one."],
                      ["CLI", "A command-line client; here, a formatter over the server's tools."], ["Demo", "Thirty minutes of running software, every Friday, with the client in the room."],
                      ["Health factor", "Collateral value over debt, adjusted; below 1 a position can be liquidated."], ["Indexer", "The service that reads the chain and serves positions and rates over REST."],
                      ["MCP", "Model Context Protocol: how an assistant calls tools and reads resources."], ["Phase gate", "The demo on which the second phase of a proposal is approved."],
                      ["Resource", "A document the server serves by URI; here, the documentation."], ["RPC", "The endpoint an app or a server reads the chain from; one per network."],
                      ["Schema", "The typed description of a tool: its arguments, its result, its disclaimer."], ["Staleness", "The age of a figure relative to the newest block the indexer has seen."],
                      ["Tool", "One typed function the server exposes; the assistant calls it and receives JSON."], ["Unsigned transaction", "Calldata the user's own wallet signs; the server never holds a key."]]}]},
        {"name": "N · Flow", "blocks": [
            {"tag": "Mechanism", "toc": "N · Flow diagram", "heading": "How a question *becomes an answer*"},
            {"flow": {"height": 400,
                      "boxes": [{"x": 0, "y": 0, "w": 150, "h": 52, "title": "Question", "sub": "User, any assistant"}, {"x": 0, "y": 90, "w": 150, "h": 52, "title": "Tool call", "sub": "MCP client"},
                                {"x": 200, "y": 90, "w": 150, "h": 52, "title": "Cache fresh?", "sub": "Keyed by block"}, {"x": 400, "y": 90, "w": 130, "h": 52, "title": "Answer", "sub": "With block number"},
                                {"x": 200, "y": 180, "w": 150, "h": 52, "title": "Read the indexer", "sub": "Three chains"}, {"x": 200, "y": 270, "w": 150, "h": 52, "title": "Stale past 300 s?", "sub": "Flag in the result"},
                                {"x": 400, "y": 270, "w": 130, "h": 52, "title": "Answer, flagged", "sub": "\"Figures as of...\""}, {"x": 0, "y": 270, "w": 150, "h": 52, "title": "build_tx", "sub": "Unsigned, user signs", "soft": True}],
                      "arrows": [{"from": [75, 52], "to": [75, 90]}, {"from": [150, 116], "to": [200, 116]}, {"from": [275, 142], "to": [275, 180], "label": "no"}, {"from": [350, 116], "to": [400, 116], "label": "yes"},
                                 {"from": [275, 232], "to": [275, 270]}, {"from": [350, 296], "to": [400, 296]}, {"from": [465, 142], "to": [465, 270]}, {"from": [150, 296], "to": [200, 296], "label": "write"}],
                      "caption": "One server, *four states.*"}},
            {"tag": "Reading", "toc": False, "body": "Hairline boxes, radius zero, one orange dot at the head of every arrow. The build_tx box is drawn in the lighter hairline because it sits outside the read path."}]},
        {"name": "O · Checklist", "blocks": [
            {"tag": "Before the beta", "toc": "O · Checklist and sign-off", "source": "Checked by the owner; ticked items dated in the decision log.", "heading": "Ready *for 6 November*",
             "checklist": [{"text": "Seven tools pass the test suite on three chains", "who": "Engineering · 23 Oct", "done": True}, {"text": "Disclaimer wording approved by Parallel", "who": "Noah · 16 Oct", "done": True},
                           {"text": "Staleness copy reviewed on a stale indexer, on purpose", "who": "Design · 30 Oct"}, {"text": "CLI installs from the repository on a clean machine", "who": "Engineering · 30 Oct"},
                           {"text": "README and install docs read by someone outside the project", "who": "Design · 3 Nov"}, {"text": "Announcement post scheduled with the Seventeenth Report", "who": "Parallel · 6 Nov"}]},
            {"tag": "Sign-off", "toc": False, "signoff": [["Owner", "Jean, Cooper Labs"], ["Design", "Nicolas"], ["Parallel", "Noah"], ["Date", ""]]}]},
        {"name": "P · Code", "blocks": [
            {"tag": "Appendix D · Schema", "toc": "P · Code and configuration", "source": "As proposed; the deployed schema is read from the server.",
             "main": [{"heading": "One tool *in sixteen lines*"}, {"space": 14},
                      {"code": {"text": "// tools/get_rates.ts · one tool, one schema, one disclaimer\nexport const getRates = tool({\n  name: \"get_rates\",\n  description: \"Borrow and savings rates per asset and chain. Figures as of a block; not advice.\",\n  input: z.object({\n    chain: z.enum([\"base\", \"arbitrum\", \"ethereum\"]),\n    asset: z.string().optional(),            // every asset when omitted\n  }),\n  async run({ chain, asset }) {\n    const { block, rates, age } = await indexer(chain).rates(asset);\n    return {\n      block, rates,\n      stale: age > 300,                       // seconds since the newest block\n      note: age > 300 ? `Figures as of block ${block}, ${age} s old.` : undefined,\n    };\n  },\n});",
                                "keywords": ["export", "const", "async", "await", "return", "tool", "z"]}}]},
            {"tag": "Worked values", "toc": False, "table": {"cols": [["Age", 90], ["stale", 90], ["Answer", None]], "mono": [0, 1], "highlight": 3,
                                                             "rows": [["4 s", "false", "Rates, block 31 240 118"], ["90 s", "false", "Rates, block 31 240 075"], ["240 s", "false", "Rates, block 31 240 000"], ["600 s", "true", "Rates, flagged: figures as of block 31 239 820, 600 s old"]]}}]}]}

# ------------------------------------------------------------------ the template, long form: the same proposal on 24 sheets, every page style in use
def _style(letter, **over):
    """A copy of a page of the page-styles guide, renamed for the proposal."""
    pg = copy.deepcopy(next(p for p in PAGE_STYLES["pages"] if p["name"].startswith(letter + " ·")))
    pg.update(over)
    return pg


def _block_page(pg, **over):
    pg = copy.deepcopy(pg)
    pg.update(over)
    return pg


_P = {pg["name"]: pg for pg in INTERNAL_DOC["pages"]}
_summary = _block_page(_P["Summary"])
_context = _block_page(_P["Context & scope"])
_context["blocks"] = [b for b in _context["blocks"] if b.get("tag") != "Timeline"]          # the timeline gets its own page
_options = _block_page(_P["Options"])
_decision = _block_page(_P["Decision & appendix"], name="Decision, and the log")
_decision["blocks"] = [b for b in _decision["blocks"] if b.get("tag") in ("Decision", "Appendix A · Decision log")]
_appendix_b = _P["Decision & appendix"]["blocks"][-1]
_glossary_rows = _P["Glossary"]["blocks"][0]["table"]["rows"]

INTERNAL_DOC["pages"] = [
    _summary,
    _style("C", name="The one sentence", toc="The one sentence", who="Summary · Proposal · Parallel MCP server"),
    _style("A", name="Part one · Context", toc="Part one · Context", n="01", kicker="Part one · Context", title="Why now, *and why a server.*",
           standfirst="Where the questions come from, what answers them today, and the two cases that made the gap visible.",
           list=[["Sections", "Context · Two cases · The numbers"], ["Pages", "06 to 08"], ["Source", "Support channel, weeks 24 to 35"], ["Reading time", "Five minutes"]]),
    _context,
    _style("K", name="Two cases, one gap", toc="Two cases, one gap"),
    _style("H", name="The numbers, twelve weeks", toc=None),
    _style("A", name="Part two · The build", toc="Part two · The build", n="02", kicker="Part two · The build", title="Six weeks, *six demos.*",
           standfirst="The four options, the one recommended, the plan by week, and how the work runs from Monday to Friday.",
           list=[["Sections", "Options · Plan · Method"], ["Pages", "10 to 16"], ["Estimate", "12 Sep 2026, one designer and one engineer"], ["Phase gate", "16 October"]]),
    _options,
    _style("E", name="Server first, or CLI first", toc=None),
    _style("F", name="The plan by week", toc=None),
    _style("D", name="Six weeks, in one figure", toc="Six weeks, in one figure"),
    _style("L", name="How a week runs", toc=None),
    _style("N", name="How a question becomes an answer", toc=None),
    _style("G", name="The build, every line", toc="The build, every line"),
    _style("B", name="Part three · Decision", toc="Part three · Decision", n="03", kicker="Part three · Decision", title="What Parallel *is asked to decide.*",
           standfirst="The three things to confirm by 21 September, the risks that remain, and what has to be true before the beta ships.",
           list=[["Sections", "Decision · Risks · Readiness"], ["Pages", "18 to 20"], ["Deadline", "21 September"], ["Owner", "Jean, Cooper Labs"]]),
    _decision,
    _style("I", name="Risks, likelihood against impact", toc=None),
    _style("O", name="Before the beta, sign-off", toc=None),
    _style("J", name="Appendices", toc="Appendices", caption="Render 03 · The block, as on the launch post",
           blocks=[{"tag": "Appendix", "toc": False, "heading": "The material *behind the argument*",
                    "body": ["The seven tools with what each returns, the terms used across the proposal, and the schema of one tool as it will be written. Nothing here changes the decision; it is what the engineering team will check.",
                             "The picture is the block from the launch post, the one exception to the kit's rule that imagery stays on the cover: a single plate on the opening page of a part."]}]),
    {"name": "Appendix B · Tools, C · Glossary", "blocks": [
        dict(_appendix_b, toc="Tools"),
        {"tag": "Appendix C · Glossary", "toc": "Glossary", "defs": _glossary_rows}]},
    _style("P", name="Appendix D · Schema of one tool", toc=None),
]
# the chart, columns, timeline, steps, flow, matrix, checklist and code pages take their Contents line from their first block's toc
for pg in INTERNAL_DOC["pages"]:
    if pg.get("toc") is None and "blocks" in pg and not pg.get("style"):
        pg.pop("toc", None)
INTERNAL_DOC["pages"][5]["blocks"][0]["toc"] = "The numbers"
INTERNAL_DOC["pages"][8]["blocks"][0]["toc"] = "Server first, or CLI first"
INTERNAL_DOC["pages"][9]["blocks"][0]["toc"] = "The plan by week"
INTERNAL_DOC["pages"][9]["blocks"][0]["source"] = "Dates agreed with Noah on 12 Sep 2026; each week ends with a Friday demo."
INTERNAL_DOC["pages"][11]["blocks"][0].update({"tag": "Method", "toc": "How a week runs", "source": "The studio's week, as run on every engagement since October.", "heading": "From Monday *to the Friday demo*"})
INTERNAL_DOC["pages"][11]["blocks"][1:] = [
    {"step": "01", "toc": False, "heading": "Monday · Scope the week", "body": "Thirty minutes with the owner at Parallel: what Friday's demo shows, written in the channel before noon.", "meta": "Owner Jean · Monday 10:00"},
    {"step": "02", "toc": False, "heading": "Tuesday to Thursday · Build", "body": "One designer and one engineer on the same branch; the schemas first, the tests with them, the copy as the tools take shape.", "meta": "Owner Cooper Labs · daily"},
    {"step": "03", "toc": False, "heading": "Thursday · Review", "body": "The week's work run end to end on a clean machine, against the three chains; what does not pass is cut from the demo, not hidden in it.", "meta": "Owner Engineering · Thursday 16:00"},
    {"step": "04", "toc": False, "heading": "Friday · Demo", "body": "Thirty minutes, working software, the owner in the room; the decisions written in the channel before the end of the day.", "meta": "Owner Jean · Friday 15:00"}]
INTERNAL_DOC["pages"][12]["blocks"][0]["toc"] = "How a question becomes an answer"
INTERNAL_DOC["pages"][16]["blocks"][0]["toc"] = "Risks, likelihood against impact"
INTERNAL_DOC["pages"][17]["blocks"][0]["toc"] = "Before the beta, and sign-off"
INTERNAL_DOC["pages"][20]["blocks"][0]["toc"] = "Schema of one tool"
INTERNAL_DOC["contents_intro"] = ("Read the summary and the statement first; they stand alone. Part one is the context, part two the build and its plan, part three the decision "
                                  "and the risks; the appendices are for the engineering team. Every table names its source in the margin, and every part opens on a divider.")
INTERNAL_DOC["versions"] = [["v0.1", "2026-09-14", "First draft for the Parallel team"], ["v0.2", "TBD", "Scope, dates and the disclaimer wording confirmed with Noah"], ["v1.0", "TBD", "Signed statement of work"]]


DECK = {
    "class": "proposal", "subject": "Parallel MCP server",
    "title": "Ship the MCP server *before the CLI.*",
    "standfirst": "Proposes a six-week, read-only MCP server for Parallel's positions, rates and governance, for a start on 28 September.",
    "kicker": "Proposal · Parallel MCP server · Parallel team, 14 September 2026",
    "version": "v0.1", "classification": "Confidential", "status": "Draft", "date": "2026-09-14", "owner": "Jean, Cooper Labs", "render": "01",
    "slides": [
        {"tag": "Summary", "heading": {"text": "One server, *every agent.*", "suffix": "(six weeks)"},
         "body": "Agents already answer questions about Parallel from stale documentation. An MCP server gives every assistant the same read-only view of the protocol, straight from the chain and the indexer. It holds no keys, signs nothing, and the CLI the team asked for is a thin client of it.",
         "figures": [["6", "Weeks, brief to release"], ["7", "Tools, read-only"], ["3", "Chains covered"], ["0", "Keys held"]]},
        {"kind": "divider", "n": "02", "kicker": "Part two · Options", "title": "Four ways *to open the door.*"},
        {"tag": "Options", "source": "Estimates in Cooper weeks, 12 Sep 2026.", "heading": "Server first, *CLI from it*",
         "table": {"cols": [["Option", 300], ["Weeks", 120], ["Reach", 180], ["Verdict", None]], "mono": [1], "strong": [0], "highlight": 1,
                   "rows": [["A · CLI first", "5", "Developers", "Serves the terminal, not the assistants"], ["B · MCP server first", "6", "Every agent", "Recommended; the CLI comes free"],
                            ["C · Both in parallel", "9", "Both", "Two codebases for one set of data"], ["D · Wait for the public API", "n/a", "Unknown", "No date; the questions keep coming"]]}},
        {"kind": "statement", "text": "An MCP server holds no keys and signs nothing; the worst it can do is give a stale answer, *and the answer says so.*", "who": "Summary · Proposal · Parallel MCP server"},
        {"tag": "Decision", "heading": "What Parallel is *asked to decide*",
         "bullets": [["The scope", "Seven tools, read-only; the CLI in week five."], ["The chains", "Base, Arbitrum and Ethereum at launch."], ["The owner", "One person who takes the Friday demo and answers within the day."]],
         "reco": ["Confirm by 21 September; the build starts on the 28th.", "Two phases at a fixed price; the second on the demo of week three, the beta on 6 November."]}]}

FACT_SHEET = {
    "subject": "Cooper Labs", "title": "We turn Web3 ideas *into products people use.*",
    "standfirst": "Cooper Labs is a product studio for Web3 teams: design and engineering in one team, from the brief to the stores, with a demo of working software every Friday.",
    "date": "2026-09-01", "version": "v1.0", "classification": "Public", "kicker": "Fact sheet · Cooper Labs · September 2026",
    "figures": [["6", "Weeks, brief to first release"], ["Weekly", "Demo, every Friday"], ["2", "Disciplines, one team"], ["Fixed", "Price per phase"]],
    "columns": [
        {"heading": "How we *work*", "bullets": [["One team, both crafts", "A designer and an engineer on every project from day one; the design system lives in Figma and in code."],
                                                ["Working software on Friday", "Thirty minutes, the client in the room, the decisions written the same day."],
                                                ["Phases with a gate", "Two or three fixed-price phases; the next one starts on a demo, not on a plan."]]},
        {"heading": "What we *don't do*", "bullets": [["No custody, no keys", "We build the product; the user signs. Nothing we ship holds funds."],
                                                     ["No slides for software", "A proposal names its demos; a demo shows the thing running."],
                                                     ["No open-ended retainers", "Scope, price and dates per phase, written before the first week."]]}],
    "table": {"heading": "Engagements, *by phase*", "cols": [["Phase", 150], ["Weeks", 70], ["Team", 120], ["Delivered", None]], "mono": [1], "strong": [0],
              "rows": [["Product", "2 to 3", "Design", "Interviews, one flow, the cut list"], ["Build", "4 to 8", "Design + engineering", "The product, its design system, its tests"],
                       ["Release", "2", "Both", "Stores, docs, launch day, hand-over"], ["Care", "monthly", "On call", "Fixes, upgrades, the next phase"]]},
    "contact": [["Website", "cooperlabs.xyz"], ["X", "@cooperlabs"], ["Telegram", "@jeanbrasse"], ["Email", "contact@cooperlabs.xyz"]],
    "footer": "Cooper Labs · Public · cooperlabs.xyz · September 2026"}


def dump(path, d):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("->", path.relative_to(ROOT.parent))


if __name__ == "__main__":
    dump(T / "internal-doc.json", INTERNAL_DOC)
    dump(X / "case-study.json", CASE_STUDY)
    dump(X / "spec.json", SPEC)
    dump(X / "post-mortem.json", POST_MORTEM)
    dump(X / "memo.json", MEMO)
    dump(X / "page-styles.json", PAGE_STYLES)
    dump(X / "deck-parallel-mcp.json", DECK)
    dump(X / "fact-sheet-cooper-labs.json", FACT_SHEET)
