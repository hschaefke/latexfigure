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

The overall structure and design of the original project are preserved.

## Getting started

In Python:

```python
import matplotlib.pyplot as plt
import latexfigure as lf

lf.setup(
    width_pt=469.0,
    columnwidth_pt=229.5,
    major_fontsize=10,
    minor_fontsize=8,
)

plt.figure(figsize=figsize_text())
plt.plot(...)

# saves by default as .pdf
lf.savefig("my_figure")
```

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

# Full text width figure
fig, ax = plt.subplots(figsize=lf.figsize_text(), constrained_layout=True)
ax.plot(x, y, marker='o')
ax.set_title("Full text width (~517.84 pt)")
ax.set_xlabel("x")
ax.set_ylabel("sqrt(x)")
lf.savefig("figure_textwidth")  # saved as PDF by default

# One column width figure
fig, ax = plt.subplots(figsize=lf.figsize_column(), constrained_layout=True)
ax.plot(x, y, marker='s', color='salmon')   # LaTeX color names are supported
ax.set_title("One column width (~251.81 pt)")
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
  \caption{Example plot scaled to full text width (517.84 pt).}
  \label{fig:figure_textwidth}
\end{figure*}

% === Normal single-column figure ===
\begin{figure}[h]
  \centering
  \includegraphics[width=\columnwidth]{figure_columnwidth.pdf}
  % alternative without explicit width:
  % \includegraphics{figure_columnwidth.pdf}
  \caption{Example plot scaled to one column width (251.81 pt).}
  \label{fig:figure_columnwidth}
\end{figure}
```
