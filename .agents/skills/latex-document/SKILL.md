---
name: latex-document
description: Use when creating or editing LaTeX source files (.tex) for articles, reports, or theses.
---

# LaTeX Document Skill

Write clean, compilable LaTeX. Prefer semantic markup and standard packages. Do not guess package names or syntax.

## When to use

- The user asks for a PDF document, paper, report, or CV.
- Refactoring or fixing compilation errors in `.tex` files.
- Adding figures, tables, or equations to an existing document.

## Principles

1. **Start from a minimal working example.** Do not add packages unless required.
2. **Semantic markup:** Use `\section`, `\emph`, `\label`/`\ref` instead of manual formatting.
3. **One sentence per line** in the `.tex` source. This keeps diffs readable.
4. **Never hardcode paths.** Use relative paths for `\includegraphics` and `\input`.

## Minimal Template

Use this unless the user provides their own preamble:

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage[english]{babel}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{geometry}
\geometry{margin=2.5cm}

% Load hyperref last
\usepackage{hyperref}
\hypersetup{colorlinks=true,linkcolor=blue,urlcolor=magenta}

\title{Title}
\author{Author}
\date{\today}

\begin{document}
\maketitle

\section{Introduction}
Content here.

\end{document}
```

## Building

Prefer `latexmk` for automatic resolution of cross-references and bibliography:

```bash
latexmk -pdf main.tex
```

To clean auxiliary files:
```bash
latexmk -C
```

If the project uses `biblatex` with `biber`, `latexmk` handles this automatically. If not, compile twice manually.

## Common Mistakes to Avoid

- **Loading packages in the wrong order.** `hyperref` must be loaded last.
- **Using `\\` for line breaks in prose.** Use a blank line for a new paragraph.
- **Inline math in display mode.** Use `\[ ... \]` or an `equation` environment, never `$$ ... $$`.
- **Guessing package names.** Only use packages you can verify exist (e.g., on CTAN).
- **Absolute paths in `\includegraphics` or `\input`.** Always relative to the `.tex` file.
- **Editing `.tex` without reading the error log.** If compilation fails, read the log from the bottom up.

## Figures, Tables, and Math

Keep it simple. Use `\includegraphics` for figures, `booktabs` for tables, and standard AMS environments for math. If the document requires complex TikZ, extensive custom formatting, or Beamer, state the increased scope and ask the user before proceeding.
