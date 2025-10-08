from __future__ import annotations
import typing


from coloredstrings import (
    color_support,
    stylize,
    types,
    utils,
)


class StyleBuilder:
    def __init__(
        self,
        fg: typing.Optional[types.Color] = None,
        bg: typing.Optional[types.Color] = None,
        attrs: typing.Iterable[types.Attribute] = (),
        next_color_for_bg: bool = False,
        mode: typing.Optional[types.ColorMode] = None,
        visible_if_colors: bool = False,
    ) -> None:
        self.fg = fg
        self.bg = bg
        self.attrs = frozenset(attrs)
        self.next_color_for_bg = next_color_for_bg
        self.mode = mode
        self.visible_if_colors = visible_if_colors

    def __call__(
        self,
        *args: typing.Any,
        sep: str = " ",
        mode: typing.Optional[types.ColorMode] = None,
    ) -> str:
        if mode is None:
            if self.mode is not None:
                mode = self.mode
            else:
                mode = color_support.detect_color_support()

        if len(args) == 1 and isinstance(args[0], str):
            text = args[0]
        else:
            text = sep.join(str(a) for a in args)

        return stylize.stylize(
            text, mode, self.fg, self.bg, self.attrs, self.visible_if_colors
        )

    def color_mode(self, mode: types.ColorMode) -> StyleBuilder:
        return StyleBuilder(self.fg, self.bg, self.attrs, self.next_color_for_bg, mode)

    @property
    def on(self) -> StyleBuilder:
        return StyleBuilder(self.fg, self.bg, self.attrs, True, self.mode)

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

    def rgb(
        self,
        color: typing.Union[int, str, typing.Tuple[int, int, int]],
        g: typing.Optional[int] = None,
        b: typing.Optional[int] = None,
    ) -> StyleBuilder:
        """
        Adds RGB color.

        `color` may be:
          - three-component tuple (r, g, b) with 0–255 integers,
          - an int interpreted as 'r' component,
          - or a CSS/hex color string (e.g. '#ff00aa' or 'fuchsia').

        Alternatively call as rgb(r, g, b) by passing `color` as the red component
        and providing `g` and `b` explicitly.

        So, possible calls of this method looks like:
        - `rgb('#f0f8ff')`
        - `rgb(0, 255, 255)`
        - `rgb((127, 255, 212))`
        - `rgb('mediumaquamarine')`

        Note, that `g` and `b` matter only when the first argument has type of `int`.
        Otherwise, they are ignored.
        """
        if isinstance(color, int):
            if g is None or b is None:
                raise ValueError("You must specify 'green' and 'blue' components also")

            rgb = types.Rgb(r=color, g=g, b=b)
        elif isinstance(color, tuple):
            rgb = types.Rgb(r=color[0], g=color[1], b=color[2])
        else:
            rgb = utils.rgb_from_hex_or_named_color(color)
        return self._with_color(rgb)

    def hex(self, color_code: str) -> StyleBuilder:
        return self.rgb(color_code)

    @property
    def reset(self) -> StyleBuilder:
        return self._with_attrs(types.Attribute.RESET)

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
    def strikethrough(self):
        return self.strike

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

    @property
    def visible(self) -> StyleBuilder:
        return StyleBuilder(
            self.fg, self.bg, self.attrs, self.next_color_for_bg, self.mode, True
        )

    def __repr__(self) -> str:
        return f"StyleBuilder(fg={self.fg!r}, bg={self.bg!r}, attrs={set(self.attrs)!r}, on={self.next_color_for_bg})"

    def _with_attrs(self, *attrs: types.Attribute) -> StyleBuilder:
        new_attrs = self.attrs.union(attrs)
        return StyleBuilder(
            self.fg, self.bg, new_attrs, self.next_color_for_bg, self.mode
        )

    def _with_color(
        self, color: typing.Union[types.Ansi16Color, types.Extended256, types.Rgb]
    ) -> StyleBuilder:
        fg = self.fg
        bg = self.bg
        on_flag = self.next_color_for_bg

        if on_flag:
            bg = color
            on_flag = False
        else:
            fg = color

        return StyleBuilder(fg, bg, self.attrs, on_flag, self.mode)
