import contextlib
import functools
import typing


import forbiddenfruit as ff


RESET = "\033[0m"

ATTRIBUTES = dict(
    reset=0,
    bold=1,
    dim=2,
    italic=3,
    underline=4,
    slow_blink=5,
    rapid_blink=6,
    inverse=7,
    hidden=8,
    strike=9,
)

FOREGROUND = dict(
    black=30,
    red=31,
    green=32,
    yellow=33,
    blue=34,
    magenta=35,
    cyan=36,
    white=37,
    bright_black=90,
    bright_red=91,
    bright_green=92,
    bright_yellow=93,
    bright_blue=94,
    bright_magenta=95,
    bright_cyan=96,
    bright_white=97,
)

BACKGROUND = dict(
    black=40,
    red=41,
    green=42,
    yellow=43,
    blue=44,
    magenta=45,
    cyan=46,
    white=47,
    bright_black=100,
    bright_red=101,
    bright_green=102,
    bright_yellow=103,
    bright_blue=104,
    bright_magenta=105,
    bright_cyan=106,
    bright_white=107,
)


def colorize_ansi(
    text: str,
    style: typing.Optional[str] = None,
    foreground: typing.Optional[str] = None,
    background: typing.Optional[str] = None,
) -> str:
    codes: list[str] = []
    if style:
        codes.append(str(ATTRIBUTES[style]))
    if foreground:
        codes.append(str(FOREGROUND[foreground]))
    if background:
        codes.append(str(BACKGROUND[background]))

    if codes:
        prefix = f"\033[{';'.join(codes)}m"
        return f"{prefix}{text}{RESET}"

    return text


def colorize_256(text: str, n: int) -> str:
    code = f"\033[38;5;{n}m"
    return f"{code}{text}{RESET}"


def colorize_true_color(
    text: str,
    foreground: typing.Optional[typing.Tuple[int, int, int]] = None,
    background: typing.Optional[typing.Tuple[int, int, int]] = None,
) -> str:
    codes: list[str] = []
    if foreground:
        r, g, b = foreground
        codes.append(f"38;2;{r};{g};{b}")
    if background:
        r, g, b = background
        codes.append(f"48;2;{r};{g};{b}")

    if codes:
        prefix = f"\033[{';'.join(codes)}m"
        return f"{prefix}{text}{RESET}"

    return text


def bold(self):
    return colorize_ansi(self, style="bold")


def dim(self):
    return colorize_ansi(self, style="dim")


def italic(self):
    return colorize_ansi(self, style="italic")


def underline(self):
    return colorize_ansi(self, style="underline")


def blink(self):
    return colorize_ansi(self, style="slow_blink")


def rapid_blink(self):
    return colorize_ansi(self, style="rapid_blink")


def inverse(self):
    return colorize_ansi(self, style="inverse")


def hidden(self):
    return colorize_ansi(self, style="hidden")


def strike(self):
    return colorize_ansi(self, style="strike")


def red(self):
    return colorize_ansi(self, foreground="red")


def green(self):
    return colorize_ansi(self, foreground="green")


def yellow(self):
    return colorize_ansi(self, foreground="yellow")


def blue(self):
    return colorize_ansi(self, foreground="blue")


def magenta(self):
    return colorize_ansi(self, foreground="magenta")


def cyan(self):
    return colorize_ansi(self, foreground="cyan")


def white(self):
    return colorize_ansi(self, foreground="white")


def black(self):
    return colorize_ansi(self, foreground="black")


def bright_red(self):
    return colorize_ansi(self, foreground="bright_red")


def on_red(self):
    return colorize_ansi(self, background="red")


def on_green(self):
    return colorize_ansi(self, background="green")


def bright_black(self):
    return colorize_ansi(self, foreground="bright_black")


def bright_green(self):
    return colorize_ansi(self, foreground="bright_green")


def bright_yellow(self):
    return colorize_ansi(self, foreground="bright_yellow")


def bright_blue(self):
    return colorize_ansi(self, foreground="bright_blue")


def bright_magenta(self):
    return colorize_ansi(self, foreground="bright_magenta")


def bright_cyan(self):
    return colorize_ansi(self, foreground="bright_cyan")


def bright_white(self):
    return colorize_ansi(self, foreground="bright_white")


def on_black(self):
    return colorize_ansi(self, background="black")


def on_white(self):
    return colorize_ansi(self, background="white")


def on_yellow(self):
    return colorize_ansi(self, background="yellow")


