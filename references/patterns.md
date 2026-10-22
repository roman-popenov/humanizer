# Pattern catalog

Each entry gives what to watch for, why it weakens the text, the fix, and when to keep it. Every fix applies the claim test and the same-terms rule in SKILL.md: a claim stays, with its degree, modality, tense, agent, scope and relationship words; a device (an announcement, a wrapper, a restatement, decoration) goes. No fix expands the writer's abbreviations, shorthand, nicknames or clipped words, or resolves a token with two readings (SKILL.md hard rule 5). The examples illustrate editing decisions. Check every original claim against the rewrite and every rewritten claim against the original: a token-check pass cannot establish that the meaning is the same.

`[W]` = documented on Wikipedia's "Signs of AI writing" (fetched 2026-10-21). `[U]` = from earlier Humanizer releases, not on Wikipedia. Both tags = partly each. *Defect*: fix any instance that fails its keep-test. *Density*: act only when the entry's own cluster test is met.

## Contents

- Staging instead of stating: P1 not X but Y, P2 closers and fragments, P3 sayings, P4 run-ups, P5 arguing with no one
- Rhythm and hedging: P6 triads, P7 stacked hedges
- Inflation and borrowed authority: P8 significance, P9 vague connection, P10 -ing riders, P11 sales language, P12 borrowed authority, P13 avoiding is/has, P14 AI vocabulary (with eras)
- Punctuation and syntax: P15 dashes, P16 repeated openings and synonym cycling, P17 passive hiding an actor
- Formatting: P18 bold, P19 headings/emoji/tables, P20 curly quotes
- Leftovers: P21 chatbot residue, P22 disclaimers, P23 heading restated, P24 writing about the document, P25 wrong reader, P26 placeholders
- Why these patterns exist

---

## Staging instead of stating

### P1. Not X but Y, X rather than Y (defect) [W]

**Watch for:** not X but Y; not just / not only / not merely X, but (also) Y; it's not X, it's Y; no X, no Y, just Z; the reversed X rather than Y, which Wikipedia notes is "particularly common in recent LLM output"; the contrast split over two sentences ("This does not mean X. It means Y."); a clipped negative tail ("..., no guessing"); the newer frames "the X is not simply Y", "rather than merely / simply", "is more than an X; it is Y" and "less like X and more like Y", which a 2026 study by Graphite measured at 32 to 576 times the human rate; and the trade-off denial "without sacrificing / compromising / losing / requiring X", which denies a cost nobody raised (up to 70 times the human rate, in GPT, Claude and Gemini models alike). The same construction in other languages (*no es solo X, sino Y*; *ce n'est pas X, c'est Y*; *nicht nur X, sondern auch Y*).
**Why:** the negative half often denies something nobody said, so the positive half sounds bigger without saying more.
**Fix:** state Y plainly, on its terms. If X carries information (the text really does deny or limit something), keep it in the same sentence as Y, after it; swapping the halves into two sentences ("It is about Y. It isn't about X.") keeps the device. Do not hide a contrast against something nobody claimed in a smaller form: "more than a caching layer" and "beyond a caching layer" are the same move. A comparison the text actually makes stays word for word ("more than I paid in Leeds", "more than two minutes faster"). If Y is a slogan, keep its literal claim at its strength, in the writer's words where no plain wording has the same degree ("une véritable révolution" stays a véritable révolution). Cut Y only when another sentence states the same claim on the same terms.
**Keep when:** the reader actually believes X and the text corrects it, or both halves carry information. A trade-off denial the reader relies on is a guarantee ("upgrades without requiring a restart" where restarts are the known cost): keep it. A source-usage hedge ("should be treated as indicative rather than definitive") is a hedge: keep its modality (P22).

> Before: It's not just a caching layer; it's a complete rethinking of how the app loads data.
> After: It is a caching layer and a complete rethinking of how the app loads data.

> Before: This does not mean every choice is equal. It means no external system confirms which choice is right.
> After: This means that no external system confirms which choice is right, not that every choice is equal.

> Before: The options come from the selected item, no guessing.
> After: The options come from the selected item. No guessing is involved.

> Before: The 40% figure should be treated as indicative rather than definitive, and does not by itself establish a trend.
> After: unchanged.
> (Both halves inform, so the contrast stays. "The 40% figure is indicative" would turn advice about how to read the figure into a statement about it.)

### P2. One-line closers, dramatic fragments, recaps (defect) [U, W]

