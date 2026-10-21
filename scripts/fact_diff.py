#!/usr/bin/env python3
"""Partial token check: what a rewrite lost or added against its original.

Usage: python3 fact_diff.py ORIGINAL REWRITE

Strict checks (any difference prints FAIL and exits 1): code blocks (fenced
or indented), inline code, URLs and Markdown link targets, quoted passages (each
compared by count, so a repeated span that changes or goes is caught), numbers
exactly as written with their signs (-20, −5.3, .05, 1e-3, 0x4601, 1920x1080),
version strings (v2.1, 2.4.0-beta),
number+unit pairs (36 MB, 30 km/h, 5 kg/m³, 5 seconds, -$14, $15/hr), labelled values
(p = 0.003, x >= 5), number ranges (2019-2021), and bounds on numbers (over
40,000, just over 40,000, about 36, up to 30, <= 5).
Review lines (exit status unaffected): number words, capitalized names
(sentence-initial ones included), numbers that now appear fewer times, and
changed counts of negations and hedges.

This is a partial check. It cannot verify claims, causes, attribution, the
pairing of values with what they measure, or meaning in general, and exit 0
does not establish that facts were preserved. A Markdown blockquote is read as
prose, since it often holds the writer's own text, and its > markers are
dropped (code inside it is still code), so a quotation without quotation marks
is left to the manual check. Always finish with the manual claim-by-claim
comparison. Exit status: 0 no strict differences found,
1 strict differences found, 2 usage error.
"""

import re
import sys
from collections import Counter

