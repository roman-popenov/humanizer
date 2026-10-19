#!/usr/bin/env python3
"""Partial token check: what a rewrite lost or added against its original.

Usage: python3 fact_diff.py ORIGINAL REWRITE

Strict checks (any difference prints FAIL and exits 1): code blocks, inline
code, URLs, quoted passages (each compared by count, so a repeated span that
changes or goes is caught), numbers exactly as written with their signs
(-20, −5.3), version strings, number+unit pairs (36 MB, 120 ms, $14), labelled
values (p = 0.003), number ranges (2019-2021), and bounds on numbers (over
40,000, just over 40,000, about 36, up to 30). Review lines (exit status
unaffected): number words, capitalized names (sentence-initial ones included),
numbers that now appear fewer times, and changed counts of negations and hedges.

This is a partial check. It cannot verify claims, causes, attribution, the
pairing of values with what they measure, or meaning in general, and exit 0
does not establish that facts were preserved. Always finish with the manual
claim-by-claim comparison. Exit status: 0 no strict differences found,
1 strict differences found, 2 usage error.
"""

import re
import sys
from collections import Counter

# Code spans and fences follow CommonMark: a fence closes only on a line of the
# same character at least as long as its opener, and an inline span closes only
# on a backtick run of its opener's length.
FENCE_OPEN = re.compile(r"^ {0,3}(`{3,}|~{3,})")
BACKTICKS = re.compile(r"`+")
BLANK_LINE = re.compile(r"\n[ \t]*\n")
URL = re.compile(r"https?://[^\s<>\"]+")
# Trailing punctuation is not part of a URL (as in GitHub's autolinks), and a
# closing bracket is part of it only when the URL opened one: a_(x)/old.
URL_TRAILING = ".,;:!?*_~'\""
URL_CLOSERS = {")": "(", "]": "["}
# One-character quotes and long single-quoted passages count too: a changed
# letter inside quotation marks is a changed quotation. A passage may run over
# line breaks but not over a blank line. An apostrophe followed by a letter
# (don't) stays inside a single-quoted passage; one after a letter (students')
# never opens one. The marks themselves are not compared, so the curly-to-
# straight fix of P20 passes.
PARA = r"(?:(?!\n[ \t]*\n)[^{q}])"
QUOTE = re.compile(
    r'"((?:' + PARA.format(q='"') + r")+)\""
    r"|“((?:" + PARA.format(q="”") + r")+)”"
    r"|«((?:" + PARA.format(q="»") + r")+)»"
    r"|‘((?:" + PARA.format(q="’") + r"|’(?=\w))+?)’(?!\w)"
    r"|(?<![\w'’])'(?=\S)((?:" + PARA.format(q="'") + r"|'(?=\w))+?)'(?!\w)"
)
VERSION = re.compile(r"(?<![\w.])[vV]\d+(?:\.\d+)*(?:[-.][A-Za-z0-9]+)*\b")
UNITS = (
    r"%|‰|°[CF]?|x|ms|µs|us|ns|s|sec|secs|min|mins|h|hr|hrs|KB|kB|MB|GB|TB|PB|Kb|Mb|Gb|"
    r"KiB|MiB|GiB|TiB|Hz|kHz|MHz|GHz|Msps|ksps|fps|px|pt|dB|dBm|mm|cm|m|km|g|kg|mg|lb|lbs|"
    r"oz|mi|ft|V|mV|W|kW|MW|mA|mAh|Wh|kWh|mmHg|bpm|rpm"
)
# An optional sign (ASCII hyphen-minus, Unicode minus or plus) is part of the
# number, so -20 -> 20 is a changed value. The lookbehinds below keep the hyphen
# in a range or date (2019-2021) from being read as a sign.
NUM = r"[+−-]?\d+(?:[.,]\d+)*"
CURRENCY = re.compile(r"[$€£¥₹]\s?" + NUM + r"(?:\s?(?:k|K|m|M|bn|B)\b)?")
QUANTITY = re.compile(r"(?<![\w.])(" + NUM + r")\s?(" + UNITS + r")(?![\w])")
RANGE = re.compile(r"(?<![\w.])" + NUM + r"\s?[–—-]\s?" + NUM + r"(?![\w.])")
BOUND = re.compile(
    r"\b(more than|greater than|less than|fewer than|at least|at most|no more than|"
    r"no fewer than|up to|over|under|above|below|exceeding|about|approximately|around|"
    r"roughly|nearly|almost|just over|just under)\s+(" + NUM + r")|([~<>≤≥≈])\s?(" + NUM + r")",
    re.I,
)
BOUND_CLASS = {
    "more than": ">", "greater than": ">", "over": ">", "above": ">", "exceeding": ">",
    "just over": ">~", ">": ">", "less than": "<", "fewer than": "<", "under": "<",
    "below": "<", "just under": "<~", "<": "<", "at least": ">=", "no fewer than": ">=",
    "≥": ">=", "at most": "<=", "no more than": "<=", "up to": "<=", "≤": "<=",
    "about": "~", "approximately": "~", "around": "~", "roughly": "~", "~": "~", "≈": "~",
    "nearly": "<~", "almost": "<~",
}
LABELLED = re.compile(r"(?<![\w])([A-Za-z]\w{0,10})\s?([=<>≤≥])\s?(" + NUM + r")")
NUMBER = re.compile(r"(?<![\w.])" + NUM + r"(?:%|x\b)?")
NAME = re.compile(r"\b[A-ZÀ-Þ][\wÀ-ɏ'’-]*(?:[ \t]+[A-ZÀ-Þ][\wÀ-ɏ'’-]*)*")
FUNCTION_WORDS = set(
    "I I'm I've I'd I'll A An The This That These Those It Its It's He She We They You "
    "My Our Your His Her Their And But Or So If When While In On At For With As By To Of "
    "From After Before Then Now Here There What Why How Each Every All No Not Yes Okay OK "
    "Also Some Most Many One Two Let's Here's There's Is Are Was Were Do Does Did Should Would "
    "Could Can Will May Might Must Whether Since Because Although Though Despite However "
    "Additionally Furthermore Moreover Notably Importantly Honestly Overall Finally".split()
)
NUMBER_WORDS = re.compile(
    r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|"
    r"hundred|thousand|million|billion|half|dozen|double|triple|twice|percent|single|both)\b",
    re.I,
)
NEGATION = re.compile(r"\b(not|no|never|none|nothing|neither|nor|without|cannot)\b|n't\b", re.I)
HEDGE = re.compile(
    r"\b(may|might|could|possibly|perhaps|likely|unlikely|probably|potential(?:ly)?|"
    r"suggests?|appears?|seems?|believed?|guess|maybe|approximately)\b",
    re.I,
)


