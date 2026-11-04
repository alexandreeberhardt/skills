#!/usr/bin/env python3
"""Turns a short JSON spec into Google Slides batchUpdate requests, in the "slides épurées" style:
white page, a label title, one bold message, a grey "Pourquoi" line, one native visual (bars,
table, line, bullets, two cards), a small footnote. Every shape is native, so the deck stays editable.

    python3 build_slides.py spec.json --revision <revisionId> [--out requests.json] [--chunk 2]

With --chunk N it writes one file per N slides (requests-1.json, ...): a batch of more than about
30 KB is slow to send. Each file holds {"requests": [...], "writeControl": {...}}; send the
"requests" list to update_presentation. The revision guards only the first call: read the deck
again for the revisionId of each next one.

The spec, every length in inches on the default 10 x 5.625 page:

{"start_index": 2,                      # where the first new slide goes (0-based)
 "slides": [
   {"id": "s_calib",                    # 5+ chars, letters, digits, _ or -; prefixes every element
    "label": "Calibration",             # the title: a short label, 28 pt, not bold
    "message": "Le système B est 8x plus lent", # the takeaway, bold 17 pt, one line (about 75 characters)
    "why": "Pourquoi : ...",            # optional grey line, 13 pt, one line (about 105 characters)
    "note": "Source : ...",             # optional footnote, 10 pt, two lines at most
    "body": {...}}]}                     # one of the bodies below

Bodies ("role" picks the colour: focus, focus_light, strong, base, warn, good):
  {"type": "bars", "caption": "Temps moyen (s)", "unit": " s", "digits": 1, "max": 60,
   "rows": [["Méthode A", 27.8, "strong"], ["Notre méthode", 53.7, "focus"]]}
  {"type": "bars2", "left": <bars>, "right": <bars>}          two bar charts side by side
  {"type": "table", "rows": [["Tête", "Col"], ["a", "1"]], "widths": [3, 2], "size": 14,
   "numbers": true, "highlight_row": 2, "colours": {"1,1": "good"}}
  {"type": "line", "x": [10, 20, 30], "y": [108, 26, 30], "y_max": 120, "y_ticks": [0, 40, 80, 120],
   "y_unit": " s", "x_title": "Après N essais", "refs": [[28, "référence 28 s", "strong"]],
   "labels": {"0": "108 s", "1": "26 s"}, "role": "focus"}
  {"type": "bullets", "items": ["...", "..."], "size": 18}
  {"type": "cards", "left": {"title": "Avant", "items": [...]}, "right": {"title": "Après", "items": [...]}}
  {"type": "formula", "text": "y = a x + b", "legend": "a : ...", "then": <table or bars>}
    The text box <id>_eq is a placeholder: the equation is then rendered with latex_eq.py and
    put in its place as an image (see "Equations: LaTeX by default" in SKILL.md).
"""
import argparse
import json
import sys

EMU = 914400
PAGE_W = 10.0
X0, W = 0.34, 9.3  # the content column: half-inch margins, near enough
TITLE_Y, MSG_Y, WHY_Y, BODY_Y, NOTE_Y = 0.3, 0.92, 1.2, 1.6, 5.0
FONT = "Arial"
INK, MUTED, WHY_INK = "#111111", "#5F6975", "#4B5563"
ROLES = {"focus": "#2A5FA8", "focus_light": "#A9BEDD", "strong": "#4B5563", "base": "#9AA3AD",
         "warn": "#B45309", "good": "#1B7F4B", "muted": MUTED, "ink": INK}
CARD_FILLS = ("#F3F4F6", "#EAF0F8")
TINT = "#EAF0F8"
GRID = "#E5E7EB"


