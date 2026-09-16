"""Cooper Labs, the strings the builders share: names, links, tagline, files.

Change here, not in the builders. Everything Cooper-specific that appears in
a document, a deck, a fact sheet or a card comes from this module or from
cooper.css; the layout code is the same engine as parallel-brand.
"""
NAME = "Cooper Labs"
FILE_PREFIX = "CooperLabs"                    # CooperLabs-Proposal-<Subject>-v0.1.pdf
CSS = "css/cooper.css"
LOGO_W = "logo/cooper_horizontal_w.svg"        # white on dark
LOGO_B = "logo/cooper_horizontal_b.svg"        # ink on light
ICON_W = "logo/cooper_icon_w.svg"
ICON_B = "logo/cooper_icon_b.svg"
RENDERS = "img/renders"                        # the brand renders, 01-06, 1841 x 1151
TAGLINE_HTML = "We turn ideas <em>into products people use.</em>"       # the leitmotiv, as on cooperlabs.xyz
PROOF_LINE = "We ship production-ready products. No fluff."             # the second recurring line, from the site
LINKS = [("Website", "cooperlabs.xyz"), ("Email", "contact@cooperlabs.xyz"), ("X", "@cooperlabs"), ("Telegram", "@jeanbrasse")]
CONTACT = [("Website", "cooperlabs.xyz"), ("Email", "contact@cooperlabs.xyz"), ("X", "@cooperlabs"), ("Telegram", "@jeanbrasse")]
NOTICE = "Internal document · Not for distribution outside Cooper Labs"
FOOTER = "Cooper Labs · Internal · Not for distribution"
FOOTER_PUBLIC = "Cooper Labs · cooperlabs.xyz"
COPYRIGHT = "Cooper Labs"
CLASSES = {"proposal": "Proposal", "case-study": "Case study", "spec": "Spec", "post-mortem": "Post-mortem", "memo": "Memo", "guide": "Guide", "report": "Report"}
DECK_LABELS = dict(CLASSES, briefing="Briefing", update="Update", pitch="Pitch", deck="Deck")