**Watch for:** a one-sentence paragraph restating the paragraph before; "That is the real win." "That distinction matters." "Let that sink in."; a set-up label before the last line ("The lesson?", "The takeaway:"); the same closer after several sections; a sentence after an example or number that only names what it showed ("This shows the importance of..."); a row of fragments ("No aesthetic prior. No nostalgia."); one word in capitals or with periods between words (every. single. day.); "In summary," / "In conclusion," recaps (Wikipedia files section summaries as a historical sign of older models; they still appear).
**Why:** the line asks the reader to pause on a point instead of adding to it.
**Fix:** a closer that states the same claim as an earlier sentence, about the same subject and on the same terms, is a repeat: cut it and quote it in the note. Anything else a closer says is a claim, including a judgment the evidence supports ("Small changes, big gains" after the numbers still says the gains were big, and "That is what really matters" ranks what came before): keep it as one plain sentence on the same terms, joined to what it draws from, without the closing-line staging. Merge a row of fragments into one sentence that keeps each claim.
**Keep when:** the short line adds a fact, a judgment, a consequence or the writer's purpose that the paragraph did not state; then only its staging changes.

> Before: Then AlphaEvolve arrived. It had no preference for symmetry. No aesthetic prior. No nostalgia for human taste. The old rules were gone.
> After: Then AlphaEvolve arrived. It had no preference for symmetry, no aesthetic prior and no nostalgia for human taste. The old rules were gone.

> Before: We moved CI to ARM runners, and a full build now takes 4 minutes instead of 9. Four minutes. Down from nine.
> After: We moved CI to ARM runners, and a full build now takes 4 minutes instead of 9.
> (The fragments restate the numbers in the sentence before them.)

> Before: Checkout lost a third of mobile users at the address form, so we cut it from nine fields to four. Completion rose 18%. The lesson for us? Every field has to earn its place.
> After: Checkout lost a third of mobile users at the address form, so we cut it from nine fields to four. Completion rose 18%. The lesson for us is that every field has to earn its place.
> (The lesson appears nowhere else, so it stays; only the set-up question goes.)

### P3. Sayings that sound deep (defect) [U]

**Watch for:** the real question is, at its core, in reality, what really matters, fundamentally, the deeper issue, the heart of the matter; X is the Y of Z; X becomes a trap; X is not a tool but a mirror; the language of, the currency of, the architecture of.
**Why:** an ordinary point is dressed as a hidden truth, and the dressing adds no detail.
**Fix:** write the literal claim the saying makes, using only what the text says and keeping its degree ("the real question", "what really matters" rank a point; the ranking stays). Cut a saying only when another sentence states the same claim on the same terms, and quote it in the note. If the saying has two literal readings and the text does not pick one, leave it as written and ask the writer in the note; never pick a reading for them.

> Before: The real question is whether teams can adapt. At its core, what really matters is organizational readiness.
> After: The real question is whether teams can adapt. What really matters is organizational readiness.
> ("At its core" says again what "what really matters" says. The two rankings stay.)

> Before: Efficiency becomes a trap when teams forget the human layer.
> After: unchanged.
> (Note to the writer: "becomes a trap" and "the human layer" do not say what goes wrong or who is forgotten. Which do you mean?)

### P4. Staged run-ups (defect) [U, W]

**Watch for:** Let's dive in, let's explore, let's break this down, here's what you need to know, now let's look at, without further ado, heads up, quick note; staged candor as a standalone opener: Honestly?, Look, Here's the thing, The thing is, Let's be honest, Real talk; time skips and recap markers that announce a move instead of making it (Flash forward, Cut to, To sum up); one- or two-word set-up questions before the answer (The result?, Why?); references and recaps that announce instead of stating (As we discussed, As mentioned above, To summarize, I am writing to); a claim-free announcement of what follows ("Here's how it works.", "Here is the list:"); sentence-initial transitions that add no relation: Additionally, Moreover, Furthermore, Notably, Importantly (Wikipedia: older models overused these, and one in isolation is "not a strong tell").
**Why:** the writer announces the point instead of making it.
**Fix:** delete the announcement and start at the point. An announcing sentence goes when the next sentences say what it promises; if it says something they do not, keep that. A set-up label can carry a ranking ("The biggest lesson?", "Here's the key insight:"): keep the ranking in the sentence ("The biggest lesson was that ..."), since "biggest" and "key" are the writer's judgments. In text you are already editing for tells, cut a sentence opener that adds no relation the sentence needs; keep one that carries a relation (However, So, Because of that). In text that otherwise reads as human, leave single openers alone. "Honestly" or "look" inside a casual sentence is ordinary; the tell is the standalone opener before a routine claim. If the run-up carries a claim (honest admits something), keep the claim. An announcement may contain a feeling, evaluation or claim about change. Preserve that content and what it refers to. "We're thrilled to announce that X" must retain the feeling about announcing X; keep the original clause if no equivalent rewrite is clear. "It wasn't easy" and "Then everything changed" may be cut only when another sentence states the same claim on the same terms. "Moving forward" and "Going forward" set a time frame for the sentence, so they stay.

> Before: Let's dive into how the scheduler picks a worker. Here's what you need to know: it picks the worker with the shortest queue.
> After: The scheduler picks the worker with the shortest queue.

> Before: Is it worth the price? Honestly? It depends on how often you'll use it.
> After: Whether it's worth the price depends on how often you'll use it.

