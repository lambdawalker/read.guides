# Reading books: editorial brief and letter tracker

These are working editorial notes, not a finalized implementation specification.

## Confirmed goals

- Create small Spanish reading books for a two-year-old, beginning with animals.
- Use short words: mostly two syllables, at most three. Short grammatical words such as el, la, se and y are necessary; confirm the precise vocabulary during manuscript review.
- The opening two pages show an animal doing something, then falling.
- Use **cayó** in the fall sentence. The child already knows and frequently uses this spoken word. Do not replace it with cae. Spoken familiarity does not establish independent reading mastery.
- Illustrations should be very colorful, hand drawn, with splashes of color and funny, slightly distorted animals.
- A Python script must overlay the sentences, assemble a PDF, and export individual pages as PNG.
- Each asset bundle must contain the illustrations and YAML with text per page.
- Books 1 and 2 together cover C, T, M, N, L, LL, B, V, P, G, Y, S and D. They need not each contain every target.
- Book 3 introduces another consonant. A longer-term introduction cadence of every three books is proposed below. Focus current work on Book 1.

## Letter and sound tracker

“In scope” means permitted/planned, not confirmed mastered. Recognition, sound association and independent reading must be tracked separately from spoken vocabulary. Vowels are provisionally available; confirm with the parent. Accents are preserved, especially in cayó.

| Letter / spelling | Current scope | Initial sound or use | Introduction | Observed mastery |
|---|---|---|---|---|
| A, E, I, O, U | Assumed available; confirm | Vowels; include correct written accents | Foundation | Not assessed |
| C | In scope | Prefer ca, co, cu initially; ce/ci separate sound pattern | Books 1–2 | Not assessed |
| T | In scope | ta, te, ti, to, tu | Books 1–2 | Not assessed |
| M | In scope | ma, me, mi, mo, mu | Books 1–2 | Not assessed |
| N | In scope | na, ne, ni, no, nu | Books 1–2 | Not assessed |
| L | In scope | la, le, li, lo, lu | Books 1–2 | Not assessed |
| LL | In scope; digraph | Usually shares Y's consonant sound in Mexican Spanish | Books 1–2 | Not assessed |
| B | In scope | Same phoneme as V | Books 1–2 | Not assessed |
| V | In scope | Same phoneme as B; distinct written letter | Books 1–2 | Not assessed |
| P | In scope | pa, pe, pi, po, pu | Books 1–2 | Not assessed |
| G | In scope | Prefer ga, go, gu initially; ge/gi and gue/gui later | Books 1–2 | Not assessed |
| Y | In scope | Consonant in cayó; conjunction y has vowel sound | Books 1–2 | Spoken word cayó is familiar; reading not assessed |
| S | In scope | sa, se, si, so, su | Books 1–2 | Not assessed |
| D | In scope | da, de, di, do, du | Books 1–2 | Not assessed |
| F | Future; proposed next consonant | fa, fe, fi, fo, fu | Book 3; reinforce 4–5 | Not assessed |
| R | Future | Single intervocalic r first; strong initial r taught separately | Proposed Book 6; reinforce 7–8 | Not assessed |
| J | Future | ja, je, ji, jo, ju | Proposed Book 9; reinforce 10–11 | Not assessed |
| Ñ | Future | ña, ñe, ñi, ño, ñu | Proposed Book 12; reinforce 13–14 | Not assessed |
| Z | Future | Usually same sound as S in Mexican Spanish | Unscheduled | Not assessed |
| H | Future | Silent in ordinary Spanish words | Unscheduled | Not assessed |
| Q | Future | Teach with U in que, qui | Unscheduled | Not assessed |
| K | Future | Lower priority; vocabulary dependent | Unscheduled | Not assessed |
| W | Future | Lower priority; vocabulary dependent | Unscheduled | Not assessed |
| X | Future | Pronunciation depends on word | Unscheduled | Not assessed |
| CH | Future; digraph | Treat as a separate sound/spelling lesson | Unscheduled | Not assessed |
| RR | Future; digraph | Strong R sound between vowels | After introduction of R | Not assessed |
| GE/GI, GUE/GUI, GÜE/GÜI, CE/CI | Later spelling patterns | Existing letters with additional rules | Unscheduled | Not assessed |

Animal names may include letters outside the initial set when needed. Prefer easy, familiar names and record incidental extra letters without treating them as a formal series introduction. For example, tigre adds R and the gr cluster, so it is more complex than pato despite both having two syllables. Candidate animal words include gato, pato, mono, vaca, puma, llama, lobo and tucán. Sentence words must also be checked, not just animal names.

## Proposed series cadence

- Books 1–2: distribute and repeat the agreed initial targets.
- Book 3: introduce one new consonant, provisionally F.
- Books 4–5: reinforce F and previous targets, without requiring another new consonant.
- Book 6: introduce one new consonant, provisionally R; Books 7–8 reinforce.
- Continue introductions in Books 9, 12, 15, etc., with two reinforcement books after each introduction.
- This interprets “new letters every three books” as an introduction at the start of each three-book cycle beginning with Book 3. Sequence and pace remain adjustable; coverage does not imply mastery.
- New spelling patterns and consonant clusters should be tracked separately from new letters.

## Book 1: proposed editorial direction

- Animal theme, short sentences, repeated ending containing **se cayó**.
- A provisional two-page example: “El pato caminó.” / “El pato se cayó.” Both sentences use past tense and only in-scope consonants.
- Keep falls gentle and amusing, with the animal visibly fine.
- Preserve character appearance between the action and fall illustrations.
- Place large, clear text on a quiet, light area with consistent positioning.
- Generate art without embedded text; the Python renderer adds the exact Spanish wording.
- Confirmed structure: six animals, one two-page story per animal, for twelve story pages.
- Proposed production defaults: square pages, one sentence per page, cover separate from story pages. Physical dimensions and typeface remain to be selected; twelve story pages are confirmed.

## Proposed production workflow

One folder per book contains images and book.yaml. YAML describes ordered pages, exact text, image paths, and optional layout settings. A Python command runnable with uv renders numbered PNG pages and the assembled PDF from the same layout. Page size, margins, font and output resolution should be configurable. Validate missing assets, font availability and text overflow before export. Finalize the manuscript before generating all illustrations.

## Next decision

Refine illustration style together using the first two-page story: “El pato caminó.” / “El pato se cayó.” Create a preview with expressive, slightly distorted anatomy, visible hand-drawn lines, colorful paint splashes and a quiet text area. The preview is an art-direction study, not a final production asset. Review the style before producing the other five stories.
