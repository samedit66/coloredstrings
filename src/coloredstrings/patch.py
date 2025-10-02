import contextlib
import typing
import functools
import itertools

from coloredstrings import (
    stylize,
    types,
    style_builder,
)


try:
    import forbiddenfruit as ff
except Exception as exc:
    raise ImportError(
        "'forbiddenfruit' is required to enable chaining on "
        'str objects (e.g. "Hello".blue.on.green).\n\n'
        "Please install it using one of these options:\n"
        "- pip install forbiddenfruit\n"
        "- uv add forbiddenfruit\n"
        "- or install the patched bundle: pip install 'coloredstrings[patched]'\n\n"
    ) from exc


def _apply(
    self: str,
    *,
    fg: typing.Optional[types.Color] = None,
    bg: typing.Optional[types.Color] = None,
    attrs: typing.Iterable[types.Attribute] = (),
) -> str:
    return stylize.stylize(self, None, fg, bg, attrs)


# Attribute painters
def bold(self: str) -> str:
    return _apply(self, attrs=[types.Attribute.BOLD])


def dim(self: str) -> str:
    return _apply(self, attrs=[types.Attribute.DIM])


def italic(self: str) -> str:
    return _apply(self, attrs=[types.Attribute.ITALIC])


def underline(self: str) -> str:
    return _apply(self, attrs=[types.Attribute.UNDERLINE])


def blink(self: str) -> str:
    return _apply(self, attrs=[types.Attribute.SLOW_BLINK])


def rapid_blink(self: str) -> str:
    return _apply(self, attrs=[types.Attribute.RAPID_BLINK])


def inverse(self: str) -> str:
    return _apply(self, attrs=[types.Attribute.INVERSE])


def hidden(self: str) -> str:
    return _apply(self, attrs=[types.Attribute.HIDDEN])


def strike(self: str) -> str:
    return _apply(self, attrs=[types.Attribute.STRIKE])


# 16-color foreground helpers
def red(self: str) -> str:
    return _apply(self, fg=types.Ansi16Color.RED)


def green(self: str) -> str:
    return _apply(self, fg=types.Ansi16Color.GREEN)


def yellow(self: str) -> str:
    return _apply(self, fg=types.Ansi16Color.YELLOW)


def blue(self: str) -> str:
    return _apply(self, fg=types.Ansi16Color.BLUE)


def magenta(self: str) -> str:
    return _apply(self, fg=types.Ansi16Color.MAGENTA)


def cyan(self: str) -> str:
    return _apply(self, fg=types.Ansi16Color.CYAN)


def white(self: str) -> str:
    return _apply(self, fg=types.Ansi16Color.WHITE)


def black(self: str) -> str:
    return _apply(self, fg=types.Ansi16Color.BLACK)


def bright_red(self: str) -> str:
    return _apply(self, fg=types.Ansi16Color.BRIGHT_RED)


def bright_black(self: str) -> str:
    return _apply(self, fg=types.Ansi16Color.BRIGHT_BLACK)


def bright_green(self: str) -> str:
    return _apply(self, fg=types.Ansi16Color.BRIGHT_GREEN)


def bright_yellow(self: str) -> str:
    return _apply(self, fg=types.Ansi16Color.BRIGHT_YELLOW)


def bright_blue(self: str) -> str:
    return _apply(self, fg=types.Ansi16Color.BRIGHT_BLUE)


def bright_magenta(self: str) -> str:
    return _apply(self, fg=types.Ansi16Color.BRIGHT_MAGENTA)


def bright_cyan(self: str) -> str:
    return _apply(self, fg=types.Ansi16Color.BRIGHT_CYAN)


def bright_white(self: str) -> str:
    return _apply(self, fg=types.Ansi16Color.BRIGHT_WHITE)


# Extended foreground helpers
def rgb(self: str, r: int, g: int, b: int) -> str:
    return _apply(self, fg=types.Rgb(r=r, g=g, b=b))


def color256(self: str, idx: int) -> str:
    return _apply(self, fg=types.Extended256(index=idx))


def hex(self: str, hex_color: str) -> str:
    color = style_builder.rgb_from_hex(hex_color)
    return rgb(self, color.r, color.g, color.b)


# background painters
def on_red(self: str) -> str:
    return _apply(self, bg=types.Ansi16Color.RED)


def on_green(self: str) -> str:
    return _apply(self, bg=types.Ansi16Color.GREEN)


def on_yellow(self: str) -> str:
    return _apply(self, bg=types.Ansi16Color.YELLOW)