# Code follows CommonMark's block structure. Blockquotes (>) and list items hold
# other blocks, and a line stays in an open one only if it carries its marker or
# indentation (or lazily continues a paragraph). Code is a fenced block, whose
# fence may sit inside a blockquote or list item and closes only on a line of the
# same character at least as long as its opener, or an indented block, four
# columns past its container, which cannot interrupt a paragraph; a heading or
# a thematic break ends a paragraph, so code may follow it directly. An inline
# span closes only on a backtick run of its opener's length.
QUOTE_MARKER = re.compile(r" {0,3}>[ \t]?")
LIST_ITEM = re.compile(r"( {0,3})([-*+]|\d{1,9}[.)])( +)(?=\S)")
EMPTY_ITEM = re.compile(r"( {0,3})([-*+]|\d{1,9}[.)])[ \t]*$")  # its content starts on the next line
FENCE = re.compile(r" {0,3}(`{3,}|~{3,})")
ATX_HEADING = re.compile(r" {0,3}#{1,6}(?:[ \t]|$)")
SETEXT_UNDERLINE = re.compile(r" {0,3}(?:=+|-+)[ \t]*$")
THEMATIC_BREAK = re.compile(r" {0,3}([-*_])(?:[ \t]*\1){2,}[ \t]*$")
# A masked span (inline code, a URL) leaves a placeholder of its own, a private
# use character that is neither a word nor a space character. A quotation that
# starts with one still opens ('https://a.b is required.'), and a quotation is
# compared with its spans put back, so swapping two of them inside it is caught.
# A private use character the text already contains is never a placeholder, and
# a URL ends where a generated placeholder starts, so its key never holds one.
MASK_BASE = 0xF0000
PLACEHOLDERS = "\U000F0000-\U0010FFFF"
MASKED = re.compile("[" + PLACEHOLDERS + "]")
BLOCKQUOTE = re.compile(r"(?m)^ {0,3}(?:>[ \t]?)+")
BACKTICKS = re.compile(r"`+")
BLANK_LINE = re.compile(r"\n[ \t]*\n")
# Between a value and its unit, label or operator, or a link and its target:
# spaces of any kind (a non-breaking space included) and at most one line
# break, indented or not, but never a blank line (5\u00a0kg, 5\n  ms, p  =  0.003).
GAP = r"[^\S\n]*(?:\n[^\S\n]*)?"
URL_START = r'https?://[^\s<>"'  # completed with the placeholders a URL stops at
URL = re.compile(URL_START + "]+")
# Every Markdown link target is protected with its own boundaries, web URLs
# included: an inline target ([guide](docs/a.md), [x](#setup), [x]( https://a.b))
# and a reference definition ([id]: https://a.b/c!), each possibly on the next
# line. A definition holds only its target and an optional title on its line, and
# may sit inside a list item; a footnote ([^1]: text) or a labelled sentence
# ([Status]: Glad to help.) is not one. Angle brackets (<https://a.b>) are not
# part of the counted target.
LINK_TARGET = re.compile(
    r"\]\(" + GAP + r"(\S+)"
    r"|(?m:^)[ \t]*(?:(?:[-*+]|\d{1,9}[.)])[ \t]+)?\[(?!\^)[^\]\n]+\]:" + GAP + r"(\S+)"
    r"""(?=[ \t]*(?:"[^"\n]*"|'[^'\n]*'|\([^)\n]*\))?[ \t]*(?m:$))"""
)
# Trailing sentence punctuation is not part of a URL (as in GitHub's autolinks),
# nor is a closing quotation mark (“see https://a.b/c”), and a closing bracket is
# part of it only when the URL opened one: a_(x)/old. A Markdown link target
# ends at the parenthesis that closes it: **[API](https://a.b/c)**.
# A trailing * _ or ~ is dropped only when the same marker opened just before
# the URL, or just before a bracket or quote mark that opens it (**https://a.b/c**,
# **(https://a.b/c)**), so https://a.b/user_ keeps its underscore. An autolink
# (<https://a.b/c!>) keeps everything up to its closing >.
URL_TRAILING = ".,;:!?'\"”’»"
URL_CLOSERS = {")": "(", "]": "["}
EMPHASIS_BEFORE = re.compile(r"([*_~]+)[(\[\"'“‘]?$")
# One-character quotes and long single-quoted passages count too: a changed
# letter inside quotation marks is a changed quotation. A passage may run over
# line breaks. In curly double quotes or guillemets it may also run over blank
# lines, since their opening and closing marks differ; straight and single
# quotes stop at a blank line, so a stray mark (12") cannot pair with one
# paragraphs later. An apostrophe followed by a letter
# (don't) stays inside a single-quoted passage; one after a letter (students')
# never opens one. A plural possessive stays inside the passage when the next
# single mark in the paragraph closes rather than opens: 'the students' books
# are here'. An abbreviated decade ('90s) never opens a passage; a two-digit
# start ('12 users were fired') does, since it cannot be told from a year ('24).
# Straight marks honour Markdown backslash escapes: a backslash is read only
# together with the character after it, so an even run (\\) is literal and the
# mark after it is real, while an escaped mark (\' or \") is part of the passage
# and never ends it. A passage between two escaped double marks (\"text\") is a
# quotation too. The marks themselves are not compared, so the curly-to-straight
# fix of P20 passes.
PARA = r"(?:(?!\n[ \t]*\n)[^{q}])"
PLAIN = r"(?:(?!\n[ \t]*\n)[^{q}\\])"  # a straight passage's text; a backslash only as an escape
POSSESSIVE = r"(?<=s){q}(?=(?:(?!\n[ \t]*\n)[^{q}{o}])*[^\s{q}]{q}(?!\w))"
CURLY_POSSESSIVE = POSSESSIVE.format(q="’", o="‘")
STRAIGHT_POSSESSIVE = POSSESSIVE.format(q="'", o="'")
YEAR = r"(?!\d{2}s\b)"
ESCAPED = r"\\(?:[^\n]|\n(?![ \t]*\n))"
EVEN_BACKSLASHES = r"(?<!\\)(?:\\\\)*"
QUOTE = re.compile(
    EVEN_BACKSLASHES + r'"((?:' + ESCAPED + "|" + PLAIN.format(q='"') + r')+)"'
    # Between escaped marks, an escaped backslash takes an escaped mark right
    # after it as text (\"say \\\" now\"), so it never closes the passage. Each
    # pair of backslashes matches one way only, so nothing backtracks.
    r"|" + EVEN_BACKSLASHES + r'\\"((?:' + PLAIN.format(q='"') + r'|\\\\(?:\\")?|\\[^"\\\n])+?)(?<!\\)\\"'
    r"|“([^”]+)”"
    r"|«([^»]+)»"
    r"|‘" + YEAR + r"((?:" + PARA.format(q="’") + r"|’(?=\w)|" + CURLY_POSSESSIVE + r")+?)"
    r"(?!" + CURLY_POSSESSIVE + r")’(?!\w)"
    r"|(?<![\w'’\\])'(?=\S)" + YEAR
    + r"((?:" + ESCAPED + "|" + PLAIN.format(q="'") + r"|'(?=\w)|" + STRAIGHT_POSSESSIVE + r")+?)"
    r"(?!" + STRAIGHT_POSSESSIVE + r")'(?!\w)"
)
# A v-prefixed version, or a three-part one with a pre-release or build suffix
# (2.4.0-beta, 1.0.0+build.5); a bare 2.4.0 is compared as a number. Either
# form keeps its whole suffix (v2.4.0+build.7).
VERSION = re.compile(
    r"(?<![\w.])(?:[vV]\d+(?:\.\d+)*(?:[-.+][A-Za-z0-9]+)*"
    r"|\d+\.\d+\.\d+(?:[-+][0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)+)\b"
)
UNITS = (
    r"%|‰|°[CF]?|x|ms|µs|us|ns|s|sec|secs|min|mins|h|hr|hrs|KB|kB|MB|GB|TB|PB|Kb|Mb|Gb|"
    r"KiB|MiB|GiB|TiB|Hz|kHz|MHz|GHz|Msps|ksps|fps|px|pt|dB|dBm|mm|cm|m|km|g|kg|mg|lb|lbs|"
    r"oz|mi|ft|V|mV|W|kW|MW|mA|mAh|Wh|kWh|mmHg|bpm|rpm|"
    r"(?:nano|micro|milli)?seconds?|minutes?|hours?|days?|weeks?|months?|years?"
)
# An optional sign (ASCII hyphen-minus, Unicode minus or plus) is part of the
# number, so -20 -> 20 is a changed value. The lookbehinds below keep the hyphen
# in a range or date (2019-2021) from being read as a sign. A leading-dot decimal
# (.05) and an exponent (1.5e3, 1e-3) are part of the number.
NUM = r"[+−-]?(?:\d+(?:[.,]\d+)*|\.\d+)(?:[eE][+−-]?\d+)?"
# A unit keeps its power, written as a superscript, after ^, or as a bare 2 or 3
# (5 kg/m³, 5 m^2, 5 kg/m2), so a changed power or denominator is caught; x and
# % take no digit power, so 0x4601 and 90x128 are not quantities.
POWER = r"(?:[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+|(?<![x%])(?:\^-?[0-9]+|[23](?![0-9])))?"
# A sign before the symbol (-$14) is kept, but not a range's hyphen ($10-$20),
# and so is a rate with its power ($15/hr, $15/m²), as for units.
CURRENCY = re.compile(
    r"(?:(?<![\w$€£¥₹])[+−-])?[$€£¥₹]\s?" + NUM + r"(?:\s?(?:k|K|m|M|bn|B)\b)?(?:/[A-Za-z]+" + POWER + r")?"
)
# A rate keeps its denominator, so 30 km/h -> 30 km is a changed unit, and a
# denominator that cannot be read still leaves the number and base unit
# compared (5 kg).
QUANTITY = re.compile(
    r"(?<![\w.])(" + NUM + r")" + GAP + r"((?:" + UNITS + r")" + POWER + r"(?:/[A-Za-zµ°%]+" + POWER + r")?)(?![\w])"
)
# A period after a range ends the sentence unless a digit follows (0.05–0.5.).
# A range may wrap after its dash but not before it: a line that starts with a
# dash is a list item (- 5\n- 10 is two values, not 5-10).
RANGE = re.compile(r"(?<![\w.])" + NUM + r"[^\S\n]*[–—-]" + GAP + NUM + r"(?!\w|\.\d)")
BOUND_WORDS = (
    "more than", "greater than", "less than", "fewer than", "at least", "at most", "no more than",
    "no fewer than", "no less than", "no greater than", "not more than", "not fewer than",
    "not less than", "not greater than", "up to", "over", "under", "above", "below", "exceeding",
    "about", "approximately", "around", "roughly", "nearly", "almost", "just over", "just under",
)
# A bound phrase may wrap onto the next line (more\nthan 5), and a bound may be
# on a price, signed or not (under €500, > $40, under -$40). A negated phrase is read whole: no less than 5
# is >= 5, the same bound as at least 5.
BOUNDED = r"((?:[+−-]?[$€£¥₹]\s?)?" + NUM + r")"
BOUND = re.compile(
    r"\b(" + "|".join(w.replace(" ", r"\s+") for w in BOUND_WORDS) + r")\s+" + BOUNDED +
    # A tilde of ~~strikethrough~~ is not "about".
    r"|(>=|<=|&gt;=|&lt;=|&ge;|&le;|&gt;|&lt;|[<>≤≥≈]|(?<!~)~(?!~))" + GAP + BOUNDED,
    re.I,
)
BOUND_CLASS = {
    "more than": ">", "greater than": ">", "over": ">", "above": ">", "exceeding": ">",
    "just over": ">~", ">": ">", "less than": "<", "fewer than": "<", "under": "<",
    "below": "<", "just under": "<~", "<": "<", "at least": ">=", "no fewer than": ">=",
    "no less than": ">=", "not fewer than": ">=", "not less than": ">=", "no greater than": "<=",
    "not more than": "<=", "not greater than": "<=",
    "≥": ">=", ">=": ">=", "at most": "<=", "no more than": "<=", "up to": "<=", "≤": "<=",
    "<=": "<=", "about": "~", "approximately": "~", "around": "~", "roughly": "~", "~": "~",
    "≈": "~", "nearly": "<~", "almost": "<~",
    # HTML entities, as Markdown renders them
    "&gt;=": ">=", "&lt;=": "<=", "&ge;": ">=", "&le;": "<=", "&gt;": ">", "&lt;": "<",
}
LABELLED = re.compile(
    r"(?<![\w])([A-Za-z]\w*)" + GAP + r"(>=|<=|!=|&gt;=|&lt;=|&ge;|&le;|&ne;|&gt;|&lt;|[=<>≤≥≠≈])" + GAP + r"(" + NUM + r")"
)
# Spellings of one operator compare equal, as they do for bounds: x ≥ 5 is x >= 5.
LABEL_OPERATOR = {"≥": ">=", "&gt;=": ">=", "&ge;": ">=", "≤": "<=", "&lt;=": "<=", "&le;": "<=",
                  "≠": "!=", "&ne;": "!=", "&gt;": ">", "&lt;": "<"}
