# Worked examples

Whole texts, before and after. The examples illustrate editing decisions; the notes below each pair name the patterns applied and what was kept, cut or flagged. Check every original claim against the rewrite and every rewritten claim against the original, on the same terms: a token-check pass (`scripts/fact_diff.py`) cannot establish that the meaning is the same.

## Contents

1. Personal blog paragraph (voice kept)
2. PR description
3. Results paragraph with numbers
4. Email
5. Non-English text (French)
6. Already-human text (no change)
7. Shorthand notes the writer asked to tidy

## 1. Personal blog paragraph

Before:

> Let's be honest — moving to Lisbon wasn't just a change of address; it was a complete reinvention of how I live. Nestled between seven hills, the city boasts a vibrant café culture, breathtaking views, and a rich tapestry of history. The rent? Not cheap. My one-bedroom in Graça costs €1,150 a month — more than I paid in Leeds. But every morning, when the 28 tram rattles past my window, I'm reminded why I came. Every. Single. Morning.

After:

> Moving to Lisbon was a complete reinvention of how I live. Nestled between seven hills, the city boasts a vibrant café culture, breathtaking views, and a rich tapestry of history. The rent is not cheap: my one-bedroom in Graça costs €1,150 a month, more than I paid in Leeds. But every morning, when the 28 tram rattles past my window, I'm reminded why I came.

