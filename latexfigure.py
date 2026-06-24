import os
from typing import Literal

import matplotlib
import matplotlib.pyplot as plt

__version__ = "1.5.0"

__all__ = [
    "Font",
    "setup",
    "savefig",
    "show",
    "savefig_show",
    "figsize",
    "figsize_text",
    "figsize_column",
    "utils_add_second_xaxis",
    "utils_add_second_yaxis",
    "utils_matplotlib_default_colors",
    "utils_hide_frame",
    "utils_adjust_lighter_grid",
]

Font = Literal["lmodern", "times", "kp"]
_SUPPORTED_FONTS: tuple[str, ...] = ("lmodern", "times", "kp")

# IEEE conference template (IEEEtran, two-column).
_default_width_pt = 516.0
_default_columnwidth_pt = 252.0
_default_file_format = "pdf"
_default_backend = "inline"

_width_pt = _default_width_pt
_columnwidth_pt = _default_columnwidth_pt
_file_format = _default_file_format
_backend = _default_backend
_last_saved = None  # path of the most recently saved figure (for show())


_preamble1 = r"""
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}

\usepackage{mathtools}
\usepackage{amsmath}
\usepackage{amssymb}
"""

_preamble2 = r"""
\usepackage{siunitx}

% Load xcolor with the SVG/X11 color set (Salmon, LightBlue, LightGreen, ...;
% note the CamelCase names) so a rich palette is available without redefining
% xcolor's built-in lowercase 'blue' or 'green'.
\usepackage[svgnames]{xcolor}
"""

def _make_preamble(font: Font) -> str:
    if font == "times":
        # Use Times font for text and math
        _preamble_font = r"\usepackage{txfonts}"
    elif font == "lmodern":
        _preamble_font = r"\usepackage{lmodern}"
    elif font == "kp":
        _preamble_font = r"\usepackage[largesmallcaps,intlimits,widermath]{kpfonts}"
    else:
        raise ValueError(
            f"Unsupported font {font!r}; expected one of {_SUPPORTED_FONTS}"
        )

    return _preamble1 + _preamble_font + _preamble2

def setup(
    width_pt: float | None = None,
    columnwidth_pt: float | None = None,
    font: Font = "lmodern",
    major_fontsize: int = 10,
    minor_fontsize: int = 8,
    light_grid: bool = True,
    thin_lines: bool = False,
    latex_custom_cmds: str = r"",
    default_file_format: str = _default_file_format,
    backend: str | None = _default_backend,
):
    r"""Setup matplotlib to be consistent with your .tex document.

    Args:
        width_pt (float, optional): Full text width of the LaTeX document
            in points (typically the value of \textwidth). If None, the
            IEEE conference template width (516.0 pt) is used.
        columnwidth_pt (float, optional): Column width in points (typically
            the value of \columnwidth). If None and `width_pt` is also
            None, the IEEE conference template column width (252.0 pt) is
            used. If `width_pt` is given but `columnwidth_pt` is not, this
            defaults to `width_pt / 2`. This value is used by
            `figsize_column()` as its base.
        font (str, optional): Font used in the LaTeX document.
            One of {"lmodern", "times", "kp"}. Defaults to "lmodern".
        major_fontsize (int, optional): Base font size (e.g., axes labels)
            to match the LaTeX document's main font size. Defaults to 10.
        minor_fontsize (int, optional): Slightly smaller font size used for
            tick labels and legends. Defaults to 8.
        light_grid (bool, optional): Enable lighter grid lines for cleaner
            plots. Defaults to True.
        thin_lines (bool, optional): Use thinner axis and plot lines to
            better match thin LaTeX lettering. Defaults to False.
        latex_custom_cmds (str, optional): Additional LaTeX commands to
            append to the preamble (e.g., custom macros or packages).
            Defaults to an empty string.
        default_file_format (str, optional): Default file format used by
            `savefig` when the filename has no extension. Defaults to
            "pdf".
        backend (str | None, optional): One of {"inline", "pgf"}, None, or
            any Matplotlib backend name. Defaults to "inline".
            - "inline" (or None): keep the active (Jupyter inline / GUI)
              backend and render text with usetex, so figures display
              inline in notebooks and pop up in scripts. `savefig` still
              exports every file through the pgf/pdflatex pipeline, so the
              saved PDF is full pgf quality regardless of the display
              backend. The on-screen preview is not pixel-identical to that
              PDF; use `show()` for an exact preview. Requires pdflatex +
              dvipng + gs.
            - "pgf": force the non-interactive pgf backend (no display),
              e.g. for headless/batch export. Preview saved files with
              `show()`.
            - any other name (e.g. "agg", "qtagg"): switch to that backend;
              `savefig` still exports through pgf.
    """
    global _file_format, _width_pt, _columnwidth_pt, _backend
    _file_format = default_file_format
    if width_pt is None:
        _width_pt = _default_width_pt
        _columnwidth_pt = (
            _default_columnwidth_pt if columnwidth_pt is None else columnwidth_pt
        )
    else:
        _width_pt = width_pt
        _columnwidth_pt = (width_pt / 2) if columnwidth_pt is None else columnwidth_pt
    _backend = backend

    if backend is None or backend == "inline":
        pass  # keep the active backend so figures display; export via pgf
    elif backend == "pgf":
        matplotlib.use("pgf")
    else:
        matplotlib.use(backend)

    preamble = _make_preamble(font) + latex_custom_cmds

    matplotlib.rcParams.update( # for all options use print(plt.rcParams)
        {
            # Use LaTeX to write all text
            "text.usetex": True,
            "font.family": "serif",
            # "font.serif": [],  # use default fonts
            # "font.sans-serif": [],  # use default fonts
            # "font.monospace": [],  # use default fonts
            # Use 10pt font in plots, to match 10pt font in document
            "axes.labelsize": major_fontsize,
            "axes.titlesize": major_fontsize,
            "font.size": major_fontsize,
            # Make the legend/label fonts a little smaller
            "legend.fontsize": minor_fontsize,
            "xtick.labelsize": minor_fontsize,
            "ytick.labelsize": minor_fontsize,
            # Use system fonts when rendering SVGs.
            "svg.fonttype": "none",
            # Same preamble for the on-screen (usetex) render and the pgf export
            "text.latex.preamble": preamble,
            "pgf.preamble": preamble,
            "pgf.texsystem": "pdflatex",
            "pgf.rcfonts": False,  # Do not override LaTeX font settings
        }
    )

    if thin_lines:
        _use_thin_lines()

    if light_grid:
        _use_lighter_grid()


