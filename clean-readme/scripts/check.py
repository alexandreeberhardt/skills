#!/usr/bin/env python3
"""Checks a repository README and its companion files against the clean-readme rules.

Usage: python3 check.py [REPOSITORY_PATH]

Prints one line per problem: LEVEL file:line [rule] message.
ERROR: rule broken. WARNING: point to check by hand.
Exit code: 1 if there is at least one error, 0 otherwise.
"""

import os
import re
import subprocess
import sys
import unicodedata

MAX_LINES = 200

TYPES = ["project", "tool", "research", "collection"]

# Allowed level 2 headings, per language.
COMMON = {
    "en": ["Disclaimer", "Contents", "Context", "Differences from upstream",
           "Limitations", "Credits", "References", "License"],
    "fr": ["Avertissement", "Sommaire", "Contexte", "Différences avec le projet d'origine",
           "Limites", "Crédits", "Références", "Licence"],
}
BY_TYPE = {
    "en": {
        "project": ["Overview", "Features", "Technical highlights", "Progress",
                    "Repository structure", "Hardware", "Build and run",
                    "Usage", "Deployment", "How it works"],
        "tool": ["Installation", "Quick start", "Features", "Configuration and options",
                 "Repository structure", "Contributing"],
        "research": ["Research question", "Progress", "Key results", "Method",
                     "Reproduce", "Repository structure", "Hardware", "Open questions"],
        "collection": ["Repository layout", "Index", "Template", "Tools"],
    },
    "fr": {
        "project": ["Aperçu", "Fonctionnalités", "Points techniques", "Avancement",
                    "Structure du dépôt", "Matériel", "Compilation et lancement",
                    "Utilisation", "Déploiement", "Fonctionnement interne"],
        "tool": ["Installation", "Usage minimal", "Fonctionnalités", "Configuration et options",
                 "Structure du dépôt", "Contribuer"],
        "research": ["Question de recherche", "Avancement", "Résultats principaux", "Méthode",
                     "Reproduire", "Structure du dépôt", "Matériel", "Questions ouvertes"],
        "collection": ["Organisation du dépôt", "Index", "Modèle", "Outils utilisés"],
    },
}
ENDING = {"en": ["Limitations", "Credits", "References", "License"],
          "fr": ["Limites", "Crédits", "Références", "Licence"]}
CONTENTS = {"en": "Contents", "fr": "Sommaire"}
STATUSES = {"en": ["In progress", "Experimental", "Paused", "Stopped", "Done"],
            "fr": ["En cours", "Expérimental", "En pause", "Arrêté", "Terminé"]}
STATUSES_NEEDING_DETAIL = {"Experimental", "Paused", "Stopped", "Expérimental", "En pause", "Arrêté"}

COMPANIONS = {
    "en": {"roadmap": "ROADMAP.md", "results": "RESULTS.md", "guide": "docs/GUIDE.md",
           "internals": "docs/HOW-IT-WORKS.md", "index": "docs/INDEX.md"},
    "fr": {"roadmap": "ROADMAP.md", "results": "RESULTATS.md", "guide": "docs/GUIDE.md",
           "internals": "docs/FONCTIONNEMENT.md", "index": "docs/INDEX.md"},
}
COMPANION_HEADINGS = {
    "en": {"roadmap": ("Roadmap", []),
           "results": ("Research results",
                       ["Contents", "Summary", "Method", "Results", "Trials",
                        "Discarded leads", "Open questions"])},
    "fr": {"roadmap": ("Feuille de route", []),
           "results": ("Résultats de recherche",
                       ["Sommaire", "Résumé", "Méthode", "Résultats", "Essais",
                        "Pistes écartées", "Questions ouvertes"])},
}

ALLOWED_LETTERS = set("àâäéèêëîïôöùûüçÿœÀÂÄÉÈÊËÎÏÔÖÙÛÜÇŸŒ²°µ€£§¤¨")
INVISIBLES = {" ", " ", " ", " ", " ", "​", "‌",
              "‍", "⁠", "﻿", "­"}
REPLACEMENTS = {"«": '"', "»": '"', "“": '"', "”": '"', "„": '"',
                "‘": "'", "’": "'", "–": "-", "—": "-", "…": "...",
                "→": "->", "←": "<-", "≤": "<=", "≥": ">=", "×": "x",
                "≠": "!=", "•": "-"}

WORDS_TO_AVOID = ["powerful", "easy", "simply", "robust", "modern", "revolutionary", "seamless",
                  "puissant", "puissante", "facile", "simplement", "il suffit de",
                  "robuste", "moderne", "incontournable", "révolutionnaire"]