def on_blue(self):
    return colorize_ansi(self, background="blue")


def on_magenta(self):
    return colorize_ansi(self, background="magenta")


def on_cyan(self):
    return colorize_ansi(self, background="cyan")


def on_bright_black(self):
    return colorize_ansi(self, background="bright_black")


def on_bright_red(self):
    return colorize_ansi(self, background="bright_red")


def on_bright_green(self):
    return colorize_ansi(self, background="bright_green")


def on_bright_yellow(self):
    return colorize_ansi(self, background="bright_yellow")


def on_bright_blue(self):
    return colorize_ansi(self, background="bright_blue")


def on_bright_magenta(self):
    return colorize_ansi(self, background="bright_magenta")


def on_bright_cyan(self):
    return colorize_ansi(self, background="bright_cyan")


def on_bright_white(self):
    return colorize_ansi(self, background="bright_white")


def _clamp(value: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(max_value, int(value)))


def on_rgb(self, r: int, g: int, b: int):
    """Apply an RGB 24-bit background color to the string. Example: 'hi'.on_rgb(255,0,0)"""
    # clamp values
    r = _clamp(r, 0, 255)
    g = _clamp(g, 0, 255)
    b = _clamp(b, 0, 255)
    return colorize_true_color(self, background=(r, g, b))


def rgb(self, r: int, g: int, b: int):
    """Apply an RGB 24-bit foreground color to the string. Example: 'hi'.rgb(255,0,0)"""
    # clamp values
    r = _clamp(r, 0, 255)
    g = _clamp(g, 0, 255)
    b = _clamp(b, 0, 255)
    return colorize_true_color(self, foreground=(r, g, b))


def color256(self, idx: int):
    idx = _clamp(idx, 0, 255)
    return colorize_256(self, idx)


_METHODS = {
    "bold": bold,
    "dim": dim,
    "faint": dim,
    "dark": dim,
    "italic": italic,
    "underline": underline,
    "blink": blink,
    "slow_blink": blink,
    "rapid_blink": rapid_blink,
    "reverse": inverse,
    "inverse": inverse,
    "hidden": hidden,
    "concealed": hidden,
    "password": hidden,
    "strike": strike,
    "red": red,
    "green": green,
    "yellow": yellow,
    "blue": blue,
    "magenta": magenta,
    "cyan": cyan,
    "white": white,
    "black": black,
    "bright_black": bright_black,
    "bright_red": bright_red,
    "bright_green": bright_green,
    "bright_yellow": bright_yellow,
    "bright_blue": bright_blue,
    "bright_magenta": bright_magenta,
    "bright_cyan": bright_cyan,
    "bright_white": bright_white,
    "on_black": on_black,
    "on_gray": on_black,
    "on_grey": on_black,
    "on_red": on_red,
    "on_green": on_green,
    "on_yellow": on_yellow,
    "on_blue": on_blue,
    "on_magenta": on_magenta,
    "on_cyan": on_cyan,
    "on_white": on_white,
    "on_bright_black": on_bright_black,
    "on_bright_grey": on_bright_black,
    "on_bright_gray": on_bright_black,
    "on_bright_red": on_bright_red,
    "on_bright_green": on_bright_green,
    "on_bright_yellow": on_bright_yellow,
    "on_bright_blue": on_bright_blue,
    "on_bright_magenta": on_bright_magenta,
    "on_bright_cyan": on_bright_cyan,
    "on_bright_white": on_bright_white,
    "rgb": rgb,
    "on_rgb": on_rgb,
    "color256": color256,
}


def patch():
    """Attach all color/format methods to built-in `str`."""
    for name, func in _METHODS.items():
        ff.curse(str, name, func)


def unpatch():
    """Remove the added methods from `str`"""
    for name in _METHODS.keys():
        ff.reverse(str, name)


def patched(func=None):
    """Attach all color/format methods to built-in `str` in a limited scope.

    Examples:
    ```python
    import coloredstrings

    # Patched `str` methods are available only within the context
    def warn(msg: str) -> None:
        with coloredstrings.patched():
            print("warning:".yellow().bold(), msg)

    # Same idea, but using a decorator
    @coloredstrings.patched
    def info(msg: str) -> None:
        print("[info]:".blue(), msg)
    ```
    """
    if func is None:

        @contextlib.contextmanager
        def _cm():
            patch()
            try:
                yield
            finally:
                unpatch()

        return _cm()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        patch()
        try:
            return func(*args, **kwargs)
        finally:
            unpatch()

    return wrapper