# A compact dimension is one value with its unit and power, attached or after a
# space (1920x1080px, 1.5x2.5cm, 3x4m², 10x20 cm); 0x4601 is hex, not 0 by 4601.
DIMENSION = re.compile(
    r"(?<![\w.])(?!0[xX])(\d+(?:\.\d+)?(?:[xX×]\d+(?:\.\d+)?)+)"
    r"(?:([A-Za-zµ°%]+" + POWER + r")|[^\S\n]+((?:" + UNITS + r")" + POWER + r")(?!\w))?(?!\w)"
)
# A hex literal (0x4601) is one number, compared as written.
NUMBER = re.compile(r"(?<![\w.])(?:0[xX][0-9A-Fa-f]+\b|" + NUM + r"(?:%|x\b)?)")
# Bold and italic are removed where a marker run opens and the same run closes
# it within a paragraph, as Markdown reads them: an asterisk pair may touch a
# word (**5**kg), an underscore pair may not (timeout_, IRDN_RAN). Where removing
# a marker would join two words or a word and a number, a space takes its place,
# so a*2 and b*3 keep both values; a lone marker stays, so 2**10 is not 210. A
# run may sit right next to another marker, so nested emphasis (**5 *kg***)
# unwraps one level per pass.
INLINE = r"((?:[^\n]|\n(?![ \t]*\n))+?)"
EMPHASIS = (
    re.compile(r"(?<!\*)(\*{1,3})(?!\s)" + INLINE + r"(?<!\s)\1"),
    re.compile(r"(?<![\w_])(_{1,3})(?!\s)" + INLINE + r"(?<!\s)\1(?!\w)"),
)
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


