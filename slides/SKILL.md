---
name: slides
description: Build or extend Google Slides decks in a clean "slides épurées" visual style - white page, Arial, a short label title, one bold takeaway line, an optional grey subline, one native grey/blue chart or light table, equations rendered in LaTeX, a small grey footnote - airy, few words. Use this skill whenever the user asks for a presentation, slides, a deck, a diaporama, a "présentation" for a course, a progress update, a lab meeting, a class or seminar session or a research result, on any subject, and whenever they say "dans le même style", "comme mes slides", "sobre", "pas beaucoup de mots", or share a docs.google.com/presentation link to add slides to. Also use it to restyle or clean up existing slides into this look.
---

# Slides épurées

This skill is first of all a **visual style**: white, airy, Arial, grey and one blue, one message
and one visual per slide, few words. Apply the look below to any subject. When the user asks for
"le même style", it is this look, unless they share a deck to match.

The content conventions further down (the "Pourquoi" line, the démarche and hypotheses tables,
the sources slide) come from research progress talks. Use them when the talk is that kind of talk
or the user asks for them; for any other subject, keep the look and let the content follow the
user's material.

Before touching a Google file, follow the `google-workspace` skill and its `references/slides.md`
(read before edit, guard each write with the revision, verify after). This skill decides the look
and the content; that one decides how to talk to the API safely.

## Anatomy of a slide

Every content slide has the same five parts, at fixed places on the 10 × 5.625 in page. Keeping
them fixed is what makes the deck look calm: the eye finds the message at the same spot each time.

| Part | Where | Style | Holds |
|---|---|---|---|
| Label title | x 0.34, y 0.3 | Arial 28, regular, near-black | 1 to 5 words naming the topic: "Calibration", "Modèle : convergence" |
| Message | y 0.92 | Arial 17, **bold** | the takeaway as a sentence, ≤ 75 characters (one line) |
| Subline (optional) | y 1.2 | Arial 13, grey #4B5563 | one line of context, ≤ 105 characters; in research talks "Pourquoi : ..." |
| Body | y 1.6 to 4.85 | one visual | bars, table, line, cards or 3-5 bullets |
| Note | y 5.0 | Arial 10, grey #5F6975 | data source, experiment or run id, caveats, [n] references; 2 lines max |

The title is a label, not a sentence, and is not bold: that is this style's convention, and the
bold message under it carries the claim. Leave the subline out when it would only repeat the
message; the slide stays as clean without it.

## Writing the words

Few words is the point. Someone reading only the bold messages should follow the whole story.