RE_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
RE_FENCE = re.compile(r"^\s*(```+|~~~+)\s*([^\s`]*)")
RE_LINK = re.compile(r"(!?)\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
RE_IMG_HTML = re.compile(r"<img\b([^>]*)>", re.I)
RE_INLINE_CODE = re.compile(r"`[^`]*`")
RE_LAYOUT_HTML = re.compile(r"<\s*(p|div|center|table|h[1-6]|br|span|font|a)\b", re.I)
RE_BADGE = re.compile(r"shields\.io|badgen\.net|badge\.svg|/badges?/", re.I)
RE_ABSOLUTE_PATH = re.compile(r"(/home/[A-Za-z0-9._-]+|/Users/[A-Za-z0-9._-]+|[A-Za-z]:\\Users\\[A-Za-z0-9._-]+)")
RE_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
RE_IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
RE_MAC = re.compile(r"\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b")
RE_ATTRIBUTION = re.compile(
    r"\b(generated|written|co-?authored)\s+(by|with)\s+(an?\s+)?(ai|llm|assistant)\b"
    r"|(g[ée]n[ée]r[ée]e?s?|[ée]crite?s?|r[ée]dig[ée]e?s?|co-?[ée]crite?s?)\s+(par|avec)\s+(une\s+|l')?"
    r"(ia|intelligence artificielle|chatbot|assistant)\b", re.I)
RE_STATUS_EN = re.compile(r"^>\s*\*\*Status\*\*\s*:\s*(.+?)(?:\s*\(version\s+\S+\s+of\s+\d{4}-\d{2}-\d{2}\))?\s*\.(?:\s+(.*))?$")
RE_STATUS_FR = re.compile(r"^>\s*\*\*État\*\*\s*:\s*(.+?)(?:\s*\(version\s+\S+\s+du\s+\d{4}-\d{2}-\d{2}\))?\s*\.(?:\s+(.*))?$")

EXAMPLE_IPS = ("127.", "0.0.0.0", "255.", "192.0.2.", "198.51.100.", "203.0.113.",
               "8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1")
EXAMPLE_EMAILS = ("example.com", "example.org", "example.net", "users.noreply.github.com")


class Report:
    def __init__(self):
        self.lines = []
        self.errors = 0
        self.warnings = 0

    def error(self, file, line, rule, message):
        self.errors += 1
        self.lines.append(f"ERROR {file}:{line} [{rule}] {message}")

    def warning(self, file, line, rule, message):
        self.warnings += 1
        self.lines.append(f"WARNING {file}:{line} [{rule}] {message}")


def anchor(text):
    """Computes a heading anchor like GitHub."""
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("`", "").strip().lower()
    t = re.sub(r"[^\w\- ]", "", t)
    return t.replace(" ", "-")


def clean_heading(text):
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return t.replace("**", "").replace("`", "").strip()


def split_lines(lines):
    """Returns for each line: (number, text, zone, code block language).

    zone is "open", "close", "code" or "text".
    """
    result = []
    in_block = False
    fence = ""
    language = ""
    for i, line in enumerate(lines, 1):
        m = RE_FENCE.match(line)
        if m and (not in_block or m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence)):
            if not in_block:
                in_block, fence, language = True, m.group(1), m.group(2)
                result.append((i, line, "open", language))
            else:
                in_block = False
                result.append((i, line, "close", language))
            continue
        result.append((i, line, "code" if in_block else "text", language))
    return result


def headings(split):
    """List of headings outside code blocks: (number, level, text)."""
    found = []
    for num, line, zone, _ in split:
        if zone != "text":
            continue
        m = RE_HEADING.match(line)
        if m:
            found.append((num, len(m.group(1)), clean_heading(m.group(2))))
    return found


def file_anchors(path):
    try:
        with open(path, encoding="utf-8") as f:
            split = split_lines(f.read().splitlines())
    except (OSError, UnicodeDecodeError):
        return set()
    seen = {}
    result = set()
    for _, _, text in headings(split):
        a = anchor(text)
        n = seen.get(a, 0)
        result.add(a if n == 0 else f"{a}-{n}")
        seen[a] = n + 1
    return result


