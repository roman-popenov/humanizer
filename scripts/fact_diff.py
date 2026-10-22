#!/usr/bin/env python3
"""Partial token check: what a rewrite lost or added against its original.

Usage: python3 fact_diff.py ORIGINAL REWRITE

What it guarantees. A strict difference prints FAIL and exits 1:
- Byte for byte, line endings included: code blocks (fenced or indented),
  read without the markers and indent of the list item or quote that holds
  them, inline code spans, and quoted passages ("...", '...', “...”, «...»).
  Each is compared by count, so a repeated span that changes or goes is caught.
- Exactly as written: URLs of any scheme, CommonMark autolinks
  (<mailto:a@b.c>), bare email addresses, and Markdown link targets.
- As values, after spacing is normalised, so rewrapping or respacing never
  fails: numbers with their signs, percent signs, multipliers and magnitudes
  (-20, −5.3, .05, 1e-3, -0x10, 5 %, 5x, 50K, 3 bn), dimensions
  (1920x1080px, 10 x 20 cm), versions (v2.1, 2.4.0-beta), numbers with
  units and rates (36 MB, 5 A, 100 Mbps, 5 percent, a 5-minute timeout,
  30 km/h, 5 kg / m³, 5 mg/kg/day), tolerances (±5 mm, 5±2 mm), prices
  (-$14, $15/hr, 50 €, 50 M€), labelled values (p = 0.003, OR = 2), ranges
  (2019-2021, 1 - 3 ms), bounds and comparisons (over 40,000, not over
  40,000, just over 40,000, about 36, up to 30, <= 5, != 3), and version
  constraints and pins (>= 2.4.0-beta, ^v2.4, ^1.2.3, ~> 1.2, == 1.2.3).
Never a difference: Markdown formatting outside code and quotations (bold and
italic, list markers including a numbered list's numbers, line wrapping, and a
prose line's ending, CRLF or LF). A value or code span never reaches across a
block (paragraph, heading, list item or quote), as in CommonMark.
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

# Code follows CommonMark's block structure as GitHub renders it (cmark-gfm).
# Blockquotes (>) and list items hold other blocks, and a line stays in an open
# one only if it carries its marker or indentation, or lazily continues a
# paragraph, which a line that starts a block never does; an item that opened
# empty ends at a blank line less indented than its content. Code is a fenced
# block, whose fence may sit inside a blockquote or list item and closes only on
# a line of the same character at least as long as its opener, or an indented
# block, four columns past its container, which cannot interrupt a paragraph; a
# heading or a thematic break ends a paragraph, so code may follow it directly.
# An inline span closes only on a backtick run of its opener's length.
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
# A blank line, with either line ending (CRLF or LF). The block reader also puts
# a boundary line before every block of the prose it returns (a paragraph,
# heading, list item or quote): a placeholder that stands for nothing, so a code
# span or a value never reaches across a block, while a quotation may and reads
# as written.
BLANK = r"\n[ \t\r]*\n"
BLANK_LINE = re.compile(BLANK)
# Between a value and its unit, label or operator, or a link and its target:
# spaces of any kind (a non-breaking space included) and at most one line
# break, indented or not, but never a blank line (5\u00a0kg, 5\n  ms, p  =  0.003).
GAP = r"[^\S\n]*(?:\n[^\S\n]*)?"
# A URL of any scheme (https://, ftp://, ssh://), also right after punctuation
# (...https://a.b). A scheme starts after a non-alphanumeric and is at most 32
# characters, so a long word without :// is scanned once, not once per letter.
URL_START = r'(?<![A-Za-z0-9])[A-Za-z][A-Za-z0-9+.-]{0,31}://[^\s<>"'  # completed with the placeholders a URL stops at
URL = re.compile(URL_START + "]+")
# A CommonMark autolink of any scheme (<https://a.b/c!>, <mailto:a@b.c>) keeps
# everything up to its >, and a bare email address is a destination too, since
# GitHub links it.
AUTOLINK = re.compile(r"<([A-Za-z][A-Za-z0-9+.-]{1,31}:[^\s<>]*)>")
EMAIL = re.compile(r"(?<![\w.+-])[\w.+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
# Every Markdown link target is protected with its own boundaries, web URLs
# included: an inline target ([guide](docs/a.md), [x](#setup), [x]( https://a.b))
# and a reference definition ([id]: https://a.b/c!), each possibly on the next
# line. A definition holds only its target and an optional title on its line (a
# title may hold escapes and run onto the next line), and may sit inside a list
# item; a footnote ([^1]: text) or a labelled sentence ([Status]: Glad to help.)
# is not one. A target in angle brackets may hold spaces (<docs/a b.md>), and the
# brackets are not part of the counted target.
LINK_TARGET = re.compile(
    r"\]\(" + GAP + r"(\S+)"
    r"|(?m:^)[ \t]*(?:(?:[-*+]|\d{1,9}[.)]|[" + PLACEHOLDERS + r"])[ \t]+)?\[(?!\^)[^\]\n]+\]:" + GAP + r"(<[^>\n]*>|\S+)"
    r"""(?=[ \t]*(?:"(?:[^"\\\n]|\\.|\n(?![^\S\n]*\n))*"|'(?:[^'\\\n]|\\.|\n(?![^\S\n]*\n))*'"""
    r"""|\((?:[^()\\\n]|\\.|\n(?![^\S\n]*\n))*\))?[ \t\r]*(?m:$))"""
)
# Trailing sentence punctuation is not part of a URL (as in GitHub's autolinks),
# nor is a closing quotation mark (“see https://a.b/c”), and a closing bracket is
# part of it only when the URL opened one: a_(x)/old. A Markdown link target
# ends at the parenthesis that closes it: **[API](https://a.b/c)**.
# A trailing * _ or ~ is dropped only when the same marker opened just before
# the URL, or just before a bracket or quote mark that opens it (**https://a.b/c**,
# **(https://a.b/c)**), so https://a.b/user_ keeps its underscore.
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
# quotation too. A straight double mark right after a digit is an inch mark
# (12" wide) and never opens a passage. The marks themselves are not compared,
# so the curly-to-straight fix of P20 passes.
PARA = r"(?:(?!" + BLANK + r")[^{q}])"
PLAIN = r"(?:(?!" + BLANK + r")[^{q}\\])"  # a straight passage's text; a backslash only as an escape
POSSESSIVE = r"(?<=s){q}(?=(?:(?!" + BLANK + r")[^{q}{o}])*[^\s{q}]{q}(?!\w))"
CURLY_POSSESSIVE = POSSESSIVE.format(q="’", o="‘")
STRAIGHT_POSSESSIVE = POSSESSIVE.format(q="'", o="'")
YEAR = r"(?!\d{2}s\b)"
ESCAPED = r"\\(?:[^\n]|\n(?![ \t\r]*\n))"
EVEN_BACKSLASHES = r"(?<!\\)(?:\\\\)*"
QUOTE = re.compile(
    EVEN_BACKSLASHES + r'(?<!\d)"((?:' + ESCAPED + "|" + PLAIN.format(q='"') + r')+)"'
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
# A bare capital that is also a letter or a label (L, A, N, J) is a unit only
# after a space: 2L is two times L and 5A is a room, but 5 A is five amperes.
UNITS = (
    r"%|‰|°[CF]?|x|ms|µs|us|ns|s|sec|secs|min|mins|h|hr|hrs|KB|kB|MB|GB|TB|PB|Kb|Mb|Gb|"
    r"KiB|MiB|GiB|TiB|bps|kbps|Kbps|Mbps|Gbps|Hz|kHz|MHz|GHz|Msps|ksps|fps|px|pt|dB|dBm|"
    r"nm|µm|um|mm|cm|m|km|g|kg|mg|lb|lbs|oz|mi|ft|yd|mph|kph|gal|mL|ml|µL|uL|(?<=\s)L|"
    r"V|mV|kV|(?<=\s)A|mA|µA|kA|Ah|mAh|W|mW|kW|MW|GW|VA|kVA|Wh|mWh|kWh|MWh|Ω|kΩ|MΩ|"
    r"µF|uF|nF|pF|mH|µH|(?<=\s)N|kN|Nm|Pa|hPa|kPa|MPa|GPa|bar|mbar|psi|mmHg|(?<=\s)J|kJ|MJ|"
    r"cal|kcal|mol|mmol|µmol|umol|nmol|pmol|µg|ug|mcg|ng|pg|nL|pL|dL|ps|fs|µV|uV|nV|nA|pA|µW|uW|nW|mΩ|"
    r"ppm|ppb|lm|lx|bpm|rpm|"
    r"(?:nano|micro|milli)?seconds?|minutes?|hours?|days?|weeks?|months?|years?|"
    r"(?:kilo|centi|milli)?(?:met(?:er|re)s?|grams?|lit(?:er|re)s?)|miles?|feet|foot|inch(?:es)?|"
    r"pounds?|ounces?|degrees?|percent|bytes?|bits?|pixels?|volts?|watts?|amps?|amperes?|ohms?"
)
# An optional sign (ASCII hyphen-minus, Unicode minus or plus) is part of the
# number, so -20 -> 20 is a changed value. The lookbehinds below keep the hyphen
# in a range or date (2019-2021) from being read as a sign. A leading-dot decimal
# (.05) and an exponent (1.5e3, 1e-3) are part of the number.
# A sign: plus, hyphen-minus, Unicode minus, or plus-minus (±5 mm, ∓0.2).
SIGN = "[+−±∓-]"
# A plus-minus may stand apart from its digits (± 5 mm); the space is dropped
# wherever a value is compared.
NUM = r"(?:[+−-]|[±∓][^\S\n]?)?(?:\d+(?:[.,]\d+)*|\.\d+)(?:[eE][+−-]?\d+)?"
# A unit keeps its power, written as a superscript, after ^, or as a bare 2 or 3
# (5 kg/m³, 5 m^2, 5 kg/m2), so a changed power or denominator is caught; x and
# % take no digit power, so 0x4601 and 90x128 are not quantities.
POWER = r"(?:[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+|(?<![x%])(?:\^-?[0-9]+|[23](?![0-9])))?"
# A plus or minus sign (not a hyphen, which may be a dash) spaced from its digits
# is the value's own only at the start of a block or after punctuation such as
# : ( = |, where it cannot be an operator. After a word or a value it is one:
# 8 runs + 25 checks and size − 1 add and subtract.
SPACED_SIGN = re.compile(r"(?m)(^|[^\w.,)\]%°‰\s])(\s*)([+−])[^\S\n]+(?=\d)")
# A unit written onto its number or slash: letters in any script (kg, µF, Ω) or a sign.
UNIT_CHARS = r"(?:[^\W\d_]|[%°‰])+"
# A rate's denominator, step by step, spaced or not (kg/m³, $15 / user, 5 MB/秒,
# 5 mg/kg/day). A unit is always a denominator, even before another value
# (30 km/h ±2 km/h); another word is one only when no value follows it, since a
# slash before a value's label separates two values (1.3 ms / overall 1.5 ms).
# After a slash, a bare capital (L, A, N, J) is a unit with or without a space.
PER = (r"[^\S\n]?/[^\S\n]?(?:(?:" + UNITS.replace("(?<=\\s)", "") + r")" + POWER + r"(?!\w)|"
       + UNIT_CHARS + POWER + r"(?!\w)(?![^\S\n]*(?:" + SIGN + r"?\.?\d|[$€£¥₹])))")
DENOMINATOR = "(?:" + PER + ")*"
# A sign before the symbol (-$14) is kept, but not a range's hyphen ($10-$20),
# and so is a rate with its power ($15/hr, $15/m²), as for units.
CURRENCY = re.compile(
    r"(?:(?<![\w$€£¥₹])" + SIGN + r")?([$€£¥₹])\s?" + NUM + r"(?:\s?(?:k|K|m|M|bn|B)\b)?" + DENOMINATOR
)
# A symbol may follow its amount (50 €, 50 M€, 50 €/hr), and is then compared as
# if it came first (€50, €50M, €50/hr). A symbol belongs to the amount written
# onto it after it (5 $20), else to an amount before it (50 € 2 nights is €50),
# else to an amount after it ($ 50).
CURRENCY_AFTER = re.compile(
    # The amount may end a multiplication chain (3x50 €, 3 x 50 €: 3 times €50).
    r"(?:(?<![\w.$€£¥₹])|(?<=\d[xX×]))(" + SIGN + r"?)((?:\d+(?:[.,]\d+)*|\.\d+)(?:[eE][+−-]?\d+)?)((?:[^\S\n]?(?:k|K|m|M|bn|B))?)" + GAP
    + r"([$€£¥₹])(?![$€£¥₹]|" + SIGN + r"?\.?\d)(" + DENOMINATOR + r")(?!\w)"
)
# A rate keeps its denominator, so 30 km/h -> 30 km is a changed unit, and a
# denominator that cannot be read still leaves the number and base unit
# compared (5 kg). A hyphen may join the number and unit (a 5-minute timeout),
# but not x, which after a hyphen is a variable (255-x), not a multiplier.
QUANTITY = re.compile(
    r"(?<![\w.])(" + NUM + r")(?:" + GAP + r"|-(?!x\b))((?:" + UNITS + r")" + POWER + DENOMINATOR + r")(?![\w])"
)
# A period after a range ends the sentence unless a digit follows (0.05–0.5.).
# A range may wrap around an en or em dash (5\n–10), but a hyphen stays on the
# first line: one that starts a line is a list marker or a sign (- 5\n- 10 is
# two values, not 5-10).
RANGE = re.compile(r"(?<![\w.])" + NUM + r"(?:[^\S\n]*-|" + GAP + r"[–—])" + GAP + NUM + r"(?!\w|\.\d)")
BOUND_WORDS = (
    "more than", "greater than", "less than", "fewer than", "at least", "at most", "no more than",
    "no fewer than", "no less than", "no greater than", "not more than", "not fewer than",
    "not less than", "not greater than", "up to", "over", "under", "above", "below", "exceeding",
    "about", "approximately", "around", "roughly", "nearly", "almost", "just over", "just under",
)
# A bound phrase may wrap onto the next line (more\nthan 5), and a bound may be
# on a price, signed or not (under €500, > $40, under -$40). A negated phrase is read whole: no less than 5
# is >= 5, the same bound as at least 5. Every comparison but = is a bound, != included,
# so turning = into != (or < into >) fails whatever word stands before it.
BOUNDED = r"((?:" + SIGN + r"?[$€£¥₹]\s?)?" + NUM + r")"
# A tilde of ~~strikethrough~~ is not "about". A version pin (== 1.2.3, ~= 3.10,
# ~> 1.2, ^1.2.3) is a bound of its own kind, so ~> is not read as >.
OPERATORS = r"==|~=|~>|\^|>=|<=|!=|&gt;=|&lt;=|&ge;|&le;|&ne;|&gt;|&lt;|[<>≤≥≈≠]|(?<!~)~(?!~)"


def bound_on(value, operators):
    """A bound phrase or operator before a value; not, no or never before a
    phrase negates it (not over 40 is at most 40)."""
    return re.compile(
        r"\b((?:(?:not|no|never)\s+)?(?:" + "|".join(w.replace(" ", r"\s+") for w in BOUND_WORDS) + r"))\s+"
        + value + r"|(" + operators + r")" + GAP + value,
        re.I,
    )


BOUND = bound_on(BOUNDED, OPERATORS)
# A version constraint (>= 2.4.0-beta, at least v2.4, ^1.2.3-rc.1) is read with its
# version, before versions leave the text.
VERSION_BOUND = bound_on("(" + VERSION.pattern + ")", OPERATORS + "|=")
NEGATED = {">": "<=", "<": ">=", ">=": "<", "<=": ">"}
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
    "!=": "!=", "≠": "!=", "&ne;": "!=",
    # version constraints
    "==": "==", "=": "==", "~=": "~=", "~>": "~>", "^": "^",
}
LABELLED = re.compile(
    r"(?<![\w])([A-Za-z]\w*)" + GAP + r"(>=|<=|!=|&gt;=|&lt;=|&ge;|&le;|&ne;|&gt;|&lt;|[=<>≤≥≠≈])" + GAP + r"(" + NUM + r")"
)
# Spellings of one operator compare equal, as they do for bounds: x ≥ 5 is x >= 5.
LABEL_OPERATOR = {"≥": ">=", "&gt;=": ">=", "&ge;": ">=", "≤": "<=", "&lt;=": "<=", "&le;": "<=",
                  "≠": "!=", "&ne;": "!=", "&gt;": ">", "&lt;": "<"}
