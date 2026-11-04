# Useful Skills

This repository stores the custom Agentic AI skills that I use.
They can work with Codex or Claude Code

## Included skills

- `brutalist-skill` — industrial/brutalist UI direction for dense, tactical, print-inspired interfaces.
- `clean-code` — removes decorative separators, alignment-only spacing, and non-ASCII symbols from code without changing logic.
- `company-fit-strategist` — infers the best company type, role, or independent path from a detailed profile.
- `founder-thesis-generator` — derives a startup thesis, wedge, customer, GTM, and validation plan from a founder profile.
- `humanizer` — rewrites text to remove common AI-writing patterns and sound more natural.
- `minimalist-skill` — premium editorial minimalism with warm monochrome palettes, flat layouts, and strong typography.
- `output-skill` — enforces complete, unabridged outputs and bans placeholder truncation patterns.
- `redesign-skill` — audits and upgrades existing app/site UI without breaking the current stack.
- `slides` — builds or extends Google Slides decks in a clean, airy style with native charts and LaTeX equations.
- `soft-skill` — high-end agency-style visual design guidance for polished UI, spacing, motion, and component treatment.
- `spotify` — queues tracks on the active Spotify device using cached local OAuth credentials.
- `stitch-skill` — generates strict `DESIGN.md` design-system instructions for Google Stitch.
- `taste-skill` — high-agency frontend design rules to override generic LLM UI defaults.
- `unseen-next-move-oracle` — identifies a high-leverage next move and hidden blind spots from a detailed profile.

## Layout

Each skill lives in `skills/<skill-name>/` and is centered around a `SKILL.md` file.
Some skills also include supporting folders such as `agents/` or `scripts/`.

## Notes

- Spotify local secrets/tokens are intentionally not committed, you need spotify credentials to interact with your account.
- User-specific Spotify listening history paths and taste exclusions should stay out of tracked skill files.
- Python cache files are intentionally omitted.
