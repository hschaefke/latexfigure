"""Minimal latexfigure demo.

Run it to generate the two figures embedded in ``example.tex``::

    python example.py        # writes plot_columnwidth.pdf + plot_textwidth.pdf
    pdflatex example.tex     # compiles example.pdf with both figures embedded

The figures are sized to match ``example.tex`` exactly, so they are included
without any scaling.
"""

import numpy as np
import matplotlib.pyplot as plt

import latexfigure as lf

# Widths measured from example.tex (\the\textwidth / \the\columnwidth for
# \documentclass[10pt,twocolumn]{article}). Re-measure for your own document --
# see the "Getting latex_page_width" section in the README.
lf.setup(
    width_pt=469.0,        # \textwidth
    columnwidth_pt=229.5,  # \columnwidth
    backend="pgf",         # headless export for this script; default is "inline"
)

x = np.linspace(0, 2 * np.pi, 200)

# 1) Single-column figure -> fits one \columnwidth.
fig, ax = plt.subplots(figsize=lf.figsize_column(), constrained_layout=True)
ax.plot(x, np.sin(x), label=r"$\sin\theta$")
ax.plot(x, np.cos(x), label=r"$\cos\theta$", color="Salmon")
ax.set_xlabel(r"angle $\theta$ [rad]")
ax.set_ylabel("amplitude")
ax.legend()
lf.savefig("plot_columnwidth")

# 2) Full text width figure -> spans both columns.
fig, ax = plt.subplots(figsize=lf.figsize_text(), constrained_layout=True)
for k in (1, 2, 3):
    ax.plot(x, np.sin(k * x) / k, label=rf"$\sin({k}\theta)/{k}$")
ax.set_xlabel(r"angle $\theta$ [rad]")
ax.set_ylabel("amplitude")
ax.legend(ncol=3)
lf.savefig("plot_textwidth")

print("Wrote plot_columnwidth.pdf and plot_textwidth.pdf")
