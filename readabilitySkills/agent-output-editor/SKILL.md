---
name: agent-output-editor
description: Turns an agent's technical output (coding session report, bug sweep summary, tool log, MEMORY.md, end-of-task message, CI log) into a report a human understands on the first read - what was done, what changed, what is verified or not, what is left to decide. Unfolds session jargon, unexplained identifiers, verbless sentences and personified code ("the docstring promises", "is_file() swallows"). Use when the user says "I don't understand what the agent did", "write me a report", "summarize the session", "explain what you changed in plain terms" (also in French: "fais-moi un compte rendu"), pastes an agent log or report, asks for a recap in a long session ("where are we?", "remind me what we decided", "I'm lost"; in French: "on en est où ?", "je suis perdu"), or calls /agent-output-editor.
---

# agent-output-editor

Clark, Martin & Mahowald (2026) ran agents through 11-turn coding sessions. The final replies of these sessions gather the costliest constructions: stacked nouns ("Fixed absolute dotfile backup path handling"), personified code ("the docstring promises", "a check that forgot its sibling type"), word sequences never seen before ("verified red against the original source", reused 4 times in one conversation), identifiers mid-sentence. The study's simulated developer kept asking to "explain the fixes in plain terms". This skill does that work by default.

## Input

An agent's output: pasted text, a file (log, MEMORY.md, report), or the current agent's work in this session. If the current agent is summarizing its own work, rely on what was **actually** done (diffs, command output). Do not rely on memory of what was planned.

## Steps

1. **Extract the facts.** For each change or finding:
   - **what**: the problem, in terms of behavior the user can observe;
   - **where**: file or module, with a `path:line` link if possible;
   - **how**: the fix in one sentence;
   - **evidence**: test added, test run and its result, manual check, or **nothing**;
   - **status**: fixed / proposed / not fixed / could not verify.
2. **Translate each agent phrase** into the real mechanism:
   | Agent phrase | Report |
   |---|---|
   | `is_file()` swallows the error | `is_file()` catches the permission error and returns False, without reporting it |
   | the docstring promises X | the function's documentation says X |
   | verified red against the original | I checked that the test fails on the original code (so it really catches the bug) |
   | as_documents: true previously mutated the tag instance | with the `as_documents: true` option, the code modified the tag object instead of making a copy |
   | xfailed lazy-intermediate Lookup behavior | a known behavior of `Lookup`, marked as an expected failure (`xfail`) in the tests |
3. **Structure** with the template below.
4. **Check honesty.** Never turn "proposed" into "fixed", or "should pass" into "passes". A test that was not run is reported as not run. If the agent's output is ambiguous on this point, say so. When rewriting a report someone else wrote, `../clarity-rewriter/references/fidelity-check.md` (in the sibling skill `clarity-rewriter`) lists the spots where rewrites slip.

## Template

```markdown
**In short**: <1 or 2 sentences: overall result and what the human needs to do, if anything>

**Fixed**
- <Observable behavior before → after>. <Where>. <Evidence>.

**Not fixed / to decide**
- <Problem>. <Why it was not fixed: design choice, risk, missing information>. <What needs deciding>.

**Verification**
- <Command run and result>, or "no tests run".

**Watch out** (if any)
- <Risky change, behavior changed for existing users>.
```

Drop empty sections. For a small task, a few sentences without headings are enough.

## Recap of a long session

When the user is lost in a long conversation, or the work changes phase, write a recap instead of a report. Rely on what was **actually** said or done: an option that was discussed is not a decision.

```markdown
**Where we are**: <starting goal, in one sentence>

**Decided**
- <decision> — <short reason>

**Done**
- <concrete result>

**Open**
- <remaining question or task> — <who needs to decide>

**Conversation vocabulary** (only if useful)
- *<term invented in the session>*: <definition in plain words>
```

Replace references to earlier turns ("that fix", "option B", "the other approach") with their content: "the fix for paths with spaces".

## Writing rules

- One sentence = an explicit human or technical subject + a concrete action verb. Code does not "want", "promise", "forget" or "swallow" anything.
- No more than two stacked nouns. Unfold the rest with prepositions.
- Every code identifier comes with what it does, at its first occurrence.
- No term invented during the session without its definition.
- Behavior before implementation: "files with spaces in their names were not backed up" before "path escaping in `backup_dotfiles()`".
- If the reader is not the repository's developer, adapt the level with the "Reader level" table in `clarity-rewriter`.