# A compact dimension is one value with its sign, unit, power and denominator,
# the unit attached, after a space or line break, or after a hyphen but not x (-2x3,
# 1920x1080px, 1.5x2.5cm, 3x4m², 10x20 cm, 10x20-cm, 10x20 kg/m²); 0x4601 is
# hex, not 0 by 4601.
DIMENSION = re.compile(
    r"(?<![\w.])(" + SIGN + r"?(?!0[xX])\d+(?:\.\d+)?(?:[xX×]\d+(?:\.\d+)?)+)"
    r"(?:(" + UNIT_CHARS + POWER + DENOMINATOR + r")"
    r"|(?:(?=\s)" + GAP + r"|-(?!x\b))((?:" + UNITS + r")" + POWER + DENOMINATOR + r")(?!\w))?(?!\w)"
)
# A chain of numbers joined by multiplication signs, spaced or not (10 x 20,
# 2x3 x 4, 10x20 x30), read as one dimension; it starts at a whole number that is
# not hex, so a name ending in a digit (a1 x 2) and 0x10 x 2 keep their spaces.
TIMES_CHAIN = re.compile(r"(?<![\w.])(?!0[xX][0-9A-Fa-f])\d+(?:[.,]\d+)*(?: ?[xX×] ?\d+(?:[.,]\d+)*)+")
# A hex literal (0x4601, -0x10) is one number with its sign, compared as written,
# and so is a number with its percent sign, multiplier or magnitude, spaced or
# not (5%, 5 %, 5x, 50K, 3 bn), as for prices.
NUMBER = re.compile(r"(?<![\w.])(?:" + SIGN + r"?0[xX][0-9A-Fa-f]+\b|" + NUM + r"(?:\s?(?:%|(?:x|k|K|M|bn|B)\b))?)")
# Bold and italic are removed where a marker run opens and the same run closes
# it within a paragraph, as Markdown reads them: an asterisk pair may touch a
# word (**5**kg), an underscore pair may not (timeout_, IRDN_RAN). Where removing
# a marker would join two words or a word and a number, a space takes its place,
# so a*2 and b*3 keep both values; a lone marker stays, so 2**10 is not 210. A
# run may sit right next to another marker, so nested emphasis (**5 *kg***)
# unwraps one level per pass.
INLINE = r"((?:[^\n]|\n(?![ \t\r]*\n))+?)"
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
NEGATION = re.compile(r"\b(not|no|never|none|nothing|neither|nor|without|cannot)\b|n['’]t\b", re.I)
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


