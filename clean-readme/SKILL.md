---
name: clean-readme
description: Creates, reworks or updates a repository README and its companion files (ROADMAP.md, RESULTS.md, docs/) following fixed rules - project type (project, tool, research, collection), status block, 200 lines at most, fixed headings, nothing invented, checked by a script. Use when the user calls /clean-readme, asks to write, redo, clean up or update a README (also in French: écrire, refaire, nettoyer ou mettre à jour un README), or gives a piece of information to file in a repository whose README already follows these rules (new trial, new result, step done, project paused).
---

# clean-readme

The README describes the current state of the project and acts as its front door. Anything that grows over time (steps, trials, detailed results, long documentation) goes into a separate file, and the README keeps a summary with a link.

Reference files, to read when they are useful:

- `references/detection.md`: recognizing the type and status of a project;
- `references/structure.md`: README sections per type, ROADMAP.md, RESULTS.md, going over 200 lines, mappings for a rework;
- `references/titles.md`: exact headings in English and French, statuses, status block, anchors;
- `templates/`: one README template per type, and the ROADMAP.md and RESULTS.md templates;
- `scripts/check.py`: automatic checks.

## Arguments

| Argument | Effect |
|---|---|
| `create`, `rework`, `update` | Forces the mode |
| `type=project`, `type=tool`, `type=research`, `type=collection` | Forces the type |
| `en`, `fr` | Forces the language |
| Free text | Information to add (new trial, status change...) |

## Choosing the mode

| Situation | Mode |
|---|---|
| No README | Create |
| README that does not follow the rules | Rework |
| README that already follows the rules | Update |

A README follows the rules when it has the status block in the format of `references/titles.md`, its level 2 headings come from the tables of that file, and `scripts/check.py` reports no error. The skill leaves no marker in the README: the type and language are detected again on each run.

If the user gives a piece of information to file while the README does not follow the rules, only make the requested addition, without restructuring. Mention in the report that a rework is possible.

## Reading the repository

Do not read all the code of a large repository. Read in this order:

1. the file tree, without ignored files (`git ls-files`, or `ls` if it is not a git repository);
2. the README and existing docs;
3. configuration and build files (Makefile, package files, framework configuration);
4. entry points and scripts;
5. the git history and tags, if it is a git repository;
6. the rest of the code only if a section needs it.

To date a trial or a result, read today's date with `date +%F`. Never guess it.

## Create mode

1. Read the repository.
2. Determine the type and status with `references/detection.md`.
3. Ask a question only if it blocks the writing (see "Questions"). Otherwise, write directly.
4. Write from the type's template in `templates/` and from `references/structure.md`. Remove sections with no real content, and their lines in the table of contents.
5. Run the checks.
6. Present the report (see "Report").

## Rework mode

1. Read the repository and the existing README.
2. Determine the type and status. The existing README takes precedence over other clues.
3. Map each existing section to the new structure (see the mappings in `references/structure.md`).
4. Ask a question only if it blocks the writing. Otherwise, write directly. All information is kept, in the README or in a companion file. An existing Credits section is kept as is.
5. Run the checks.
6. Present the report, plus what was moved and to which file, and the passages that look outdated (contradicted by the code or the history), without deleting them.

## Questions

The skill asks as few questions as possible: one short message at most, and only if the information blocks the writing.

- The type is ambiguous: two types have strong clues, or no clue is usable.
- The status is Paused or Stopped, and no source gives the reason.
- A research result is claimed without a number or a file that proves it.

Everything else is decided by the skill and stated in the report. The user corrects it afterwards if they wish.

## Report

At the end, a short message that gives:

- the type and status chosen, with the main clues;
- the free sections added, if any;
- the files created or modified;
- what is still missing: screenshots to take, information to provide;
- the script warnings that were kept, with their justification.

## Update mode

Detect the type from the README headings and the language from its status block (`references/detection.md`), then file the information without asking for a plan first:

| Information received | Where it goes |
|---|---|
| New trial | RESULTS.md, trials table, with the next number. Create the file if it does not exist |
| New consolidated result | RESULTS.md, new `### Rn` section, and a line in the README's Key results if it is important |
| Step finished or started | ROADMAP.md, then the README's progress summary |
| Status change | README status block |
| Project that changed nature (proof of concept that became stable) | Suggest the new type. Once accepted, restructure |
| New feature or command | Matching README section |

Still run all the checks. If the README was edited by hand and no longer follows the rules, fix the formatting issues reported by the script and list them in the report. End with the report of the changes.

## Files produced

At most 5 documentation files created by the skill, README included:

