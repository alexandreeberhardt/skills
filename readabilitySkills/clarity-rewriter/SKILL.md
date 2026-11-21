---
name: clarity-rewriter
description: Rewrites a text (response, paragraph, report, message) so its reader understands it on the first read, without losing or adding information. Undoes the constructions LLMs overuse (stacked nouns, personified code, ad hoc denominal verbs, relatives without "that", telegraphic style, session jargon), balances density (unfolds compressed passages, cuts filler), adapts the level to the reader (beginner, practitioner, expert, decision maker), then checks the meaning is intact. Use when the user says "rephrase this more clearly", "I don't understand your answer", "simplify without dropping anything", "too dense", "too long", "too terse", "explain it like I know nothing", "version for my manager", "more technical", "does it still say the same thing?" (also in French: "reformule plus clairement", "je ne comprends pas", "trop dense", "vulgarise", "version pour mon manager"), when a length limit applies (Slack message, commit, summary), or calls /clarity-rewriter.
---

# clarity-rewriter

Goal: the reader understands every sentence **on the first read**, and the new version contains **exactly the same information** as the original.

Basis: Clark, Martin & Mahowald (2026) show that LLMs trained under length pressure always take the short form and pack meaning into constructions that are costly to read. Humans spread information evenly: they add optional words where what follows is hard, and drop them where it is predictable. Rewriting clearly means **putting words back in the right places**. It does not mean making everything longer.

## Steps

1. **List the content.** Before touching the text, list the units of information: facts, numbers, names, conditions, caveats, degrees of certainty, requested actions. This list is the contract checked at step 6.
2. **Pick the reader.** See "Reader level" below. By default, the reader is the person in the conversation, at the level their own messages show.
3. **Diagnose the density**, per paragraph: too compressed, too diluted, or uneven (filler followed by an overloaded sentence, the most common case). For a long text, run `linguistic-linter` to spot the constructions.
4. **Rewrite** sentence by sentence with the transformation grid, then restructure if needed: conclusion or action first, one new fact per clause, a list only for 3 or more parallel items.
5. **Apply the length limit**, if there is one: cut secondary **information**, whole. Do not compress the **syntax** of everything. Three clear facts are worth more than six unreadable ones. Say what was cut if it matters.
6. **Check fidelity.** Go back to the list from step 1: every unit must appear in the new version, with the same strength. A caveat ("probably") does not become a certainty, a condition does not disappear. For a high-stakes text, or when the user asks "does it still say the same thing?", run the full check in `references/fidelity-check.md`.
7. **Return** the new version. Add a "Changes: …" line only if the user wants to see the work.

## Transformation grid

| Obstacle | Example | Transformation |
|---|---|---|
| Stacked nouns (3+) | *absolute dotfile backup path handling* | Unfold: *how absolute paths are handled when backing up dotfiles* |
| Chain of "de" (French) | *la gestion de la config du chemin de sauvegarde* | *la façon dont on configure le chemin où se fait la sauvegarde* |
| Inanimate subject + animate verb | *`is_file()` swallows that* | Real mechanism: *`is_file()` catches the error and returns False* |
| Ad hoc denominal verb | *calendar it*, *calendariser* | Common verb + complement: *put it in your calendar* |
| Reduced object relative | *the papercut people feel* | Put *that* back, or use a subject relative: *the small annoyance that people run into* |
| Subject far from its verb | *The guitar sitting in the corner because you're still deciding teaches you zero chords.* | Bring them together: *While you're still deciding, the guitar sits in the corner. It teaches you nothing.* |
| Dash aside in the middle | *All five shapes — a, b, c, d, e — leave…* | Move the list out: *All five shapes leave… The five are: a, b, c, d, e.* |
| Rare word sequence / session jargon | *verified red against the original source* | Say what it means: *I checked that each test fails on the original code* |
| Dropped function words | *Fixed. Tested. Pushed.* | *I fixed the bug, ran the tests, and pushed the change.* |
| Sentence with no verb | *No new branch, no change in control flow — just closing the gap.* | *The fix adds no branch and does not change the control flow. It only closes a gap in the check.* |
| Filler | preamble, restated question, "In other words…", a conclusion that repeats the text, generic caveats | Delete |

Where to add words: where what follows is surprising (a new term, a condition, an exception, a change of subject, a counterintuitive conclusion). Where to remove them: where what follows is predictable. A short form that is already clear stays: "He sent us a photo" does not need to become "He sent a photo to us".

## Reader level

Cues, from most to least reliable: what the user says ("it's for my CFO"), the vocabulary they use, their questions (**what** = beginner, **how** = practitioner, **trade-offs** = expert, **impact** = decision maker), the context. Ask one question only if the level is unclear **and** it changes the answer a lot. Otherwise pick the most likely level and state it in one line ("Version for a non-technical reader:").

| | Beginner | Practitioner | Expert | Decision maker |
|---|---|---|---|---|
| Opening | What it is and why it matters | The direct answer | The direct answer | The conclusion and what needs deciding |
| Jargon | None, or defined at first use | Domain terms; define the rare ones | Free, but no private session jargon | None |
| Detail | The principle, one example | The steps | Trade-offs, edge cases | Cost, risk, timeline, options |
| Dense constructions | Unfold all | Unfold when 3 or more pile up | Tolerated if conventional in the domain | Unfold all |

Expert does not mean compressed: an expert wants fewer explanations, not sentences that are harder to parse.

## Rules

- **Add nothing that is not in the original.** No invented example, no extra advice, no "in summary". Exceptions: making explicit a relation the original implies ("so", "because"), and, for a beginner, an example or analogy marked as such.
- **Remove nothing informative.** You can drop an exact repetition or an empty phrase. Never drop a caveat, an exception, a number or a condition. For a beginner or a decision maker, an implementation detail can go only if it has no bearing on their decision. Say that it was removed.
- **Keep the register and the voice.** A casual answer stays casual. Do not talk down to a beginner ("it's really simple!").
- **Keep technical terms exact.** Explain them, do not replace them with an approximate word. Code, file names and commands stay as they are. Define a term once, then reuse the same word.
- **Same language as the original**, unless asked otherwise.

## Example

Before:
> Your instinct is right; the convoluted sentence you are currently reading is quietly eating its own reader-patience budget — footnote it.

Content list: (1) the reader's instinct is right; (2) the sentence is convoluted; (3) it wears out the reader's patience; (4) recommendation: move this content to a footnote.

After:
> You're right. This sentence is convoluted, and it uses up the reader's patience. Move it to a footnote.

Same fact, two readers. Original: *`is_file()` swallows the PermissionError and returns False, so the dotfile backup path handling silently skips unreadable configs.*

- Beginner: *When the program isn't allowed to read a configuration file, it acts as if the file doesn't exist. It doesn't warn you, so the backup leaves that file out.*
- Decision maker: *Risk: some configurations are not backed up, and no message reports it. A simple fix is ready.*