def opens_fence(rest):
    """Match a fence opener; a backtick fence's info string cannot contain a backtick."""
    m = FENCE.match(rest)
    return m if m and not (m.group(1)[0] == "`" and "`" in rest[m.end():]) else None


def list_kind(item):
    """Name the list an item belongs to: its bullet, or an ordered list's delimiter."""
    marker = item.group(2)
    return marker if marker in "-*+" else marker[-1]


def mask_markers(raw, markers, masked):
    """Take out the container markers a prose line carries, in order: a quote marker
    is dropped, as BLOCKQUOTE drops one that starts a line, and a list marker (bullet
    or item number) is masked. None of them is a fact or a comparison."""
    pos = 0
    for marker in markers:
        m = re.compile(r"(?<!\d)" + re.escape(marker)).search(raw, pos)
        if m is None:
            continue
        if marker == ">":
            start = m.start() if raw[:m.start()].strip() else 0
            end = m.end() + (raw[m.end():m.end() + 1] in " \t")
            raw, pos = raw[:start] + raw[end:], start
        else:
            raw = raw[:m.start()] + mask(marker, masked) + raw[m.end():]
            pos = m.start() + 1
    return raw


def inside(raw, rest):
    """Return a line from where its container's markers and indent end, as written.

    rest is what is left of the line, tabs expanded, once its containers are
    matched; a tab that straddles the container's edge stays with the line."""
    line = raw.rstrip("\r\n")
    width = len(line.expandtabs(4)) - len(rest)
    col = i = 0
    while i < len(line) and col < width:
        col = col + 4 - col % 4 if line[i] == "\t" else col + 1
        i += 1
    return raw[i - 1 if col > width else i:]