class Git:
    def __init__(self, repo):
        self.repo = repo
        self.active = False
        self.tracked = set()
        try:
            r = subprocess.run(["git", "-C", repo, "ls-files", "-z"], capture_output=True, check=True)
            self.tracked = {p for p in r.stdout.decode("utf-8", "replace").split("\0") if p}
            self.active = True
        except (OSError, subprocess.CalledProcessError):
            pass

    def is_tracked(self, relative_path):
        p = relative_path.rstrip("/")
        return p in self.tracked or any(s.startswith(p + "/") for s in self.tracked)

    def is_ignored(self, relative_path):
        r = subprocess.run(["git", "-C", self.repo, "check-ignore", "-q", relative_path],
                           capture_output=True)
        return r.returncode == 0


def describe(characters):
    parts = []
    for c in sorted(characters):
        replacement = REPLACEMENTS.get(c)
        hint = f" -> {replacement!r}" if replacement else ""
        parts.append(f"{c!r} ({unicodedata.name(c, 'unknown').lower()}){hint}")
    return ", ".join(parts)


def check_characters(report, name, split):
    """One message per line and per kind of problem, to keep the report readable."""
    for num, line, zone, _ in split:
        invisibles, emojis, drawing, others = set(), set(), set(), set()
        for c in line:
            if c in INVISIBLES:
                invisibles.add(c)
            elif ord(c) < 128 or c in ALLOWED_LETTERS or c == "️":
                continue
            elif "─" <= c <= "╿":
                drawing.add(c)
            elif unicodedata.category(c) == "So":
                emojis.add(c)
            else:
                others.add(c)
        if invisibles:
            codes = ", ".join(f"U+{ord(c):04X}" for c in sorted(invisibles))
            report.error(name, num, "characters", f"invisible character: {codes}")
        if drawing:
            report.error(name, num, "characters",
                         "box-drawing characters: use ASCII indentation")
        if emojis:
            if zone == "text":
                report.error(name, num, "emojis", f"forbidden emoji or symbol: {describe(emojis)}")
            else:
                report.warning(name, num, "emojis",
                               f"symbol in a code block: {describe(emojis)}; accepted only in real output")
        if others:
            if zone == "text":
                report.error(name, num, "characters", f"non-keyboard character: {describe(others)}")
            else:
                report.warning(name, num, "characters",
                               f"non-keyboard character in a code block: {describe(others)}; "
                               "accepted only in real output")


def check_form(report, name, split, repo, git, file_dir):
    for num, line, zone, language in split:
        if zone == "open" and not language:
            report.error(name, num, "code", "code block without a language")
        if zone == "code" and language in ("", "bash", "sh", "shell", "zsh", "console") \
                and re.match(r"^\s*\$\s", line):
            report.error(name, num, "code", "command preceded by '$'")
        if zone != "text":
            continue
        no_code = RE_INLINE_CODE.sub("", line)
        if RE_BADGE.search(no_code):
            report.error(name, num, "badges", "badges are forbidden")
        m = RE_LAYOUT_HTML.search(no_code)
        if m:
            report.error(name, num, "html", f"layout HTML tag <{m.group(1)}>")
        for img in RE_IMG_HTML.finditer(no_code):
            attrs = img.group(1)
            alt = re.search(r"\balt\s*=\s*\"([^\"]*)\"", attrs)
            if not alt or not alt.group(1).strip():
                report.error(name, num, "images", "<img> tag without alt text")
            src = re.search(r"\bsrc\s*=\s*\"([^\"]*)\"", attrs)
            if src:
                check_target(report, name, num, src.group(1), True, repo, git, file_dir)
        for m in RE_LINK.finditer(no_code):
            image, text, target = m.group(1) == "!", m.group(2), m.group(3)
            if image and not text.strip():
                report.error(name, num, "images", "image without alt text")
            check_target(report, name, num, target, image, repo, git, file_dir)


def check_target(report, name, num, target, image, repo, git, file_dir):
    if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
        return
    path, _, fragment = target.partition("#")
    if not path:
        target_abs = os.path.join(repo, name)
    else:
        target_abs = os.path.normpath(os.path.join(file_dir, path))
    relative = os.path.relpath(target_abs, repo)
    if relative.startswith(".."):
        report.error(name, num, "links", f"link leaves the repository: {target}")
        return
    if not os.path.exists(target_abs):
        report.error(name, num, "links", f"missing target: {target}")
        return
    if git.active and path:
        if git.is_ignored(relative):
            report.error(name, num, "links", f"target ignored by git, the link will break online: {target}")
        elif not git.is_tracked(relative):
            report.warning(name, num, "links", f"target not tracked by git yet, to commit: {target}")
    if image and path and not relative.replace(os.sep, "/").startswith("docs/images/"):
        report.warning(name, num, "images", f"image outside docs/images/: {target}")
    if fragment and target_abs.endswith(".md"):
        if fragment not in file_anchors(target_abs):
            report.error(name, num, "anchors", f"anchor not found: #{fragment}")


