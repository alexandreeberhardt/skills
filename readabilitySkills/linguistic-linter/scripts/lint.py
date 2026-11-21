#!/usr/bin/env python3
"""Detects the hard-to-read linguistic constructions described in
Clark, Martin & Mahowald (2026), arXiv:2610.29162.

Usage:
    python lint.py FILE [--lang en|fr|auto] [--json]
    cat text.txt | python lint.py - [--json]

English: needs spaCy + an English model (en_core_web_trf preferred,
otherwise en_core_web_md / en_core_web_sm).
French: regular-expression heuristics (no spaCy needed).

Every detection is a CANDIDATE: the model reading the report must judge
each case in context (the paper does the same with an external
classifier for denominal verbs and inanimate subjects).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict

# --------------------------------------------------------------------------
# Heuristic lexicons
# --------------------------------------------------------------------------

# Verbs that normally select an animate subject (lemma form).
ANIMATE_VERBS_EN = {
    "eat", "swallow", "bite", "chew", "digest", "promise", "forget", "remember",
    "want", "hope", "wish", "decide", "refuse", "insist", "pretend", "lie",
    "complain", "argue", "fight", "hate", "love", "like", "care", "worry",
    "expect", "believe", "think", "know", "feel", "notice", "ask", "beg",
    "demand", "tell", "whisper", "scream", "shout", "cry", "laugh", "smile",
    "hesitate", "try", "struggle", "breathe", "sleep", "wake", "die", "kill",
    "starve", "choke", "sneak", "lurk", "hide", "punish", "reward", "trust",
    "betray", "forgive", "teach", "learn", "understand", "agree", "disagree",
    "mind", "dislike", "enjoy", "prefer", "intend", "plan", "dream", "fear",
    "panic", "sulk", "nag", "lie", "cheat", "steal", "grab", "squat",
}
# French verbs that normally take an animate subject. Stems are followed by
# a verb ending so that nouns sharing the stem ("revue", "critique", "refus",
# "oubli", "aval", "hésitation") are not matched.
_FR_END = r"(?:e|es|ent|ait|aient|é|ée|és|ées|er|era|eront)"
_FR_STEMS_1 = (
    r"mang|aval|m[aâ]ch|dig[èé]r|oubli|esp[éè]r|d[ée]cid|refus|d[ée]test|ador|"
    r"inqui[èé]t|r[ée]clam|cri|hurl|h[ée]sit|respir|rêv|pardonn|cach|tu|"
    r"ignor|aim|pleur|mépris|soupçonn|réfléchi"
)
ANIMATE_VERBS_FR = (
    rf"(?:{_FR_STEMS_1}){_FR_END}|"
    r"mord|mordent|mordait|mordu|promet|promettent|promettait|promis|"
    r"veut|veulent|voulait|voulu|ment|mentent|mentait|dort|dorment|dormait|"
    r"meurt|meurent|sait|savent|savait|comprend|comprennent|comprenait|"
    r"craint|craignent|craignait|trahit|trahissent|trahi|"
    r"se plaint|se plaignent|se bat|se battent"
)

# Ad hoc denominal verbs common in LLM output (English).
DENOMINAL_EN = {
    # Verbs that are standard in technical English (cache, version, ship,
    # flag, batch, benchmark...) are left out: they are not ad hoc.
    "calendar", "footnote", "papercut", "scope", "gate", "bucket",
    "sandbox", "action", "task", "bookmark", "sunset", "greenlight",
    "spotlight", "pressure-test", "stress-test", "sanity-check", "timebox",
    "bottleneck", "fence", "guardrail", "backstop", "paper", "cushion",
    "shim", "ladder", "funnel", "pipeline", "dogfood", "hand-wave",
    "red-team", "workshop", "journal", "baseline",
}
DENOMINAL_FR = (
    r"calendaris\w*|scop\w*|shipp\w*|monitor\w*|challeng\w*|forward\w*|"
    r"process\w*|timebox\w*|benchmark\w*|templatis\w*|sandbox\w*|bucketis\w*|"
    r"prioris\w*|adress\w* (?:un|le|ce|les|ces) (?:probl|bug|souci|point)\w*|"
    r"impact\w* (?:le|la|les|ce|cette)|baselin\w*|cach\w* (?:le|la|les) r[ée]sultat"
)

# Verbs taking a complement clause where "that" is optional.
THAT_OPTIONAL_HEADS = {
    "know", "think", "say", "believe", "realize", "notice", "find", "mean",
    "suggest", "show", "assume", "guess", "hope", "feel", "claim", "confirm",
    "verify", "ensure", "check", "see", "argue", "decide", "sure", "certain",
    "aware", "glad", "clear", "possible", "likely",
}

RELATIVIZERS = {"that", "which", "who", "whom", "whose", "where", "when"}
ANIMATE_PRONOUNS = {"i", "you", "he", "she", "we", "they", "me", "him", "her",
                    "us", "them", "someone", "somebody", "everyone", "everybody",
                    "anyone", "anybody", "nobody", "people", "who"}
# Heads that denote people: "the developer forgot" is not a personification.
HUMAN_NOUNS_EN = {
    "developer", "developers", "dev", "devs", "user", "users", "customer",
    "customers", "client", "clients", "team", "person", "people", "reader",
    "readers", "author", "authors", "manager", "managers", "maintainer",
    "maintainers", "reviewer", "reviewers", "engineer", "engineers", "human",
    "humans", "child", "children", "man", "men", "woman", "women", "colleague",
    "colleagues", "boss", "student", "students", "teacher", "teachers", "kid",
    "kids", "friend", "friends", "agent", "model", "assistant", "owner", "owners",
    "candidate", "candidates", "founder", "founders", "employee", "employees",
    "cat", "cats", "dog", "dogs", "bird", "birds", "animal", "animals", "horse",
    "horses", "mouse", "mice", "fish",
}
# Common adjectives with no telltale suffix: never part of a noun chain.
PLAIN_ADJS = {"own", "new", "old", "big", "small", "main", "other", "same",
              "whole", "full", "high", "low", "good", "bad", "last", "first",
              "next", "only", "real", "true", "raw", "top", "key", "red", "black",
              "white", "long", "short", "fast", "slow", "hard", "soft", "late",
              "early", "free", "open", "clean", "safe", "wrong", "right"}
# Adjective suffixes: an "ADJ" without one of these, inside a noun chain, is
# usually a noun the small model mis-tagged ("dotfile backup path").
ADJ_SUFFIXES = ("al", "ive", "ous", "ful", "less", "able", "ible", "ic", "ary",
                "ent", "ant", "ed", "ing", "y", "ish", "ile", "ar", "ory", "ute",
                "ete", "ure", "ine", "ate", "ior", "est", "er")
INANIMATE_PRONOUNS = {"it", "this", "that", "which", "something", "everything",
                      "nothing", "anything"}


@dataclass
class Finding:
    feature: str
    sentence_index: int
    span: str
    sentence: str
    hint: str


# --------------------------------------------------------------------------
# English (spaCy)
# --------------------------------------------------------------------------

def load_spacy_en():
    try:
        import spacy  # noqa: WPS433
    except ImportError:
        sys.exit("spaCy is not installed: pip install spacy && "
                 "python -m spacy download en_core_web_sm")
    for name in ("en_core_web_trf", "en_core_web_lg", "en_core_web_md", "en_core_web_sm"):
        try:
            return spacy.load(name), name
        except OSError:
            continue
    sys.exit("No English spaCy model found: python -m spacy download en_core_web_sm")


# Three or more very short sentences in a row ("Fixed. Tested. Pushed.",
# "Corrigé. Testé. Poussé.").
TELEGRAPHIC = re.compile(r"(?<!\S)(?:[A-ZÀ-ÖØ-Þ][^\s.!?]*(?:\s+[^\s.!?]+){0,2}[.!?](?:\s+|$)){3,}")

CODE_SPAN = re.compile(r"`[^`]+`")


def preprocess(text: str) -> str:
    # As in the paper: code blocks removed, inline code replaced by a
    # single word so the sentence still counts as one sentence.
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = CODE_SPAN.sub("CODEX", text)
    text = re.sub(r"https?://\S+", "URLX", text)
    return text


def lint_en(text: str):
    nlp, model = load_spacy_en()
    doc = nlp(preprocess(text))
    findings: list[Finding] = []
    sents = list(doc.sents)
    words = sum(1 for t in doc if not t.is_punct and not t.is_space)
    dep_lengths = []

    for i, sent in enumerate(sents):
        s = sent.text.strip()
        if not s:
            continue

        # -- Dependencies: mean length and distant subject-verb
        arcs = [abs(t.i - t.head.i) for t in sent
                if t.dep_ != "ROOT" and not t.is_punct and not t.head.is_punct]
        content_words = [t for t in sent if not t.is_punct]
        if arcs and 1 <= len(content_words) <= 30:
            dep_lengths.append(sum(arcs) / len(arcs))
        for t in sent:
            if t.dep_ in ("nsubj", "nsubjpass") and t.head.pos_ in ("VERB", "AUX"):
                gap = [w for w in doc[min(t.i, t.head.i) + 1:max(t.i, t.head.i)]
                       if not w.is_punct]
                if len(gap) >= 7:
                    findings.append(Finding(
                        "long_dependency", i,
                        f"{t.text} … {t.head.text} ({len(gap)} words in between)", s,
                        "Move the subject closer to its verb; take the aside out into its own sentence."))

        # -- Object relatives (with / without relativizer)
        for t in sent:
            if t.dep_ != "relcl":
                continue
            kids = list(t.children)
            has_subj = any(k.dep_ in ("nsubj", "nsubjpass") and k.lower_ not in RELATIVIZERS
                           for k in kids)
            rel = [k for k in kids if k.lower_ in RELATIVIZERS or k.tag_ in ("WDT", "WP", "WP$")]
            if not has_subj:
                continue  # subject relative: not relevant
            if t.head.pos_ not in ("NOUN", "PROPN", "PRON"):
                # dubious parse: a "relative" attached to a verb is
                # usually a complement clause without "that"
                if not rel:
                    findings.append(Finding(
                        "optional_that_dropped", i, f"{t.head.text} … {t.text}", s,
                        "Add \"that\" if the clause is long or surprising."))
                continue
            span = f"{t.head.text} … {t.text}"
            if rel:
                findings.append(Finding("object_relative_with_relativizer", i, span, s,
                                        "Readable form (keep)."))
            else:
                findings.append(Finding(
                    "object_relative_reduced", i, span, s,
                    "Put \"that\"/\"which\" back, or rephrase as a subject relative."))

        # -- Complement clause without optional "that"
        for t in sent:
            if t.dep_ == "ccomp" and t.head.lemma_.lower() in THAT_OPTIONAL_HEADS and t.i > t.head.i:
                if not any(k.dep_ == "mark" for k in t.children):
                    findings.append(Finding(
                        "optional_that_dropped", i, f"{t.head.text} … {t.text}", s,
                        "Add \"that\" if the clause is long or surprising."))

        # -- Denominal verbs (heuristic list)
        for t in sent:
            if t.pos_ == "VERB" and t.lemma_.lower() in DENOMINAL_EN:
                findings.append(Finding(
                    "denominal_verb", i, t.text, s,
                    "Replace with a common verb + complement (e.g. \"put it in the calendar\")."))

        # -- Inanimate subject + animate verb
        for t in sent:
            if t.dep_ != "nsubj" or t.head.pos_ != "VERB":
                continue
            v = t.head
            if v.lemma_.lower() not in ANIMATE_VERBS_EN:
                continue
            if any(k.dep_ == "auxpass" for k in v.children):
                continue
            low = t.lower_
            inanimate = (
                low in INANIMATE_PRONOUNS
                or t.text == "CODEX"
                # VERB/X: nouns the small model mis-tags ("the docstring promises")
                or (t.pos_ in ("NOUN", "VERB", "X") and low not in ANIMATE_PRONOUNS
                    and low not in HUMAN_NOUNS_EN
                    and t.ent_type_ not in ("PERSON", "NORP", "ORG"))
            )
            if inanimate:
                findings.append(Finding(
                    "inanimate_subject_animate_verb", i, f"{t.text} {v.text}", s,
                    "Describe the real mechanism (e.g. \"swallows the error\" -> \"catches the exception and ignores it\")."))

        # -- Stacked nouns (>= 3 nouns in a compound chain)
        seen = set()
        for t in sent:
            if t.pos_ not in ("NOUN", "PROPN") or t.dep_ == "compound" or t.i in seen:
                continue
            def in_chain(c):
                if c.dep_ == "compound" and c.pos_ in ("NOUN", "PROPN", "ADJ"):
                    return True
                # mis-tagged noun: "dotfile" / "backup" parsed as ADJ amod
                return (c.dep_ == "amod" and c.pos_ == "ADJ"
                        and not c.lower_.endswith(ADJ_SUFFIXES)
                        and c.lower_ not in PLAIN_ADJS
                        and c.head.pos_ in ("NOUN", "PROPN"))
            chain = [c for c in t.subtree if in_chain(c)]
            chain = [c for c in chain if c.head == t or in_chain(c.head)]
            if len(chain) + 1 >= 3:
                toks = sorted(chain + [t], key=lambda x: x.i)
                seen.update(x.i for x in toks)
                findings.append(Finding(
                    "stacked_nouns", i, doc[toks[0].i:toks[-1].i + 1].text, s,
                    "Unfold with prepositions or a relative clause (\"the handling of ... for ...\")."))

    for m in TELEGRAPHIC.finditer(preprocess(text)):
        findings.append(Finding("optional_words_dropped", -1, m.group(0).strip(), m.group(0).strip(),
                                "Telegraphic style: restore subject, verb and connectives."))

    return findings, {"words": words, "sentences": len(sents), "model": model,
                      "mean_dependency_length": round(sum(dep_lengths) / len(dep_lengths), 2)
                      if dep_lengths else None}


# --------------------------------------------------------------------------
# French (heuristics)
# --------------------------------------------------------------------------

SENT_SPLIT = re.compile(r"(?<=[.!?…])\s+(?=[A-ZÀ-ÖØ-Þ«\"`])")
DE_CHAIN = re.compile(
    r"\b\w+(?:\s+(?:de la|de l'|du|des|de|d')\s*\w+){3,}", re.I)
FR_FUNCTION_WORDS = r"(?:le|la|les|et|de|des|du|un|une|ce|cette|au|aux|en|sur|par|pour|avec|est|sont)"
ENG_COMPOUND = re.compile(rf"\b(?:(?!{FR_FUNCTION_WORDS}\b)[a-z]+[- ]){{2,3}}(?:handling|path|policy|flow|check|"
                          r"logic|layer|config|pipeline|budget|loop|state|backoff|retry|"
                          r"fallback|cache|guard|wrapper|helper)\b", re.I)
# Subject = a noun phrase that opens a sentence or a clause (after a comma
# or a coordinating conjunction), up to 8 words before the verb. Object
# clitics between subject and verb are allowed ("la config l'avale").
_FR_DET = r"(?:le|la|les|l'|ce|cet|cette|ces|son|sa|ses|leur|leurs|un|une|des|chaque|tout|toute)"
_FR_CLITIC = r"(?:ne\s+|n'|se\s+|s'|l'|le\s+|la\s+|les\s+|lui\s+|leur\s+|y\s+|en\s+)*"
INANIMATE_SUBJ_FR = re.compile(
    rf"(?:^|[,;:]\s*|\b(?:et|mais|car|donc|puis|alors)\s+)"
    rf"(?P<subj>{_FR_DET}\s*(?P<head>[^\W\d_]+)(?:\s+[^\s,;:.!?]+){{0,8}}?)\s+"
    rf"{_FR_CLITIC}(?P<verb>{ANIMATE_VERBS_FR})\b", re.I)
# Pronoun subjects: only ça / cela / il / elle directly before the verb.
# Impersonal "il faut", "il y a" never match because those verbs are not listed.
PRONOUN_SUBJ_FR = re.compile(
    rf"\b(?P<subj>ça|cela|il|elle|ils|elles)\s+{_FR_CLITIC}(?P<verb>{ANIMATE_VERBS_FR})\b", re.I)
# Heads that denote people: a subject headed by one of these is not a personification.
HUMAN_NOUNS_FR = {
    "utilisateur", "utilisateurs", "utilisatrice", "développeur", "développeurs",
    "développeuse", "dev", "devs", "client", "clients", "cliente", "équipe",
    "personne", "personnes", "gens", "lecteur", "lecteurs", "lectrice", "auteur",
    "auteurs", "autrice", "manager", "managers", "user", "users", "humain",
    "humains", "enfant", "enfants", "homme", "hommes", "femme", "femmes",
    "collègue", "collègues", "chef", "cheffe", "patron", "patronne", "mainteneur",
    "mainteneurs", "relecteur", "relecteurs", "reviewer", "reviewers", "agent",
    "modèle", "assistant", "candidat", "candidate", "élève", "élèves", "public",
}
# Nested object relatives: "le correctif que le test que tu as écrit valide".
NESTED_RELATIVE_FR = re.compile(
    rf"\b[^\W\d_]+\s+qu(?:e\s+|')\s*{_FR_DET}\s*(?:[^\W\d_]+\s+){{0,2}}?[^\W\d_]+\s+qu(?:e\b|')",
    re.I)
DASH_INCISE = re.compile(r"\s[—–-]\s[^—–]{15,}?\s[—–-]\s")


def lint_fr(text: str):
    text = preprocess(text)
    sents = [s.strip() for s in SENT_SPLIT.split(text) if s.strip()]
    findings: list[Finding] = []
    words = len(re.findall(r"\w+", text))
    for i, s in enumerate(sents):
        n = len(re.findall(r"\w+", s))
        if n > 30:
            findings.append(Finding("long_sentence", i, f"{n} words", s,
                                    "Split into two sentences; bring subject and verb together."))
        for m in DE_CHAIN.finditer(s):
            findings.append(Finding("stacked_nouns", i, m.group(0), s,
                                    "Chain of noun complements: unfold with a verb or a relative clause."))
        for m in ENG_COMPOUND.finditer(s):
            findings.append(Finding("stacked_nouns", i, m.group(0), s,
                                    "Stacked English compound: translate and unfold."))
        for m in re.finditer(rf"\b(?:{DENOMINAL_FR})\b", s, re.I):
            findings.append(Finding("denominal_verb", i, m.group(0), s,
                                    "Denominal verb / anglicism: replace with a common verb if the reader does not know it."))
        for m in INANIMATE_SUBJ_FR.finditer(s):
            if m.group("head").lower() in HUMAN_NOUNS_FR:
                continue
            findings.append(Finding("inanimate_subject_animate_verb", i,
                                    f"{m.group('subj')} … {m.group('verb')}", s,
                                    "Personification candidate: check the subject is inanimate, then describe the real mechanism."))
        for m in PRONOUN_SUBJ_FR.finditer(s):
            findings.append(Finding("inanimate_subject_animate_verb", i, m.group(0), s,
                                    "Personification candidate if the pronoun stands for a thing: describe the real mechanism."))
        for m in NESTED_RELATIVE_FR.finditer(s):
            findings.append(Finding("nested_object_relative", i, m.group(0), s,
                                    "Nested relative clauses: split into two sentences."))
        for m in DASH_INCISE.finditer(s):
            findings.append(Finding("long_dependency", i, m.group(0).strip(), s,
                                    "Dash aside: take it out into its own sentence."))
    for m in TELEGRAPHIC.finditer(text):
        findings.append(Finding("optional_words_dropped", -1, m.group(0).strip(), m.group(0).strip(),
                                "Telegraphic style: restore subject, verb and connectives."))
    return findings, {"words": words, "sentences": len(sents), "model": "regex-fr"}


# --------------------------------------------------------------------------

def detect_lang(text: str) -> str:
    fr = len(re.findall(r"\b(?:le|la|les|des|est|une|que|qui|pas|pour|avec)\b", text, re.I))
    en = len(re.findall(r"\b(?:the|is|are|and|that|with|for|not|this|you)\b", text, re.I))
    return "fr" if fr > en else "en"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="text/markdown file, or - for stdin")
    ap.add_argument("--lang", choices=["en", "fr", "auto"], default="auto")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
    lang = detect_lang(text) if args.lang == "auto" else args.lang
    findings, meta = lint_en(text) if lang == "en" else lint_fr(text)

    counts: dict[str, int] = {}
    for f in findings:
        counts[f.feature] = counts.get(f.feature, 0) + 1
    per_1k = {k: round(v * 1000 / max(meta["words"], 1), 2) for k, v in counts.items()}
    meta.update({"lang": lang, "counts": counts, "per_1k_words": per_1k})

    if args.json:
        print(json.dumps({"meta": meta, "findings": [asdict(f) for f in findings]},
                         ensure_ascii=False, indent=2))
        return

    print(f"# linguistic-linter report ({lang}, {meta['model']})")
    print(f"{meta['words']} words, {meta['sentences']} sentences"
          + (f", mean dependency length {meta['mean_dependency_length']}"
             if meta.get("mean_dependency_length") else ""))
    print()
    if not findings:
        print("No candidates found.")
        return
    print("| feature | n | per 1k words |\n|---|---|---|")
    for k in sorted(counts, key=counts.get, reverse=True):
        print(f"| {k} | {counts[k]} | {per_1k[k]} |")
    print()
    for f in findings:
        if f.feature == "object_relative_with_relativizer":
            continue
        print(f"- [{f.feature}] \"{f.span}\"")
        print(f"    sentence {f.sentence_index}: {f.sentence[:200]}")
        print(f"    -> {f.hint}")


if __name__ == "__main__":
    main()