def split_code(text, masked):
    """Return the code blocks (fenced or indented) as written, the text outside them,
    and the placeholder that marks where each block of that text starts.

    A block is compared without its containers' markers and indent, so
    renumbering a list or requoting a passage changes no code. An ordered
    list's item numbers (1. Install) are formatting, not facts: they are masked
    in the text, so a quotation still restores them."""
    blocks, kept, blanks = [], [], []
    boundary = mask("", masked)

    def hold(lines):
        """Record a code block from its (raw, content) lines; a placeholder on its own
        paragraph keeps its place, so a quotation that spans the block puts it back
        and a swap of two blocks is caught."""
        blocks.append("".join(content for _, content in lines))
        return "\n" + mask("".join(raw for raw, _ in lines), masked) + "\n\n"

    # ">" for a blockquote, or (content indent, list kind) for a list item; outermost first
    containers = []
    code = None      # the open code block: [(raw, content) lines, container depth, closing fence or None]
    para = False     # the last line was paragraph text, which a lazy line may continue
    empty = None     # the depth of a list item opened with no content that has none yet
    for raw in text.splitlines(keepends=True):
        rest = raw.rstrip("\r\n").expandtabs(4)
        matched, markers = 0, []  # the container markers this line carries, in order
        for container in containers:
            if container == ">":
                m = QUOTE_MARKER.match(rest)
                if m is None:
                    break
                rest = rest[m.end():]
                markers.append(">")
            elif rest.strip():  # a blank line stays in a list item
                if indent_of(rest) < container[0]:
                    break
                rest = rest[container[0]:]
            elif matched == empty and indent_of(rest) < container[0]:
                break  # unless the item opened empty and is still empty
            else:
                rest = rest[container[0]:]  # and gives up the item's indent, as far as it has one
            matched += 1
        if matched < len(containers):
            # A line outside an open container is lazy text only if it starts no
            # block. Any list item starts one here, empty or numbered from 2: the
            # paragraph it follows is inside the container it left, so the rule
            # that such an item cannot interrupt a paragraph does not apply.
            starts_block = (QUOTE_MARKER.match(rest) or opens_fence(rest) or ATX_HEADING.match(rest)
                            or THEMATIC_BREAK.match(rest) or LIST_ITEM.match(rest) or EMPTY_ITEM.match(rest))
            if para and rest.strip() and not starts_block:
                kept.append(raw)  # a lazy continuation keeps every container open
                continue
            del containers[matched:]
            para = False
            if empty is not None and empty >= matched:
                empty = None
        if code and code[1] > len(containers):  # its container closed, so it did too
            kept += [hold(code[0])] + [raw for raw, _ in blanks]
            code, blanks = None, []
        if code and code[2]:
            code[0].append((raw, inside(raw, rest)))
            if code[2].match(rest):
                kept.append(hold(code[0]))
                code = None
            continue
        # New containers; four columns in is code or paragraph text, never a marker.
        depth = len(containers)
        while indent_of(rest) < 4 and not THEMATIC_BREAK.match(rest):  # - - - is no item
            m = QUOTE_MARKER.match(rest)
            if m:
                containers.append(">")
                markers.append(">")
                rest, para = rest[m.end():], False
                continue
            m = LIST_ITEM.match(rest)
            if m and (not para or can_interrupt(m)):
                # Five or more spaces after the marker start indented code one column in.
                width = m.end() if len(m.group(3)) <= 4 else m.end(2) + 1
                containers.append((width, list_kind(m)))
                markers.append(m.group(2))
                rest, para = rest[width:], False
                continue
            m = EMPTY_ITEM.match(rest)
            if m and not para:  # an empty item never interrupts a paragraph
                containers.append((m.end(2) + 1, list_kind(m)))
                markers.append(m.group(2))
                rest, empty = "", len(containers) - 1
            break
        if (rest.strip() or len(containers) > depth) and empty is not None and empty < depth:
            empty = None  # content, or a new container, fills the empty item it is in
        if code:  # an open indented block
            if not rest.strip() and len(containers) == depth:  # an empty new item ends it
                blanks.append((raw, inside(raw, rest)))  # kept only if the block continues after it
                continue
            if indent_of(rest) >= 4 and code[1] == len(containers):
                code[0] += blanks + [(raw, inside(raw, rest))]
                blanks = []
                continue
            kept += [hold(code[0])] + [raw for raw, _ in blanks]
            code, blanks = None, []
        if not rest.strip():
            kept.append(mask_markers(raw, markers, masked))
            para = False
            continue
        # A line that does not continue a paragraph starts a block.
        starts = not para or ATX_HEADING.match(rest) or THEMATIC_BREAK.match(rest)
        if indent_of(rest) >= 4 and not para:
            code = [[(raw, inside(raw, rest))], len(containers), None]
            continue
        m = opens_fence(rest)
        if m:
            closer = re.compile(r" {0,3}" + re.escape(m.group(1)[0]) + "{%d,}[ \t]*$" % len(m.group(1)))
            code, para = [[(raw, inside(raw, rest))], len(containers), closer], False
            continue
        kept.append((boundary + "\n" if starts else "") + mask_markers(raw, markers, masked))
        # A heading or thematic break ends the paragraph: Title\n---, # Title, ***.
        para = not ((para and SETEXT_UNDERLINE.match(rest)) or ATX_HEADING.match(rest)
                    or THEMATIC_BREAK.match(rest))
    if code:  # an unclosed block runs to the end of the text
        kept += [hold(code[0])] + [raw for raw, _ in blanks]
    return blocks, "".join(kept), boundary