def indent_of(line):
    """Count the leading spaces of a line whose tabs are already expanded."""
    return len(line) - len(line.lstrip(" "))


def can_interrupt(item):
    """Only a bullet, or an ordered list starting at 1, can interrupt a paragraph."""
    return item.group(2) in "-*+" or item.group(2)[:-1] == "1"


def list_kind(item):
    """Name the list an item belongs to: its bullet, or an ordered list's delimiter."""
    marker = item.group(2)
    return marker if marker in "-*+" else marker[-1]


def split_code(text):
    """Return the code blocks (fenced or indented) as written, and the text outside them."""
    blocks, kept, blanks = [], [], []
    # ">" for a blockquote, or (content indent, list kind) for a list item; outermost first
    containers = []
    code = None      # the open code block: [lines, container depth, closing fence or None]
    para = False     # the last line was paragraph text, which a lazy line may continue
    for raw in text.splitlines(keepends=True):
        rest = raw.rstrip("\r\n").expandtabs(4)
        matched = 0
        for container in containers:
            if container == ">":
                m = QUOTE_MARKER.match(rest)
                if m is None:
                    break
                rest = rest[m.end():]
            elif rest.strip():  # a blank line stays in a list item
                if indent_of(rest) < container[0]:
                    break
                rest = rest[container[0]:]
            matched += 1
        if matched < len(containers):
            item = LIST_ITEM.match(rest)
            # The next item of the same list (10. then 2.) starts a block; it is
            # not a new list interrupting the paragraph.
            sibling = item and containers[matched] != ">" and containers[matched][1] == list_kind(item)
            starts_block = (QUOTE_MARKER.match(rest) or FENCE.match(rest) or ATX_HEADING.match(rest)
                            or THEMATIC_BREAK.match(rest) or (item and (can_interrupt(item) or sibling)))
            if para and rest.strip() and not starts_block:
                kept.append(raw)  # a lazy continuation keeps every container open
                continue
            del containers[matched:]
            para = False
        if code and code[1] > len(containers):  # its container closed, so it did too
            blocks.append("".join(code[0]))
            kept += ["\n"] + blanks
            code, blanks = None, []
        if code and code[2]:
            code[0].append(raw)
            if code[2].match(rest):
                blocks.append("".join(code[0]))
                kept.append("\n")
                code = None
            continue
        # New containers; four columns in is code or paragraph text, never a marker.
        while indent_of(rest) < 4 and not THEMATIC_BREAK.match(rest):  # - - - is no item
            m = QUOTE_MARKER.match(rest)
            if m:
                containers.append(">")
                rest, para = rest[m.end():], False
                continue
            m = LIST_ITEM.match(rest)
            if m and (not para or can_interrupt(m)):
                # Five or more spaces after the marker start indented code one column in.
                width = m.end() if len(m.group(3)) <= 4 else m.end(2) + 1
                containers.append((width, list_kind(m)))
                rest, para = rest[width:], False
                continue
            m = EMPTY_ITEM.match(rest)
            if m and not para:  # an empty item never interrupts a paragraph
                containers.append((m.end(2) + 1, list_kind(m)))
                rest = ""
            break
        if code:  # an open indented block
            if not rest.strip():
                blanks.append(raw)  # kept only if the block continues after it
                continue
            if indent_of(rest) >= 4 and code[1] == len(containers):
                code[0] += blanks + [raw]
                blanks = []
                continue
            blocks.append("".join(code[0]))
            kept += ["\n"] + blanks
            code, blanks = None, []
        if not rest.strip():
            kept.append(raw)
            para = False
            continue
        if indent_of(rest) >= 4 and not para:
            code = [[raw], len(containers), None]
            continue
        m = FENCE.match(rest)
        # A backtick fence's info string cannot contain a backtick.
        if m and not (m.group(1)[0] == "`" and "`" in rest[m.end():]):
            closer = re.compile(r" {0,3}" + re.escape(m.group(1)[0]) + "{%d,}[ \t]*$" % len(m.group(1)))
            code, para = [[raw], len(containers), closer], False
            continue
        kept.append(raw)
        # A heading or thematic break ends the paragraph: Title\n---, # Title, ***.
        para = not ((para and SETEXT_UNDERLINE.match(rest)) or ATX_HEADING.match(rest)
                    or THEMATIC_BREAK.match(rest))
    if code:  # an unclosed block runs to the end of the text
        blocks.append("".join(code[0]))
        kept += ["\n"] + blanks
    return blocks, "".join(kept)


