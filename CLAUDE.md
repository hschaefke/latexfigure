# latexfigure

Single-file Python package for publication-quality Matplotlib figures whose text
and sizing exactly match a LaTeX document. Builds on simon-bachhuber/myplotlib.

## Layout
- `latexfigure.py` — the entire library (`setup`, `figsize` / `figsize_text` /
  `figsize_column`, `savefig`, `show` / `savefig_show`, `utils_*`). No package dir.
- `example.py` — runnable demo; writes `plot_columnwidth.pdf` + `plot_textwidth.pdf`
  (gitignored).
- `example.tex` / `example.pdf` — demo doc embedding those figures, plus the
  `\textwidth` / `\columnwidth` measurement rulers.
- `pyproject.toml` — setuptools, `py-modules = ["latexfigure"]`.

## Dev setup
Needs a LaTeX toolchain on PATH: `pdflatex`, `dvipng`, `ghostscript` (text is
typeset by LaTeX; figures export via the pgf backend).

```bash
python -m venv .venv
.venv/bin/pip install -e .       # pulls matplotlib + PyMuPDF
.venv/bin/python example.py      # regenerate the demo figures
pdflatex example.tex             # -> example.pdf
```

No automated tests: verify by rendering a figure through pgf (check embedded
LaTeX fonts with `pdffonts`) and/or compiling `example.tex`.

## Design notes
- `setup(backend=...)` defaults to `"inline"`: keeps the active backend for
  inline/popup display, while `savefig()` always exports through pgf
  (`backend="pgf"`) — the saved PDF is full pgf quality regardless of display.
  Also accepts `"pgf"` (headless), `None`, or any matplotlib backend name.
  The same preamble goes to both `text.latex.preamble` and `pgf.preamble`.
- `show()` / `savefig_show()` rasterize the saved PDF via PyMuPDF (a real
  dependency) and display via IPython — notebook only.
- Colors: `xcolor[svgnames]`, CamelCase names (`Salmon`, `LightBlue`, ...). The
  preamble does NOT redefine `green` / `blue`.
- Default template: IEEE conference (`\textwidth = 516.0`, `\columnwidth = 252.0`).

## Conventions
- Keep it a single module; match the existing docstring style.
- Version lives in `pyproject.toml` and `latexfigure.__version__` — keep in sync.
- Commit/push only when asked; confirm before pushing.