def on_blue(self: str) -> str:
    return _apply(self, bg=types.Ansi16Color.BLUE)


def on_magenta(self: str) -> str:
    return _apply(self, bg=types.Ansi16Color.MAGENTA)


def on_cyan(self: str) -> str:
    return _apply(self, bg=types.Ansi16Color.CYAN)


def on_white(self: str) -> str:
    return _apply(self, bg=types.Ansi16Color.WHITE)


def on_black(self: str) -> str:
    return _apply(self, bg=types.Ansi16Color.BLACK)


def on_bright_red(self: str) -> str:
    return _apply(self, bg=types.Ansi16Color.BRIGHT_RED)


def on_bright_black(self: str) -> str:
    return _apply(self, bg=types.Ansi16Color.BRIGHT_BLACK)


def on_bright_green(self: str) -> str:
    return _apply(self, bg=types.Ansi16Color.BRIGHT_GREEN)


def on_bright_yellow(self: str) -> str:
    return _apply(self, bg=types.Ansi16Color.BRIGHT_YELLOW)


def on_bright_blue(self: str) -> str:
    return _apply(self, bg=types.Ansi16Color.BRIGHT_BLUE)


def on_bright_magenta(self: str) -> str:
    return _apply(self, bg=types.Ansi16Color.BRIGHT_MAGENTA)


def on_bright_cyan(self: str) -> str:
    return _apply(self, bg=types.Ansi16Color.BRIGHT_CYAN)


def on_bright_white(self: str) -> str:
    return _apply(self, bg=types.Ansi16Color.BRIGHT_WHITE)


# Extended background painters
def on_rgb(self: str, r: int, g: int, b: int) -> str:
    return _apply(self, bg=types.Rgb(r=r, g=g, b=b))


def on_color256(self: str, idx: int) -> str:
    return _apply(self, bg=types.Extended256(index=idx))


def on_hex(self: str, hex_color: str) -> str:
    color = style_builder.rgb_from_hex(hex_color)
    return on_rgb(self, color.r, color.g, color.b)


_PROPERTIES = {
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
    "strike": strike,
    "red": red,
    "green": green,
    "yellow": yellow,
    "blue": blue,
    "magenta": magenta,
    "cyan": cyan,
    "white": white,
    "black": black,
    "grey": bright_black,
    "gray": bright_black,
    "bright_black": bright_black,
    "bright_red": bright_red,
    "bright_green": bright_green,
    "bright_yellow": bright_yellow,
    "bright_blue": bright_blue,
    "bright_magenta": bright_magenta,
    "bright_cyan": bright_cyan,
    "bright_white": bright_white,
    "on_red": on_red,
    "on_green": on_green,
    "on_yellow": on_yellow,
    "on_blue": on_blue,
    "on_magenta": on_magenta,
    "on_cyan": on_cyan,
    "on_white": on_white,
    "on_black": on_black,
    "on_bright_red": on_bright_red,
    "on_bright_black": on_bright_black,
    "on_bright_green": on_bright_green,
    "on_bright_yellow": on_bright_yellow,
    "on_bright_blue": on_bright_blue,
    "on_bright_magenta": on_bright_magenta,
    "on_bright_cyan": on_bright_cyan,
    "on_bright_white": on_bright_white,
}


_METHODS = {
    "rgb": rgb,
    "color256": color256,
    "hex": hex,
    "on_rgb": on_rgb,
    "on_color256": on_color256,
    "on_hex": on_hex,
}


def patch_strings():
    """Attach all color/format methods to built-in `str`."""
    for name, func in _PROPERTIES.items():
        ff.curse(str, name, property(func))
    for name, func in _METHODS.items():
        ff.curse(str, name, func)


def unpatch_strings():
    """Remove the added methods from `str`"""
    for name in itertools.chain(_PROPERTIES.keys(), _METHODS.keys()):
        ff.reverse(str, name)


def colored_strings(func=None):
    """Attach all color/format methods to built-in `str` in a limited scope.

    Examples:
    ```python
    from coloredstrings.patch import colored_strings

    # Patched `str` methods are available only within the context
    def warn(msg: str) -> None:
        with colored_strings():
            print("warning:".yellow.bold, msg)

    # Same idea, but using a decorator
    @colored_strings
    def info(msg: str) -> None:
        print("[info]:".blue, msg)
    ```
    """
    if func is None:

        @contextlib.contextmanager
        def _cm():
            patch_strings()
            try:
                yield
            finally:
                unpatch_strings()

        return _cm()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        patch_strings()
        try:
            return func(*args, **kwargs)
        finally:
            unpatch_strings()

    return wrapper