> Before: We're excited to share that the app now works offline. Here's how it works: your changes sync when you reconnect.
> After: We're excited to share that the app now works offline. Your changes sync when you reconnect.
> (The excitement is a stated feeling, so its clause stays; only the announcement of the explanation goes.)

### P5. Arguing with no one (defect) [U]

**Watch for:** This isn't (mainly) about, I'm not saying, To be clear, Don't get me wrong, This is not to say, Some might say... but, A tempting approach would be, One might be tempted to, You might think... but, It would be easy to just.
**Why:** the text answers an objection or rejects an option that appears nowhere else, so the framing stages a debate the reader never started.
**Fix:** remove the staging. If the rejected option or the answer carries information (a consequence, a reason, a judgment such as "tempting"), keep it as a plain statement.
**Keep when:** the text attributes the objection and answers it, or the option is one a reader would actually weigh. Several unrelated rejections in a row are a stronger sign than one.

> Before: Session tokens are rotated every 24 hours. A tempting approach would be to rotate them by restarting the auth service on a cron job, but that would drop every active session. Rotation happens in place, and clients refresh transparently.
> After: Session tokens are rotated every 24 hours, in place, and clients refresh transparently. Restarting the auth service on a cron job would be a tempting way to rotate them, but it would drop every active session.

## Rhythm and hedging

### P6. Forced triads (density) [W]

**Watch for:** three adjectives, three short phrases or three parallel examples whose items overlap or name nothing the text supports, or several triads in a row. Wikipedia: the sign "is stronger when it appears in contexts where most people would not bother", such as edit summaries; commit messages are a similar short-text context, though the page names only edit summaries.
**Why:** threes sound complete whether or not the content is.
**Fix:** keep every item that carries a distinct idea. Cut an item only when it repeats another. Vary a paragraph built as three parallel sentences without dropping any of them.
**Keep when:** the meaning has three parts.

> Before: The new dashboard is fast, quick, and easy to use.
> After: The new dashboard is fast and easy to use.
> ("Fast" and "quick" are one claim.)

> Before: A career can look promising and fail. A relationship can feel important and end. A skill can take years and remain useless. These decisions rarely explain themselves.
> After: A career can look promising and fail, a relationship can feel important and end, and a skill can take years and remain useless. These decisions rarely explain themselves.

### P7. Stacked hedges (defect) [U]

**Watch for:** two or more hedges on one claim that express the same doubt: could potentially, might possibly, may perhaps, possibly could.
**Why:** a repeated hedge makes the claim vaguer without adding a reason for doubt.
**Fix:** remove only semantic duplicates. Keep one hedge for each distinct limit: scope ("in some regions"), probability ("may"), evidence ("it could be argued"), magnitude ("some effect"). Attribution is separate from probability: "I think it might fail" and "I suspect it may fail" say who doubts and how likely, so both parts stay.
**Keep when:** the hedges qualify different things. Single hedges such as *perhaps* and *tends to* are human habits, as are scope statements, safety notices and labels like "this is an inference".

> Before: The change could potentially possibly reduce load times.
> After: The change could reduce load times.

> Before: In some regions, the policy may have some effect on outcomes.
> After: unchanged (scope, probability and magnitude are three different limits).

## Inflation and borrowed authority

Apply the preservation rules to every assertion inside inflated wording. Significance, evaluation and interpretation are the writer's claims even when they are generic, figurative or unsupported: each stays, said once, at its degree, and goes into the note as unsupported when the text gives no evidence for it. What goes is a participle frame (", marking ..."), a doubled formula ("Despite ..., ... Despite these challenges"), and a significance line that states the same claim as another sentence. Words that carry the claim's degree or relation stay (*pivotal, testament, in our journey*).

### P8. Inflated significance and stock outlook (defect) [W]

