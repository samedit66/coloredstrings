from __future__ import annotations
import typing
import re


from coloredstrings import (
    color_support,
    stylize,
    types,
)


class StyleBuilder:
    def __init__(
        self,
        fg: typing.Optional[types.Color] = None,
        bg: typing.Optional[types.Color] = None,
        attrs: typing.Iterable[types.Attribute] = (),
        on: bool = False,
        default_mode: typing.Optional[types.ColorMode] = None,
    ) -> None:
        self.fg = fg
        self.bg = bg
        self.attrs = frozenset(attrs)
        self._on = on
        self._default_mode = default_mode

    def __call__(
        self,
        *args: typing.Any,
        sep: str = " ",
        mode: typing.Optional[types.ColorMode] = None,
    ) -> str:
        if mode is None:
            if self._default_mode is not None:
                mode = self._default_mode
            else:
                mode = color_support.detect_color_support()

        if len(args) == 1 and isinstance(args[0], str):
            text = args[0]
        else:
            text = sep.join(str(a) for a in args)

        return stylize.stylize(text, mode, self.fg, self.bg, self.attrs)

    def color_mode(self, mode: types.ColorMode) -> StyleBuilder:
        return StyleBuilder(self.fg, self.bg, self.attrs, self._on, mode)

    @property
    def on(self) -> StyleBuilder:
        return StyleBuilder(self.fg, self.bg, self.attrs, True, self._default_mode)

    @property
    def black(self) -> StyleBuilder:
        return self._with_color(types.Ansi16Color.BLACK)

    @property
    def red(self) -> StyleBuilder:
        return self._with_color(types.Ansi16Color.RED)

    @property
    def green(self) -> StyleBuilder:
        return self._with_color(types.Ansi16Color.GREEN)

    @property
    def yellow(self) -> StyleBuilder:
        return self._with_color(types.Ansi16Color.YELLOW)

    @property
    def blue(self) -> StyleBuilder:
        return self._with_color(types.Ansi16Color.BLUE)

    @property
    def magenta(self) -> StyleBuilder:
        return self._with_color(types.Ansi16Color.MAGENTA)

    @property
    def cyan(self) -> StyleBuilder:
        return self._with_color(types.Ansi16Color.CYAN)

    @property
    def white(self) -> StyleBuilder:
        return self._with_color(types.Ansi16Color.WHITE)

    @property
    def bright_black(self) -> StyleBuilder:
        return self._with_color(types.Ansi16Color.BRIGHT_BLACK)

    @property
    def gray(self) -> StyleBuilder:
        return self.bright_black

    @property
    def grey(self) -> StyleBuilder:
        return self.bright_black

    @property
    def bright_red(self) -> StyleBuilder:
        return self._with_color(types.Ansi16Color.BRIGHT_RED)

    @property
    def bright_green(self) -> StyleBuilder:
        return self._with_color(types.Ansi16Color.BRIGHT_GREEN)

    @property
    def bright_yellow(self) -> StyleBuilder:
        return self._with_color(types.Ansi16Color.BRIGHT_YELLOW)

    @property
    def bright_blue(self) -> StyleBuilder:
        return self._with_color(types.Ansi16Color.BRIGHT_BLUE)

    @property
    def bright_magenta(self) -> StyleBuilder:
        return self._with_color(types.Ansi16Color.BRIGHT_MAGENTA)

    @property
    def bright_cyan(self) -> StyleBuilder:
        return self._with_color(types.Ansi16Color.BRIGHT_CYAN)

    @property
    def bright_white(self) -> StyleBuilder:
        return self._with_color(types.Ansi16Color.BRIGHT_WHITE)

    def color256(self, index: int) -> StyleBuilder:
        return self._with_color(types.Extended256(index=index))

    def rgb(self, r: int, g: int, b: int) -> StyleBuilder:
        return self._with_color(types.Rgb(r=r, g=g, b=b))

    def hex(self, color_code: str) -> StyleBuilder:
        return self._with_color(rgb_from_hex(color_code))

    @property
    def bold(self) -> StyleBuilder:
        return self._with_attrs(types.Attribute.BOLD)

    @property
    def dim(self) -> StyleBuilder:
        return self._with_attrs(types.Attribute.DIM)

    @property
    def faint(self) -> StyleBuilder:
        return self.dim

    @property
    def dark(self) -> StyleBuilder:
        return self.dim

    @property
    def italic(self) -> StyleBuilder:
        return self._with_attrs(types.Attribute.ITALIC)

    @property
    def underline(self) -> StyleBuilder:
        return self._with_attrs(types.Attribute.UNDERLINE)

    @property
    def blink(self) -> StyleBuilder:
        return self._with_attrs(types.Attribute.SLOW_BLINK)

    @property
    def slow_blink(self) -> StyleBuilder:
        return self.blink

    @property
    def rapid_blink(self) -> StyleBuilder:
        return self._with_attrs(types.Attribute.RAPID_BLINK)

    @property
    def inverse(self) -> StyleBuilder:
        return self._with_attrs(types.Attribute.INVERSE)

    @property
    def reverse(self) -> StyleBuilder:
        return self.inverse

    @property
    def hidden(self) -> StyleBuilder:
        return self._with_attrs(types.Attribute.HIDDEN)

    @property
    def concealed(self) -> StyleBuilder:
        return self.hidden

    @property
    def strike(self) -> StyleBuilder:
        return self._with_attrs(types.Attribute.STRIKE)

    @property
    def framed(self) -> StyleBuilder:
        return self._with_attrs(types.Attribute.FRAMED)

    @property
    def encircle(self) -> StyleBuilder:
        return self._with_attrs(types.Attribute.ENCIRCLE)

    @property
    def circle(self) -> StyleBuilder:
        return self.encircle

    @property
    def overline(self) -> StyleBuilder:
        return self._with_attrs(types.Attribute.OVERLINE)

    @property
    def double_underline(self) -> StyleBuilder:
        return self._with_attrs(types.Attribute.DOUBLE_UNDERLINE)

    def __repr__(self) -> str:
        return f"StyleBuilder(fg={self.fg!r}, bg={self.bg!r}, attrs={set(self.attrs)!r}, on={self._on})"

    def _with_attrs(self, *attrs: types.Attribute) -> StyleBuilder:
        new_attrs = self.attrs.union(attrs)
        return StyleBuilder(self.fg, self.bg, new_attrs, self._on, self._default_mode)

    def _with_color(
        self, color: typing.Union[types.Ansi16Color, types.Extended256, types.Rgb]
    ) -> StyleBuilder:
        fg = self.fg
        bg = self.bg
        on_flag = self._on

        if on_flag:
            bg = color
            on_flag = False
        else:
            fg = color

        return StyleBuilder(fg, bg, self.attrs, on_flag, self._default_mode)


def rgb_from_hex(hex_code: str) -> types.Rgb:
    s = hex_code.strip()

    # Accepted input:
    # '#ffcc00', 'ffcc00', '#FC0', 'fc0', '0xffcc00', '0xFC0'
    if s.lower().startswith("0x"):
        s = s[2:]
    if s.startswith("#"):
        s = s[1:]

    # valid forms: 3 or 6 hex digits
    if not re.fullmatch(r"[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6}", s):
        raise ValueError(
            f"Invalid hex color format: {hex_code!r}. "
            "Expected formats: '#RRGGBB', 'RRGGBB', '#RGB', 'RGB', or with '0x' prefix."
        )

    # expand shorthand (e.g. 'fc0' -> 'ffcc00')
    if len(s) == 3:
        s = "".join(ch * 2 for ch in s)

    r = int(s[0:2], 16)
    g = int(s[2:4], 16)
    b = int(s[4:6], 16)

    return types.Rgb(r=r, g=g, b=b)