def mask(span, masked):
    """Record a masked span and return an unused placeholder that stands for it."""
    code = MASK_BASE + len(masked)
    while chr(code) in masked:
        code += 1
    masked[chr(code)] = span
    return chr(code)


def split_inline_code(text, masked, boundary):
    """Return the inline code spans as written, and the text around them; a span ends with its block."""
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
        if close and boundary not in text[m.end():close.start()] and not BLANK_LINE.search(text, m.end(), close.start()):
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


def unmask(text, masked):
    """Put masked spans back: a backtick in a link target is part of the URL."""
    return MASKED.sub(lambda s: masked[s.group(0)], text)


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
            full = unmask(target, masked)
            targets[full[1:-1] if full.startswith("<") else full] += 1
            kept += [text[pos:start], mask(full, masked)]
            pos = start + len(target)
        m = LINK_TARGET.search(text, max(start + len(target), m.start() + 1))
    kept.append(text[pos:])
    return targets, "".join(kept)


def strip_protected(text):
    """Split a text into its protected spans, the prose left over, the masked spans,
    and the placeholder that marks block boundaries in that prose."""
    # A private use character already in the text stands for itself.
    facts, masked = {}, {c: c for c in MASKED.findall(text)}
    blocks, body, boundary = split_code(text, masked)
    facts["code_blocks"] = Counter(blocks)
    # Blockquote markers in the prose are dropped (code keeps its own).
    spans, body = split_inline_code(BLOCKQUOTE.sub("", body), masked, boundary)
    facts["inline_code"] = Counter(spans)
    urls, body = split_link_targets(body, masked)

    def destination(m, span):
        """Count a destination as written, code spans in it restored, and mask it."""
        full = unmask(span, masked)
        urls[full] += 1
        return m.group(0).replace(span, mask(full, masked), 1)
    body = AUTOLINK.sub(lambda m: destination(m, m.group(1)), body)
    # A bare URL outside a link: the search resumes where each URL ends, so text
    # trimmed from its end is searched again. A URL stops at an inline-code
    # placeholder but keeps a private use character the text itself contains.
    stops = "".join(c for c, span in masked.items() if span != c)
    url_pattern = re.compile(URL_START + stops + "]+") if stops else URL
    kept, pos = [], 0
    m = url_pattern.search(body)
    while m:
        before = EMPHASIS_BEFORE.search(body, max(0, m.start() - 4), m.start())
        url = trim_url(m.group(0), before.group(1) if before else "")
        urls[url] += 1
        kept += [body[pos:m.start()], mask(url, masked)]
        pos = m.start() + len(url)
        m = url_pattern.search(body, pos)
    kept.append(body[pos:])
    def address(m):
        """Count an email address; an underscore run that opens before it and closes
        after it (_a@b.org_) is emphasis, not part of the address."""
        run = re.match(r"_*", m.group(0)).group(0)
        if run and re.match(re.escape(run) + r"(?!\w)", m.string[m.end():]):
            return destination(m, m.group(0)[len(run):])
        return destination(m, m.group(0))
    body = EMAIL.sub(address, "".join(kept))
    facts["urls"] = urls
    return facts, body, masked, boundary


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


