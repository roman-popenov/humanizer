# Guide for agents

This file explains how to change Humanizer without breaking its package or prompt.

## What this repo contains

Humanizer is an agent skill written in Markdown, with one Python script. `SKILL.md` is the prompt that agents read, and it points to the files in `references/` and `scripts/`. The repo has no build step.

Keep the skill portable. Do not write instructions that limit it to one or two agent tools.

## Key files

- `SKILL.md` is the source of truth and the repo's only skill file. It contains portable YAML metadata, the scope, the hard rules, the claim test, the workflow, voice, output modes, and a one-line index of the patterns.
- `references/patterns.md` holds the full pattern entries. Each entry has a `### P<n>. Name (kind) [tags]` heading, sits in a `##` group, and is ordered by strength and frequency. The skill reads an entry when it marks that pattern.
- `references/examples.md` holds whole-text before/after examples with notes on what was cut, kept, and flagged.
- `scripts/fact_diff.py` compares an original with its rewrite and reports changed numbers, quotes, code, URLs, and names. The skill runs it on every rewrite. It uses only the Python standard library.
- `README.md` explains installation, use, and patterns.
- `CHANGELOG.md` holds the release notes, newest first. Old notes keep the pattern numbers their release used.
- `.claude-plugin/plugin.json` describes the Claude plugin and points its skill loader at the root `SKILL.md`.
- `.claude-plugin/marketplace.json` lets users add this repo as a Claude marketplace.
- `.cursor-plugin/plugin.json` describes the Cursor plugin. Omit a `skills` path so Cursor loads the root `SKILL.md`.
- `agents/openai.yaml` holds the display name, short description, and default prompt for OpenAI-compatible agents.
- `scripts/validate-package.py` checks package files and shared values.

## Rules for changes

Keep `SKILL.md`, `references/patterns.md`, and `README.md` in sync.

- **Patterns:** Patterns are numbered from 1 without gaps in `references/patterns.md`, strongest and most frequent first. Each is a *defect* or a *density* pattern, tagged `[W]` when Wikipedia's page documents it and `[U]` when it does not. A new tell earns a pattern only when no existing pattern already implies it; prefer folding it into an existing pattern. If you add, remove, rename, regroup, or renumber a pattern, update the `SKILL.md` index, the README tables and their groups, the README section title, and every `P<n>` reference in `SKILL.md` and `references/`. The validator derives the count from the headings and checks the index and the README tables against them.
- **Claims:** Every example must keep every claim of its Before text on the same terms and add nothing. Run `scripts/fact_diff.py` on any pair you change, then check the claims by hand.
- **Fact check:** Keep `scripts/fact_diff.py` on the Python standard library and runnable as `python3 scripts/fact_diff.py ORIGINAL REWRITE`. Keep its exit status: 0 for no strict difference, 1 for a strict difference, 2 for a usage error. If you change what it checks, update Step 4 in `SKILL.md` and the README's fact check section.
- **Hard rules:** If you renumber the hard rules in `SKILL.md`, update every "hard rule N" reference. The validator checks them.
- **Version:** Keep the same version in `SKILL.md` under `metadata.version`, the first `CHANGELOG.md` heading, `.claude-plugin/plugin.json`, and `.cursor-plugin/plugin.json`. Do not add a top-level `version` field to the skill.
- **Compatibility:** Keep install and use instructions neutral across agents. Names such as Claude Code, Cursor, OpenCode, and Codex are examples, not limits.
- **Description:** The plugin manifests use the first sentence of the `SKILL.md` description.
- **Length:** Every word of `SKILL.md` is read on each use. The validator caps it at 5,500 words; a change that adds words should earn them. The skill reads `references/` only when it needs an entry or an example, but it may read the whole catalog for a long text, so keep entries short.
- **History:** Add a short `CHANGELOG.md` note for any behavior change or non-obvious fix.
- **Checks:** Before publishing, run `python3 scripts/validate-package.py`, `npx skills add . --list`, and `claude plugin validate .`.

## Writing style

Use Plain Language in code comments, prompts, documentation, descriptions, validation messages, and progress reports.

- Lead with the main point.
- Use common words and active voice.
- Keep sentences and paragraphs short.
- Use one term for the same item.
- Use `must` for requirements.
- Use headings, lists, and tables when they help the reader.
- Remove repeated or unnecessary words.
- Limit acronyms and explain technical terms.
- Avoid double negatives.
- Keep exact identifiers, commands, paths, schema fields, quotations, watched phrases, and behavior-bearing examples.
- Keep the full technical meaning.

## Editing the skill

- Keep the YAML metadata valid.
- Treat the prompt below the metadata and the files in `references/` as the product.
- Prefer a short, clear instruction over another exception or repeated explanation.