def mask(span, masked):
    """Record a masked span and return an unused placeholder that stands for it."""
    code = MASK_BASE + len(masked)
    while chr(code) in masked:
        code += 1
    masked[chr(code)] = span
    return chr(code)


def split_inline_code(text, masked):
    """Return the inline code spans as written, and the text around them."""
    spans, kept, pos, i = [], [], 0, 0
    while True:
        m = BACKTICKS.search(text, i)
        if m is None:
            break
        backslashes = len(text[:m.start()]) - len(text[:m.start()].rstrip("\\"))
        if backslashes % 2:  # an escaped backtick (\`) is literal and opens nothing
            i = m.start() + 1
            continue
        close = re.compile(r"(?<!`)`{%d}(?!`)" % len(m.group(0))).search(text, m.end())
        if close and not BLANK_LINE.search(text, m.end(), close.start()):
            spans.append(text[m.start():close.end()])
            kept += [text[pos:m.start()], mask(spans[-1], masked)]
            pos = i = close.end()
        else:
            i = m.end()  # an unmatched run is literal text
    kept.append(text[pos:])
    return spans, "".join(kept)


def trim_url(url, emphasis=""):
    """Trim trailing punctuation, unmatched brackets, and supplied emphasis markers."""
    while url:
        if url[-1] in URL_TRAILING or url[-1] in emphasis:
            url = url[:-1]
        elif url[-1] in URL_CLOSERS and url.count(url[-1]) > url.count(URL_CLOSERS[url[-1]]):
            url = url[:-1]
        else:
            break
    return url


