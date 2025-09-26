from __future__ import annotations
import dataclasses
import enum
import typing
import re


class Attribute(enum.IntEnum):
    BOLD = enum.auto()
    DIM = enum.auto()
    ITALIC = enum.auto()
    UNDERLINE = enum.auto()
    SLOW_BLINK = enum.auto()
    RAPID_BLINK = enum.auto()
    INVERSE = enum.auto()
    HIDDEN = enum.auto()
    STRIKE = enum.auto()


class Color(enum.IntEnum):
    BLACK = enum.auto()
    RED = enum.auto()
    GREEN = enum.auto()
    YELLOW = enum.auto()
    BLUE = enum.auto()
    MAGENTA = enum.auto()
    CYAN = enum.auto()
    WHITE = enum.auto()
    BRIGHT_BLACK = enum.auto()
    BRIGHT_RED = enum.auto()
    BRIGHT_GREEN = enum.auto()
    BRIGHT_YELLOW = enum.auto()
    BRIGHT_BLUE = enum.auto()
    BRIGHT_MAGENTA = enum.auto()
    BRIGHT_CYAN = enum.auto()
    BRIGHT_WHITE = enum.auto()


@dataclasses.dataclass(frozen=True)
class Extended256:
    index: int


@dataclasses.dataclass(frozen=True)
class Rgb:
    r: int
    g: int
    b: int


class StyleBuilder:
    def __init__(
        self,
        fg: typing.Union[Color, Extended256, Rgb, None] = None,
        bg: typing.Union[Color, Extended256, Rgb, None] = None,
        attrs: typing.Iterable[Attribute] | None = None,
        on: bool = False,
    ) -> None:
        self.fg = fg
        self.bg = bg
        self.attrs = frozenset(attrs or ())
        self._on = on

    @property
    def on(self) -> StyleBuilder:
        """Return a new StyleBuilder where the next color call will set the background."""
        return StyleBuilder(self.fg, self.bg, self.attrs, True)

    def with_attrs(self, *attrs: Attribute) -> StyleBuilder:
        """Return a new StyleBuilder with given attributes added."""
        new_attrs = self.attrs.union(attrs)
        return StyleBuilder(self.fg, self.bg, new_attrs, self._on)

    def with_color(self, color: typing.Union[Color, Extended256, Rgb]) -> StyleBuilder:
        """
        Return a new StyleBuilder with color applied.
        If self._on is True, the color will be set to background and _on cleared.
        Otherwise color will be set to foreground.
        Accepts Color, Extended256, or Rgb.
        """
        fg = self.fg
        bg = self.bg
        on_flag = self._on

        if on_flag:
            bg = color
            on_flag = False
        else:
            fg = color

        return StyleBuilder(fg, bg, self.attrs, on_flag)

    @property
    def black(self) -> StyleBuilder:
        return self.with_color(Color.BLACK)

    @property
    def red(self) -> StyleBuilder:
        return self.with_color(Color.RED)

    @property
    def green(self) -> StyleBuilder:
        return self.with_color(Color.GREEN)

    @property
    def yellow(self) -> StyleBuilder:
        return self.with_color(Color.YELLOW)

    @property
    def blue(self) -> StyleBuilder:
        return self.with_color(Color.BLUE)

    @property
    def magenta(self) -> StyleBuilder:
        return self.with_color(Color.MAGENTA)

    @property
    def cyan(self) -> StyleBuilder:
        return self.with_color(Color.CYAN)

    @property
    def white(self) -> StyleBuilder:
        return self.with_color(Color.WHITE)

    @property
    def bright_black(self) -> StyleBuilder:
        return self.with_color(Color.BRIGHT_BLACK)

    @property
    def gray(self) -> StyleBuilder:
        return self.bright_black()

    @property
    def grey(self) -> StyleBuilder:
        return self.bright_black()

    @property
    def bright_red(self) -> StyleBuilder:
        return self.with_color(Color.BRIGHT_RED)

    @property
    def bright_green(self) -> StyleBuilder:
        return self.with_color(Color.BRIGHT_GREEN)

    @property
    def bright_yellow(self) -> StyleBuilder:
        return self.with_color(Color.BRIGHT_YELLOW)

    @property
    def bright_blue(self) -> StyleBuilder:
        return self.with_color(Color.BRIGHT_BLUE)

    @property
    def bright_magenta(self) -> StyleBuilder:
        return self.with_color(Color.BRIGHT_MAGENTA)

    @property
    def bright_cyan(self) -> StyleBuilder:
        return self.with_color(Color.BRIGHT_CYAN)

    @property
    def bright_white(self) -> StyleBuilder:
        return self.with_color(Color.BRIGHT_WHITE)

    def color256(self, index: int) -> StyleBuilder:
        return self.with_color(Extended256(index=index))

    def rgb(self, r: int, g: int, b: int) -> StyleBuilder:
        return self.with_color(Rgb(r=r, g=g, b=b))

    def hex(self, color_code: str) -> StyleBuilder:
        return self.with_color(rgb_from_hex(color_code))

    @property
    def bold(self) -> StyleBuilder:
        return self.with_attrs(Attribute.BOLD)

    @property
    def dim(self) -> StyleBuilder:
        return self.with_attrs(Attribute.DIM)

    @property
    def italic(self) -> StyleBuilder:
        return self.with_attrs(Attribute.ITALIC)

    @property
    def underline(self) -> StyleBuilder:
        return self.with_attrs(Attribute.UNDERLINE)

    @property
    def blink(self) -> StyleBuilder:
        return self.with_attrs(Attribute.SLOW_BLINK)

    @property
    def rapid_blink(self) -> StyleBuilder:
        return self.with_attrs(Attribute.RAPID_BLINK)

    @property
    def inverse(self) -> StyleBuilder:
        return self.with_attrs(Attribute.INVERSE)

    @property
    def hidden(self) -> StyleBuilder:
        return self.with_attrs(Attribute.HIDDEN)

    @property
    def strike(self) -> StyleBuilder:
        return self.with_attrs(Attribute.STRIKE)

    def __repr__(self) -> str:
        return f"StyleBuilder(fg={self.fg!r}, bg={self.bg!r}, attrs={set(self.attrs)!r}, on={self._on})"


