# Humanizer 

sponsored by [cfo.ai](https://cfo.ai)

[![GitHub stars](https://img.shields.io/github/stars/blader/humanizer?style=flat)](https://github.com/blader/humanizer/stargazers) [![skills.sh installs](https://skills.sh/b/blader/humanizer)](https://skills.sh/blader/humanizer) 


Humanizer makes AI-written text sound like a person wrote it, without changing what it says. It is built on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), the guide Wikipedia editors use to catch AI-generated text, and it works in Claude Code, Codex, and any other agent that supports skills.

**Before:**
> I'm thrilled to announce that shared drafts are finally here! 🚀 For months, our own team was drowning in files named final_v7.docx — and we knew there had to be a better way. Now two people can edit the same doc at once, with every change appearing live for both of them. It's not just a feature; it's a whole new way to collaborate. Comments stay anchored to the exact sentence they reference, even as the text around them evolves. And the best part? It's available today on every plan, completely free. Let that sink in.

**After:**
> I'm thrilled to announce that shared drafts are finally here! For months, our own team was drowning in files named final_v7.docx, and we knew there had to be a better way. Now two people can edit the same doc at once, with every change appearing live for both of them. It's a feature and a whole new way to collaborate. Comments stay anchored to the exact sentence they reference, even as the text around them evolves. The best part is that it's available today on every plan, completely free.

The rewrite keeps every claim in the draft at the strength the writer gave it and removes the devices around them: the emoji, the connector dash, the not-X-but-Y contrast, the set-up question, and the closing line.

In a blind test of an earlier version, judges preferred Humanizer's rewrite over the original AI text 16 times out of 16 ([#229](https://github.com/blader/humanizer/issues/229)).

Humanizer edits for human readers. Getting past AI detectors is not a goal, and detectors still flag most of its output.

## The five strongest tells

These are the most common signs of AI writing. Humanizer removes any of them on sight and keeps the claim each one carries:

1. **Not X but Y:** "It's not just a feature, it's a shift."
2. **One-line closers:** "Let that sink in."
3. **Sayings that sound deep:** "At its core, what really matters is..."
4. **A staged run-up:** "Here's the thing." "Honestly?"
5. **Arguing with no one:** "I'm not saying X, but..."

Humanizer checks for [26 patterns](#the-26-patterns) in all.

## Installation

Once installed, the skill answers to `/humanizer`.

### Claude Code

```text
/plugin marketplace add blader/humanizer
/plugin install humanizer@humanizer
```

The plugin answers to `/humanizer:humanizer`. It needs Claude Code 2.1.142 or newer; on older versions, use `npx skills add blader/humanizer --global --agent claude-code`.

### Codex

```bash
npx skills add blader/humanizer --global --agent codex
```

### Claude.ai and Claude Desktop

Download this repository as a ZIP (**Code → Download ZIP**) and upload it as a skill in Settings.

### Other agents

```bash
npx skills add blader/humanizer --global --agent '*'
```

This installs Humanizer for every agent the Skills CLI supports, including Gemini CLI, GitHub Copilot, and Windsurf. Leave off `--global` in any command above to install it only in the current project. For an agent the Skills CLI does not know, copy `SKILL.md` and the `references` and `scripts` folders into its skill folder.

## Usage

Call the skill directly:

```
/humanizer

[paste your text here]
```

Or ask in plain language:

```
Please humanize this text: [your text]
```

To rewrite a file, give Humanizer its path:

```
Humanize the prose in docs/launch-post.md
```

To check a draft without changing it, ask for a review:

```
Check this PR description for AI tells: [your text]
```

A review lists each tell with its pattern ID, the quoted words, and a suggested fix. It never says whether a model wrote the text.

### Match your voice

If you want the rewrite to sound more like you, include a sample:

```
/humanizer

Here's a sample of my writing for voice matching:
[paste 2-3 paragraphs of your own writing]

Now humanize this text:
[paste AI text to humanize]
```

Humanizer follows the sample's rhythm, word choice, punctuation, and deliberate quirks, including dashes if you use them.

## How it works

A language model writes whatever is most likely to come next, so by default it makes the choice that fits the widest range of readers and subjects. A person chooses for one reader and one subject. Every tell Humanizer looks for is a form of that default choice: a sentence that signals importance instead of adding a fact, rhythm or formatting applied by rule, an ordinary fact dressed as a pivotal one, text left over from the chat, or a reply that re-explains what the reader already knows.

> "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."
> Wikipedia, ["Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

Humanizer separates what a passage says from the device that carries it. A claim is anything the text asserts or does: a number, a name, a cause, a hedge, an opinion, a judgment of significance, a request, an offer, or thanks. A device is wording that can change without changing any claim: a run-up, a chat wrapper, a not-X-but-Y contrast, a closing one-liner, an -ing rider, or decorative bold. Humanizer removes the devices and keeps each claim on the same terms: the same degree (*pivotal* does not become *major*), modality (*should* does not become *is*), tense, actor, scope, and relationship words (*in connection with* does not become *to celebrate*). When no plain wording keeps every term, Humanizer keeps the writer's wording for that clause and removes only what surrounds it.

It does not make things up. It adds no fact, example, source, number, actor, reason, or purpose, even one that is true. If a sentence needs a detail the text does not give, Humanizer writes a simpler sentence or asks.

Humanizer reads the whole text, marks tells with the pattern index in `SKILL.md`, and reads the full entry in `references/patterns.md` for each pattern it marks. It rewrites only the marked passages, runs the fact check below, and compares the two texts claim by claim in both directions. Last, it sweeps the rewrite for devices that survived and for terms that moved. Unmarked sentences stay as they are, and a text with no tells comes back unchanged.

When you paste text, Humanizer returns the rewrite first, with no preamble. A short note follows when there is a judgment call you should see: a passage it cut as a repeat (quoted, so you can restore it), a claim it kept but could not support, or a question about a missing or ambiguous detail. Point it at a file and it edits the prose in place, leaving code, commands, paths, URLs, link targets, frontmatter, data values, quotations, and names byte for byte. When another task uses it for its own output, such as a PR description or a commit message, it returns only the text.

Personal writing keeps its opinions, doubts, humor, asides, and odd details. Technical and reference prose stays neutral. The writer's conventions stay too: UK or US spelling, the serial comma, quote style, heading case, abbreviations, shorthand, and all-lowercase notes. A request to tidy up is not a request to spell out shorthand, and Humanizer never resolves a token with two readings (*wed*: Wednesday or a wedding) without asking.

Some habits also appear in careful human writing, so Humanizer leaves them alone: a single hedge or intensifier, a single transition word or dash in text that otherwise reads as human, formal words outside the watch list, unsourced statements, salutations and sign-offs, repetition for rhythm, and an opinion said plainly once.

### The fact check

`scripts/fact_diff.py` compares an original with its rewrite and reports what changed. It needs Python 3 and no packages.

```bash
python3 scripts/fact_diff.py original.txt rewrite.txt
```

A strict difference prints a `FAIL` line and sets exit status 1. Strict checks cover code blocks, inline code, URLs, quoted passages, numbers as written with their signs, version strings, numbers with units, labelled values (`p = 0.003`), ranges, and bounds (*over*, *just over*, *about*, *up to*). Review lines do not change the exit status. They list names, number words, numbers now said fewer times, and changed counts of negations and hedges. Exit status 0 means no strict difference was found, and 2 means a usage error.

The script cannot see claims, causes, or attribution, so a clean run does not prove that the meaning survived. That is why Humanizer follows it with the claim-by-claim comparison. An agent that cannot run scripts does the whole comparison by hand.

## The 26 patterns

The patterns are numbered by strength and frequency. Each pattern has one of two kinds:

- A *defect* is fixed wherever an instance fails its keep-test.
- A *density* pattern counts only when its own cluster test is met, such as several listed words, more than one connector dash in a paragraph, or triads in a row. A single instance in text that otherwise reads as human stays.

`[W]` marks a pattern documented on Wikipedia's page, checked against the page as of 2026-10-15. `[U]` marks guidance from earlier Humanizer releases that the page does not list. Both tags mean partly each. [references/patterns.md](references/patterns.md) has the full entries, with watch lists, fixes, keep-tests, and examples.

### A. Staging instead of stating

| # | Pattern | Kind | Before | After |
|---|---------|------|--------|-------|
| P1 | **Not X but Y, X rather than Y** | defect [W] | "It's not just X, it's Y", "This does not mean X. It means Y." | State Y plainly; keep X in the same sentence only when it informs; a real comparison stays word for word |
| P2 | **One-line closers, dramatic fragments, recaps** | defect [U, W] | "Four minutes. Down from nine." after the numbers; "The lesson?"; "No prior. No nostalgia."; "In summary," | Cut a closer that restates an earlier sentence; turn any other closer into one plain sentence that keeps its claim |
| P3 | **Sayings that sound deep** | defect [U] | "At its core, what really matters is...", "Efficiency becomes a trap" | Write the literal claim on the same terms; if the saying has two readings, leave it and ask |
| P4 | **Staged run-ups** | defect [U, W] | "Let's dive in", "Honestly?", "Here's how it works.", "Additionally," | Delete the announcement; keep any feeling, ranking, or claim inside it ("We're thrilled to announce") |
| P5 | **Arguing with no one** | defect [U] | "I'm not saying...", "A tempting approach would be..." | Drop the staging; keep the rejected option's content and any judgment of it |

### B. Rhythm and hedging

| # | Pattern | Kind | Before | After |
|---|---------|------|--------|-------|
| P6 | **Forced triads** | density [W] | "fast, quick, and easy to use" | Cut an item only when it repeats another |
| P7 | **Stacked hedges** | defect [U] | "could potentially possibly reduce" | Keep one hedge for each distinct limit; keep attribution such as "I think" |

### C. Inflation and borrowed authority

| # | Pattern | Kind | Before | After |
|---|---------|------|--------|-------|
| P8 | **Inflated significance and stock outlook** | defect [W] | ", marking a pivotal moment in...", "Despite these challenges... continues to thrive", "The future looks bright" | Keep the significance claim in the writer's words; turn a participle frame into its own clause |
| P9 | **Vague connection or association** | defect [W] | "associated with the leadership of", "in connection with" | Keep the wording, never invent a role or a purpose, and ask the writer |
| P10 | **Shallow -ing riders** | defect [W] | ", highlighting...", ", reflecting...", ", showcasing..." | Make the rider its own clause with the same verb; note it when the text does not support it |
| P11 | **Sales language** | defect [W] | "nestled within the breathtaking region", "stands as a vibrant town" | Cut a frame that adds nothing ("stands as" becomes "is"); keep each evaluation at its degree |
| P12 | **Borrowed authority** | defect [W] | "Experts believe...", "cited in The New York Times, BBC, Financial Times, and The Hindu" | Keep the attribution and every named outlet; ask the writer who the experts are |
| P13 | **Avoiding is, are and has** | defect [W] | "The gallery features four separate spaces" | Use is, are, or has where the longer verb means exactly that; keep a verb that names a role, as in "serves as" |
| P14 | **AI vocabulary** | density [W] | "delve", "tapestry", "testament", "showcase", in a cluster | Act on a cluster, not one word; replace a word only with one of the same degree and kind |

### D. Punctuation and syntax

| # | Pattern | Kind | Before | After |
|---|---------|------|--------|-------|
| P15 | **Dashes as the universal connector** | density [W] | "The new policy — announced without warning — affects thousands" | Use the punctuation that states the relation; keep ranges and the writer's own habit |
| P16 | **Repeated sentence openings** | density [U] | "She noted... She noted... She filed..." | Merge the sentences or begin with the action |
| P17 | **Passive hiding a known actor** | density [U] | "It was decided by the board that..." | Name the actor the text gives; never invent one |

### E. Formatting

| # | Pattern | Kind | Before | After |
|---|---------|------|--------|-------|
| P18 | **Bold as decoration, bold-label lists** | defect [W] | "**OKRs**, **KPIs**"; "**Performance:** Performance has been enhanced" | Remove the bold; keep a label's words when they say something the line does not |
| P19 | **Decorative headings, emoji and tiny tables** | defect [W, U] | "🚀 Launch Phase:", "The decision, on one screen", a two-row table | Remove the decoration; keep each heading's words unless the heading itself is the tell |
| P20 | **Curly quotes in a straight-quote format** | density [W] | `said “the project”` in a Markdown file | Match the target format, consistently |

### F. Leftovers from the chat and the draft

| # | Pattern | Kind | Before | After |
|---|---------|------|--------|-------|
| P21 | **Chatbot residue and clerk tone** | defect [W] | "Great question! ... I hope this helps!", "I hope this message finds you well" | Remove the empty wrapper; keep every offer, request, question, thanks, and apology |
| P22 | **Source and knowledge disclaimers** | defect [W] | "Information about her early life is not publicly available", "She likely grew up..." | Keep the claim and its hedge, and list it in the note as unverified |
| P23 | **Heading restated as the first sentence** | defect [U] | "## Installation" + "This section covers installation." | Delete the restatement only when it says no more than the heading |
| P24 | **Writing about the document or the process** | defect [W, U] | "The table below compares the plans.", "compiled from..." | Write about the subject; keep guarantees, history, provenance, and reasons |
| P25 | **Re-explaining what the reader knows** | defect [U] | A reply that walks the diagnosis and the evidence before the decision | In a reply, put the decision first; move the evidence after it, never delete it |
| P26 | **Leftover placeholders and template text** | defect [W] | "[Company Name]", "INSERT_X", "(add citation)" | List it in the note; never fill it |

## Full example

**Before (AI-sounding):**
> I recently spent five unforgettable days in Lisbon last October, and let me tell you — this city completely stole my heart. From the moment I checked into my charming hotel perched high in the historic Alfama district, I knew I was somewhere truly special.
>
> Yes, the famous hills are challenging — with countless stairs between my hotel and everything else, my legs certainly felt it! — but every climb rewards you with breathtaking, panoramic views that make it all worthwhile.
>
> No trip would be complete without riding the iconic Tram 28, a roughly forty-minute journey shared with plenty of fellow travelers eager to capture the magic. And the food? Simply divine. While the pastéis de nata at Pastéis de Belém are a beloved national treasure, my absolute favorite came from a hidden gem in Graça, still warm from the oven.
>
> But what truly makes Lisbon special isn't just the sights — it's the feeling. Wander just a block or two above the main squares and you'll discover a quieter, more authentic side of the city, inviting you to slow down and savor every moment.
>
> Of course, the must-see São Jorge Castle offers stunning views over the rooftops below. The queues can be long, but the experience is absolutely worth it for any history buff or curious traveler.
>
> Would I go back? Absolutely — next time in spring, and with better shoes! Lisbon isn't just a place to visit; it's a place to fall in love with, again and again. ✨

**After:**
> I recently spent five unforgettable days in Lisbon last October, and this city completely stole my heart. From the moment I checked into my charming hotel perched high in the historic Alfama district, I knew I was somewhere truly special.
>
> The famous hills are challenging (with countless stairs between my hotel and everything else, my legs certainly felt it!), but every climb rewards you with breathtaking, panoramic views that make it all worthwhile.
>
> No trip would be complete without riding the iconic Tram 28, a roughly forty-minute journey shared with plenty of fellow travelers eager to capture the magic. The food is simply divine. While the pastéis de nata at Pastéis de Belém are a beloved national treasure, my absolute favorite came from a hidden gem in Graça, still warm from the oven.
>
> But what truly makes Lisbon special is the feeling, not just the sights. Wander just a block or two above the main squares and you'll discover a quieter, more authentic side of the city. It invites you to slow down and savor every moment.
>
> Of course, the must-see São Jorge Castle has stunning views over the rooftops below. The queues can be long, but the experience is absolutely worth it for any history buff or curious traveler.
>
> I'd absolutely go back, next time in spring, and with better shoes! Lisbon is a place to fall in love with, again and again, not just a place to visit.

**Note returned with it:**
> "Unforgettable", "charming", "truly special", "breathtaking", "simply divine", "hidden gem", "stunning" and "absolutely worth it" are your own judgments, so they stay at the strength you gave them. Tell me which ones to tone down if you want the post plainer.

The rewrite removes the run-up "let me tell you", the staged "Yes," and "Would I go back?", the set-up question "And the food?", the connector dashes, the two not-X-but-Y contrasts, the -ing rider, the emoji, and "offers" where it means "has". Every opinion, number, and place stays.

## Sources

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) is the source for the pattern list.
- [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup) maintains the page.

## Version history

See [CHANGELOG.md](CHANGELOG.md).

## License

MIT

If Humanizer helps you, a star helps other people find it.