def link_target(url):
    """Cut a Markdown link target at the parenthesis that closes the link."""
    depth, i = 0, 0
    while i < len(url):
        c = url[i]
        if c == "\\":  # an escaped character (a\)b) is part of the target
            i += 2
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            if depth == 0:
                return url[:i]
            depth -= 1
        i += 1
    return url


def split_link_targets(text, masked):
    """Return the Markdown link targets, and the text with them masked."""
    targets, kept, pos = Counter(), [], 0
    m = LINK_TARGET.search(text)
    while m:
        run, start = (m.group(1), m.start(1)) if m.group(1) else (m.group(2), m.start(2))
        if run.startswith("<"):  # <docs/a b.md> may hold spaces; it ends at its >
            close = text.find(">", start)
            target = text[start:close + 1] if close != -1 and "\n" not in text[start:close] else ""
        else:
            target = link_target(run) if m.group(1) else run
        if target:
            targets[target[1:-1] if target.startswith("<") else target] += 1
            kept += [text[pos:start], mask(target, masked)]
            pos = start + len(target)
        m = LINK_TARGET.search(text, max(start + len(target), m.start() + 1))
    kept.append(text[pos:])
    return targets, "".join(kept)


def strip_protected(text):
    """Split a text into its protected spans, the prose left over, and the masked spans."""
    # A private use character already in the text stands for itself.
    facts, masked = {}, {c: c for c in MASKED.findall(text)}
    blocks, body = split_code(text)
    facts["code_blocks"] = Counter(blocks)
    # Blockquote markers in the prose are dropped (code keeps its own).
    spans, body = split_inline_code(BLOCKQUOTE.sub("", body), masked)
    facts["inline_code"] = Counter(spans)
    urls, body = split_link_targets(body, masked)
    # A bare URL outside a link: the search resumes where each URL ends, so text
    # trimmed from its end is searched again. A URL stops at an inline-code
    # placeholder but keeps a private use character the text itself contains.
    stops = "".join(c for c, span in masked.items() if span != c)
    url_pattern = re.compile(URL_START + stops + "]+") if stops else URL
    kept, pos = [], 0
    m = url_pattern.search(body)
    while m:
        if body.endswith("<", 0, m.start()) and body.startswith(">", m.end()):
            url = m.group(0)
        else:
            before = EMPHASIS_BEFORE.search(body, max(0, m.start() - 4), m.start())
            url = trim_url(m.group(0), before.group(1) if before else "")
        urls[url] += 1
        kept += [body[pos:m.start()], mask(url, masked)]
        pos = m.start() + len(url)
        m = url_pattern.search(body, pos)
    facts["urls"] = urls
    kept.append(body[pos:])
    return facts, "".join(kept), masked


