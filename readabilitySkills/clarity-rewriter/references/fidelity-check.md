# Fidelity check

A rewrite is faithful when a reader who reads only the new version **makes the same decisions** as if they had read the original. Any simplification pulls the text toward common forms, and common forms can erase a nuance. This check catches those losses.

Use it at step 6 of `clarity-rewriter` for a high-stakes text, or on its own when the user asks "does it still say the same thing?", "check you didn't lose anything", or gives an original and a rewrite (summary, translation, simplification, agent report).

## Steps

1. **Split the original into units of information.** One unit = one claim that can be checked on its own. For each, note:
   - the **content** (who, what, how much, where, when);
   - the **polarity** (affirmed / negated);
   - the **modality** (certain, likely, possible, recommended, required);
   - the **scope** (all, some, except X, only if Y);
   - the **relations** (cause, condition, concession, time order);
   - the **source** (observed, assumed, reported, tested or not).
2. **Find each unit in the rewrite** and classify it:
   - ✅ kept;
   - ⚠️ weakened or strengthened (modality or scope changed);
   - ❌ lost;
   - ➕ added (not in the original);
   - 🔀 distorted (relation reversed, assigned to the wrong subject, cause turned into mere sequence).
3. **Check the fragile spots**, where rewrites slip most often:
   - numbers, units, dates, versions, proper names, code identifiers;
   - negations and double negations;
   - quantifiers ("most" turned into "all", "3 out of 5" turned into "some");
   - caveats ("I couldn't verify", "untested", "to be confirmed");
   - who did what (the agent, the user, a test, a tool);
   - unfolded metaphors: when unfolding "this asymmetry bites", check the chosen meaning is the right one ("causes a problem", not "causes a crash").

## Report format

```
Fidelity: <faithful | faithful with caveats | unfaithful>
Units: <n> in the original — <a> kept, <b> changed, <c> lost, <d> added

Gaps:
1. ❌ Lost — original: "…" → missing. Fix: add "…" after "…".
2. ⚠️ Strengthened — "should work" became "works". Fix: "should work".

Removed on purpose: <redundancy, pleasantries, detail dropped for the reader>
```

For each gap, give the **minimal fix**, not a full new rewrite. If there are no gaps, one line is enough.

## Judgment rules

- **Unfaithful** as soon as a unit that changes a decision is lost, added or distorted: a condition, a caveat, a number, a required action, an unfixed error.
- **Faithful with caveats** for minor gaps: an intensity adverb, an illustrative example removed while the rule remains.
- **Accepted losses**: exact redundancy, pleasantries, meta-commentary, an implementation detail removed **explicitly** for a non-technical reader. List them under "Removed on purpose".
- A change of style is never a gap. Judge the meaning, not the words.
- If the original's meaning is unclear, flag it as a **source ambiguity**. Do not silently pick one reading.
