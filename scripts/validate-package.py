#!/usr/bin/env python3
"""Check Humanizer's package files without external dependencies."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def read_package_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        raise SystemExit(f"Cannot read {path.relative_to(ROOT)}: {error}")


SKILL_PATH = ROOT / "SKILL.md"
PATTERNS_PATH = ROOT / "references" / "patterns.md"
EXAMPLES_PATH = ROOT / "references" / "examples.md"
FACT_DIFF_PATH = ROOT / "scripts" / "fact_diff.py"
SKILL = read_package_file(SKILL_PATH)
PATTERNS = read_package_file(PATTERNS_PATH)
EXAMPLES = read_package_file(EXAMPLES_PATH)
FACT_DIFF = read_package_file(FACT_DIFF_PATH)
README = read_package_file(ROOT / "README.md")
CHANGELOG = read_package_file(ROOT / "CHANGELOG.md")
try:
    PLUGIN = json.loads(read_package_file(ROOT / ".claude-plugin" / "plugin.json"))
except json.JSONDecodeError as error:
    raise SystemExit(f"Fix the JSON in .claude-plugin/plugin.json: {error}")
try:
    CURSOR_PLUGIN = json.loads(
        read_package_file(ROOT / ".cursor-plugin" / "plugin.json")
    )
except json.JSONDecodeError as error:
    raise SystemExit(f"Fix the JSON in .cursor-plugin/plugin.json: {error}")


def require_match(match: re.Match[str] | None, message: str) -> re.Match[str]:
    if match is None:
        raise SystemExit(message)
    return match


yaml_metadata = require_match(
    re.match(r"\A---\n(.*?)\n---\n", SKILL, re.DOTALL),
    "SKILL.md must begin with YAML metadata",
).group(1)

for unsupported_field in ("version:", "compatibility:", "allowed-tools:"):
    if re.search(rf"(?m)^{re.escape(unsupported_field)}", yaml_metadata):
        raise SystemExit(f"Remove unsupported YAML field: {unsupported_field[:-1]}")

skill_version = require_match(
    re.search(r'(?m)^\s+version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)["\']?\s*$', yaml_metadata),
    "Add metadata.version to SKILL.md as a three-part version",
).group(1)
changelog_version = require_match(
    re.search(r"(?m)^## ([0-9]+\.[0-9]+\.[0-9]+)$", CHANGELOG),
    "Add a version heading to CHANGELOG.md",
).group(1)

package_versions = {
    skill_version,
    changelog_version,
    str(PLUGIN.get("version", "")),
    str(CURSOR_PLUGIN.get("version", "")),
}
if len(package_versions) != 1:
    raise SystemExit(
        f"Use one package version in all files: {sorted(package_versions)}"
    )

skill_files = {path.relative_to(ROOT) for path in ROOT.rglob("SKILL.md")}
if SKILL_PATH.is_symlink() or skill_files != {Path("SKILL.md")}:
    raise SystemExit("Keep one regular SKILL.md at the repo root")
if PLUGIN.get("skills") != ["./"]:
    raise SystemExit("Point the Claude plugin skill loader at the repo root")
if CURSOR_PLUGIN.get("name") != "humanizer":
    raise SystemExit("Set the Cursor plugin name to humanizer")
if "skills" in CURSOR_PLUGIN:
    raise SystemExit("Omit skills from the Cursor plugin so it loads the root SKILL.md")

skill_description = " ".join(
    require_match(
        re.search(r"(?m)^description: \|\n((?:  .*\n)+)", yaml_metadata + "\n"),
        "Write the SKILL.md description as an indented block",
    ).group(1).split()
)
# The Agent Skills format caps the description at 1,024 characters.
if len(skill_description) > 1024:
    raise SystemExit(
        f"Keep the SKILL.md description at 1,024 characters or fewer; it has {len(skill_description)}"
    )
MARKETPLACE = json.loads(read_package_file(ROOT / ".claude-plugin" / "marketplace.json"))
package_descriptions = {
    str(PLUGIN.get("description", "")),
    str(CURSOR_PLUGIN.get("description", "")),
    *(str(plugin.get("description", "")) for plugin in MARKETPLACE.get("plugins", [])),
}
if len(package_descriptions) != 1 or not skill_description.startswith(
    next(iter(package_descriptions))
):
    raise SystemExit(
        "Use the first sentence of the SKILL.md description in every plugin manifest: "
        f"{sorted(package_descriptions)}"
    )

# SKILL.md links to its bundled files; a moved or renamed file breaks the skill.
bundled_paths = sorted(
    {
        path.rstrip(".")
        for path in re.findall(r"\b((?:references|scripts)/[\w.-]+)", SKILL + PATTERNS + EXAMPLES)
    }
)
if not {"references/patterns.md", "references/examples.md", "scripts/fact_diff.py"} <= set(bundled_paths):
    raise SystemExit(
        "Link references/patterns.md, references/examples.md and scripts/fact_diff.py from the skill"
    )
missing_files = [path for path in bundled_paths if not (ROOT / path).is_file()]
if missing_files:
    raise SystemExit(f"Add the files that SKILL.md and references/ name: {missing_files}")
try:
    compile(FACT_DIFF, str(FACT_DIFF_PATH.relative_to(ROOT)), "exec")
except SyntaxError as error:
    raise SystemExit(f"Fix the syntax of scripts/fact_diff.py: {error}")

# The pattern catalog lives in references/patterns.md. Each entry has a heading
# of the form "### P<n>. <name> (<kind>) [<tags>]" inside a "## <group>" section.
PATTERN_HEADING = re.compile(
    r"^### P([0-9]+)\. (.+) \((defect|density)\) \[([WU](?:, [WU])*)\]$"
)
catalog: dict[int, tuple[str, str, str]] = {}
catalog_order: list[int] = []
catalog_groups: list[tuple[str, list[int]]] = []
for line in PATTERNS.splitlines():
    if line.startswith("## "):
        catalog_groups.append((line[3:].strip(), []))
    elif line.startswith("### P"):
        heading = require_match(
            PATTERN_HEADING.match(line),
            f"Write each references/patterns.md heading as '### P<n>. Name (defect|density) [W|U]': {line!r}",
        )
        number = int(heading.group(1))
        if number in catalog:
            raise SystemExit(f"Number each pattern once in references/patterns.md: P{number}")
        if not catalog_groups:
            raise SystemExit(f"Put P{number} under a '## ' group heading in references/patterns.md")
        catalog[number] = (heading.group(2), heading.group(3), heading.group(4))
        catalog_order.append(number)
        catalog_groups[-1][1].append(number)
catalog_groups = [(name, numbers) for name, numbers in catalog_groups if numbers]
pattern_count = len(catalog_order)
if pattern_count == 0 or catalog_order != list(range(1, pattern_count + 1)):
    raise SystemExit(
        f"Number references/patterns.md patterns from 1 upward without gaps: {catalog_order}"
    )

# Every use reads the SKILL.md index, so it must list the same patterns, in the
# same order, with the same names, kinds, and tags as the catalog.
index_rows = re.findall(
    r"(?m)^\| P([0-9]+) \| (.+?) \| (defect|density) \[([WU](?:, [WU])*)\] \|", SKILL
)
index_order = [int(number) for number, *_ in index_rows]
if index_order != catalog_order:
    raise SystemExit(
        f"List patterns 1 through {pattern_count} once each, in order, in the SKILL.md index: {index_order}"
    )
index_mismatches = [
    f"P{number}: {(name, kind, tags)!r} should be {catalog[int(number)]!r}"
    for number, name, kind, tags in index_rows
    if (name, kind, tags) != catalog[int(number)]
]
if index_mismatches:
    raise SystemExit(
        "Match the SKILL.md index to references/patterns.md: " + "; ".join(index_mismatches)
    )

# The README groups its tables like the catalog and uses the same names.
readme_section = require_match(
    re.search(r"(?ms)^## The ([0-9]+) patterns$(.*?)(?=^## )", README),
    f"Title the README pattern section 'The {pattern_count} patterns'",
)
if int(readme_section.group(1)) != pattern_count:
    raise SystemExit(f"Title the README pattern section 'The {pattern_count} patterns'")
for anchor in re.findall(r"\(#the-([0-9]+)-patterns\)", README):
    if int(anchor) != pattern_count:
        raise SystemExit(f"Point README links at #the-{pattern_count}-patterns, not #the-{anchor}-patterns")
readme_patterns: dict[int, tuple[str, str, str]] = {}
readme_order: list[int] = []
readme_groups: list[tuple[str, list[int]]] = []
for line in readme_section.group(2).splitlines():
    group = re.match(r"^### (?:[A-Z]\. )?(.+)$", line)
    if group:
        readme_groups.append((group.group(1).strip(), []))
    elif re.match(r"^\| P[0-9]", line):
        row = require_match(
            re.match(
                r"^\| P([0-9]+) \| \*\*(.+?)\*\* \| (defect|density) \[([WU](?:, [WU])*)\] \|",
                line,
            ),
            f"Write each README pattern row as '| P<n> | **Name** | kind [tags] | ...': {line[:60]!r}",
        )
        number = int(row.group(1))
        if not readme_groups:
            raise SystemExit(f"Put README row P{number} under a '### ' group heading")
        readme_patterns[number] = (row.group(2), row.group(3), row.group(4))
        readme_order.append(number)
        readme_groups[-1][1].append(number)
if sorted(readme_order) != catalog_order or len(readme_order) != pattern_count:
    raise SystemExit(
        f"List patterns 1 through {pattern_count} once each in the README tables: {readme_order}"
    )
renamed = [
    f"P{number}: {readme_patterns[number]!r} should be {entry!r}"
    for number, entry in catalog.items()
    if readme_patterns[number] != entry
]
if renamed:
    raise SystemExit(
        "Match the README pattern names, kinds, and tags to references/patterns.md: "
        + "; ".join(renamed)
    )
readme_grouping = [(name, numbers) for name, numbers in readme_groups if numbers]
if readme_grouping != catalog_groups:
    raise SystemExit(
        "Group the README tables like references/patterns.md: "
        f"{readme_grouping} should be {catalog_groups}"
    )

# A renumber can leave a pattern reference pointing at the wrong pattern or at
# nothing. CHANGELOG.md keeps the numbers each release used, so read only the
# skill files.
skill_text = {"SKILL.md": SKILL, "references/patterns.md": PATTERNS, "references/examples.md": EXAMPLES}
for name, text in skill_text.items():
    references = sorted(
        {int(pattern or section) for pattern, section in re.findall(r"\bP([0-9]+)\b|§([0-9]+)", text)}
    )
    missing_patterns = [number for number in references if not 1 <= number <= pattern_count]
    if missing_patterns:
        raise SystemExit(
            f"Point every pattern reference in {name} at a pattern from 1 to "
            f"{pattern_count}: {missing_patterns}"
        )

# The same holds for the numbered hard rules in SKILL.md.
hard_rules = require_match(
    re.search(r"(?ms)^## Hard rules$(.*?)(?=^## )", SKILL),
    "Keep the '## Hard rules' section in SKILL.md",
).group(1)
# The rules are read by their written numbers, so check those, not just the count.
hard_rule_numbers = [int(number) for number in re.findall(r"(?m)^([0-9]+)\. ", hard_rules)]
hard_rule_count = len(hard_rule_numbers)
if hard_rule_count == 0 or hard_rule_numbers != list(range(1, hard_rule_count + 1)):
    raise SystemExit(f"Number the hard rules in SKILL.md 1 through {hard_rule_count} in order: {hard_rule_numbers}")
for name, text in skill_text.items():
    missing_rules = sorted(
        {int(number) for number in re.findall(r"(?i)\bhard rule ([0-9]+)", text)}
        - set(range(1, hard_rule_count + 1))
    )
    if missing_rules:
        raise SystemExit(
            f"Point every hard rule reference in {name} at a rule from 1 to "
            f"{hard_rule_count}: {missing_rules}"
        )

# Every word of SKILL.md is read on each use, so the budget is in words. The
# references are read only when a pattern or an example is needed.
skill_words = len(SKILL.split())
if skill_words > 5500:
    raise SystemExit(f"Keep SKILL.md at 5,500 words or fewer; it has {skill_words}")

print(f"Humanizer package v{skill_version} is valid")