| File | When to create it |
|---|---|
| `README.md` | Always |
| `ROADMAP.md` | Roadmap already present, user request, or more than 10 lines of progress in the README |
| `RESULTS.md` (`RESULTATS.md` in French) | Research, from the first result or the first trial |
| `docs/GUIDE.md` | README over 200 lines: detailed installation, configuration, hardware |
| `docs/HOW-IT-WORKS.md` (`docs/FONCTIONNEMENT.md` in French) | README over 200 lines: architecture, internals |
| `docs/INDEX.md` | Collection whose index pushes the README over 200 lines |

- Existing files outside this list (`CHANGELOG.md`, other `docs/` folders) are not renamed, modified or deleted. The README may link to them.
- File names without accents or spaces. Images in `docs/images/`.
- Only the root README is handled, unless asked for a subfolder.

## Writing rules

### Language

In this order: language requested by the user, language of the existing README, language the user writes in. All repository files in the same language. Headings, statuses and file names come from the tables in `references/titles.md`.

### Style

- Clear, precise, short sentences: one idea per sentence.
- No marketing tone. Words to avoid: powerful, easy, simply, robust, modern, seamless, revolutionary (and their French equivalents: puissant, facile, simplement, il suffit de, robuste, moderne, incontournable, révolutionnaire). Accepted in a proper noun or in the literal sense.
- "I" for a solo project, "we" for a team, the same person everywhere.

### Characters

- Only characters typed on a standard keyboard: ASCII letters, digits and punctuation, plus accented Latin letters for French text (`é`, `è`, `à`, `ç`, `œ`, uppercase accented letters...).
- Forbidden: curly quotes and French guillemets, curly apostrophe, en and em dashes, the single-character ellipsis, arrows, non-keyboard math symbols, box-drawing characters for trees, non-breaking spaces and zero-width characters.
- Replace with `"`, `'`, `-` or `:`, `...`, `->`, `<=`, `x`.
- Formulas: GitHub LaTeX (`$...$`) or ASCII in a code block.
- Real output copied into a code block stays as is.

### Emojis

Forbidden in all files produced by the skill, ROADMAP.md included: statuses are written in text.

### Markdown form

- A single level 1 heading (readable project name). Sections at level 2, subsections at level 3, never deeper.
- Level 2 headings taken from `references/titles.md`, plus at most 2 free sections justified by the content, mentioned in the report, placed next to the closest fixed section and before the common ending.
- Code blocks always with a language. Copyable commands, without a leading `$`. Output in a separate `text` block.
- Images with alt text, relative paths.
- Relative links for repository files.
- No badges. No layout HTML. `<details>` and a sized `<img>` tolerated if needed.
- No statement that the content was generated or co-written by AI. Mentions of AI tools as the subject of the project are fine.

### Reliability

- Never invent a result, number, date, command, version or status. Leave the information out and mention it in the report, or ask if it blocks the writing. An unknown date is written "unknown" ("inconnue" in French).
- Project commands (Makefile targets, scripts, entry points) must exist in the repository. External tools used are listed in the prerequisites.
- Links, anchors and images point to files that exist and are tracked by git.
- If the overview needs missing screenshots, list the ones to take instead of leaving an empty link.
- Lose nothing: content removed from the README is moved to a companion file.

### Personal data

In copied output and examples, replace:

- local absolute paths (`/home/<user>/...`) with a relative path or `~`;
- secrets (tokens, passwords, keys, `.env` content): remove them;
- personal IP addresses, MAC addresses and host names with example values (`192.0.2.10`, `00:11:22:33:44:55`);
- email addresses the repository does not already show.

## Checks

Run the script from this skill's folder:

```bash
python3 scripts/check.py <repository-path>
```

- `ERROR`: rule broken, to fix before handing back.
- `WARNING`: point to judge. Fix it, or justify it in the report (word "simple" in the literal sense, target to commit, real output copied).
- Run again until there are zero errors.

The script checks length, characters, emojis, headings and their order, the table of contents, the status block, links, anchors, images, code blocks, badges, HTML and personal data patterns.

The skill checks by itself what the script cannot judge:

- the commands quoted exist in the repository;
- external tools are listed in the prerequisites;
- no secret that a pattern does not catch;
- the style (short sentences, words to avoid depending on context);
- information that is still valid has not been lost.

## What the skill does not do

- It does not commit or push.
- It does not delete content without moving it.
- It does not modify the project's code.
- It does not run the project's commands, unless asked: it only checks that they exist.
- It does not manage `CHANGELOG.md`, nor READMEs in several languages (`README.fr.md`).
- It does not add any marker or comment of its own to the files it writes.
- It does not create a `LICENSE` file and does not suggest a license. The License section only exists if the repository already has a license file.
- It does not write a Credits section: the user decides to add it. It keeps an existing one.
