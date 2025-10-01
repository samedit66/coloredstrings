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


_BACKGROUND_MARKER = "__on__"


def _get_on(self: str) -> bool:
    return bool(getattr(self, _BACKGROUND_MARKER, False))


def _set_on(self: str, value: bool) -> None:
    setattr(self, _BACKGROUND_MARKER, bool(value))


def _apply(
    self: str,
    *,
    fg: typing.Optional[types.Color] = None,
    bg: typing.Optional[types.Color] = None,
    attrs: typing.Iterable[types.Attribute] = (),
) -> str:
    on_flag = _get_on(self)
    if on_flag and fg is not None and bg is None:
        bg = fg
        fg = None

    result = stylize.stylize(self, None, fg, bg, tuple(attrs))

    _set_on(self, False)
    return result


def on(self: str) -> str:
    _set_on(self, True)
    return self


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


# 16-color helpers
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


# Extended color helpers
def rgb(self: str, r: int, g: int, b: int) -> str:
    return _apply(self, fg=types.Rgb(r=r, g=g, b=b))


def color256(self: str, idx: int) -> str:
    return _apply(self, fg=types.Extended256(index=idx))


def hex(self: str, hex_color: str) -> str:
    color = style_builder.rgb_from_hex(hex_color)
    return rgb(self, color.r, color.g, color.b)


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
    "on": on,
}


_METHODS = {
    "rgb": rgb,
    "color256": color256,
    "hex": hex,
}


def patch():
    """Attach all color/format methods to built-in `str`."""
    ff.curse(str, _BACKGROUND_MARKER, False)
    for name, func in _PROPERTIES.items():
        ff.curse(str, name, property(func))
    for name, func in _METHODS.items():
        ff.curse(str, name, func)


def unpatch():
    """Remove the added methods from `str`"""
    ff.reverse(str, _BACKGROUND_MARKER)
    for name in itertools.chain(_PROPERTIES.keys(), _METHODS.keys()):
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