def split_fences(text):
    """Return the fenced code blocks and the text outside them."""
    blocks, kept, block, closer = [], [], [], None
    for line in text.splitlines(keepends=True):
        if closer is None:
            m = FENCE_OPEN.match(line)
            # A backtick fence's info string cannot contain a backtick.
            if m and not (m.group(1)[0] == "`" and "`" in line[m.end():]):
                closer = re.compile(r"^ {0,3}" + re.escape(m.group(1)[0]) + "{%d,}[ \t]*$" % len(m.group(1)))
                block = [line]
            else:
                kept.append(line)
        else:
            block.append(line)
            if closer.match(line.rstrip("\r\n")):
                blocks.append("".join(block))
                kept.append("\n")
                closer = None
    if closer is not None:  # an unclosed fence runs to the end of the text
        blocks.append("".join(block))
    return blocks, "".join(kept)


def split_inline_code(text):
    """Return the inline code spans, line breaks read as spaces, and the rest."""
    spans, kept, pos, i = [], [], 0, 0
    while True:
        m = BACKTICKS.search(text, i)
        if m is None:
            break
        close = re.compile(r"(?<!`)`{%d}(?!`)" % len(m.group(0))).search(text, m.end())
        if close and not BLANK_LINE.search(text, m.end(), close.start()):
            spans.append(re.sub(r"[ \t]*\r?\n[ \t]*", " ", text[m.start():close.end()]))
            kept += [text[pos:m.start()], " "]
            pos = i = close.end()
        else:
            i = m.end()  # an unmatched run is literal text
    kept.append(text[pos:])
    return spans, "".join(kept)


def trim_url(url):
    while url:
        if url[-1] in URL_TRAILING:
            url = url[:-1]
        elif url[-1] in URL_CLOSERS and url.count(url[-1]) > url.count(URL_CLOSERS[url[-1]]):
            url = url[:-1]
        else:
            break
    return url


def strip_protected(text):
    """Split a text into its protected spans and the prose left over."""
    facts = {}
    blocks, body = split_fences(text)
    facts["code_blocks"] = Counter(blocks)
    spans, body = split_inline_code(body)
    facts["inline_code"] = Counter(spans)
    facts["urls"] = Counter(trim_url(m.group(0)) for m in URL.finditer(body))
    body = URL.sub(lambda m: " " + m.group(0)[len(trim_url(m.group(0))):], body)
    return facts, body