def check_data(report, name, split):
    for num, line, zone, _ in split:
        if zone in ("open", "close"):
            continue
        for m in RE_ABSOLUTE_PATH.finditer(line):
            report.error(name, num, "data", f"local absolute path: {m.group(0)}")
        for m in RE_EMAIL.finditer(line):
            if not m.group(0).lower().endswith(EXAMPLE_EMAILS):
                report.warning(name, num, "data", f"email address to check: {m.group(0)}")
        for m in RE_IPV4.finditer(line):
            ip = m.group(0)
            if all(0 <= int(x) <= 255 for x in ip.split(".")) and not ip.startswith(EXAMPLE_IPS):
                report.warning(name, num, "data", f"IP address to check: {ip}")
        for m in RE_MAC.finditer(line):
            mac = m.group(0).lower()
            if mac.replace("-", ":") not in ("00:00:00:00:00:00", "ff:ff:ff:ff:ff:ff"):
                report.warning(name, num, "data", f"MAC address to check: {m.group(0)}")
        if RE_ATTRIBUTION.search(line):
            report.error(name, num, "ai", "statement that the content was generated by AI")


def check_style(report, name, split):
    for num, line, zone, _ in split:
        if zone != "text":
            continue
        no_code = RE_INLINE_CODE.sub("", line).lower()
        for word in WORDS_TO_AVOID:
            if re.search(r"(?<!\w)" + re.escape(word) + r"(?!\w)", no_code):
                report.warning(name, num, "style",
                               f"word to avoid '{word}' (accepted in a proper noun or in the literal sense)")


def detect_language(lines, level2):
    """Language of the README: from the status block label, otherwise from the headings."""
    for line in lines:
        if line.lstrip().startswith(">"):
            if "**Status**" in line:
                return "en"
            if "**État**" in line:
                return "fr"
    en = sum(1 for _, _, t in level2 if t in sum(BY_TYPE["en"].values(), COMMON["en"]))
    fr = sum(1 for _, _, t in level2 if t in sum(BY_TYPE["fr"].values(), COMMON["fr"]))
    return "fr" if fr > en else "en"


def detect_type(level2, lang):
    """Type whose specific headings appear the most in the README, or None if it is not clear."""
    names = {t[2] for t in level2}
    scores = {}
    for project_type in TYPES:
        own = set(BY_TYPE[lang][project_type])
        for other in TYPES:
            if other != project_type:
                own -= set(BY_TYPE[lang][other])
        scores[project_type] = len(names & own)
    best = max(scores.values())
    winners = [t for t, n in scores.items() if n == best]
    return winners[0] if best > 0 and len(winners) == 1 else None


def check_readme(report, repo, git):
    path = os.path.join(repo, "README.md")
    if not os.path.isfile(path):
        report.error("README.md", 0, "files", "README.md not found at the root")
        return None
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    if len(lines) > MAX_LINES:
        report.error("README.md", len(lines), "length", f"{len(lines)} lines, maximum {MAX_LINES}")

    split = split_lines(lines)
    found = headings(split)
    level2 = [t for t in found if t[1] == 2]
    lang = detect_language(lines, level2)
    project_type = detect_type(level2, lang)

    level1 = [t for t in found if t[1] == 1]
    if len(level1) != 1:
        report.error("README.md", level1[1][0] if len(level1) > 1 else 1, "headings",
                     f"{len(level1)} level 1 heading(s), exactly 1 is required")
    for num, level, _ in found:
        if level > 3:
            report.error("README.md", num, "headings", f"level {level} heading: never deeper than 3")

    if project_type:
        allowed = set(COMMON[lang]) | set(BY_TYPE[lang][project_type])
    else:
        allowed = set(COMMON[lang]).union(*BY_TYPE[lang].values())
    free = [t for t in level2 if t[2] not in allowed]
    if len(free) > 2:
        for num, _, text in free:
            report.error("README.md", num, "headings",
                         f"free section '{text}': {len(free)} free sections, maximum 2")

    ending = ENDING[lang]
    names = [t[2] for t in level2]
    first_ending = next((i for i, n in enumerate(names) if n in ending), None)
    if first_ending is not None:
        after = names[first_ending:]
        positions = [ending.index(n) for n in after if n in ending]
        if any(n not in ending for n in after) or positions != sorted(positions):
            report.error("README.md", level2[first_ending][0], "order",
                         "the common ending must come last, in this order: " + ", ".join(ending))

    check_contents(report, split, level2, lang)
    check_status(report, split, lang)

    check_characters(report, "README.md", split)
    check_form(report, "README.md", split, repo, git, repo)
    check_data(report, "README.md", split)
    check_style(report, "README.md", split)
    return lang, project_type