def unwrap(m):
    """Keep what a marker pair encloses, with a space where removal would join words."""
    text, inner = m.string, m.group(2)
    before = text[m.start() - 1] if m.start() else " "
    after = text[m.end()] if m.end() < len(text) else " "
    def joins(a, b):
        return (a.isalnum() or a == "_") and (b.isalnum() or b == "_")
    return (" " if joins(before, inner[0]) else "") + inner + (" " if joins(inner[-1], after) else "")


def strip_emphasis(text):
    """Remove paired bold and italic markers, keeping the words they enclose."""
    for _ in range(3):  # each pass unwraps one level of nesting (**a *b* c**)
        before = text
        for pattern in EMPHASIS:
            text = pattern.sub(unwrap, text)
        if text == before:
            break
    return text


def extract(text):
    """Return token counts, review counts, and prose for the fact comparison."""
    facts, body, masked = strip_protected(text)
    facts["quotes"] = Counter(MASKED.sub(lambda s: masked[s.group(0)], next(g for g in m.groups() if g))
                              for m in QUOTE.finditer(body))
    # Bold and italic go before any value is read, so removing them (P18)
    # changes no value; they also hide sentence starts from the name check.
    body = strip_emphasis(body)
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
        num = re.sub(r"\s", "", num)  # a price may be written $ 40
        bounds[f"{BOUND_CLASS[' '.join(word.lower().split())]} {num}"] += 1
    facts["bounds"] = bounds
    # A dimension is read last, so a bound or label beside it reads as before
    # (about 10x20 cm is ~ 10; from 5x15 = 75 has no label).
    dimensions = Counter(" ".join(filter(None, (m.group(1), m.group(2) or m.group(3))))
                         for m in DIMENSION.finditer(body))
    body = DIMENSION.sub(" ", body)
    # Numbers are compared exactly as written: 3,000 and 3000 differ, and so do
    # 1,5 and 1.5. A rewrite should not reformat data (hard rule 4).
    facts["numbers"] = dimensions + Counter(m.group(0).rstrip(".") for m in NUMBER.finditer(body))
    facts["number_words"] = Counter(m.group(0).lower() for m in NUMBER_WORDS.finditer(body))
    facts["negations"] = len(NEGATION.findall(body))
    facts["hedges"] = len(HEDGE.findall(body))
    # A sentence-initial word is kept as a candidate name ("Alice approved it"):
    # dropping it hid real names. Ordinary words capitalized by position are
    # compared without case (see diff), so "Moving" is kept by "moving".
    names = Counter()
    for m in NAME.finditer(body):
        words = m.group(0).split()
        while words and words[0].rstrip(".,'’-") in FUNCTION_WORDS:
            words = words[1:]
        if words:
            names[" ".join(words).rstrip(".,'’-")] += 1
    facts["names"] = names
    facts["prose"] = body  # where names were read from, for the comparison
    return facts


def has_phrase(text, phrase, ignore_case=False):
    """Check for a whole phrase, allowing varied whitespace and optional case folding."""
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
        """Show a span with its counts when it appears in both texts."""
        return f"{t} ({a[t]} -> {b[t]})" if a[t] and b[t] else t
    return (sorted(show(t) for t in a if a[t] > b[t]),
            sorted(show(t) for t in b if b[t] > a[t]))


def diff(original, rewrite):
    """Return strict and review differences as lost and added items by kind."""
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
                """Check a text as written and as prose for a name, ignoring case for one word."""
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
    """Print token differences and return 0, 1 for strict changes, or 2 for bad input."""
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