def extract(text):
    facts, body = strip_protected(text)
    # A quotation re-wrapped over lines is the same quotation.
    facts["quotes"] = Counter(" ".join(next(g for g in m.groups() if g).split())
                              for m in QUOTE.finditer(body))
    facts["versions"] = Counter(m.group(0) for m in VERSION.finditer(body))
    body = VERSION.sub(" ", body)
    facts["currency"] = Counter(re.sub(r"\s", "", m.group(0)) for m in CURRENCY.finditer(body))
    facts["quantities"] = Counter(f"{m.group(1)} {m.group(2)}" for m in QUANTITY.finditer(body))
    facts["labelled"] = Counter(" ".join(m.groups()) for m in LABELLED.finditer(body))
    facts["ranges"] = Counter(re.sub(r"\s", "", m.group(0)) for m in RANGE.finditer(body))
    bounds = Counter()
    for m in BOUND.finditer(body):
        word, num = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
        bounds[f"{BOUND_CLASS[word.lower()]} {num}"] += 1
    facts["bounds"] = bounds
    # Numbers are compared exactly as written: 3,000 and 3000 differ, and so do
    # 1,5 and 1.5. A rewrite should not reformat data (hard rule 4).
    facts["numbers"] = Counter(m.group(0).rstrip(".") for m in NUMBER.finditer(body))
    facts["number_words"] = Counter(m.group(0).lower() for m in NUMBER_WORDS.finditer(body))
    facts["negations"] = len(NEGATION.findall(body))
    facts["hedges"] = len(HEDGE.findall(body))
    plain = re.sub(r"[*_]{1,3}", "", body)  # bold and italic markers hide sentence starts
    # A sentence-initial word is kept as a candidate name ("Alice approved it"):
    # dropping it hid real names. Ordinary words capitalized by position are
    # compared without case (see diff), so "Moving" is kept by "moving".
    names = Counter()
    for m in NAME.finditer(plain):
        words = m.group(0).split()
        while words and words[0].rstrip(".,'’") in FUNCTION_WORDS:
            words = words[1:]
        if words:
            names[" ".join(words).rstrip(".,'’")] += 1
    facts["names"] = names
    return facts


def has_phrase(text, phrase, ignore_case=False):
    flags = re.I if ignore_case else 0
    return re.search(r"(?<![\w])" + re.escape(phrase) + r"(?![\w])", text, flags) is not None


STRICT = ("code_blocks", "inline_code", "urls", "quotes", "versions", "currency",
          "quantities", "labelled", "ranges", "bounds", "numbers")
# Protected spans are compared by count: with two `upload()` and one `delete()`,
# turning one upload into a delete keeps the set of spans the same.
COUNTED = ("code_blocks", "inline_code", "urls", "quotes")
REVIEW = ("number_words", "names")


def count_changes(a, b):
    """Spans the rewrite has fewer of (lost) or more of (added) than the original."""
    def show(t):
        return f"{t} ({a[t]} -> {b[t]})" if a[t] and b[t] else t
    return (sorted(show(t) for t in a if a[t] > b[t]),
            sorted(show(t) for t in b if b[t] > a[t]))


def diff(original, rewrite):
    a, b = extract(original), extract(rewrite)
    report = {}
    for kind in STRICT + REVIEW:
        if kind == "names":
            # A name counts as kept if it appears as a whole word anywhere in the
            # rewrite. A one-word candidate is compared without case, since it may
            # be an ordinary word capitalized only because it starts a sentence.
            def kept(n, text):
                return has_phrase(text, n, ignore_case=" " not in n)
            lost = sorted(n for n in a[kind] if not kept(n, rewrite))
            added = sorted(n for n in b[kind] if not kept(n, original))
        elif kind in COUNTED:
            lost, added = count_changes(a[kind], b[kind])
        else:
            # Repeating a fact is not adding one, so presence is compared here;
            # fewer repetitions are reported separately for review.
            lost = sorted(set(a[kind]) - set(b[kind]))
            added = sorted(set(b[kind]) - set(a[kind]))
        if lost or added:
            report[kind] = (lost, added)
    fewer = sorted(f"{n} ({a['numbers'][n]} -> {b['numbers'][n]})"
                   for n in a["numbers"] if 0 < b["numbers"][n] < a["numbers"][n])
    if fewer:
        report["numbers_fewer_times"] = (fewer, [])
    for kind in ("negations", "hedges"):
        if a[kind] != b[kind]:
            report[kind] = ([f"{a[kind]} in original, {b[kind]} in rewrite"], [])
    return report


def main(argv):
    if len(argv) != 3:
        print("Usage: python3 fact_diff.py ORIGINAL REWRITE", file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as f:
        original = f.read()
    with open(argv[2], encoding="utf-8") as f:
        rewrite = f.read()
    report = diff(original, rewrite)
    if not report:
        print("fact_diff: no token differences found (claims still need the manual check)")
        return 0
    failed = False
    for kind, (lost, added) in report.items():
        level = "FAIL" if kind in STRICT else "review"
        failed = failed or kind in STRICT
        if kind in ("negations", "hedges", "numbers_fewer_times"):
            print(f"[{level}] {kind}: {lost}")
            continue
        if lost:
            print(f"[{level}] {kind} lost: {lost}")
        if added:
            print(f"[{level}] {kind} added: {added}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