Notes: P4 (staged candor "Let's be honest"), P1 ("wasn't just a change of address": a move always changes the address, so the second half carries the claim, kept in the writer's words), P11 and P14 call for restraint: "nestled", "boasts", "vibrant", "breathtaking" and "rich tapestry" each carry the writer's description or opinion, and "sits", "has", "lively", "beautiful" and "rich" would lower or drop it, so that sentence stays as written (if the writer wants it plainer, ask which opinions to tone down). P15 (two connector dashes), P2 ("Every. Single. Morning." restates "every morning" from the sentence before it, so it is a repeat). Kept: first person, the serial comma, the tram, the comparison with Leeds, every number and place.

## 2. PR description

Before:

> ## 🚀 Overview
>
> This change adds a robust retry mechanism to the `upload_chunk()` function, ensuring seamless uploads even in the face of transient network failures.
>
> ## ✨ Key Changes
>
> - **Retry Logic:** Added exponential backoff with a maximum of 5 attempts.
> - **Configuration:** The retry count is now configurable via `UPLOAD_MAX_RETRIES`.
> - **Testing:** Added comprehensive unit tests covering all edge cases.
>
> ## 💡 Impact
>
> Upload failures were a pivotal pain point for users. This change not only improves reliability but also enhances the overall user experience.

After:

> ## Overview
>
> This change adds a robust retry mechanism to the `upload_chunk()` function, so uploads are seamless even during transient network failures.
>
> ## Key Changes
>
> - Added exponential backoff with a maximum of 5 attempts.
> - The retry count is now configurable via `UPLOAD_MAX_RETRIES`.
> - Added comprehensive unit tests covering all edge cases.
>
> ## Impact
>
> Upload failures were a pivotal pain point for users. This change improves reliability and enhances the overall user experience.

Notes: P19 (emoji in headings; the heading words and their Title Case stay, since the document uses them throughout), P18 (bold labels that repeat their lines), P10 ("ensuring seamless uploads" becomes a plain clause that keeps the effect, not a purpose), P1 ("not only ... but also": both halves carry a claim, so both stay). "Robust", "seamless", "pivotal", "comprehensive" and "all edge cases" are the writer's claims and stay at their degree; a reviewer may ask for evidence, and the note can say so.

## 3. Results paragraph with numbers

Before:

> These numbers highlight the crucial importance of data augmentation. Notably, the augmented model achieved an F1 score of 0.871 (95% CI 0.859–0.883), a substantial improvement over the baseline's 0.812 (95% CI 0.798–0.826). This 7.3% relative gain highlights the robustness of our approach, showcasing its potential for real-world deployment. Furthermore, inference latency remained virtually unchanged at 41 ms versus 40 ms, demonstrating that these gains come at negligible cost.

After:

> These numbers highlight how crucial data augmentation is. The augmented model achieved an F1 score of 0.871 (95% CI 0.859–0.883), a substantial improvement over the baseline's 0.812 (95% CI 0.798–0.826). This 7.3% relative gain highlights the robustness of our approach and showcases its potential for real-world deployment. Inference latency remained virtually unchanged at 41 ms versus 40 ms, which demonstrates that these gains come at negligible cost.
>
> (Note to the writer: one benchmark gain does not establish robustness or readiness for deployment. Both claims are kept at your wording's strength; support or cut them.)

Notes: P8 and P14 (the formula "the crucial importance of" becomes "how crucial", which keeps the degree word and drops the formula; "Notably" and "Furthermore" open sentences in a cluster), P10 (the riders "showcasing ..." and "demonstrating that ..." become clauses with the same verbs). The writer's reporting verbs stay: "highlight", "showcase" and "demonstrate" set how strongly the numbers back each claim, and "shows" or "proves" would change that. The repeated "highlight" is the writer's; a plain verb of the same strength would also do. Every number and both confidence intervals are kept with their en dashes (ranges, not connectors), and so are the writer's own judgments "substantial" and "virtually unchanged".

## 4. Email

Before:

> Hi Priya,
>
> Thank you so much for your prompt response! I wanted to circle back on the venue booking for the offsite. The Harbour Room is available on 14 March for up to 40 people, which is a testament to how early we started planning. In terms of next steps, we'll need to pay the €500 deposit by Friday.
>
> Should anything be unclear, I'm more than happy to help! Would you like me to set up a call with the venue to go through the catering options?
>
> Best,
> Sam

After:

> Hi Priya,
>
> Thank you so much for your prompt response! The Harbour Room is available for the offsite on 14 March for up to 40 people, which is a testament to how early we started planning. We'll need to pay the €500 deposit by Friday.
>
> I'm more than happy to help if anything is unclear. Would you like me to set up a call with the venue to go through the catering options?
>
> Best,
> Sam

Notes: P4 ("I wanted to circle back on the venue booking" and "In terms of next steps" only announce; the offsite stays named in the next sentence). P21 and P8 call for restraint here: "Thank you so much", "prompt", "more than happy" and "a testament to" carry the writer's thanks, offer and judgment at a degree that "Thanks", "quick", "happy" and "shows" would lower, so they stay. Kept: the salutation and sign-off (letters had them before chatbots), every date and amount, and the question about a call in the writer's own form.

## 5. Non-English text (French)

Before:

> Ce projet n'est pas seulement une application, c'est une véritable révolution dans la gestion des stocks. Au cœur de notre démarche : la simplicité, la fiabilité et l'innovation. Grâce à notre solution, les entrepôts réduisent leurs erreurs d'inventaire de 30 %. Le message est clair : la gestion des stocks ne sera plus jamais la même.

After:

> Ce projet est une application, et une véritable révolution dans la gestion des stocks. La simplicité, la fiabilité et l'innovation sont au cœur de notre démarche. Grâce à notre solution, les entrepôts réduisent leurs erreurs d'inventaire de 30 %. La gestion des stocks ne sera plus jamais la même.
>
> (Note to the writer: the 30 % figure is the only evidence for the revolution claim and for the prediction in the last sentence.)

Notes: the structural patterns transfer across languages. P1 ("n'est pas seulement..., c'est...": both halves are claims, so the project stays an application and a "véritable révolution", in the writer's words), P2 and P4 (the colon staging in "Au cœur de notre démarche :" and the run-up "Le message est clair :" go; the three values are distinct, so the triad stays). The last sentence adds a prediction that the change is permanent, which the first sentence does not make, so it stays. The third sentence has no tell and is unchanged. The 30 % figure keeps its French spacing, and the output stays in French.

## 6. Already-human text

Before:

> The kettle's been making that noise again, a sort of high whistle that stops when you lift it. Mum says it's limescale. I've descaled it with citric acid and it's no better, so I'm starting to think it's the element. Very annoying, but it still boils, so it can wait until payday.

After: unchanged.

Notes: British spelling, a family member's opinion reported as hers, a hedge that marks real doubt ("starting to think"), an intensifier ("very"), and a repeated "so" that is the writer's rhythm. No pattern clusters here, so nothing changes. Returning a text unchanged, with one line saying so, is a correct result.

## 7. Shorthand notes the writer asked to tidy

Request: "can you tidy these up a bit?"

Before:

> tues - got the bike back from the shop. £85, approx what J quoted. new chain + pads, rides way smoother. guy reckons the rear tyre has a few hundred km left.
>
> todo: haircut before wed. pay J back.

After: unchanged.

> (Note to the writer: I left your shorthand and lowercase as you wrote them. Does "before wed" mean Wednesday or a wedding? I can spell it out once you say.)

Notes: hard rule 5. "Tidy" does not license expanding *approx*, *pads*, *J* or *todo*, turning "+" into "and", or capitalizing: each is the writer's convention, and a journal entry that reads as theirs is the point. "wed" has two readings, so it stays and the note asks; writing "Wednesday" would pick one for the writer. "guy reckons" keeps its hedge and its vagueness (not "the mechanic says"). No pattern clusters here, so nothing else changes.
