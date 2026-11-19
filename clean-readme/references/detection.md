# Detecting the type and status

The skill chooses the type and status from the clues, and states them in the report. It only asks if the case is ambiguous.

## The 4 types

| Type | Question the README answers | Examples |
|---|---|---|
| Project | What was built and how does it work? | Game, circuit board, FPGA processor, network server, application, website |
| Tool | How do I install it and use it? | Library, command-line tool, document template, site theme or template |
| Research | What question, where does the project stand, what was found? | Proof of concept, reverse engineering, experimental study, machine learning project |
| Collection | What does the repository contain and how do I find my way? | Lab or CTF reports, course notes, exercise collection |

## Order of sources

Stop as soon as a source is enough:

1. what the user says ("it's a POC", "it's my library");
2. the existing README: if it already follows the rules, its level 2 headings give the type (Quick start: Tool, Key results: Research, Index: Collection, Build and run: Project) and its status block gives the language (`**Status**` or `**État**`);
3. the existing README and docs otherwise: vocabulary, sections present;
4. the repository structure, configuration files and git history.

## Tie-breaking question

When clues are not enough: what is the main content the reader comes for?

| The reader comes for... | Type |
|---|---|
| What was built, to see or run | Project |
| A way to use it in their own work | Tool |
| The answer to a question whose answer is not known yet | Research |
| A collection of independent items | Collection |

An unfinished project is not necessarily research. Known goal and remaining work: Project in progress. Not known yet whether it is feasible, or how: Research.

## Clues per type

- A strong clue is almost enough on its own. A weak clue only counts when added to others.
- If two types have strong clues, ask.
- Clues that need a hosting API (GitHub, GitLab) are only used if the information is available. The skill must work offline.
- If the folder is not a git repository, do without clues from history and tags.

### Tool

- Strong:
  - publishable package: `pyproject.toml` or `setup.py` with a package name, `Cargo.toml` with `[lib]`, `package.json` with `bin`, `main` or `exports` and without `"private": true`, `go.mod` of a module, `*.gemspec`, library `pom.xml` or `build.gradle`;
  - automated publishing (workflow to PyPI, npm, crates.io, Docker Hub);
  - reusable template: repository marked as template, `cookiecutter.json`, LaTeX class or style (`.cls`, `.sty`), site theme (`theme.toml` for Hugo, Jekyll theme `*.gemspec`);
  - single-header library (`.h`) meant to be included elsewhere.
- Weak: version tags, releases, `CHANGELOG.md`, `CONTRIBUTING.md`, `examples/` folder, documentation site (`mkdocs.yml`, `docs/conf.py`), tests and continuous integration, license.

### Project

- Strong:
  - hardware: KiCad (`*.kicad_pro`, `*.kicad_pcb`), Eagle (`*.sch`, `*.brd`), Gerber files, 3D models (`*.stl`, `*.step`, FreeCAD);
  - FPGA: Vivado (`*.xpr`) or Quartus (`*.qpf`) project, `*.vhd` or `*.v` sources with constraints (`*.xdc`, `*.qsf`);
  - embedded: `*.ino`, `platformio.ini`, Makefile targeting `avr-gcc` or `arm-none-eabi-gcc`;
  - website: `index.html` at the root, Hugo, Jekyll (`_config.yml`), Astro, Vite, Next or Svelte configuration, `CNAME` file, GitHub Pages deployment workflow;
  - application: single entry point (`main.c`, `main.py`, `src/main.rs`) without a publishable package, assets (`assets/`, `sprites/`, `sounds/`), mobile project (`AndroidManifest.xml`, `*.xcodeproj`);
  - service: `Dockerfile` or `docker-compose.yml` that runs the application.
- Weak: screenshots or video in the repository, Makefile with a `run` target.

### Research

- Strong:
  - experiment outputs: `results/`, `runs/`, `out/`, `logs/`, `experiments/`, `outputs/`, `mlruns/`, `wandb/`;
  - machine learning: `*.ipynb` notebooks, model weights (`*.pt`, `*.ckpt`, `*.h5`, `*.onnx`, `*.safetensors`), `data/` with a dataset, experiment or parameter sweep configurations;
  - reverse engineering or networking: captures (`*.pcap`, `*.pcapng`), memory or firmware dumps, Ghidra, IDA or radare2 projects, `patches/` folder on a third-party project;
  - vocabulary in the name, README or docs: poc, proof of concept, experimental, hypothesis, trial, benchmark, study, investigation, reverse engineering.
- Weak: `*.bib` files, LaTeX `paper/` folder, measurement or plotting scripts.

### Collection

- Strong:
  - several sibling folders with the same internal structure, often numbered (`session_1/`, `lab1/`, `week-01/`, `day01/`, `chapter-3/`);
  - a blank template to copy (`TEMPLATE.md`);
  - mostly independent Markdown files, PDFs or solutions, with no single entry point;
  - a README that is mostly a long list of links ("awesome" list).
- Weak: vocabulary such as writeup, solutions, notes, exercises, course, CTF, Advent of Code, LeetCode; one README per subfolder.

## Ambiguous cases

| Situation | Chosen type |
|---|---|
| Website (portfolio, landing page, blog, web application) | Project. The README says what the site is, where to see it online, how to run it locally and how to deploy it. The published content is not copied. |
| Site theme or template made to be reused | Tool |
| Research code published for others to use | Tool if the README is mostly about using it, Research if its main content is what was found. |
| Proof of concept that became working and stable | Project or Tool. Suggest the type change. |
| Repository holding several independent projects | Collection, with an index of the projects |
| Personal configuration (dotfiles) | Tool if it provides an install script, Collection otherwise |
| Documentation, course or guide | Collection |
| Modified fork of another project | Same type as the upstream project, with the "Differences from upstream" section right after Context |
| Empty or almost empty repository | Ask directly |

## Clues for the status

- what the existing README says takes precedence over the following clues;
- archived repository, if the information is available: Stopped or Done;
- no commit for more than 6 months: Paused or Stopped. Ask for the reason only if no source gives it;
- recent, stable version tags: Done or In progress, with the latest version;
- many "WIP", "in progress", "TODO" words in the README: In progress or Experimental.

Useful commands:

```bash
git log -1 --format=%cs
git tag --sort=-creatordate | head -5
git log --oneline | wc -l
```

## Form in the report

```text
Type: Research (runs/ folder with 12 experiment outputs, .pcap captures, the README talks about a proof of concept).
Status: Paused (last commit 7 months ago, reason given in the README).
```
