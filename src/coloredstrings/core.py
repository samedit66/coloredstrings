import contextlib
import functools


try:
    import forbiddenfruit as ff
except Exception as e:
    raise ImportError(
        "forbiddenfruit is required for this module to patch builtins. "
        "Install it with `pip install forbiddenfruit`."
    ) from e


ANSI = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "italic": "\033[3m",
    "underline": "\033[4m",
    "blink": "\033[5m",
    "inverse": "\033[7m",
    "hidden": "\033[8m",
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bright_black": "\033[90m",
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


def bold(self):
    return _wrap(ANSI["bold"], self)


def dim(self):
    return _wrap(ANSI["dim"], self)


def italic(self):
    return _wrap(ANSI["italic"], self)


def underline(self):
    return _wrap(ANSI["underline"], self)


def inverse(self):
    return _wrap(ANSI["inverse"], self)


def on_red(self):
    return _wrap("\033[41m", self)


def on_green(self):
    return _wrap("\033[42m", self)


def rgb(self, r: int, g: int, b: int):
    """Apply an RGB 24-bit foreground color to the string. Example: 'hi'.rgb(255,0,0)"""
    # clamp values
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))
    code = f"\033[38;2;{r};{g};{b}m"
    return _wrap(code, self)


def color256(self, idx: int):
    idx = max(0, min(255, int(idx)))
    code = f"\033[38;5;{idx}m"
    return _wrap(code, self)


_METHODS = {
    "red": red,
    "green": green,
    "yellow": yellow,
    "blue": blue,
    "magenta": magenta,
    "cyan": cyan,
    "white": white,
    "black": black,
    "bright_red": bright_red,
    "bold": bold,
    "dim": dim,
    "italic": italic,
    "underline": underline,
    "inverse": inverse,
    "on_red": on_red,
    "on_green": on_green,
    "rgb": rgb,
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
    """Attach all color/format methods to built-in `str` but in 
    a limited scoped defined by either a context manager or a function.
    
    Examples:
    ```python
    import coloredstrings

    with coloredstrings.patched():
        print("Error!".red())

    @coloredstrings.patched
    def success():
        print("Success".green())
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