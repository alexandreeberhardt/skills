---
name: clean-code
version: 1.0.0
description: |
  Clean cosmetic formatting from code files: removes decorative separator
  comments (─────), alignment spaces used only for visual alignment,
  non-keyboard symbols (→, –, …, ✓), and replaces them with plain ASCII
  equivalents. Does not change logic or structure.
allowed-tools:
  - Read
  - Edit
  - Grep
  - Glob
---

# CleanCode: Remove Cosmetic Formatting

Clean the target files by applying the following rules, in order.

## Rules

### 1. Decorative separator comments
Remove lines that are only decoration, keeping the label if there is one.

Before:
```python
# ──────────────────────────────────────────────────────────────────────────────
# Dataset
# ──────────────────────────────────────────────────────────────────────────────
```
After:
```python
# Dataset
```

Single-line decorative comments with no label are deleted entirely.

### 2. Non-keyboard symbols
Replace with plain ASCII:

| Symbol | Replace with |
|--------|-------------|
| `→`    | `->`        |
| `–`    | `-`         |
| `…`    | `...`       |
| `✓`    | (remove)    |
| any other non-ASCII symbol in comments or strings | closest ASCII equivalent or remove |

Do NOT touch accented letters in natural language text (é, à, ç, etc.) — those are valid keyboard characters in French and other languages.

### 3. Alignment spaces in comments and docstrings
Remove extra spaces inserted only to align columns vertically.

Before:
```python
ap.add_argument("--epochs",      type=int,   default=10)
ap.add_argument("--lr",          type=float, default=1e-3)
```
After:
```python
ap.add_argument("--epochs", type=int, default=10)
ap.add_argument("--lr", type=float, default=1e-3)
```

Before:
```python
    x : LongTensor de forme (window_size,)   - tokens en entrée
    y : int                                   - token cible
```
After:
```python
    x : LongTensor de forme (window_size,) - tokens en entrée
    y : int - token cible
```

Same rule applies to inline comments:
```python
emb = self.embedding(x)                 # (batch, seq_len, embed_dim)
```
becomes:
```python
emb = self.embedding(x) # (batch, seq_len, embed_dim)
```

### 4. Alignment spaces in variable assignments
Remove extra spaces used to align `=` signs across multiple lines.

Before:
```python
train_ds = SchedSwitchDataset(train_seqs, window_size)
val_ds   = SchedSwitchDataset(val_seqs,   window_size)
test_ds  = SchedSwitchDataset(test_seqs,  window_size)
```
After:
```python
train_ds = SchedSwitchDataset(train_seqs, window_size)
val_ds = SchedSwitchDataset(val_seqs, window_size)
test_ds = SchedSwitchDataset(test_seqs, window_size)
```

## Workflow

1. If the user specifies files or a directory, work on those. Otherwise ask.
2. For each file:
   a. Grep for non-ASCII characters to find symbols to fix.
   b. Grep for the `──` pattern to find separator comments.
   c. Read the file to spot alignment patterns visually.
   d. Apply all fixes with Edit.
3. After all edits, do a final Grep to confirm nothing was missed.

## What NOT to change

- Logic, variable names, or structure.
- Accented letters in French or other natural language text.
- Intentional ASCII art that is part of the program output (e.g. `print("===")`).
- String content that is user-facing output, unless it contains a non-keyboard symbol.