def check_contents(report, split, level2, lang):
    contents_name = CONTENTS[lang]
    others = [t for t in level2 if t[2] != contents_name]
    contents = next((t for t in level2 if t[2] == contents_name), None)
    if len(others) >= 5 and not contents:
        report.error("README.md", 1, "contents", f"{len(others)} level 2 sections: a table of contents is required")
        return
    if not contents:
        return
    if len(others) < 5:
        report.warning("README.md", contents[0], "contents",
                       f"table of contents with only {len(others)} sections: remove it")
    contents_end = next((t[0] for t in level2 if t[0] > contents[0]), 10 ** 9)
    links = set()
    for num, line, zone, _ in split:
        if contents[0] < num < contents_end and zone == "text":
            links.update(m.group(3).lstrip("#") for m in RE_LINK.finditer(line) if m.group(3).startswith("#"))
    expected = {anchor(t[2]) for t in others}
    for a in sorted(expected - links):
        report.error("README.md", contents[0], "contents", f"section missing from the table of contents: #{a}")
    for a in sorted(links - expected):
        report.error("README.md", contents[0], "contents", f"table of contents link without a level 2 section: #{a}")


def check_status(report, split, lang):
    regex = RE_STATUS_EN if lang == "en" else RE_STATUS_FR
    label = "**Status**" if lang == "en" else "**État**"
    for num, line, zone, _ in split:
        if zone == "text" and line.lstrip().startswith(">") and label in line:
            m = regex.match(line.strip())
            if not m:
                report.error("README.md", num, "status", "malformed status block (see references/titles.md)")
                return
            if m.group(1) not in STATUSES[lang]:
                report.error("README.md", num, "status",
                             f"unknown status '{m.group(1)}', allowed values: " + ", ".join(STATUSES[lang]))
            elif m.group(1) in STATUSES_NEEDING_DETAIL and not (m.group(2) or "").strip():
                report.error("README.md", num, "status", f"the status '{m.group(1)}' needs a detail")
            return
    report.error("README.md", 1, "status", f"status block missing (line starting with '> {label}')")


def check_companion(report, repo, git, relative, lang, key):
    path = os.path.join(repo, relative)
    if not os.path.isfile(path):
        return
    with open(path, encoding="utf-8") as f:
        split = split_lines(f.read().splitlines())
    check_characters(report, relative, split)
    check_form(report, relative, split, repo, git, os.path.dirname(path))
    check_data(report, relative, split)
    check_style(report, relative, split)
    found = headings(split)
    for num, level, _ in found:
        if level > 3:
            report.error(relative, num, "headings", f"level {level} heading: never deeper than 3")
    if key in COMPANION_HEADINGS[lang]:
        title1, allowed2 = COMPANION_HEADINGS[lang][key]
        level1 = [t for t in found if t[1] == 1]
        if len(level1) != 1 or level1[0][2] != title1:
            report.error(relative, level1[0][0] if level1 else 1, "headings",
                         f"expected level 1 heading: '{title1}'")
        for num, level, text in found:
            if level == 2 and text not in allowed2:
                report.error(relative, num, "headings", f"unexpected level 2 heading: '{text}'")


def main():
    repo = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    if not os.path.isdir(repo):
        print(f"Folder not found: {repo}")
        return 2
    report = Report()
    git = Git(repo)
    result = check_readme(report, repo, git)
    lang = result[0] if result else "en"
    for key, relative in COMPANIONS[lang].items():
        check_companion(report, repo, git, relative, lang, key)
    other = "fr" if lang == "en" else "en"
    for key in ("results", "internals"):
        if os.path.isfile(os.path.join(repo, COMPANIONS[other][key])):
            report.error(COMPANIONS[other][key], 0, "language",
                         f"file name in {other} while the README is in {lang}")
    if result:
        print(f"Detected: language {result[0]}, type {result[1] or 'unclear'}")
    for line in report.lines:
        print(line)
    print(f"{report.errors} error(s), {report.warnings} warning(s)")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
