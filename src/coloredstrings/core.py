import contextlib
import functools


import forbiddenfruit as ff


ANSI = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "italic": "\033[3m",
    "underline": "\033[4m",
    "blink": "\033[5m",
    "inverse": "\033[7m",
    "hidden": "\033[8m",
    "strike": "\033[9m",
    "black": "\033[30m",
    "grey": "\033[30m",
    "gray": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bright_black": "\033[90m",
    "bright_grey": "\033[90m",
    "bright_gray": "\033[90m",
    "bright_red": "\033[91m",
    "bright_green": "\033[92m",
    "bright_yellow": "\033[93m",
    "bright_blue": "\033[94m",
    "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m",
    "bright_white": "\033[97m",
}


def _wrap(code: str, text: str) -> str:
    """Wrap text with an ANSI code and reset at the end (safe for chaining)."""
    return f"{code}{text}{ANSI['reset']}"


def bold(self):
    return _wrap(ANSI["bold"], self)


def dim(self):
    return _wrap(ANSI["dim"], self)


def italic(self):
    return _wrap(ANSI["italic"], self)


def underline(self):
    return _wrap(ANSI["underline"], self)


def blink(self):
    return _wrap(ANSI["blink"], self)


def inverse(self):
    return _wrap(ANSI["inverse"], self)


def hidden(self):
    return _wrap(ANSI["hidden"], self)


def strike(self):
    return _wrap(ANSI["strike"], self)


def red(self):
    return _wrap(ANSI["red"], self)


def green(self):
    return _wrap(ANSI["green"], self)


def yellow(self):
    return _wrap(ANSI["yellow"], self)


def blue(self):
    return _wrap(ANSI["blue"], self)


def magenta(self):
    return _wrap(ANSI["magenta"], self)


def cyan(self):
    return _wrap(ANSI["cyan"], self)


def white(self):
    return _wrap(ANSI["white"], self)


def black(self):
    return _wrap(ANSI["black"], self)


def bright_red(self):
    return _wrap(ANSI["bright_red"], self)


def on_red(self):
    return _wrap("\033[41m", self)


def on_green(self):
    return _wrap("\033[42m", self)


def bright_black(self):
    return _wrap(ANSI["bright_black"], self)


def bright_green(self):
    return _wrap(ANSI["bright_green"], self)


def bright_yellow(self):
    return _wrap(ANSI["bright_yellow"], self)


def bright_blue(self):
    return _wrap(ANSI["bright_blue"], self)


def bright_magenta(self):
    return _wrap(ANSI["bright_magenta"], self)


def bright_cyan(self):
    return _wrap(ANSI["bright_cyan"], self)


def bright_white(self):
    return _wrap(ANSI["bright_white"], self)


def on_black(self):
    return _wrap("\033[40m", self)


def on_white(self):
    return _wrap("\033[47m", self)


def on_yellow(self):
    return _wrap("\033[43m", self)


def on_blue(self):
    return _wrap("\033[44m", self)


def on_magenta(self):
    return _wrap("\033[45m", self)


def on_cyan(self):
    return _wrap("\033[46m", self)


def on_bright_black(self):
    return _wrap("\033[100m", self)


def on_bright_red(self):
    return _wrap("\033[101m", self)


def on_bright_green(self):
    return _wrap("\033[102m", self)


def on_bright_yellow(self):
    return _wrap("\033[103m", self)


def on_bright_blue(self):
    return _wrap("\033[104m", self)


def on_bright_magenta(self):
    return _wrap("\033[105m", self)


def on_bright_cyan(self):
    return _wrap("\033[106m", self)


def on_bright_white(self):
    return _wrap("\033[107m", self)


def _clamp(value: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(max_value, int(value)))


def on_rgb(self, r: int, g: int, b: int):
    """Apply an RGB 24-bit background color to the string. Example: 'hi'.on_rgb(255,0,0)"""
    # clamp values
    r = _clamp(r, 0, 255)
    g = _clamp(g, 0, 255)
    b = _clamp(b, 0, 255)
    code = f"\033[48;2;{r};{g};{b}m"
    return _wrap(code, self)


def rgb(self, r: int, g: int, b: int):
    """Apply an RGB 24-bit foreground color to the string. Example: 'hi'.rgb(255,0,0)"""
    # clamp values
    r = _clamp(r, 0, 255)
    g = _clamp(g, 0, 255)
    b = _clamp(b, 0, 255)
    code = f"\033[38;2;{r};{g};{b}m"
    return _wrap(code, self)


def color256(self, idx: int):
    idx = _clamp(idx, 0, 255)
    code = f"\033[38;5;{idx}m"
    return _wrap(code, self)


_METHODS = {
    "bold": bold,
    "dim": dim,
    "faint": dim,
    "dark": dim,
    "italic": italic,
    "underline": underline,
    "blink": blink,
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