# golden_ratio = 2.0 / (5**0.5 - 1)
inches_per_pt = 1 / 72.27

def figsize(
    width_pt: float | None = None,
    fraction: float = 1.0,
    ratio: float = 1.62,
    subplots: tuple[int, int] = (1, 1),
) -> tuple[float, float]:
    r"""
    Compute figure size (width, height) in inches for LaTeX documents.

    Parameters
    ----------
    width_pt : float, optional
        Base width in LaTeX points. If None, the value configured via
        `setup()` is used (typically the LaTeX \textwidth). Pass e.g.
        \columnwidth if needed.
    fraction : float, optional
        Fraction of this width to occupy (e.g. 0.8 → 80% of width).
    ratio : float, optional
        Width-to-height ratio. Default 1.62 (approx. golden ratio).
    subplots : tuple[int, int], optional
        Rows and columns of subplots; height scales with n_rows/n_cols
        so each subplot keeps the requested width/height ratio.

    Returns
    -------
    (float, float)
        Figure dimensions in inches for Matplotlib's figsize.
    """
    if width_pt is None:
        width_pt = _width_pt
    fig_width_in = width_pt * inches_per_pt * fraction
    n_rows, n_cols = subplots
    fig_height_in = fig_width_in * (n_rows / n_cols) / ratio
    return fig_width_in, fig_height_in

def figsize_text(fraction: float = 1.0, ratio: float = 1.62,
                 subplots: tuple[int, int] = (1, 1),
                 width_pt: float | None = None) -> tuple[float, float]:
    r"""Figure size in inches based on LaTeX \textwidth."""
    return figsize(width_pt if width_pt is not None else _width_pt,
                   fraction, ratio, subplots)


def figsize_column(fraction: float = 1.0, ratio: float = 1.62,
                   subplots: tuple[int, int] = (1, 1),
                   width_pt: float | None = None) -> tuple[float, float]:
    r"""Figure size in inches based on LaTeX \columnwidth."""
    return figsize(width_pt if width_pt is not None else _columnwidth_pt,
                   fraction, ratio, subplots)

