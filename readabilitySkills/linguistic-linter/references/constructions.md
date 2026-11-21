# Catalog of hard-to-read constructions

Source: Clark, Martin & Mahowald (2026), *Why is AI-generated language so hard to understand?* (arXiv:2610.29162).

The paper measures seven families of constructions. For each one, it explains why it costs a human reader effort, and why a model pushed toward information density prefers it. This file covers those seven families, with their French equivalents where they exist.

Main finding: compared with human writing, all nine frontier models studied use more **inanimate subjects with animate verbs** and more **rare word sequences**. Most of them also use, in conversation, **longer dependencies**, more **stacked nouns** and more **object relatives without "that"**. The effect is stronger in long conversations (chat, code) than in single-turn texts (essays).

Why: a model trained with a length penalty ends up always choosing the shorter form, even when the context calls for the longer one. Humans choose based on context. This preference then spreads to constructions never seen during training.

---

## 1. Reduced object relative (no relativizer)

**What it is.** A relative clause where the modified noun is the object of the clause's verb, without "that" or "which".

- *Or a first name **he'd never hear anyone use***.
- *the papercut **people feel** day-to-day*.

**Cost.** Object relatives are harder than subject relatives: the word order is unusual and the dependency is longer. Without "that", the reader also loses the cue that announces the relative clause.

**Why a model prefers it.** It drops an optional word. It also replaces a longer passive ("the house that was built by…").

**Fix.** Put "that" / "which" back. Or switch to a subject relative ("a name that nobody around him uses"). Or split into two sentences.

**French.** "que" is mandatory, so the reduction does not exist. But nested object relatives are still costly: "le correctif **que** le test **que** tu as écrit valide". Unfold them. The script reports them as `nested_object_relative`.

## 2. Ad hoc denominal verb

**What it is.** A noun used as a verb in an unconventional way.

- *So yes — **calendar** it.* / *…footnote it.* / *…which **cushions** price spikes* (figurative use).

**Cost.** Changing a word's category forces the reader to reanalyze the sentence. Words that can be either a noun or a verb are processed more slowly.

**Why a model prefers it.** "Calendar it" is shorter than "put it in your calendar".

**Fix.** Replace with a common verb plus a complement: "put it in your calendar", "add a footnote".

**French.** Neologisms in -iser and verbalized anglicisms: "calendariser", "prioriser" (now common), "scoper", "shipper", "monitorer", "adresser un problème". Flag them only if the target reader is not used to them.

## 3. Inanimate subject + animate verb (personification)

**What it is.** An object, a concept or a piece of code performs an action normally reserved for living beings.

- *The whole conversation is **eating** its own tail.*
- *`is_file()` **swallows** that and returns False.*
- *Puzzle patterns where this asymmetry **bites**.*
- *The docstring **promises**…* / *a check that covered str but **forgot** its sibling…*

**Cost.** Readers use animacy as a parsing cue. A mismatch can trigger reanalysis (the P600 brain response).

**Why a model prefers it.** The metaphorical verb stands for a longer phrase: "bites" replaces "causes an issue".

**Fix.** Say what actually happens: "`is_file()` catches the exception and returns False", "this case causes a problem when…". A conventional, transparent personification can stay ("the test fails", "the function returns").

**French.** Same pattern: "ce bug **mord** quand…", "la config **avale** l'erreur", "le parseur **oublie** le cas bytes", "la doc **promet** que…".

## 4. Stacked nouns (compounds of 3 or more nouns)

**What it is.** At least three nouns in a row, each modifying the next.

- *a horror movie soundtrack generator*
- *Fixed absolute dotfile backup path handling*
- *Policy 1's class-time shutdown requirement*
- *reader-patience budget*

**Cost.** The grouping of the words is ambiguous ("Squad Helps Dog Bite Victim"). Reading is disrupted.

**Why a model prefers them.** They pack a lot of meaning into few tokens.

**Fix.** Unfold with prepositions, a relative clause or a verb: "how absolute paths are handled when backing up dotfiles".

**French.** French rarely stacks bare nouns. The equivalent is the **chain of noun complements** ("la gestion de la configuration du chemin de sauvegarde des fichiers") and **English calques** ("le path handling", "la policy de retry backoff"). Flag from three chained "de", or from an English compound of three or more terms.

## 5. Long syntactic dependencies

**What it is.** A large distance between two syntactically linked words: subject and verb, verb and object.

- *The guitar **sitting in the corner because you're still "deciding"** teaches you zero chords.* (subject "guitar" far from its verb "teaches")
- *All five expression shapes — attribute access, subscript, calls, nested calls, string literals — leave current on…*

**Cost.** Working memory has to hold the pending element (dependency locality theory). Humans naturally avoid long distances.

**Fix.** Move the subject close to its verb. Take the aside out into its own sentence. Put heavy information at the end of the sentence.

**French.** Same principles. Watch for dash asides between subject and verb.

## 6. Unattested word pairs / low-frequency sequences

**What it is.** Word pairs (bigrams) absent from a human reference corpus, or unusual collocations.

- *Every behavioral test was verified **red** against the original source*
- *the existing **xfailed lazy-intermediate** Lookup behavior*
- *quietly eating its own **reader-patience budget***
- *not really a **gear trap***

**Cost.** Hard-to-predict words take longer to process: reading time grows with surprisal.

**Why a model prefers them.** Under density pressure, predictable words get dropped. What remains is less predictable.

**Fix.** Go back to expected collocations. Spell out private jargon ("verified red" → "I checked that each test fails on the original code"). Restore dropped function words.

## 7. Dropped optional words (non-uniform information density)

This is not a feature measured on its own in the paper. It is the mechanism shared by the features above, and the one Experiment 2 demonstrates. Alternations involved (short form → long form):

| Alternation | Short | Long |
|---|---|---|
| Complement clause | knew the answer was wrong | knew **that** the answer was wrong |
| Object relative | the book the professor wrote | the book **that** the professor wrote |
| Adjective + that | was sure the door was locked | was sure **that** the door was locked |
| so (that) | so we could follow | so **that** we could follow |
| Genitive | the old house's roof | the roof **of** the old house |
| all (of) | all the cookies | all **of** the cookies |
| (in order) to | to catch the train | **in order** to catch the train |
| Dative | gave his wife a gift | gave a gift **to** his wife |

Humans choose based on context. They keep "that" when what follows is hard to predict, to spread information evenly (the uniform information density hypothesis, UID). A model under a length penalty **always** picks the short form. Do not force the long form everywhere: restore it where what follows is surprising or heavy.

**French.** Equivalents: dropped subject or verb ("Corrigé. Testé. Poussé."), telegraphic style, dropped articles and connectives ("donc", "parce que", "ce qui veut dire que").

---

## Side signals (seen in agent output)

These features are not measured in the paper. They often come with the features above in coding transcripts (Table 2):

- Code identifiers mid-sentence with no explanation (`as_documents: true previously mutated the tag instance…`).
- Lists between dashes in the middle of a sentence.
- Sentences with no main verb ("No new branch, no change in control flow — just closing the gap…").
- Session jargon introduced earlier and reused without being redefined ("used 4× in one conversation").
