# Structure of the README and companion files

The exact headings and their translation are in `titles.md`. A section with no real content is omitted. Sections are in the order given.

## Common beginning (all types)

1. Level 1 heading: readable project name. If it is not obvious, start from the repository name and make it readable.
2. Description: 2 to 4 sentences. What the project is, what it is made with, what it is for. For research: the goal and the progress in short.
3. Status block (format in `titles.md`).
4. Disclaimer: optional, for a security or reverse engineering project, or one that touches a commercial product. Educational use, no affiliation with the brand studied, possible risks. Two or three sentences.
5. Contents: links to level 2 headings, only if there are at least 5 other level 2 sections.
6. Context: only if the project needs framing (setting, motivation, constraints).
7. Differences from upstream: only for a fork.

## Body by type

### Project

- Overview: images, diagram, board layout, demo video. For a site: link to the live version and screenshots.
- Features: short list.
- Technical highlights: optional. The technical concepts used and what the project shows (UDP sockets, POSIX threads, dynamic library loading...). Short list, one item per line.
- Progress: only if the project is not finished. Table of 10 rows at most, Status column in text. Beyond that, create ROADMAP.md and keep only a summary with a link.
- Repository structure.
- Hardware: if the project uses any.
- Build and run: starts with `### Prerequisites` (system, versions, dependencies, hardware, "tested on").
- Usage.
- Deployment: for a site or a service.
- How it works: brief, otherwise moved to `docs/HOW-IT-WORKS.md`.

### Tool

- Installation: starts with `### Prerequisites` (system, versions, dependencies, "tested on").
- Quick start: an example that works, copyable as is.
- Features.
- Configuration and options: short, otherwise moved to `docs/GUIDE.md`.
- Repository structure: optional.
- Contributing: optional, how to report a problem or suggest a change.

### Research

- Research question: what we want to find out.
- Progress: summary in 3 to 8 lines (current step, what is blocking), link to ROADMAP.md if it exists.
- Key results: 1 to 6 numbered results (R1, R2...), one or two sentences each, with a link to `RESULTS.md#r1`.
- Method: a few sentences (tools, data, protocol).
- Reproduce: starts with `### Prerequisites`, then only the commands that reproduce the key results. Flag a command that needs specific hardware or takes a long time.
- Repository structure.
- Hardware: if the project uses any.
- Open questions: what remains to be found and the planned next steps.

### Collection

- Repository layout: the common shape of each entry (typical tree).
- Index: table of entries with link, theme and status (values from `titles.md`).
- Template: link to the blank template if it exists.
- Tools: they also act as prerequisites.

## Free sections

- At most 2 level 2 sections outside the tables of `titles.md`, when the content justifies it (a custom protocol, an instruction set, the rules of a game).
- Mention them in the report.
- Place them next to the fixed section closest in topic, always before the common ending.

## Common ending (all types)

1. Limitations: what does not work or is restricted today. For research, what remains to be found goes in Open questions.
2. Credits: never written by the skill, the user decides to add it. An existing Credits section is kept as is.
3. References: papers, documentation, related projects. For academic research, optional `### Citation`, with a BibTeX entry or a `CITATION.cff` file.
4. License: only if the repository already has a license file (`LICENSE`, `LICENSE.md`, `COPYING`). One line that names the license and links to the file. Never suggest or create a license.

## Repository structure (tree)

- In a `text` block, in ASCII: 4-space indentation, no box-drawing characters.
- 2 levels at most.
- Without generated files or files ignored by git.
- A short comment after `#` for each important folder or file.

```text
src/             # server code
    main.c       # entry point
docs/            # documentation and images
Makefile         # build
```

## ROADMAP.md

- Level 1 heading, then a single large table, columns: Phase, Step, Description, Status.
- The Status cell contains only the status in text: Done, In progress, To do. No emoji.
- Each step is a verifiable action, not a vague theme.
- The README keeps only a progress summary and a link.

## RESULTS.md

- No emoji. Clear and precise sentences.
- A part with no content is omitted.

1. Level 1 heading.
2. Contents: links to level 2 and 3 headings.
3. Summary: what is known today, in a few sentences.
4. Method: tools, hardware, data, protocol.
5. Results: `### R1`, `### R2`... For each: the statement in bold on the first line, the evidence (numbers, screenshots, files), the date, the command or file that produces it.
6. Trials: numbered table, columns #, Date, Trial, Result, Conclusion.
7. Discarded leads: what was tried without success, with the reason in one or two sentences.
8. Open questions: what remains to be understood, with the trial planned to answer it.

Update rules:

- The numbering of results and trials never changes.
- Rewrite, do not strike through. An invalidated result moves to Discarded leads with the reason.

## Going over 200 lines

Move long sections and replace them with a 2 or 3 sentence summary and a link, in this order:

1. How it works -> `docs/HOW-IT-WORKS.md`.
2. Detailed installation -> `docs/GUIDE.md`.
3. Configuration and options -> `docs/GUIDE.md`.
4. Detailed hardware -> `docs/GUIDE.md`.

Depending on the type:

- Collection: an index that is too long goes to `docs/INDEX.md`. The README keeps the number of entries, the themes and the 5 to 10 most recent or most important entries.
- Research: the detailed method goes to the Method part of RESULTS.md. The README keeps 3 or 4 sentences of it.

If the README is still over 200 lines: shorten the summaries and lists (Features, Technical highlights, Repository structure), then move the longest remaining section to `docs/GUIDE.md` or `docs/HOW-IT-WORKS.md` depending on its topic.

## Common mappings in a rework

Usual headings of old READMEs and where they usually go.

| Old heading | Destination |
|---|---|
| About, Introduction, Presentation | Description or Context |
| Demo, Screenshots | Overview |
| Getting started, Quick start | Quick start (Tool) or Build and run (Project) |
| Build, Compiling, Running | Build and run |
| Requirements, Dependencies | `### Prerequisites` |
| Architecture, Internals | How it works |
| Project structure, Layout | Repository structure |
| Roadmap, TODO | Progress and ROADMAP.md |
| Results, Benchmarks, Experiments | Key results and RESULTS.md |
| Future work, Next steps | Open questions (Research) or Progress |
| Team, Authors, Acknowledgements | Credits, kept as is |
| Known issues, Limitations, Caveats | Limitations |