class Deck:
    def __init__(self):
        self.reqs = []

    # -- primitives ---------------------------------------------------------------------------

    @staticmethod
    def rgb(colour):
        colour = ROLES.get(colour, colour).lstrip("#")
        return {k: round(int(colour[i:i + 2], 16) / 255, 3) for k, i in (("red", 0), ("green", 2), ("blue", 4))}

    @staticmethod
    def props(page, x, y, w, h, sy=1):
        return {"pageObjectId": page,
                "size": {"width": {"magnitude": max(int(w * EMU), 1), "unit": "EMU"},
                         "height": {"magnitude": max(int(h * EMU), 1), "unit": "EMU"}},
                "transform": {"scaleX": 1, "scaleY": sy, "translateX": int(x * EMU), "translateY": int(y * EMU),
                              "unit": "EMU"}}

    def text(self, oid, page, x, y, w, h, s, size=16, bold=False, colour=INK, align="START", middle=False):
        self.reqs.append({"createShape": {"objectId": oid, "shapeType": "TEXT_BOX",
                                          "elementProperties": self.props(page, x, y, w, h)}})
        self.reqs.append({"insertText": {"objectId": oid, "text": s}})
        self.reqs.append({"updateTextStyle": {"objectId": oid, "textRange": {"type": "ALL"},
                          "fields": "fontFamily,fontSize,bold,foregroundColor", "style": {
                              "fontFamily": FONT, "fontSize": {"magnitude": size, "unit": "PT"}, "bold": bold,
                              "foregroundColor": {"opaqueColor": {"rgbColor": self.rgb(colour)}}}}})
        if align != "START":
            self.reqs.append({"updateParagraphStyle": {"objectId": oid, "textRange": {"type": "ALL"},
                                                       "style": {"alignment": align}, "fields": "alignment"}})
        if middle:
            self.reqs.append({"updateShapeProperties": {"objectId": oid, "fields": "contentAlignment",
                                                        "shapeProperties": {"contentAlignment": "MIDDLE"}}})

    def bullets(self, oid, space=10):
        self.reqs.append({"createParagraphBullets": {"objectId": oid, "textRange": {"type": "ALL"},
                                                     "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"}})
        self.reqs.append({"updateParagraphStyle": {"objectId": oid, "textRange": {"type": "ALL"}, "fields": "spaceBelow",
                                                   "style": {"spaceBelow": {"magnitude": space, "unit": "PT"}}}})

    def shape(self, oid, page, kind, x, y, w, h, fill):
        self.reqs.append({"createShape": {"objectId": oid, "shapeType": kind,
                                          "elementProperties": self.props(page, x, y, w, h)}})
        self.reqs.append({"updateShapeProperties": {"objectId": oid, "shapeProperties": {
            "shapeBackgroundFill": {"solidFill": {"color": {"rgbColor": self.rgb(fill)}}},
            "outline": {"propertyState": "NOT_RENDERED"}},
            "fields": "shapeBackgroundFill.solidFill.color,outline.propertyState"}})

    def line(self, oid, page, x1, y1, x2, y2, colour, weight=1.5, dash="SOLID"):
        """A line runs from its box's top-left to its bottom-right: a rising one is flipped (scaleY -1)."""
        up = y2 < y1
        top, h = min(y1, y2), abs(y2 - y1)
        self.reqs.append({"createLine": {"objectId": oid, "category": "STRAIGHT", "elementProperties":
                                         self.props(page, x1, top + h if up else top, x2 - x1, h, sy=-1 if up else 1)}})
        self.reqs.append({"updateLineProperties": {"objectId": oid, "fields": "lineFill.solidFill.color,weight,dashStyle",
                          "lineProperties": {"lineFill": {"solidFill": {"color": {"rgbColor": self.rgb(colour)}}},
                                             "weight": {"magnitude": weight, "unit": "PT"}, "dashStyle": dash}}})

    # -- slide frame --------------------------------------------------------------------------

    def frame(self, slide, index):
        page = slide["id"]
        self.reqs.append({"createSlide": {"objectId": page, "insertionIndex": index,
                                          "slideLayoutReference": {"predefinedLayout": "BLANK"}}})
        self.text(f"{page}_title", page, X0, TITLE_Y, W, 0.6, slide["label"], size=28)
        if slide.get("message"):
            self.text(f"{page}_msg", page, X0, MSG_Y, W, 0.5, slide["message"], size=17, bold=True)
        if slide.get("why"):
            self.text(f"{page}_why", page, X0, WHY_Y, W, 0.36, slide["why"], size=13, colour=WHY_INK)
        if slide.get("note"):
            self.text(f"{page}_note", page, X0, NOTE_Y, W, 0.5, slide["note"], size=10, colour=MUTED)

    # -- bodies -------------------------------------------------------------------------------

    def bars(self, page, p, spec, x=X0, y=BODY_Y, w=W, bottom=4.85):
        rows = spec["rows"]
        if spec.get("caption"):
            self.text(f"{page}_{p}cap", page, x, y, w, 0.4, spec["caption"], size=15, colour=MUTED)
            y += 0.45
        row_h = spec.get("row_h") or min(0.6, (bottom - y) / len(rows))
        label_w = spec.get("label_w") or min(2.6, max(1.4, 0.11 * max(len(r[0]) for r in rows) + 0.3))
        value_w = spec.get("value_w", 1.0)
        bar_x, bar_w = x + label_w + 0.1, w - label_w - 0.1 - value_w
        vmax = spec.get("max") or max(r[1] for r in rows) * 1.05
        unit, digits = spec.get("unit", ""), spec.get("digits", 1)
        for i, row in enumerate(rows):
            label, value, role = row[0], row[1], (row[2] if len(row) > 2 else "base")
            strong = role in ("focus", "warn", "good")
            ry = y + i * row_h
            self.text(f"{page}_{p}l{i}", page, x, ry, label_w, row_h, label, size=14, bold=strong, align="END",
                      middle=True)
            bw = max(bar_w * value / vmax, 0.04)
            self.shape(f"{page}_{p}b{i}", page, "RECTANGLE", bar_x, ry + row_h * 0.2, bw, row_h * 0.6, role)
            shown = f"{value:.{digits}f}".replace(".", spec.get("decimal", ",")) + unit
            self.text(f"{page}_{p}v{i}", page, bar_x + bw + 0.05, ry, value_w, row_h, shown, size=14, bold=True,
                      colour=role if strong else WHY_INK, middle=True)

    def table(self, page, spec, x=X0, y=BODY_Y):
        rows = spec["rows"]
        ncols = len(rows[0])
        widths = spec.get("widths") or [W / ncols] * ncols
        size = spec.get("size", 14)
        oid = f"{page}_table"
        self.reqs.append({"createTable": {"objectId": oid, "rows": len(rows), "columns": ncols,
                                          "elementProperties": self.props(page, x, y, sum(widths), 0.4 * len(rows))}})
        for c, wdt in enumerate(widths):
            self.reqs.append({"updateTableColumnProperties": {"objectId": oid, "columnIndices": [c], "fields": "columnWidth",
                              "tableColumnProperties": {"columnWidth": {"magnitude": int(wdt * EMU), "unit": "EMU"}}}})
        colours = {tuple(int(v) for v in k.split(",")): c for k, c in (spec.get("colours") or {}).items()}
        highlight = spec.get("highlight_row")
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                cell = {"rowIndex": r, "columnIndex": c}
                self.reqs.append({"insertText": {"objectId": oid, "cellLocation": cell, "text": str(value)}})
                colour = colours.get((r, c), "focus" if r == highlight else INK)
                self.reqs.append({"updateTextStyle": {"objectId": oid, "cellLocation": cell, "textRange": {"type": "ALL"},
                                  "fields": "fontFamily,fontSize,bold,foregroundColor", "style": {
                                      "fontFamily": FONT, "fontSize": {"magnitude": size, "unit": "PT"},
                                      "bold": r == 0 or c == 0,
                                      "foregroundColor": {"opaqueColor": {"rgbColor": self.rgb(colour)}}}}})
                if spec.get("numbers") and c > 0:
                    self.reqs.append({"updateParagraphStyle": {"objectId": oid, "cellLocation": cell, "fields": "alignment",
                                      "textRange": {"type": "ALL"}, "style": {"alignment": "END"}}})
        self.reqs.append({"updateTableCellProperties": {"objectId": oid, "fields": "contentAlignment", "tableRange": {
            "location": {"rowIndex": 0, "columnIndex": 0}, "rowSpan": len(rows), "columnSpan": ncols},
            "tableCellProperties": {"contentAlignment": "MIDDLE"}}})
        if highlight is not None:
            self.reqs.append({"updateTableCellProperties": {"objectId": oid, "tableRange": {
                "location": {"rowIndex": highlight, "columnIndex": 0}, "rowSpan": 1, "columnSpan": ncols},
                "tableCellProperties": {"tableCellBackgroundFill": {"solidFill": {"color": {"rgbColor": self.rgb(TINT)}}}},
                "fields": "tableCellBackgroundFill.solidFill.color"}})

    def line_chart(self, page, spec):
        xs, ys = spec["x"], spec["y"]
        x0, x1, top, bottom = 1.1, 8.0, BODY_Y + 0.15, 4.35
        ymax = spec.get("y_max") or max(ys) * 1.1
        unit, role = spec.get("y_unit", ""), spec.get("role", "focus")

        def X(v):
            return x0 + (v - xs[0]) / (xs[-1] - xs[0]) * (x1 - x0)

        def Y(v):
            return bottom - v / ymax * (bottom - top)

        for v in spec.get("y_ticks", []):
            self.line(f"{page}_g{v}", page, x0 - 0.1, Y(v), x1 + 0.1, Y(v) + 0.0001, GRID, 0.75)
            self.text(f"{page}_gl{v}", page, 0.3, Y(v) - 0.15, 0.65, 0.3, f"{v}{unit}", size=12, colour=MUTED,
                      align="END", middle=True)
        for i, v in enumerate(xs):
            self.text(f"{page}_x{i}", page, X(v) - 0.3, bottom + 0.05, 0.6, 0.3, str(v), size=12, colour=MUTED,
                      align="CENTER")
        if spec.get("x_title"):
            self.text(f"{page}_xt", page, x0, bottom + 0.32, x1 - x0, 0.3, spec["x_title"], size=12, colour=MUTED,
                      align="CENTER")
        for k, (value, label, ref_role) in enumerate(spec.get("refs", [])):
            self.line(f"{page}_r{k}", page, x0 - 0.1, Y(value), x1 + 0.1, Y(value) + 0.0001, ref_role, 1.25, "DASH")
            self.text(f"{page}_rt{k}", page, x1 + 0.15, Y(value) - 0.17, 1.8, 0.34, label, size=12, colour=ref_role,
                      middle=True)
        for i in range(len(xs) - 1):
            self.line(f"{page}_s{i}", page, X(xs[i]), Y(ys[i]), X(xs[i + 1]), Y(ys[i + 1]), role, 2.25)
        for i, (vx, vy) in enumerate(zip(xs, ys)):
            self.shape(f"{page}_p{i}", page, "ELLIPSE", X(vx) - 0.07, Y(vy) - 0.07, 0.14, 0.14, role)
        for i, label in (spec.get("labels") or {}).items():
            i = int(i)
            above = i == 0 or ys[i] >= ys[i - 1]  # a label goes where the line does not
            self.text(f"{page}_v{i}", page, X(xs[i]) - 0.5, Y(ys[i]) + (-0.42 if above else 0.1), 1.0, 0.3, label,
                      size=13, bold=True, colour=role, align="CENTER")

    def bullet_list(self, page, spec):
        oid = f"{page}_body"
        self.text(oid, page, X0, BODY_Y + 0.1, W, 3.2, "\n".join(spec["items"]), size=spec.get("size", 18))
        self.bullets(oid)

    def cards(self, page, spec):
        for k, (side, x, w) in enumerate((("left", X0, 4.5), ("right", 5.06, 4.6))):
            # Plain columns: no filled or rounded background (the user's preference).
            card = spec[side]
            self.text(f"{page}_{side}h", page, x, BODY_Y + 0.15, w - 0.14, 0.45, card["title"], size=18, bold=True,
                      colour=INK)
            oid = f"{page}_{side}b"
            self.text(oid, page, x, BODY_Y + 0.7, w - 0.14, 2.2, "\n".join(card["items"]), size=15)
            self.bullets(oid)

    def body(self, slide):
        page, spec = slide["id"], slide["body"]
        kind = spec["type"]
        if kind == "bars":
            self.bars(page, "c", spec)
        elif kind == "bars2":
            self.bars(page, "l", spec["left"], X0, BODY_Y, 4.6)
            self.bars(page, "r", spec["right"], 5.06, BODY_Y, 4.6)
        elif kind == "table":
            self.table(page, spec)
        elif kind == "line":
            self.line_chart(page, spec)
        elif kind == "bullets":
            self.bullet_list(page, spec)
        elif kind == "cards":
            self.cards(page, spec)
        elif kind == "formula":
            self.text(f"{page}_eq", page, X0, BODY_Y, W, 0.42, spec["text"], size=18, bold=True, colour="focus")
            if spec.get("legend"):
                self.text(f"{page}_leg", page, X0, BODY_Y + 0.4, W, 0.36, spec["legend"], size=12, colour=WHY_INK)
            then = spec.get("then")
            if then and then["type"] == "table":
                self.table(page, then, y=BODY_Y + 0.9)
            elif then and then["type"] == "bars":
                self.bars(page, "c", then, y=BODY_Y + 0.9)
        else:
            sys.exit(f"{page}: unknown body type {kind!r}")


