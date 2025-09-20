import contextlib
import functools

import forbiddenfruit as ff

from coloredstrings import colors


_METHODS = {
    "bold": colors.bold,
    "dim": colors.dim,
    "faint": colors.dim,
    "dark": colors.dim,
    "italic": colors.italic,
    "underline": colors.underline,
    "blink": colors.blink,
    "slow_blink": colors.blink,
    "rapid_blink": colors.rapid_blink,
    "reverse": colors.inverse,
    "inverse": colors.inverse,
    "hidden": colors.hidden,
    "concealed": colors.hidden,
    "password": colors.hidden,
    "strike": colors.strike,
    "red": colors.red,
    "green": colors.green,
    "yellow": colors.yellow,
    "blue": colors.blue,
    "magenta": colors.magenta,
    "cyan": colors.cyan,
    "white": colors.white,
    "black": colors.black,
    "bright_black": colors.bright_black,
    "bright_red": colors.bright_red,
    "bright_green": colors.bright_green,
    "bright_yellow": colors.bright_yellow,
    "bright_blue": colors.bright_blue,
    "bright_magenta": colors.bright_magenta,
    "bright_cyan": colors.bright_cyan,
    "bright_white": colors.bright_white,
    "on_black": colors.on_black,
    "on_gray": colors.on_black,
    "on_grey": colors.on_black,
    "on_red": colors.on_red,
    "on_green": colors.on_green,
    "on_yellow": colors.on_yellow,
    "on_blue": colors.on_blue,
    "on_magenta": colors.on_magenta,
    "on_cyan": colors.on_cyan,
    "on_white": colors.on_white,
    "on_bright_black": colors.on_bright_black,
    "on_bright_grey": colors.on_bright_black,
    "on_bright_gray": colors.on_bright_black,
    "on_bright_red": colors.on_bright_red,
    "on_bright_green": colors.on_bright_green,
    "on_bright_yellow": colors.on_bright_yellow,
    "on_bright_blue": colors.on_bright_blue,
    "on_bright_magenta": colors.on_bright_magenta,
    "on_bright_cyan": colors.on_bright_cyan,
    "on_bright_white": colors.on_bright_white,
    "rgb": colors.rgb,
    "on_rgb": colors.on_rgb,
    "color256": colors.color256,
    "on_color256": colors.on_color256,
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
