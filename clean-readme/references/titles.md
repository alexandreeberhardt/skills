# Reference headings, statuses and labels

Exact texts to use. Level 2 headings of the README are taken only from these tables, except for at most 2 free sections. Level 3 headings are free, except those listed here.

## Status block

A blockquote, right after the description.

```markdown
> **Status**: Paused. Sensor communication works, but measurements are not recorded yet. Work resumes when a new board arrives.
```

With a version:

```markdown
> **Status**: Done (version 1.2.0 of 2026-01-10).
```

In French:

```markdown
> **État** : En pause. La communication avec le capteur fonctionne, mais les mesures ne sont pas encore enregistrées. Reprise à la réception d'une nouvelle carte.
> **État** : Terminé (version 1.2.0 du 2026-01-10).
```

- No "last updated" date: the git history already gives it, and it goes stale.
- The version and its date come from git tags or releases, never from a guess.

## Statuses

| Status | In French | Meaning | Required detail after the status |
|---|---|---|---|
| In progress | En cours | Active development | None |
| Experimental | Expérimental | Partly works, may change or break | What works and what does not, in one sentence |
| Paused | En pause | Temporarily stopped | The reason and what will allow work to resume |
| Stopped | Arrêté | Abandoned or not completed | The reason, and where the project stopped |
| Done | Terminé | Finished and working | None |

In a README progress table and in ROADMAP.md, the Status column uses text: Done, In progress, To do (Fait, En cours, À faire).

## README: common headings

| Level | English | French | Types |
|---|---|---|---|
| 1 | (project name) | (nom lisible du projet) | All |
| 2 | Disclaimer | Avertissement | All, optional |
| 2 | Contents | Sommaire | All, from 5 other level 2 sections |
| 2 | Context | Contexte | All, optional |
| 2 | Differences from upstream | Différences avec le projet d'origine | Fork |
| 2 | Repository structure | Structure du dépôt | Project, Tool, Research |
| 2 | Hardware | Matériel | Project, Research |
| 2 | Features | Fonctionnalités | Project, Tool |
| 2 | Progress | Avancement | Project, Research |
| 2 | Limitations | Limites | All |
| 2 | Credits | Crédits | All, only if the user writes it |
| 2 | References | Références | All |
| 3 | Citation | Citer ce travail | Under References, academic research |
| 2 | License | Licence | All, only if the repository has a license file |

## README: type-specific headings

| Level | English | French | Type |
|---|---|---|---|
| 2 | Overview | Aperçu | Project |
| 2 | Technical highlights | Points techniques | Project, optional |
| 2 | Build and run | Compilation et lancement | Project |
| 3 | Prerequisites | Prérequis | Under Build and run, Installation or Reproduce |
| 2 | Usage | Utilisation | Project |
| 2 | Deployment | Déploiement | Project |
| 2 | How it works | Fonctionnement interne | Project |
| 2 | Installation | Installation | Tool |
| 2 | Quick start | Usage minimal | Tool |
| 2 | Configuration and options | Configuration et options | Tool |
| 2 | Contributing | Contribuer | Tool |
| 2 | Research question | Question de recherche | Research |
| 2 | Key results | Résultats principaux | Research |
| 2 | Method | Méthode | Research |
| 2 | Reproduce | Reproduire | Research |
| 2 | Open questions | Questions ouvertes | Research |
| 2 | Repository layout | Organisation du dépôt | Collection |
| 2 | Index | Index | Collection |
| 2 | Template | Modèle | Collection |
| 2 | Tools | Outils utilisés | Collection |

## Companion files

| File (en / fr) | Level 1 (en / fr) | Level 2 (en / fr) |
|---|---|---|
| `ROADMAP.md` / `ROADMAP.md` | Roadmap / Feuille de route | None: a single table |
| `RESULTS.md` / `RESULTATS.md` | Research results / Résultats de recherche | Contents / Sommaire, Summary / Résumé, Method / Méthode, Results / Résultats, Trials / Essais, Discarded leads / Pistes écartées, Open questions / Questions ouvertes |
| `docs/GUIDE.md` / `docs/GUIDE.md` | Guide / Guide | Headings taken from the README: Installation, Configuration and options, Hardware |
| `docs/HOW-IT-WORKS.md` / `docs/FONCTIONNEMENT.md` | How it works / Fonctionnement interne | Free |
| `docs/INDEX.md` / `docs/INDEX.md` | Index / Index | Free, for example one level 2 per theme |

- The level 1 heading of RESULTS.md differs from the level 2 "Results", otherwise GitHub produces the same anchor twice.
- Each result in RESULTS.md has a level 3 heading reduced to its number (`### R1`), and its statement in bold on the next line. The `#r1` anchor stays stable if the statement is reworded.

## Anchors

The skill and the script compute anchors like GitHub:

1. remove formatting (links, code, HTML);
2. lowercase, keep accents;
3. remove punctuation except `-` and `_`;
4. replace spaces with hyphens;
5. for a duplicate heading, add `-1`, `-2`...

Example: `## Repository structure` gives `#repository-structure`, and `## Structure du dépôt` gives `#structure-du-dépôt`.
