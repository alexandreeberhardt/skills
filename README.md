# Skills

This repository stores the custom agent skills I use with Codex or Claude Code.
Each skill is a folder centered on a `SKILL.md` file.

## Repository layout

```text
<skill-name>/                  # standalone skill
    SKILL.md                   # instructions read by the agent
    scripts/                   # helper scripts, for some skills
designSkills/<skill-name>/     # UI design skills
startupSkills/<skill-name>/    # startup and career skills
```

## Index

| Entry | Theme | Description |
|---|---|---|
| [brutalist-skill](designSkills/brutalist-skill/) | Design | UI rules for a Swiss-print, terminal-like look: rigid grids, strong type contrast, utilitarian colors |
| [good-design](designSkills/good-design/) | Design | Reviews or designs anything with 14 concrete tests from Paul Graham's "Taste for Makers". Written in French |
| [minimalist-skill](designSkills/minimalist-skill/) | Design | UI rules for an editorial look: warm monochrome palette, flat layouts, no gradients or heavy shadows |
| [redesign-skill](designSkills/redesign-skill/) | Design | Audits an existing site or app and improves its UI without changing the stack |
| [soft-skill](designSkills/soft-skill/) | Design | UI rules for a polished agency look: fonts, spacing, shadows, cards and animations |
| [stitch-skill](designSkills/stitch-skill/) | Design | Writes a `DESIGN.md` design system for Google Stitch |
| [taste-skill](designSkills/taste-skill/) | Design | Frontend rules to avoid the generic look of AI-generated interfaces |
| [output-skill](designSkills/output-skill/) | Code | Stops the agent from truncating code or leaving placeholders |
| [clean-code](clean-code/) | Code | Removes decorative separators, alignment-only spacing and non-ASCII symbols without changing logic |
| [company-fit-strategist](startupSkills/company-fit-strategist/) | Startup | From a detailed profile, suggests the kind of company, role or independent path that fits best |
| [founder-thesis-generator](startupSkills/founder-thesis-generator/) | Startup | From a founder profile, suggests a startup to found: thesis, first customer, go-to-market, validation plan |
| [unseen-next-move-oracle](startupSkills/unseen-next-move-oracle/) | Startup | From a detailed profile, points out a next move and blind spots the person has missed |
| [plan-strategique](plan-strategique/) | Planning | Builds or updates a strategic plan in 7 steps (Arthur Perticoz's method). Written in French |
| [clean-readme](clean-readme/) | Writing | Creates, reworks or updates a README and its companion files, with a script that checks the result |
| [humanizer](humanizer/) | Writing | Rewrites text to remove common signs of AI writing, based on Wikipedia's guide |
| [slides](slides/) | Media | Builds or extends Google Slides decks with native charts and LaTeX equations |
| [spotify](spotify/) | Media | Queues tracks on the active Spotify device |
| [variantes](variantes/) | Media | Generates 10 profile-photo variants: crop, retouch, background removal, studio backgrounds, lighting |

## Tools

- Codex or Claude Code
- Python 3, for the scripts of `clean-readme`, `slides` and `spotify`
- Your own Spotify credentials, for `spotify`: secrets and tokens are not committed
- macOS with `swiftc` and ImageMagick, for `variantes`: its Vision helpers are compiled on first run