**Watch for:** stands or serves as, is a testament or reminder, a crucial / pivotal / vital / significant / key role or moment, plays a significant role in shaping, underscores or highlights its importance, reflects broader, contributing to the, setting the stage for, marking or shaping the, represents or marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted; "Despite its ..., X faces several challenges ... Despite these challenges, X continues to thrive"; sections titled Challenges and Legacy or Future Outlook; send-offs: the future looks bright, exciting times ahead, a step in the right direction, looking ahead, what comes next; stock scene-setters ("In today's fast-paced world", which a 2024 GPTZero vendor list puts at 107 times the human rate); importance flags: "this matters", "why X matters", "X matters because", "the distinction matters", "matters most" (Graphite 2026: 12 to 357 times the human rate, in Claude as well as GPT models; Wikipedia's significance list has "distinction [matters/is important] because").
**Why:** an ordinary detail is said to mark a change, prove a legacy or promise a future, in a formula that fits any subject. The move appears at three scales: a phrase, a stock section, a closing paragraph.
**Fix:** keep the fact and the significance claim in the writer's words. A participle frame ("..., marking a pivotal moment in X") becomes a clause with the same verb ("..., which marked a pivotal moment in X", or "This marked a pivotal moment in X."). Keep the writer's degree word unless a plain word has the same degree. Cut a significance line only when another sentence states the same claim on the same terms. Keep real plans the text states: "Looking ahead" before a stated plan sets its time frame and stays, as "Moving forward" does (P4). An importance flag states significance, which is a claim: keep it once, with any reason after *because* and any ranking (*matters most*); cut it only when it repeats a significance the text already states, and remove closing-line staging as in P2.

> Before: The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions and enhance regional governance.
> After: The Statistical Institute of Catalonia was officially established in 1989, which marked a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions and enhance regional governance.
> (Note to the writer: nothing in the text supports "a pivotal moment in the evolution of regional statistics in Spain". Add a source or cut it.)

> Before: Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of Chennai's growth.
> After: Korattur is industrially prosperous but faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, it continues to thrive as an integral part of Chennai's growth.
> (Note to the writer: "Ongoing initiatives" names none: which are they?)

> Before: Cold starts now take 300 ms instead of 2 s, the biggest single win for mobile users. This matters.
> After: Cold starts now take 300 ms instead of 2 s, the biggest single win for mobile users.
> ("This matters" repeats the significance the sentence already states.)

> Before: The redesigned checkout went live on 3 May, marking an exciting new chapter in our journey.
> After: The redesigned checkout went live on 3 May. This marked an exciting new chapter in our journey.
> (The participle becomes its own sentence with the same verb; the writer's judgment stays in their words.)

### P9. Vague connection or association (defect) [W]

**Watch for:** associated with, in association with, connected to or with, in connection with, linked to, tied to; elaborate versions such as "ventured into politics as a candidate" for "was a candidate". Wikipedia lists this among the most common signs as of October 2026.
**Why:** it says two things are related without saying how. "Associated with the leadership of ExampleCorp" hides whether he was the CEO, a board member or a consultant.
**Fix:** keep the vague wording, since it is the writer's relationship word; never invent a role or turn a connection into a purpose. When the relationship matters to the reader, ask the writer in the note what it was.

> Before: The concerts were organised in connection with the celebrations of Pakistan's 50th anniversary.
> After: unchanged.
> (Note to the writer: "to celebrate" would turn a connection into a purpose. Were the concerts part of the celebrations, or timed to them?)

### P10. Shallow -ing riders (defect) [W]

**Watch for:** a present-participle phrase at the end of a sentence that comments on significance: highlighting, underscoring, emphasizing, ensuring, reflecting, symbolizing, contributing to, cultivating, fostering, encompassing, enhancing, showcasing; also *valuable insights*, *align with*, *resonate with*; a main result tacked on the same way ("..., cutting build time from 9 to 4 minutes"), which reads as an afterthought: give it its own clause. Attaching it to a named source ("Roger Ebert highlighted the lasting influence") does not make it true.
**Why:** an interpretation is bolted onto a fact, so it reads as part of the evidence. Models use present-participle clauses at 2 to 5 times the human rate (Reinhart et al., PNAS 2025); a narrative participle ("leaning on his agility, he dodged") is ordinary grammar and not this pattern.
**Fix:** keep the fact, and make each rider its own plain clause with the same verb and relation: a hedge stays a hedge, an effect stays an effect (never a purpose), a possibility stays a possibility, and a reporting or relationship verb (*highlight, resonate with, reflect*) stays unless a plain verb has the same strength. That holds for a broad rider too ("reflecting a deep connection to the land" is the writer's interpretation): keep it and list it in the note when the text gives no evidence for it. Cut a rider only when it states the same claim as the sentence it hangs on ("highlighting its importance" after a sentence that already called the thing important), and quote it in the note.

> Before: The temple's color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.
> After: The temple's color palette is blue, green, and gold. It resonates with the region's natural beauty and symbolizes Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes. It reflects the community's deep connection to the land.
> (Note to the writer: the resonance with the region's natural beauty and the community's connection to the land are interpretations the text does not support. Add a source or cut them.)

### P11. Sales language (defect) [W]

**Watch for:** boasts a, vibrant, rich (figurative), profound, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, featuring, diverse array, breathtaking, must-visit, stunning, seamless.
**Why:** the text reads like an advertisement or a travel guide, which Wikipedia notes happens "even when prompted to use an encyclopedic style".
**Fix:** state what the thing is, and cut a frame that adds nothing: *stands as* becomes *is*. *Boasts* presents a feature with pride and a figurative word such as *nestled* describes the place, so both are the writer's and stay unless the writer agrees to *has* or *is in*. Every evaluation stays, including praise of a secondary noun ("the breathtaking region"): keep the writer's word unless a plain word has the same degree, since *lively* is milder than *vibrant* and *great* is milder than *stunning*. A superlative slogan ("a must-visit") keeps its strength ("a must-visit" or "you must visit it"); cut it only when another sentence says the same. Keep every content word and checkable claim inside the praise, even a vague one ("cultural heritage"), and ask about vague ones in the note.
**Keep when:** the text is advertising and the writer wants it to sell; then cut the stock phrases and keep the enthusiasm through the content: every feature, number, offer and call to action.

> Before: Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.
> After: Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo is a vibrant town with a rich cultural heritage and stunning natural beauty.
> (Note to the writer: "stands as" became "is"; every evaluation stays in your words. An encyclopedia would need a source for them.)

### P12. Borrowed authority (defect) [W]

**Watch for:** experts argue, observers have cited, industry reports, some critics argue, several sources or publications (when only a few are given), such as (before what is really the whole list); notability frames: cited, featured or profiled in [outlets], independent coverage, trade publications, regional media, written by a leading expert, maintains an active social media presence, was identified by.
**Why:** a vague authority props up a claim, or a list of outlets props up a person, with the emphasis on the sources instead of on what they said.
**Fix:** if the text names who said what, write that plainly. If an attribution names no one, keep it (deleting it turns a hedged claim into a bare assertion) and ask the writer in the note who it was. Keep every named outlet and number, without the canned frame.
**Keep when:** a missing citation alone is not a tell; most writing is unsourced.

> Before: Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists. Experts believe it plays a crucial role in the regional ecosystem.
> After: unchanged.
> (Note to the writer: which experts? Naming them would remove the tell. The attribution stays, since deleting it would turn their belief into your assertion.)

> Before: Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.
> After: Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She is active on social media, with over 500,000 followers.
> (The passive stays: "cited in" an outlet need not mean the outlet itself cited her.)

### P13. Avoiding is, are and has (defect) [W]

**Watch for:** serves as, stands as, functions as, operates as, has emerged as, marks, represents [a]; boasts, features, offers, maintains [a]; refers to; holds the distinction of being (Wikipedia shows a model turning "is the first" into it). Wikipedia cites a study of arXiv abstracts that found "an over 10% decrease" in *is* and *are* in 2023. Do not confuse with "has been featured" (present perfect).
**Fix:** use is, are or has where the longer verb means exactly that. Keep the verb when it carries information: a role or function ("operates as a relay"), timing ("began his career as"), an offer ("offers a free trial"), an ongoing activity ("maintains the library"), a degree ("stands out as").

> Before: Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.
> After: Gallery 825 serves as LAAA's exhibition space for contemporary art. It has four separate spaces and boasts over 3,000 square feet.
> ("Features" means has here. "Serves as" names a role and "boasts" adds pride, so both stay.)

### P14. AI vocabulary (density) [W]

Wikipedia: "One or two of these words appearing in an edit may be coincidental, but an edit ... introducing lots of them, lots of times, is one of the strongest tells." Act on a cluster. Take the list literally: a word's synonyms are not tells, and literal senses (an *underscore* character, a *key* in a map, *robust* statistics) are not tells.

Wikipedia's list as of 2026-10-21, by era (rough, not hard cutoffs):

| era | words |
|---|---|
| 2023 to mid-2024 (GPT-4) | Additionally (sentence-initial), boasts, bolstered, crucial, delve, emphasizing, enduring, garner, intricate/intricacies, interplay, key, landscape (abstract), meticulously, pivotal, underscore (verb), tapestry (abstract), testament, valuable, vibrant |
| mid-2024 to mid-2025 (GPT-4o) | align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant |
| mid-2025 to mid-2026 (GPT-5) | emphasizing, enhance, highlighting, showcasing |
| mid-2026 on (GPT-6) | challenge, clearer, dependable, echoed, foster, leverage, matters, multifaceted, practical, prioritize, quietly, steady, universally |

Also on the page's main list: deep dive, robust, meticulous, highlight (verb), showcase. The page cites a single product review for the GPT-6 row; a 2026 study by Graphite, which compared 90,000 model-written articles with 10,000 written before ChatGPT, measured four of its words well above the human rate: *dependable* (59x in GPT-6 Astra), *practical* (26x), *steady* (6x in Claude Opus 5) and *matters* (as in "matters because", 357x in GPT-6 Astra; see P8). Wikipedia notes that Grok output overuses "scientific" words (*causal, empirical, correlate*). Its list of signs of human writing adds plain verbs where models pick stiff or euphemistic ones: *wrote* (not *authored*), *moved* (*relocated*), *used* (*utilized*), *tried* (*attempted*), *died* (*passed away*). Stiff synonyms count toward the cluster; replace one only with a word of the same meaning and register, and keep a euphemism the writer chose for tone.
**Fix:** preserve the degree and kind of every evaluation. Rewrite the surrounding syntax first. Replace a listed word only when the replacement expresses the same judgment at the same strength in this context; otherwise keep the original word. Crucial stays crucial and pivotal stays pivotal: *very important* and *major* are lower degrees, and *essential* claims necessity, a different kind. A lone listed word stays as written, since one word is not a cluster. A listed reporting verb (underscore, highlight, showcase) stays unless a plain verb has the same evidential strength.

> Before: Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.
> After: A distinctive feature of Somali cuisine is its use of camel meat. The widespread adoption of pasta in the local cuisine is an enduring testament to Italian colonial influence and showcases how these dishes have integrated into the traditional diet.
> ("Additionally", "the incorporation of" and "culinary landscape" go. "Enduring testament" and "showcases" stay: "evidence" and "shows" are weaker.)

## Punctuation and syntax

### P15. Dashes as the universal connector (density) [W]

**Watch for:** em dashes (—) or spaced hyphens (` - `, ` -- `) joining clauses, more than one per paragraph (or several across a short post of one-line paragraphs); and, in text that has other tells, a single dash that pivots between two clauses ("X — it's Y", "X — but Y", "the best of both worlds — Y"). Wikipedia: models use them "in places where humans are more likely to use commas, parentheses, colons", "in a formulaic, pat way", and usually with spaces around them. The page files this sign under historical indicators, dated "2022–September 2026", because the newest models have been found to suppress dashes. Graphite's October 2026 measurement agrees: GPT-6 Astra uses em dashes about one eighth as often as human writers, and Claude Opus 5.5 almost never (0.015 per 1,000 words, against 2.92 for Opus 5). A text with no dashes is therefore no evidence either way; act on dashes only where they cluster as connectors.
**Fix:** replace connector dashes with the punctuation that states how the clauses relate (comma, colon, parentheses, full stop), or rewrite the sentence. Choose punctuation for the relationship between clauses and the writer's conventions; impose no punctuation or sentence-length quota, and do not flatten every dash into a comma or a full stop: parentheses are a human habit that current models use far less (SKILL.md, Not tells).
**Keep:** en dashes in ranges (2019–2021, pp. 12–15) and compound names; a single dash in text that otherwise reads as human; dashes in code, commands, paths and URLs; the writer's dashes when their sample or the rest of their text uses them.

> Before: The new policy — announced without warning — affects thousands of workers. The changes -- long overdue according to critics -- will take effect immediately.
> After: The new policy, announced without warning, affects thousands of workers. The changes, long overdue according to critics, will take effect immediately.

> Before: The update does not change the file format — but it does change the load order.
> After: The update does not change the file format, but it does change the load order.
> (Every word stays; the comma states the contrast the dash staged.)

### P16. Repeated openings and synonym cycling (density) [U, W]

**Watch for:** three or more sentences in a row starting with the same subject, often *she* or *he* (from earlier Humanizer releases, not from Wikipedia; repeated openings are common in human writing too, so act only on a run of them). And the opposite habit: one thing renamed in each sentence to avoid repeating a word ("the dashboard ... the interface ... the portal ... the analytics hub"). Wikipedia files this "elegant variation" as a historical sign, from a repetition penalty in older models, and Graphite's 2026 study found model-written articles use a wider vocabulary than human ones.
**Fix:** for openings, merge sentences or begin with the action; do not ban the word, and a remaining sentence may still start with it. For synonym cycling, keep one name for one thing, the writer's first or most specific one.
**Keep when:** the repetition is rhythm on purpose ("She came. She saw. She conquered."), or the different names are different things.

> Before: She noted the door. She noted the lock on it. She filed both away.
> After: She noted the door and its lock, then filed both away.

### P17. Passive hiding a known actor (density) [U]

**Watch for:** passive verbs or subjectless fragments where the text elsewhere says who acts.
**Why:** this is a clarity edit, not evidence of AI writing on its own: in a 2025 study (Reinhart et al., PNAS), GPT-4o used the agentless passive at half the human rate. Act on it in text you are already editing for other tells.
**Fix:** name the actor the text gives. If the text never says who, keep the passive; inventing an actor ("the system", "we") breaks hard rule 2.

> Before: It was decided by the board that the release would be delayed.
> After: The board decided that the release would be delayed.
> (The text names who decided, not who delays, so the second passive stays.)

## Formatting

### P18. Bold as decoration, bold-label lists (defect) [W]

**Watch for:** bold on every key term or acronym; vertical lists where every item opens with a bold label and a colon.
**Why:** Wikipedia traces it to READMEs, slide decks and listicles: emphasis on everything, "often in a key takeaways fashion".
**Fix:** remove the bold. A label whose words say something its line does not (a topic, a category) keeps its words as a plain lead-in; never fold them into the sentence, which can change its scope. Turn a labelled list into prose when the labels carry nothing their lines do not.
**Keep when:** the document's format needs the bold (a glossary, a reference table, a house style).

> Before: It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.
> After: It blends OKRs (Objectives and Key Results), KPIs (Key Performance Indicators), and visual strategy tools such as the Business Model Canvas (BMC) and Balanced Scorecard (BSC).

> Before:
> - **User Experience:** The user experience has been significantly improved with a new interface.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.
>
> After: The user experience has been significantly improved with a new interface, performance has been enhanced through optimized algorithms, and security has been strengthened with end-to-end encryption.

> Before:
> - **Rollback:** Each deploy keeps the previous image for 7 days.
> - **Secrets:** Rotated keys take effect on the next restart.
>
> After:
> - Rollback: Each deploy keeps the previous image for 7 days.
> - Secrets: Rotated keys take effect on the next restart.
> (The labels name topics the lines do not, so their words stay; only the bold goes.)

### P19. Decorative headings, emoji and tiny tables (defect) [W, U]

**Watch for:** emoji or arrows (→) in front of headings and bullets; decorative symbols in prose: ⚠ or ✅ as markers, box-drawing lines (─), which vendor data from Pangram puts at 57 to 940 times the human rate; a horizontal rule between every section; a top-level heading that repeats the document's own title; headings that skip levels; small, thin tables that would read better as a sentence; headings in Title Case **when the surrounding document uses sentence case**. From earlier Humanizer releases: a heading written for effect ("The decision, on one screen") instead of naming the content.
**Fix:** remove the decoration, let the title stand once, turn a two-row table into prose. A symbol that says something stays: → meaning "leads to", ≈ before a number and the writer's own shorthand are conventions (SKILL.md hard rule 5), and so is technical notation. Keep each heading's words unless the heading itself is the tell. Change heading case only to match the document or a named house style; Title Case is correct in many styles.

> Before: 🚀 **Launch Phase:** The product launches in Q3 / 💡 **Key Insight:** Users prefer simplicity
> After: The product launches in Q3. Key insight: users prefer simplicity.
> ("Launch Phase" repeats its line and goes. "Key Insight" ranks the finding, so the words stay without the emoji and bold.)

### P20. Curly quotes in a straight-quote format (density) [W]

**Watch for:** curly quotes and apostrophes (“...”, ’) mixed with straight ones, or curly quotes in a target that uses straight ones (code comments, Markdown docs, commit messages). Wikipedia: ChatGPT and DeepSeek typically use curly quotes, while "Gemini and Claude models typically do not"; Word and macOS auto-curl, and typeset publications use them.
**Fix:** match the target format, consistently. Never convert quotes the writer typed on purpose.

## Leftovers from the chat and the draft

### P21. Chatbot residue and clerk tone (defect) [W]

**Watch for:** I hope this helps, Of course!, Certainly!, Great question!, You're absolutely right, here is a ..., a more detailed breakdown; clerk or customer-service tone in a reply: I have carefully reviewed, I apologize for any inconvenience this may have caused. Wikipedia describes these as correspondence pasted into an article. Also stock email pleasantries: "I hope (or trust) this message finds you well" and "I am writing to" (both among the page's search phrases for AI-written messages).
**Fix:** remove the wrapper that carries nothing: praise for the question, "I hope this helps", a hope-you're-well opener, "Here is an overview of". Preserve every offer, request, question, thanks, apology and encouragement, with its conditions and any request for a response, including engagement prompts on posts ("Drop a comment below" asks readers to reply). Do not add a purpose or eligibility condition. "Let me know if you'd like me to add benchmarks" can become "Tell me if you want me to add benchmarks", never "I can add benchmarks if that helps review". Clerk tone keeps its content: the apology, and the care the writer claims ("carefully"). Remove correspondence-specific content only when the user explicitly authorizes that transformation (for example, "turn this into an article").
**Keep when:** a greeting, sign-off, question, offer or encouragement serves what the writer is trying to do, in any genre: emails, comments, PR descriptions, reports, posts.

> Before: Great question! Here is an overview of the French Revolution. It began in 1789 when a financial crisis and food shortages led to widespread unrest. I hope this helps! Let me know if you'd like me to expand on any section.
> After: The French Revolution began in 1789 when a financial crisis and food shortages led to widespread unrest. Let me know if you'd like me to expand on any section.

### P22. Source and knowledge disclaimers (defect) [W]

**Watch for:** while specific details are limited or scarce, not widely available, documented or disclosed, in the provided or available sources, based on available information, maintains a low profile, keeps personal details private, likely [grew up, studied, began], it is believed that; source-usage hedges: "[claim] should be treated as ... rather than ...", "does not by itself establish" (keep their modality: *should be treated as* is advice, not a statement); a disambiguation that "X should not be confused with Y", which the page calls less reliable than the other two (keep any real disambiguation). Wikipedia lists source-availability hedges among the most common signs as of October 2026 and calls the guess that follows them speculative, "including the very claim that it's 'not documented'". Cutoff phrases ("as of my last knowledge update", "up to my last training update") are historical (2022-2023) but still appear in pasted text, and so is the didactic "it's important (or critical) to note / remember", which the page files as the 2023-24 era of these disclaimers.
**Why:** a model that found no source fills the gap with a claim about sources and a guess about the subject.
**Fix:** a style edit cannot verify these, so do not resolve them. Keep each claim and its hedge at its strength (reword only the stock phrasing), and list every unverified claim in the note so the writer can check or cut it. Cut them only when the user asks.

> Before: Information about her early life is not publicly available, suggesting she maintains a low profile. She likely grew up in a middle-class household, which shaped her later interest in education reform.
> After: unchanged.
> (Note to the writer: four claims here are unverified: that her early life is undocumented, that she keeps a low profile, where she grew up, and what shaped her interest in education reform. Wikipedia's page calls all of these speculative, including the claim that nothing is documented. Check them against a source or cut them.)

### P23. Heading restated as the first sentence (defect) [U]

**Watch for:** a heading followed by a one-line paragraph that repeats it before the content starts.
**Fix:** delete the restatement when it says no more than the heading. If it adds a claim the heading does not make ("## Performance / Speed matters." claims speed matters), it is content: keep it, or join it to the next sentence.

> Before: ## Installation / This section covers installation. / Run the installer, then restart the shell.
> After: ## Installation / Run the installer, then restart the shell.

### P24. Writing about the document or the process (defect) [W, U]

**Watch for:** a layout the reader can see ("the table below compares"); how the text was made ("generated from", "compiled from"); in change descriptions (commit messages, PR bodies, edit summaries), procedural boasts: "while preserving", "retaining", "ensuring", "avoided", "aimed to", "refined", "streamlined", "enhanced", "in compliance with", "neutral tone", which Wikipedia documents as typical of AI edit summaries; clerk remarks about the effort ("I have carefully reviewed").
**Fix:** write about the subject, and remove narration that tells the reader nothing about it. Keep provenance, previous behaviour, reasons for a change, compatibility guarantees and known limits wherever they inform the reader, including PR descriptions and commit messages; state each plainly, once.

> Before: The table below compares the plans. [table]
> After: [table]
> (The reader can see that the table compares the plans.)

> Before: The figures below are drawn from each vendor's published pricing; anything we could not confirm is flagged rather than guessed.
> After: The figures below are drawn from each vendor's published pricing. Anything we could not confirm is flagged, not guessed.

> Before: Refactored the parser to improve readability while preserving existing behavior and ensuring backward compatibility.
> After: unchanged.
> (Wikipedia lists "while preserving" and "ensuring" among AI edit-summary habits, but here they state guarantees a reviewer relies on, and each rewording tried moved who ensures what. Keep them.)

### P25. Re-explaining what the reader knows (defect) [U]

Act on this only when the text is a reply and you can see, or the text plainly shows, what the other person already knows. If you cannot tell, leave the order alone.
**Watch for:** a short reply that restates the problem, walks through the diagnosis and lays out the evidence before reaching the decision; background the other person wrote themselves; the answer in the last line.
**Fix:** put the decision first. Keep the reasoning, evidence and background claims afterward, even when the reader already knows them. Delete a passage only when its claim survives elsewhere in the rewrite on the same terms. Move material into a separate artifact only when the user explicitly authorizes that transformation and receives the material as part of the requested output.

> Before: Yeah, you're right, this works around the issue rather than fixing it. The real fix is in `MergeService`: when we move a child under a new parent, it should update `pipeline_id` along with `parent_id`. We can backfill the bad rows from the audit log with `Change.where(field: "pipeline_id", source: "merge")`. I checked QA: 123 past merges, only 6 rows wrong now, so the cleanup is small. Since `MergeService` is shared and not specific to this account, I'd rather open a separate ticket than widen this PR. The fallback here is fine to keep until then.
>
> After: Yeah, you're right, this works around the issue rather than fixing it. Since `MergeService` is shared and not specific to this account, I'd rather open a separate ticket than widen this PR. The fallback here is fine to keep until then.
>
> The real fix is in `MergeService`: when we move a child under a new parent, it should update `pipeline_id` along with `parent_id`. We can backfill the bad rows from the audit log with `Change.where(field: "pipeline_id", source: "merge")`. I checked QA: 123 past merges, only 6 rows wrong now, so the cleanup is small.

### P26. Leftover placeholders and template text (defect) [W]

**Watch for:** [Company Name], [insert date], INSERT_X, Lorem ipsum, "(add citation)", "Your Name", fill-in-the-blank phrasing.
**Fix:** never fill a placeholder with invented content. Leave it, and list it in the note so the writer can fill it.

---

## Why these patterns exist

Wikipedia's account has two causes. Pretraining pulls output toward "the most statistically likely result that applies to the widest variety of cases", so specific, unusual facts give way to generic, positive ones; then tuning on human feedback pushes it toward "the most broadly palatable prose". The result is a text that is "simultaneously less specific and more exaggerated". Most patterns here are one of those two moves: a sentence that signals importance instead of adding a fact, or a shape (triad, contrast, closer, bold label) applied whether or not the content needs it. Word habits change from one model generation to the next (see P14's eras), and so do some structural ones: the page now files em dashes and "In summary" recaps under historical indicators, while noting that dashes are still produced.
