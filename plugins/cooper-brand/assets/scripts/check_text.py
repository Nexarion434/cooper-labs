#!/usr/bin/env python3
"""Catch the sentences a model writes and a person does not.

    python3 check_text.py doc.json [more.json ...]     # lint a description before it is built
    python3 check_text.py --text "the sentence"        # lint one string
    python3 check_text.py doc.json --strict            # notes count as failures too

The builders run this on every description, so the copy is caught where it can
still be rewritten rather than in the PDF. Two lists:

  faults   the em dash and the en dash used as punctuation, three dots for a
           trailing thought, emoji, "lorem", an unfilled version or date.
           A fault fails the build.
  tells    the words and turns that mark machine prose: "delve", "leverage",
           "seamless", "robust", "it's not just X, it's Y", "in today's ...
           landscape", "moreover", "underscores", "testament", a sentence that
           opens on "Overall". A tell is printed and the build goes on.

Rewrite, do not soften: the studio's voice is short sentences, one idea each,
a figure where a model would put an adjective. The em dash is replaced by a
period when the second half is a sentence, by a comma when it is an aside, by
a colon when what follows explains, and by the middle dot in a meta line.
"""
import sys, re, json

FAULTS = [
    (r"—", "em dash", "a period, a comma, a colon, or the middle dot in a meta line"),
    (r"(?<=\w)\s*–\s*(?=\w)", "en dash", "'to' in a range (2023 to 2026), a comma elsewhere"),
    (r"\.\.\.|…", "trailing dots", "finish the sentence"),
    ("[\\U0001F300-\\U0001FAFF\\u2600-\\u27BF\\uFE0F]", "emoji", "words"),
    (r"\blorem\b", "lorem text", "the real copy, or a visible TBD"),
    (r"\bv[Xx]\.[Xx]\b", "unfilled version", "the version"),
    (r"\bDD MONTH\b", "unfilled date", "the date"),
]

TELLS = [
    (r"\bdelve[sd]?\b", "look at, read, dig into"),
    (r"\bleverag(e|es|ed|ing)\b", "use"),
    (r"\butilis|utiliz", "use"),
    (r"\bseamless(ly)?\b", "say what happens instead"),
    (r"\brobust\b", "a number: how many, how often"),
    (r"\bcutting[- ]edge\b|\bstate[- ]of[- ]the[- ]art\b|\bbest[- ]in[- ]class\b|\bworld[- ]class\b", "what it does that others do not"),
    (r"\bgame[- ]chang(er|ing)\b|\brevolutionary\b|\btransformative\b", "the effect, measured"),
    (r"\binnovative\b|\bcutting\b.{0,6}\bedge\b", "what is new in it"),
    (r"\bholistic\b|\bsynerg(y|ies|istic)\b|\bparadigm\b", "plain words"),
    (r"\blandscape\b|\brealm\b|\btapestry\b|\bfabric of\b", "the market, the field, the file"),
    (r"\bmyriad\b|\bplethora\b|\bvast array\b", "a number"),
    (r"\bvibrant\b|\bbustling\b|\bthriving\b", "a figure, or nothing"),
    (r"\b(a|is a) testament to\b", "the evidence itself"),
    (r"\bunderscor(e|es|ing)\b|\bhighlight(s|ing)? the importance\b", "says, shows"),
    (r"\bpivotal\b|\bcrucial\b|\bvital\b|\bparamount\b", "say why it matters, once"),
    (r"\bunlock(s|ing)?\b|\bunleash\b|\bempower(s|ing|ed)?\b|\bsupercharg\w*\b", "the verb for what it does"),
    (r"\bstreamlin(e|es|ed|ing)\b|\belevat(e|es|ing) (your|the)\b|\bharness(es|ing)?\b|\bfoster(s|ing)?\b", "a plain verb"),
    (r"\bnavigat(e|ing) the (complexit|challeng)", "say what is hard"),
    (r"\bembark(s|ing)? on\b|\b(our|the) journey\b|\bdeep dive\b|\bdive (deep|into)\b", "start, read, look at"),
    (r"\bin today'?s\b|\bever[- ]evolving\b|\bfast[- ]paced\b|\brapidly changing\b", "the date and the fact"),
    (r"\bit'?s worth noting\b|\bit is (important|worth) (to note|noting)\b|\bneedless to say\b", "note it, or cut it"),
    (r"\bwhen it comes to\b|\bin the world of\b|\bthe realm of\b", "the subject, named"),
    (r"(?:^|(?<=[.!?] ))\s*(Moreover|Furthermore|Additionally|In conclusion|In summary|Overall|That said|Indeed|Ultimately)\b", "start on the fact"),
    (r"\bnot (just|only) [^.;]{2,40}?,? (but|it'?s)\b", "one claim, stated once"),
    (r"\bmore than just\b|\bat the end of the day\b|\brest assured\b|\blook no further\b", "the claim itself"),
    (r"\b(truly|really|very|incredibly|remarkably|significantly|substantially) \w+", "the figure"),
    (r"\bplays? a (key|vital|crucial|significant) role\b|\bserves? as (a|the)\b|\bstands? as (a|the)\b", "does what, exactly"),
    (r"\bboasts?\b", "has"),
    (r"\bwe're excited to\b|\bwe are thrilled\b|\bexciting\b", "what shipped, and when"),
    (r"\bcomprehensive\b|\bseamless experience\b|\bend[- ]to[- ]end solution\b", "what is in it"),
    (r"\bdesigned to ensure\b|\bensur(e|es|ing) that\b", "does, keeps, stops"),
]


