---
name: linguistic-linter
description: Flags the constructions in a text that slow down human reading and that recent LLMs overuse, based on Clark, Martin & Mahowald (2026) - object relatives without "that", ad hoc denominal verbs ("calendar it"), inanimate subjects with animate verbs ("the function swallows the error"), stacked nouns, long dependencies, rare word sequences, telegraphic style. Returns a located list with a suggested fix for each case, without rewriting the text. Also compares several versions of a text and says which is most readable. Use when the user asks "is this readable?", "what's wrong with this text?", "which one is clearer?", "compare these two answers", "is the rewrite better?" (also in French: "laquelle est la plus claire ?"), wants a readability audit, wants to know why an AI response is hard to read, or calls /linguistic-linter. Works in English (spaCy script) and French (heuristics).
---

# linguistic-linter

Source: Clark, Martin & Mahowald (2026), *Why is AI-generated language so hard to understand?* Frontier models use more constructions known to slow down reading than humans do, because reinforcement learning under length pressure makes the shortest form the default.

This skill **detects** these constructions and suggests a fix. It does not rewrite the text: rewriting belongs to `clarity-rewriter`.

Files:

- `references/constructions.md`: the families of constructions, with examples, their cognitive cost, the fix and their French equivalent. Read it before the first audit.
- `scripts/lint.py`: automatic detection of candidates.

## Audit (one text)

1. **Get the text.** Pasted text, a file, or the agent's last response if the user says "your answer". Save it to a temporary file if needed.
2. **Run the script** if Python is available:
   ```bash
   python3 <skill>/scripts/lint.py FILE --lang auto   # readable report
   python3 <skill>/scripts/lint.py FILE --json        # machine-readable
   ```
   `<skill>` is the folder of this skill (the one holding this `SKILL.md`): the command runs from the user's project, not from here.
   English needs spaCy (`pip install spacy && python -m spacy download en_core_web_sm`; `en_core_web_trf` is more accurate and used first when installed). French uses regular expressions and needs nothing. If spaCy is missing for an English text, do not install it without asking: do step 3 alone.
3. **Read it yourself.** The script only outputs candidates. For each one, decide:
   - **keep**: a conventional construction that is transparent to the reader ("the test fails", "the function returns", "prioritize");
   - **flag**: a real reading cost.
   Add what the script misses: unexpected word sequences, undefined session jargon, unexplained code identifiers, sentences with no verb. The small spaCy model also misses some personifications when it tags the verb as a noun ("this asymmetry bites").
4. **Write the report** in the format below.

### What counts as a problem

A construction is not wrong in itself. It becomes a problem when it **piles up**, or when it lands where the reader has the least context. Priorities:

1. Cases that force the reader to reread the sentence.
2. Pile-ups: several features in one sentence.
3. Isolated, light cases. Mention them only when asked.

Do not flag conventional metaphors ("the server goes down"), technical terms the target reader knows, or a missing "that" in a short, predictable sentence.

### Report format

```
Readability: <good | needs work | hard> — <n> issues in <m> sentences

| # | Sentence (excerpt) | Feature | Why it's hard | Suggested fix |
|---|---|---|---|---|
| 1 | "…" | inanimate subject + animate verb | "swallows" hides the mechanism | "catches the exception and returns False" |

Rates (per 1,000 words): <script table, if run>
Pile-ups: sentences <i, j> combine 3 or more features.
```

Sort by severity, not by order of appearance. Beyond 15 issues, give the 15 most severe and the count of the rest.

## Comparison (several versions)

For 2 or more versions of the same content (two models, before/after a rewrite, several drafts):

1. **Run the script** on each version with `--json`. Compare `per_1k_words` for each feature and, in English, `mean_dependency_length`. Reread the candidates: a high rate can come from legitimate technical terms.
2. **Check the content is the same.** A version that is more readable because it says less does not win. If the contents differ, say what is missing and where (use `../clarity-rewriter/references/fidelity-check.md`, from the sibling skill `clarity-rewriter`, when one version is the original).
3. **Look beyond the script**: where the key point sits (first sentence, or buried), density (telegraphic or padded), fit for the target reader if one is named.
4. **Answer**:

```markdown
| Feature (per 1k words) | A | B |
|---|---|---|
| inanimate subject + animate verb | 18.4 | 5.1 |
| … | | |

**Verdict**: B is more readable. <2 or 3 sentences: the decisive difference, quoting one sentence from each version.>

**Still to fix in B**: <1 to 3 sentences from B that still trip the reader, with the fix>
```

Do not confuse readable with short: a longer version wins if it is understood in one read and the other in two. A tie is possible: say it plainly rather than forcing a winner.
