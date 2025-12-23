import matplotlib
import matplotlib.pyplot as plt

_default_width_pt = 517.840015 # IFAC World Congress template
_default_file_format = "pdf"

_width_pt = _default_width_pt
_columnwidth_pt = _default_width_pt / 2
_file_format = _default_file_format


_preamble1 = r"""
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}

\usepackage{mathtools}
\usepackage{amsmath}
\usepackage{amssymb}
"""

_preamble2 = r"""
\usepackage{siunitx}

% Define some colors
\usepackage{xcolor}
% salmon = #FA8072
\definecolor{salmon}{RGB}{250, 128, 114}
\definecolor{salmonDarker}{RGB}{184, 61, 48}
% lightblue = #7BC8F6
\definecolor{lightblue}{RGB}{123, 200, 246}
\definecolor{lightblueDarker}{RGB}{39, 105, 143}
% green = #008000
\definecolor{green}{RGB}{0, 128, 0}
% blue = #0343DF
\definecolor{blue}{RGB}{3, 67, 223}

% then use these colors with
% \textcolor{salmon}{Loreum ips ...}
"""

def _make_preamble(font: str):
    if font == "times":
        # Use Times font for text and math
        _preamble_font = r"\usepackage{txfonts}"
    elif font == "lmodern":
        _preamble_font = r"\usepackage{lmodern}"
    elif font == "kp":
        _preamble_font = r"\usepackage[largesmallcaps,intlimits,widermath]{kpfonts}"
    else:
        raise NotImplementedError

    return _preamble1 + _preamble_font + _preamble2

def setup(
    width_pt: float = _default_width_pt,
    columnwidth_pt: float | None = None,
    font: str = "lmodern",
    major_fontsize: int = 10,
    minor_fontsize: int = 8,
    light_grid: bool = True,
    thin_lines: bool = False,
    latex_custom_cmds: str = r"",
    default_file_format: str = _default_file_format,
):
    """Setup matplotlib to be consistent with your .tex document.

    Args:
        width_pt (float, optional): Full text width of the LaTeX document
            in points (typically the value of \textwidth). Defaults to
            _default_width_pt.
        columnwidth_pt (float, optional): Column width in points (typically
            the value of \columnwidth). If None, it defaults to half of
            width_pt. This value is used by figsize_column() as its base.
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
            _default_file_format (e.g., "pdf").
    """
    global _file_format, _width_pt, _columnwidth_pt
    _file_format = default_file_format
    _width_pt = width_pt
    _columnwidth_pt = (width_pt / 2) if columnwidth_pt is None else columnwidth_pt

    matplotlib.use("pgf")

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
            "pgf.preamble": _make_preamble(font) + latex_custom_cmds,
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
    width_pt: float = _width_pt,
    fraction: float = 1.0,
    ratio: float = 1.62,
    subplots: tuple[int, int] = (1, 1),
) -> tuple[float, float]:
    """
    Compute figure size (width, height) in inches for LaTeX documents.

    Parameters
    ----------
    width_pt : float, optional
        Base width in LaTeX points. Defaults to `_width_pt` set in `setup()`
        (usually the LaTeX \textwidth). Pass e.g. \columnwidth if needed.
    fraction : float, optional
        Fraction of this width to occupy (e.g. 0.8 → 80% of width).
    ratio : float, optional
        Width-to-height ratio. Default 1.62 (approx. golden ratio).
    subplots : tuple[int, int], optional
        Rows and columns of subplots; height scales with n_rows/n_cols.

    Returns
    -------
    (float, float)
        Figure dimensions in inches for Matplotlib's figsize.
    """
    fig_width_in = width_pt * inches_per_pt * fraction
    n_rows, n_cols = subplots
    # fig_height_in = fig_width_in * n_rows / (ratio * n_cols)
    fig_height_in = fig_width_in / ratio
    return fig_width_in, fig_height_in

def figsize_text(fraction: float = 1.0, ratio: float = 1.62,
                 subplots: tuple[int, int] = (1, 1),
                 width_pt: float | None = None) -> tuple[float, float]:
    """Figure size in inches based on LaTeX \\textwidth."""
    return figsize(width_pt or _width_pt, fraction, ratio, subplots)


def figsize_column(fraction: float = 1.0, ratio: float = 1.62,
                   subplots: tuple[int, int] = (1, 1),
                   width_pt: float | None = None) -> tuple[float, float]:
    """Figure size in inches based on LaTeX \\columnwidth."""
    return figsize(width_pt or _columnwidth_pt, fraction, ratio, subplots)

def savefig(filename: str, transparent=True, dpi=300, tight=False, **kwargs):
    """Saves the current matplotlib figure.

    Args:
        filename (str): Name of the file
        transparent (bool, optional): Make background transparent. Defaults to True.
        dpi (int, optional): DPI of non-vectorized graphics. Defaults to 300.
        tight (bool, optional): Enables tight figure padding. Defaults to False.
    """
    split = filename.split(".")
    if len(split) == 2:
        filename, format = split
    elif len(split) == 1:
        format = _file_format
    else:
        raise Exception(
            f"The fileformat could not be uniquely infered from the filename={filename}"
        )

    # Defaults (only if user didn't pass them)
    if format.lower() in ["jpg", "jpeg", "png", "tiff"]:
        kwargs.setdefault("dpi", dpi)
    if tight:
        kwargs.setdefault("bbox_inches", "tight")

    plt.savefig(
        f"{filename}.{format}", format=format, transparent=transparent, **kwargs
    )

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

def utils_adjust_ligher_grid(alpha: float):
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

def utils_hide_frame(ax, sides=[0, 1, 2, 3]):
    """Hides the framewires around the figure.
    E.g. [1, 3] hides upper-right axes
    y |_
       x
    """
    for i, spine in enumerate(ax.spines.values()):
        if i not in sides:
            continue
        spine.set_visible(False)