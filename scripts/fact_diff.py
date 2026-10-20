#!/usr/bin/env python3
"""Partial token check: what a rewrite lost or added against its original.

Usage: python3 fact_diff.py ORIGINAL REWRITE

Strict checks (any difference prints FAIL and exits 1): code blocks, inline
code, URLs, quoted passages (each compared by count, so a repeated span that
changes or goes is caught), numbers exactly as written with their signs
(-20, −5.3, .05, 1e-3), version strings, number+unit pairs (36 MB, 30 km/h,
-$14), labelled values (p = 0.003, x >= 5), number ranges (2019-2021), and
bounds on numbers (over 40,000, just over 40,000, about 36, up to 30, <= 5).
Review lines (exit status unaffected): number words, capitalized names
(sentence-initial ones included), numbers that now appear fewer times, and
changed counts of negations and hedges.

This is a partial check. It cannot verify claims, causes, attribution, the
pairing of values with what they measure, or meaning in general, and exit 0
does not establish that facts were preserved. A Markdown blockquote is read as
prose, since it often holds the writer's own text, so a quotation without
quotation marks is left to the manual check. Always finish with the manual
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
# Trailing sentence punctuation is not part of a URL (as in GitHub's autolinks),
# and a closing bracket is part of it only when the URL opened one: a_(x)/old.
# A trailing * _ or ~ is dropped only when the same marker opened just before
# the URL (**https://a.b/c**), so https://a.b/user_ keeps its underscore.
URL_TRAILING = ".,;:!?'\""
URL_CLOSERS = {")": "(", "]": "["}
EMPHASIS_BEFORE = re.compile(r"[*_~]+$")
# One-character quotes and long single-quoted passages count too: a changed
# letter inside quotation marks is a changed quotation. A passage may run over
# line breaks. In curly double quotes or guillemets it may also run over blank
# lines, since their opening and closing marks differ; straight and single
# quotes stop at a blank line, so a stray mark (12") cannot pair with one
# paragraphs later. An apostrophe followed by a letter
# (don't) stays inside a single-quoted passage; one after a letter (students')
# never opens one. The marks themselves are not compared, so the curly-to-
# straight fix of P20 passes.
PARA = r"(?:(?!\n[ \t]*\n)[^{q}])"
QUOTE = re.compile(
    r'"((?:' + PARA.format(q='"') + r")+)\""
    r"|“([^”]+)”"
    r"|«([^»]+)»"
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
# in a range or date (2019-2021) from being read as a sign. A leading-dot decimal
# (.05) and an exponent (1.5e3, 1e-3) are part of the number.
NUM = r"[+−-]?(?:\d+(?:[.,]\d+)*|\.\d+)(?:[eE][+−-]?\d+)?"
# A sign before the symbol (-$14) is kept, but not a range's hyphen ($10-$20).
CURRENCY = re.compile(r"(?:(?<![\w$€£¥₹])[+−-])?[$€£¥₹]\s?" + NUM + r"(?:\s?(?:k|K|m|M|bn|B)\b)?")
# A rate keeps its denominator, so 30 km/h -> 30 km is a changed unit.
QUANTITY = re.compile(
    r"(?<![\w.])(" + NUM + r")\s?((?:" + UNITS + r")(?:/[A-Za-zµ°%]+)?)(?![\w])"
)
RANGE = re.compile(r"(?<![\w.])" + NUM + r"\s?[–—-]\s?" + NUM + r"(?![\w.])")
BOUND = re.compile(
    r"\b(more than|greater than|less than|fewer than|at least|at most|no more than|"
    r"no fewer than|up to|over|under|above|below|exceeding|about|approximately|around|"
    r"roughly|nearly|almost|just over|just under)\s+(" + NUM + r")"
    r"|(>=|<=|&gt;=|&lt;=|&ge;|&le;|&gt;|&lt;|[~<>≤≥≈])\s?(" + NUM + r")",
    re.I,
)
BOUND_CLASS = {
    "more than": ">", "greater than": ">", "over": ">", "above": ">", "exceeding": ">",
    "just over": ">~", ">": ">", "less than": "<", "fewer than": "<", "under": "<",
    "below": "<", "just under": "<~", "<": "<", "at least": ">=", "no fewer than": ">=",
    "≥": ">=", ">=": ">=", "at most": "<=", "no more than": "<=", "up to": "<=", "≤": "<=",
    "<=": "<=", "about": "~", "approximately": "~", "around": "~", "roughly": "~", "~": "~",
    "≈": "~", "nearly": "<~", "almost": "<~",
    # HTML entities, as Markdown renders them
    "&gt;=": ">=", "&lt;=": "<=", "&ge;": ">=", "&le;": "<=", "&gt;": ">", "&lt;": "<",
}
LABELLED = re.compile(
    r"(?<![\w])([A-Za-z]\w{0,10})\s?(>=|<=|!=|&gt;=|&lt;=|&ge;|&le;|&ne;|&gt;|&lt;|[=<>≤≥≠≈])\s?(" + NUM + r")"
)
# Spellings of one operator compare equal, as they do for bounds: x ≥ 5 is x >= 5.
LABEL_OPERATOR = {"≥": ">=", "&gt;=": ">=", "&ge;": ">=", "≤": "<=", "&lt;=": "<=", "&le;": "<=",
                  "≠": "!=", "&ne;": "!=", "&gt;": ">", "&lt;": "<"}
NUMBER = re.compile(r"(?<![\w.])" + NUM + r"(?:%|x\b)?")
# Capitals exclude the multiplication sign (U+00D7) that sits inside À-Þ.
NAME = re.compile(r"\b[A-ZÀ-ÖØ-Þ][\w'’-]*(?:[ \t]+[A-ZÀ-ÖØ-Þ][\w'’-]*)*")
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
    """Return the inline code spans as written, and the text around them."""
    spans, kept, pos, i = [], [], 0, 0
    while True:
        m = BACKTICKS.search(text, i)
        if m is None:
            break
        close = re.compile(r"(?<!`)`{%d}(?!`)" % len(m.group(0))).search(text, m.end())
        if close and not BLANK_LINE.search(text, m.end(), close.start()):
            spans.append(text[m.start():close.end()])
            kept += [text[pos:m.start()], " "]
            pos = i = close.end()
        else:
            i = m.end()  # an unmatched run is literal text
    kept.append(text[pos:])
    return spans, "".join(kept)


def trim_url(url, emphasis=""):
    while url:
        if url[-1] in URL_TRAILING or url[-1] in emphasis:
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
    urls, kept, pos = Counter(), [], 0
    for m in URL.finditer(body):
        before = EMPHASIS_BEFORE.search(body, max(0, m.start() - 3), m.start())
        url = trim_url(m.group(0), before.group(0) if before else "")
        urls[url] += 1
        kept += [body[pos:m.start()], " ", m.group(0)[len(url):]]
        pos = m.end()
    facts["urls"] = urls
    kept.append(body[pos:])
    return facts, "".join(kept)


def extract(text):
    facts, body = strip_protected(text)
    facts["quotes"] = Counter(next(g for g in m.groups() if g) for m in QUOTE.finditer(body))
    facts["versions"] = Counter(m.group(0) for m in VERSION.finditer(body))
    body = VERSION.sub(" ", body)
    facts["currency"] = Counter(re.sub(r"\s", "", m.group(0)) for m in CURRENCY.finditer(body))
    facts["quantities"] = Counter(f"{m.group(1)} {m.group(2)}" for m in QUANTITY.finditer(body))
    facts["labelled"] = Counter(f"{m.group(1)} {LABEL_OPERATOR.get(m.group(2), m.group(2))} {m.group(3)}"
                                for m in LABELLED.finditer(body))
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
    # Bold and italic markers hide sentence starts; an underscore inside a word
    # (IRDN_RAN) is not one, and removing it would invent a name.
    plain = re.sub(r"(?<!\w)[*_]{1,3}|[*_]{1,3}(?!\w)", "", body)
    # A sentence-initial word is kept as a candidate name ("Alice approved it"):
    # dropping it hid real names. Ordinary words capitalized by position are
    # compared without case (see diff), so "Moving" is kept by "moving".
    names = Counter()
    for m in NAME.finditer(plain):
        words = m.group(0).split()
        while words and words[0].rstrip(".,'’-") in FUNCTION_WORDS:
            words = words[1:]
        if words:
            names[" ".join(words).rstrip(".,'’-")] += 1
    facts["names"] = names
    facts["prose"] = plain  # where names were read from, for the comparison
    return facts


def has_phrase(text, phrase, ignore_case=False):
    flags = re.I if ignore_case else 0
    words = r"\s+".join(re.escape(w) for w in phrase.split())  # any spacing or line break
    return re.search(r"(?<![\w])" + words + r"(?![\w])", text, flags) is not None


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
            # rewrite, as written or in the prose it was read from (removing code
            # can join two words). A one-word candidate is compared without case,
            # since it may be an ordinary word capitalized only because it starts
            # a sentence.
            def kept(n, text, prose):
                return any(has_phrase(t, n, ignore_case=" " not in n) for t in (text, prose))
            lost = sorted(n for n in a[kind] if not kept(n, rewrite, b["prose"]))
            added = sorted(n for n in b[kind] if not kept(n, original, a["prose"]))
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
    # An unreadable input is a usage error (2), never a strict difference (1).
    try:
        with open(argv[1], encoding="utf-8") as f:
            original = f.read()
        with open(argv[2], encoding="utf-8") as f:
            rewrite = f.read()
    except (OSError, UnicodeDecodeError) as error:
        print(f"fact_diff: cannot read input: {error}", file=sys.stderr)
        return 2
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