def check(spec):
    """The style's limits, before anything is sent: a line that wraps lands on the next element."""
    warnings = []
    for s in spec["slides"]:
        page = s["id"]
        if not (5 <= len(page) <= 40) or not all(ch.isalnum() or ch in "_-" for ch in page):
            sys.exit(f"{page!r}: an id is 5 to 40 letters, digits, _ or -")
        for key, limit in (("label", 45), ("message", 75), ("why", 105), ("note", 240)):
            if len(s.get(key) or "") > limit:
                warnings.append(f"{page}: {key} is {len(s[key])} characters, more than about {limit}: it will wrap")
        body = s.get("body", {})
        if body.get("type") == "bullets":
            if len(body["items"]) > 5:
                warnings.append(f"{page}: {len(body['items'])} bullets; keep three to five")
            for item in body["items"]:
                if len(item) > 110:
                    warnings.append(f"{page}: a bullet of {len(item)} characters runs over two lines")
        if body.get("type") == "table" and len(body["rows"]) > 8:
            warnings.append(f"{page}: {len(body['rows'])} table rows; past 7 the table reaches the footnote")
    return warnings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("spec")
    parser.add_argument("--revision", required=True)
    parser.add_argument("--out", default="requests.json")
    parser.add_argument("--chunk", type=int, default=0, help="slides per output file (0: one file)")
    args = parser.parse_args()
    spec = json.load(open(args.spec))
    for warning in check(spec):
        print("WARNING:", warning, file=sys.stderr)
    slides = spec["slides"]
    groups = [slides[i:i + args.chunk] for i in range(0, len(slides), args.chunk)] if args.chunk else [slides]
    index = spec.get("start_index", 1)
    for n, group in enumerate(groups, 1):
        deck = Deck()
        for slide in group:
            deck.frame(slide, index)
            deck.body(slide)
            index += 1
        out = args.out if len(groups) == 1 else args.out.replace(".json", f"-{n}.json")
        payload = {"requests": deck.reqs}
        if n == 1:
            payload["writeControl"] = {"requiredRevisionId": args.revision}
        with open(out, "w") as handle:
            json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"))
        print(f"{out}: {len(group)} slides, {len(deck.reqs)} requests, {len(json.dumps(payload)) // 1024} KB")


if __name__ == "__main__":
    main()