def walk(o, path=""):
    """Every string in a description, with the key path it came from."""
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, f"{path}.{k}" if path else str(k))
    elif isinstance(o, (list, tuple)):
        for i, v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")


def scan(obj):
    """(faults, tells): each one (path, what, excerpt, instead)."""
    faults, tells = [], []
    for path, s in walk(obj):
        code = ".code." in path or path.endswith(".code")     # a listing may elide an address; prose may not
        for pat, what, instead in FAULTS:
            if code and what in ("trailing dots", "en dash"):
                continue
            m = re.search(pat, s)
            if m:
                faults.append((path, what, excerpt(s, m), instead))
        for pat, instead in TELLS:
            m = re.search(pat, s, re.I | re.M)
            if m:
                tells.append((path, m.group(0).strip(), excerpt(s, m), instead))
    return faults, tells


def excerpt(s, m, span=34):
    a, b = max(0, m.start() - span), min(len(s), m.end() + span)
    return ("…" if a else "") + s[a:b].replace("\n", " ") + ("…" if b < len(s) else "")


def report(obj, name="", strict=False, quiet_ok=True):
    """Print what was found; return the number of failures."""
    faults, tells = scan(obj)
    for path, what, ex, instead in faults:
        print(f"  ! {what} in {path}: {ex}\n      write {instead}")
    for path, word, ex, instead in tells:
        print(f"  tell: '{word}' in {path}: {ex}\n      write {instead}")
    if not faults and not tells and not quiet_ok:
        print(f"ok   {name}: no em dash, no machine prose")
    return len(faults) + (len(tells) if strict else 0)


def gate(d, name="the description", skip=False):
    """The builders' gate: print what was found, stop on a fault, go on after a tell."""
    if skip:
        return
    faults, tells = scan(d)
    for path, what, ex, instead in faults:
        print(f"  ! {what} in {path}: {ex}\n      write {instead}")
    for path, word, ex, instead in tells:
        print(f"  tell: '{word}' in {path}: {ex}\n      write {instead}")
    if faults:
        sys.exit(f"{len(faults)} fault{'s' if len(faults) > 1 else ''} in {name}: rewrite the copy, nothing was built (--no-lint to build anyway)")
    if tells:
        print(f"  {len(tells)} tell{'s' if len(tells) > 1 else ''}: the copy reads like a model wrote it; rewrite before it goes out")


def main():
    args = sys.argv[1:]
    strict = "--strict" in args
    args = [a for a in args if a != "--strict"]
    if "--text" in args:
        i = args.index("--text")
        sys.exit(1 if report(args[i + 1], "the text", strict, quiet_ok=False) else 0)
    if not args:
        print(__doc__); sys.exit(1)
    bad = 0
    for p in args:
        with open(p, encoding="utf-8") as fh:
            d = json.load(fh)
        print(f"---- {p}")
        bad += report(d, p, strict, quiet_ok=False)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
