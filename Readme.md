# latexfigure

Create publication-quality Matplotlib plots that match your LaTeX document.

Install with
```bash
pip install git+https://github.com/hschaefke/latexfigure
```

This project builds upon
https://github.com/simon-bachhuber/myplotlib.

It slightly extends the library by adding:

- Single- and two-column LaTeX support via explicit handling of `\textwidth` and `\columnwidth`

- A more flexible `savefig` wrapper with finer control over export options.

- Inline previews: figures display in Jupyter / pop up in scripts while still
  exporting through the pgf pipeline (see [Previewing figures](#previewing-figures)).

The overall structure and design of the original project are preserved.

## Requirements

A working LaTeX installation is required (text is typeset by LaTeX). For the
inline preview you additionally need `pdflatex`, `dvipng` and `ghostscript`
(all shipped with TeX Live / MacTeX).

Install with the optional `preview` extra to enable `lf.show()`:

```bash
pip install "latexfigure[preview] @ git+https://github.com/hschaefke/latexfigure"
```

## Getting started

In Python:

```python
import numpy as np
import matplotlib.pyplot as plt
import latexfigure as lf

# With no width_pt, setup() defaults to the IEEE conference template
# (\textwidth = 516.0 pt, \columnwidth = 252.0 pt). Override either value to
# match a different LaTeX class — see "Getting latex_page_width" below.
lf.setup(
    width_pt=469.0,
    columnwidth_pt=229.5,
    major_fontsize=10,
    minor_fontsize=8,
)  # backend="inline" by default → figures display in notebooks

plt.figure(figsize=lf.figsize_text())

# example plot
x = np.linspace(0, 2*np.pi, 100)
plt.plot(x, np.sin(x))

# saves by default as .pdf (always rendered via pgf for full quality)
lf.savefig("my_figure")
```

## Previewing figures

`setup()` runs in `backend="inline"` mode by default: the active Matplotlib
backend is kept, so figures display inline in Jupyter and pop up in scripts,
with text rendered by LaTeX. `lf.savefig()` always exports through the
pgf/pdflatex pipeline, so the **saved PDF is full pgf quality** regardless of
the display backend.

The on-screen inline preview is not pixel-identical to the exported PDF. For an
exact, pixel-faithful preview of the file you just saved, use `lf.show()` (needs
the `preview` extra):

```python
lf.savefig("my_figure")
lf.show()                 # rasterizes my_figure.pdf and displays it inline
# or in one call:
lf.savefig_show("my_figure")
```

For headless/batch export without any display, use `lf.setup(backend="pgf")`.

In Latex:

```latex
\usepackage{graphicx}

% begin document

\begin{figure}
  \centering
  \includegraphics{my_figure.pdf}
\end{figure}
```

## Getting `latex_page_width`

Obtain the `width_pt` and `columnwidth` argument of `figsize` by using

```latex
% your document class here
\documentclass[twocolumn]{article}
\begin{document}

% gives the width of the current document in pts
\the\textwidth\\
\the\columnwidth\\

\end{document}
```

If you want the values also in mm and a visual check (a line of exactly that length), use the additional `layouts` package:

```latex
\documentclass[twocolumn]{article}
\usepackage{layouts}

\begin{document}

% --- Full text width (whole page / both columns) ---
\noindent\the\textwidth\par                         % width in pt
\printinunitsof{mm}\prntlen{\textwidth}\par         % width in mm
\noindent\rule{\textwidth}{0.4pt}\par               % visual line

% --- Single column width (for two-column layout) ---
\noindent\the\columnwidth\par
\printinunitsof{mm}\prntlen{\columnwidth}\par
\noindent\rule{\columnwidth}{0.4pt}\par

\end{document}
```

With the measured values, you can now configure `latexfigure` and generate figures that exactly match either the full text width or a single column width in your LaTeX document:

```python
# Example data
x = range(10)
y = [i**0.5 for i in x]

# Full text width figure (width_pt=469.0 as configured above)
fig, ax = plt.subplots(figsize=lf.figsize_text(), constrained_layout=True)
ax.plot(x, y, marker='o')
ax.set_title("Full text width (~469 pt)")
ax.set_xlabel("x")
ax.set_ylabel("sqrt(x)")
lf.savefig("figure_textwidth")  # saved as PDF by default

# One column width figure (columnwidth_pt=229.5 as configured above)
fig, ax = plt.subplots(figsize=lf.figsize_column(), constrained_layout=True)
ax.plot(x, y, marker='s', color='salmon')   # matplotlib named color
ax.set_title("One column width (~229.5 pt)")
ax.set_xlabel("x")
ax.set_ylabel("sqrt(x)")
lf.savefig("figure_columnwidth")  # saved as PDF by default
```

## Including figures in LaTeX

In LaTeX, the generated figures can be included directly without additional scaling:

```latex
% === Full-width figure over both columns ===
\begin{figure*}[h]
  \centering
  \includegraphics[width=\textwidth]{figure_textwidth.pdf}
  % alternative without explicit width:
  % \includegraphics{figure_textwidth.pdf}
  \caption{Example plot scaled to full text width (469 pt).}
  \label{fig:figure_textwidth}
\end{figure*}

% === Normal single-column figure ===
\begin{figure}[h]
  \centering
  \includegraphics[width=\columnwidth]{figure_columnwidth.pdf}
  % alternative without explicit width:
  % \includegraphics{figure_columnwidth.pdf}
  \caption{Example plot scaled to one column width (229.5 pt).}
  \label{fig:figure_columnwidth}
\end{figure}
```

## Custom LaTeX colors

`setup()` loads `xcolor` with the `svgnames` option, so the full SVG/X11 color
set is available in LaTeX text such as axis labels — without redefining xcolor's
standard `green` or `blue`. The SVG names are **CamelCase**: `Salmon`,
`LightBlue`, `LightGreen`, `DarkGreen`, `SteelBlue`, ... (the lowercase `green`
/ `blue` still resolve to xcolor's built-ins):

```python
ax.set_xlabel(r"\textcolor{DarkGreen}{time} [s]")
```

> Note: Matplotlib color names (e.g. `color='salmon'`) are a separate system
> (matplotlib's CSS4 names) and are unaffected by the LaTeX preamble.

## Upgrading to 1.5

Version 1.5 cleans up several rough edges. If you are upgrading from an earlier
1.x:

- **Default template changed**: `setup()` with no arguments now configures the
  IEEE conference template (`\textwidth = 516.0 pt`, `\columnwidth = 252.0 pt`)
  instead of the previous IFAC World Congress width. Pass `width_pt` /
  `columnwidth_pt` explicitly if you depend on the old values.
- **Inline display by default**: `setup()` now uses `backend="inline"`, so
  figures display inline in Jupyter / pop up in scripts. `savefig()` still
  exports through pgf, so the saved file is unchanged in quality. Use
  `backend="pgf"` for the old headless behavior, or `backend=None` / any
  Matplotlib backend name for full control.
- **`figsize()` now reflects `setup()` calls**: previously the default
  `width_pt` was captured at import time and silently ignored later `setup()`
  calls. It now resolves to the configured value at call time.
- **`figsize(..., subplots=...)` now works as documented**: the height scales
  with `n_rows / n_cols` rather than being ignored.
- **`savefig()` accepts filenames with multiple dots and paths**
  (`fig.v2.pdf`, `./out/fig.pdf`).
- **LaTeX preamble no longer redefines standard colors**: the custom
  `\definecolor` block (which silently overrode `\color{blue}` and
  `\color{green}`) is gone. `xcolor` is loaded with `svgnames` instead, exposing
  the SVG/X11 palette (CamelCase names: `Salmon`, `LightBlue`, `LightGreen`, ...)
  without shadowing built-in colors. The previously custom `salmon` /
  `salmonDarker` / `lightblue` / `lightblueDarker` definitions are gone — use the
  SVG names (`Salmon`, `LightBlue`, ...) instead.
- **`utils_adjust_ligher_grid` was renamed to `utils_adjust_lighter_grid`**
  (typo fix).
- **Self-dependency removed**: `pyproject.toml` no longer lists `latexfigure` as
  its own dependency; `matplotlib>=3.6` is the runtime dependency. Install the
  `preview` extra for `lf.show()`.