def read_bounds(pattern, body):
    """Count each bound as its comparison and value: no more than 40 and <= 40 agree."""
    bounds = Counter()
    for m in pattern.finditer(body):
        word, value = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
        word = " ".join(word.lower().split())
        if word in BOUND_CLASS:
            kind = BOUND_CLASS[word]
        else:  # a negated phrase
            kind = BOUND_CLASS[word.split(" ", 1)[1]]
            kind = NEGATED.get(kind, "not " + kind)
        value = re.sub(r"\s", "", value)  # a price may be written $ 40
        bounds[f"{kind} {value}"] += 1
    return bounds


def extract(text):
    """Return token counts, review counts, and prose for the fact comparison."""
    facts, body, masked, boundary = strip_protected(text)
    # A quotation is compared exactly as written: the block boundaries come out
    # and the masked spans go back in.
    facts["quotes"] = Counter(MASKED.sub(lambda s: masked[s.group(0)], next(g for g in m.groups() if g).replace(boundary + "\n", ""))
                              for m in QUOTE.finditer(body))
    # Bold and italic go before any value is read, so removing them (P18)
    # changes no value; they also hide sentence starts from the name check.
    body = strip_emphasis(body)
    # Spacing is never a fact: any run of spaces and line breaks reads as one
    # space, and a blank line as a paragraph break, so rewrapping or respacing a
    # value passes. Values stop at a paragraph break and at a block boundary.
    body = re.sub(r"\s+", lambda m: "\n\n" if BLANK_LINE.search(m.group(0)) else " ", body)
    facts["versions"] = Counter(m.group(0) for m in VERSION.finditer(body))
    version_bounds = read_bounds(VERSION_BOUND, body)
    body = VERSION.sub(" ", body)
    # Spaces around a multiplication sign or a range's dash are spacing too:
    # 10 x 20 cm is the dimension 10x20 cm, and 1 -3 ms is the range 1-3 ms,
    # whose 3 is not negative.
    body = TIMES_CHAIN.sub(lambda m: m.group(0).replace(" ", ""), body)
    # A plus-minus glued to the value before it is a tolerance of its own: 5±2 mm is
    # 5 and ±2 mm, so the sign is compared.
    body = re.sub(r"(?<=[\w.%])([±∓])", r" \1", body)
    # Temperature: − 5 °C is −5 °C. A masked code span, link or URL before the sign
    # is a value, as in `a` + 3; a block boundary or a list marker is not.
    operands = {c for c, span in masked.items() if span and not re.fullmatch(r"[-*+]|\d{1,9}[.)]", span)}
    body = SPACED_SIGN.sub(lambda m: m.group(0) if m.group(1) in operands else m.group(1) + m.group(2) + m.group(3),
                           body)
    body = RANGE.sub(lambda m: re.sub(r"\s", "", m.group(0)), body)
    after = list(CURRENCY_AFTER.finditer(body))
    taken = {m.start(4) for m in after}  # a symbol read with the amount before it
    facts["currency"] = (Counter(re.sub(r"\s", "", m.group(0)) for m in CURRENCY.finditer(body)
                                 if m.start(1) not in taken)
                         + Counter(m.group(1) + m.group(4) + m.group(2) + re.sub(r"\s", "", m.group(3) + m.group(5))
                                   for m in after))
    facts["quantities"] = Counter(re.sub(r"\s", "", m.group(1)) + " " + m.group(2).replace(" ", "")
                                  for m in QUANTITY.finditer(body))
    # The operator and value are always compared (as bounds); the word before the
    # operator is compared too when it is a label: a letter (I = 5 A), a symbol in
    # capitals (OR = 2), or a word that is not a function word (latency < 5). A
    # function word is prose (Latency is now < 5 ms).
    facts["labelled"] = Counter(f"{m.group(1)} {LABEL_OPERATOR.get(m.group(2), m.group(2))} " + re.sub(r"\s", "", m.group(3))
                                for m in LABELLED.finditer(body)
                                if len(m.group(1)) == 1 or m.group(1).isupper()
                                or m.group(1).capitalize() not in FUNCTION_WORDS)
    facts["ranges"] = Counter(re.sub(r"\s", "", m.group(0)) for m in RANGE.finditer(body))
    facts["bounds"] = version_bounds + read_bounds(BOUND, body)
    # A dimension is read last, so a bound or label beside it reads as before
    # (about 10x20 cm is ~ 10; from 5x15 = 75 has no label).
    dimensions = Counter(" ".join(filter(None, (m.group(1), (m.group(2) or m.group(3) or "").replace(" ", ""))))
                         for m in DIMENSION.finditer(body))
    body = DIMENSION.sub(" ", body)
    # Numbers are compared exactly as written: 3,000 and 3000 differ, and so do
    # 1,5 and 1.5. A rewrite should not reformat data (hard rule 4).
    facts["numbers"] = dimensions + Counter(re.sub(r"\s", "", m.group(0)).rstrip(".") for m in NUMBER.finditer(body))
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
        # newline="" keeps CRLF, so a code block whose line endings change is caught.
        with open(argv[1], encoding="utf-8", newline="") as f:
            original = f.read()
        with open(argv[2], encoding="utf-8", newline="") as f:
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