def rgb_from_hex(color_code: str) -> Rgb:
    if not isinstance(color_code, str):
        raise TypeError("color_code must be a str")

    s = color_code.strip()

    # Accepted input:
    # '#ffcc00', 'ffcc00', '#FC0', 'fc0', '0xffcc00', '0xFC0'
    if s.lower().startswith("0x"):
        s = s[2:]
    if s.startswith("#"):
        s = s[1:]

    # valid forms: 3 or 6 hex digits
    if not re.fullmatch(r"[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6}", s):
        raise ValueError(
            f"Invalid hex color format: {color_code!r}. "
            "Expected formats: '#RRGGBB', 'RRGGBB', '#RGB', 'RGB', or with '0x' prefix."
        )

    # expand shorthand (e.g. "fc0" -> "ffcc00")
    if len(s) == 3:
        s = "".join(ch * 2 for ch in s)

    r = int(s[0:2], 16)
    g = int(s[2:4], 16)
    b = int(s[4:6], 16)

    return Rgb(r=r, g=g, b=b)


# class Color(enum.IntEnum):
#    No = 0
#    Ansi = 1
#    Extended256 = 2
#    TrueColor = 3
#
#
## def style(
#    text: str,
#    color_mode: ColorMode,
#    fg: typing.Union[Color, Extended256, Rgb, None] = None,
#    bg: typing.Union[Color, Extended256, Rgb, None] = None,
#    attrs: typing.Iterable[Attribute] | None = None,
# ) -> str: ...
#