def savefig(filename: str, transparent=True, dpi=300, tight=False,
            backend: str = "pgf", **kwargs):
    """Saves the current matplotlib figure.

    By default the file is rendered through the pgf/pdflatex pipeline (even
    when `setup(backend="inline")` is active), so the exported figure has full
    pgf quality regardless of the on-screen display backend.

    Args:
        filename (str): Name of the file. If it has no extension, the
            default file format configured via `setup()` is used.
            Filenames containing multiple dots (e.g. "fig.v2.pdf") and
            paths (e.g. "./out/fig.pdf") are handled correctly.
        transparent (bool, optional): Make background transparent. Defaults to True.
        dpi (int, optional): DPI of non-vectorized graphics. Defaults to 300.
            Only affects raster formats (jpg, png, tiff); ignored for
            vector formats (pdf, svg).
        tight (bool, optional): Use a tight bounding box (bbox_inches="tight").
            Defaults to False.
        backend (str, optional): Matplotlib backend used to render this file.
            Defaults to "pgf" for publication-quality output. Pass e.g. "agg"
            for a quick raster export without LaTeX.
    """
    global _last_saved

    stem, ext = os.path.splitext(filename)
    if ext:
        format = ext.lstrip(".")
        filename = stem
    else:
        format = _file_format

    if not format:
        raise ValueError(
            f"Could not infer a file format from filename={filename!r}; "
            "pass a filename with an extension or set a default via setup()."
        )

    # Defaults (only if user didn't pass them)
    if format.lower() in ("jpg", "jpeg", "png", "tiff"):
        kwargs.setdefault("dpi", dpi)
    if tight:
        kwargs.setdefault("bbox_inches", "tight")

    out_path = f"{filename}.{format}"
    plt.savefig(
        out_path, format=format, transparent=transparent, backend=backend, **kwargs
    )
    _last_saved = out_path


def show(filename: str | None = None, dpi: int = 200):
    """Display a saved figure inline (e.g. in Jupyter) by rasterizing its PDF.

    Useful in `backend="pgf"` mode, or to preview the exact exported PDF
    (pixel-faithful, unlike the `backend="inline"` on-screen render).

    Requires PyMuPDF: ``pip install latexfigure[preview]``.

    Args:
        filename (str, optional): PDF to display. Defaults to the file most
            recently written by `savefig`.
        dpi (int, optional): Rasterization resolution. Defaults to 200.
    """
    try:
        import fitz  # PyMuPDF
    except ImportError as e:
        raise ImportError(
            "show() needs PyMuPDF. Install it with: pip install latexfigure[preview]"
        ) from e
    from IPython.display import Image, display

    path = filename or _last_saved
    if path is None:
        raise ValueError(
            "No figure to show: call savefig() first or pass a filename."
        )

    doc = fitz.open(path)
    try:
        for page in doc:
            pix = page.get_pixmap(dpi=dpi)
            display(Image(data=pix.tobytes("png")))
    finally:
        doc.close()


def savefig_show(filename: str, preview_dpi: int = 200, **kwargs):
    """Convenience: `savefig(filename, **kwargs)` followed by `show()`."""
    savefig(filename, **kwargs)
    show(dpi=preview_dpi)

def _use_thin_lines():
    matplotlib.rcParams.update(
        {
            # Decrease lineweidths to match thinner TeX lettering.
            "axes.linewidth": 0.1,
            "lines.linewidth": 0.5,
        }
    )

_light_grid_params = {
    # corresponds to default b0b0b0 with grid.alpha=0.3,
    # but looks better
    "grid.color": "e7e7e7",
}

def _use_lighter_grid():
    matplotlib.rcParams.update(_light_grid_params)

def utils_adjust_lighter_grid(alpha: float):
    global _light_grid_params
    _light_grid_params = {"grid.color": "b0b0b0", "grid.alpha": alpha}
    _use_lighter_grid()

def utils_add_second_xaxis(ax):
    """Adds a second x-axis on top frame of figure"""
    ax2 = ax.twiny()
    ax2.set_xticks(ax.get_xticks())
    ax2.set_xbound(ax.get_xbound())
    return ax2

def utils_add_second_yaxis(ax):
    """Adds a second y-axis on right frame of figure"""
    ax2 = ax.twinx()
    ax2.set_yticks(ax.get_yticks())
    ax2.set_ybound(ax.get_ybound())
    return ax2

def utils_matplotlib_default_colors() -> list[str]:
    """Defaults colors used by matplotlib"""
    return plt.rcParams["axes.prop_cycle"].by_key()["color"]

def utils_hide_frame(ax, sides: tuple[int, ...] = (0, 1, 2, 3)):
    """Hides the framewires around the figure.
    E.g. (1, 3) hides upper-right axes
    y |_
       x
    """
    for i, spine in enumerate(ax.spines.values()):
        if i not in sides:
            continue
        spine.set_visible(False)