- One message per slide. Two claims means two slides.
- Put the number in the message when there is one, with what it compares to: "Nouvelle méthode : −32 % ; l'ancienne version fait pire que la référence", not "Résultats de l'essai 3".
- In a research talk, the subline is "Pourquoi : ...": why this experiment or change was made, usually what the previous slide revealed. Every change must be justified on the slide itself in those talks.
- Bullets: 3 to 5, one line or two, parallel phrasing, no typed "-" (real bullets).
- Be honest on the slide. A hypothesis not tested says "Pas testé"; a weak comparison says so in the note ("indicatif : conditions différentes"). A deck that admits limits is more credible.
- In French decks, use French typography: a space before ":" and ";", « guillemets », decimal comma (27,8 s), "×" for ratios.
- No em dashes; a colon or a new sentence instead.
- Write in the user's language.
- Cite sources with [n] in the text or the note, and end the deck with a "Sources" slide. Only cite what you actually have (the user's papers, a deck they made, a paper you read); never invent a venue or a year. When a reference lacks its venue, give authors, title and year only.

## Colours carry meaning

Colour says which element matters, never decorates. Use the same roles on every slide:

| Role | Hex | Use |
|---|---|---|
| focus | #2A5FA8 | the subject of the talk (our method), its value labels, the equation |
| focus_light | #A9BEDD | our method in a weaker version (a run that failed, an older variant) |
| strong | #4B5563 | strong alternatives (best known options, state of the art) |
| base | #9AA3AD | baselines (default option, naive rule) |
| warn | #B45309 | "Non", a failure, a value that went wrong |
| good | #1B7F4B | "Confirmé" |
| tint | #EAF0F8 | at most one highlighted table cell, sparingly; never a card background |

Background stays white; text near-black #111111. No accent bars, no shadows, no stock icons.

**No filled or rounded "cards".** Never use tinted rounded backgrounds. Group content with a
bold black subheading and plain text or bullets on white. A diagram box
(a step, a component) is a plain RECTANGLE with no fill and a thin grey outline (#B8B8B8, 0.75 pt);
arrows can stay blue. Tables: thin grey borders, bold header, no coloured rows.

## Choosing the visual

- A comparison of a few values → horizontal **bars**, labels right-aligned on the left, value at the end of each bar, our method in focus colour. Two metrics side by side → **bars2**.
- Values looked up across a few dimensions (calibration, per-item breakdown, parameter sweep) → a light **table**: bold header and first column, numbers right-aligned, one tinted row at most, ≤ 7 rows.
- Something over time or over training → a **line** with dots, a few labelled points, dashed reference lines for the baselines with their label at the right end.
- Before/after, two options → two **columns**: a bold subheading and 2-3 bullets each, no background.
- A plan, next steps, reasons → **bullets**.
- A formula and its parameters → **formula** with a table under it. Equations are LaTeX images by default (next section).
- A summary of iterations → a table "Étape | Pourquoi ce changement | Ce qu'on voulait montrer | Résultat" (12 pt is fine there).
- A list of hypotheses → a table "Hypothèse | Statut | Preuve", the status coloured (good / warn / grey for "Pas testé").

Charts are built from native shapes (rectangles, lines, ellipses, text boxes) so the user can edit
them in Slides and they match the fonts exactly. Do not paste chart images: Slides only inserts
images from public URLs, and an image breaks the style.

## Equations: LaTeX by default

Every equation on a slide is a LaTeX image, not Unicode text: real fractions, indices, ∂, ẋ, ½.
It reads as more professional. Only the equation is an image; its legend
(what the symbols mean, the parameter values) stays a native grey text box under it. If `latex` is
missing, say so and keep the equations as text.

**Write the LaTeX** in one JSON file, one entry per equation block (math mode, no `$`):

- several lines: `\begin{aligned} ... &= ... \\ ... &= ... \end{aligned}`, aligned on `=`;
- words inside: `\text{total cost}`, `\operatorname{argmax}`, subscripts `x_{\text{max}}`;
- inline fractions `\tfrac{C}{2}` and `\big( \big)` keep a line low; write `\partial F/\partial x`
  rather than a stacked fraction when the column is tight;
- keep a block narrower than its column: break a long condition over two or three lines.

**Render**: `python3 <skill>/scripts/latex_eq.py eqs.json --out <dir>`. It writes one small
transparent PNG per equation in the focus blue, `manifest.json` with each size in EMU, and
`sheet.png` with every equation; read the sheet before going further. Sizes: scale 1.3 (default)
matches 16 pt body text, 1.5 for the one key equation of a slide, 1.2 for two blocks stacked in a
narrow column (`{"tex": ..., "scale": 1.5}`).

**Insert** (Slides only takes images from a public URL):

1. Create a Drive folder "<deck> equations (temp)" and upload each PNG into it with `create_file`
   (`base64Content` from `base64 -i f.png | tr -d '\n'`, `contentMimeType` image/png,
   `disableConversionToGoogleType` true). If Drive answers "not a valid base64 string", the copy
   was garbled: render that one again with `--colors 6` (shorter text) and retry.
2. The connector can only share with an e-mail address, so ask the user to set the folder to
   "Anyone with the link: Viewer" and wait for their ok.
3. One `update_presentation` batch: a `createImage` per equation with
   `https://drive.google.com/uc?export=view&id=<fileId>`, the size from the manifest (scale 1)
   and its position, then `deleteObject` of the text boxes it replaces (`<slide>_eq` from
   `build_slides.py`), then any move of the legend under it. The batch is atomic: if one image
   cannot be fetched, nothing changes.
4. Check the thumbnails, then tell the user they can make the folder private again or delete it: Slides
   keeps its own copy.

Keep `eqs.json` next to the deck's other files: to change an equation, edit it, render again and
replace the image.

## Deck structure (research and progress talks)

Only for that kind of talk; any other subject keeps the look and follows the user's outline.
For a progress talk, in this order; drop what does not apply:

1. Title slide (keep the user's own if the deck has one).
2. Where we were: the previous result, one slide.
3. What we varied (parameters, the formula) when the talk is about an experiment.
4. Démarche: the summary table of steps, each with its reason.
5. One slide per step, each with its "Pourquoi".
6. Hypotheses: what is confirmed, refuted, not tested.
7. Prochaines étapes: 3 to 5 bullets, what comes next and why.
8. Sources.

About 1.5 to 2 minutes per slide when presented.

## Workflow

1. **Read the deck** (if one exists): `read_presentation` with the mask from the google-workspace reference, then look at two or three slides. `read_slide_page_thumbnail` returns a URL; download it with `curl -sL -o s.png '<url>'` and open the PNG with the Read tool. Keep the user's slides as they are unless asked; match their fonts if they differ from Arial.
2. **Gather the numbers** from the user's data before writing anything. Every figure on a slide must trace to a source you can name in the note.
3. **Write a spec** (JSON) with one entry per slide: id, label, message, why, note, body. The format is in the docstring of `scripts/build_slides.py`.
4. **Build**: `python3 <skill>/scripts/build_slides.py spec.json --revision <revisionId> --out req.json --chunk 2`. It warns when a message, a "Pourquoi" or a bullet will wrap: shorten the words, never the font.
5. **Send** each `req-N.json` as the `requests` of `update_presentation`. Read the deck again before each call for a fresh `revisionId`; only the first file carries the guard, add it to the others yourself.
6. **Equations**: if the slides hold any, render and insert them as LaTeX images (section above); the build leaves the text version as a placeholder at the right spot.
7. **Look at every new slide**: download the thumbnails, stitch them into one image (Pillow: paste 800×450 tiles in a grid), read it, and fix overlaps or wrapped lines before reporting.
8. **Report** in a few lines: which slides were added where, what to check (any number you inferred, any source without a venue).

## Editing slides afterwards

Small edits are cheap; prefer them to rebuilding:

- Change words: `replaceAllText` with `pageObjectIds` set to the slide, no revision guard needed. Keep the new text as short as the old one.
- Move or resize: the API stores shapes with a base size of 3 000 000 EMU and a scale. An `updatePageElementTransform` in ABSOLUTE mode must give `scaleX = wanted width in EMU / 3 000 000` (same for height), not 1, or the shape shrinks or a line turns diagonal. Read the element's `size` and `transform` first.
- Table: change column widths with `updateTableColumnProperties`; a header that wraps needs a wider column, not a smaller font. `insertTableRows` copies no bold: restyle the header and first column after it. Each extra row is about 0.35 in; past 7 rows the table reaches the footnote, so shorten cells first.
- A message that wraps lands on the "Pourquoi" line: shorten it to ≤ 75 characters.

## Without the Google Slides connector

If only Drive is available, say so and ask the user to enable Google Slides in the chat's
connector settings (same file, same link). If they prefer a file, build a .pptx with the `pptx`
skill using the same anatomy, sizes and colours.
