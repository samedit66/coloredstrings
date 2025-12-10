from __future__ import annotations

import dataclasses
import warnings
from typing import (
    Any,
    Dict,
    FrozenSet,
    Optional,
    Tuple,
    Union,
)

from coloredstrings import color_support, stylize, types, utils


@dataclasses.dataclass(frozen=True)
class StyleBuilder:
    fg: Optional[types.Color] = None
    """Foreground color."""

    bg: Optional[types.Color] = None
    """Background color."""

    attrs: FrozenSet[types.Attribute] = dataclasses.field(default_factory=frozenset)
    """Styling attributes (bold, italic, etc.)."""

    next_color_for_bg: bool = False
    """Whether the next `color` method should be treated as setting the background color."""

    mode: types.ColorMode = dataclasses.field(
        default_factory=color_support.detect_color_support
    )
    """Color mode."""

    only_visible_if_colors_enabled: bool = False
    """Used for `visible` style: whether the text should be replaced with an empty string when colors are not available."""

    # This annotation hurts me very much...
    extensions: Dict[str, Union[str, Tuple[int, int, int], StyleBuilder]] = (
        dataclasses.field(default_factory=dict)
    )
    """User-defined extension styles."""

    url: Optional[str] = None
    """URL address for `link` style."""

    def __call__(
        self,
        *args: Any,
        sep: str = " ",
        mode: Optional[types.ColorMode] = None,
    ) -> str:
        if mode is None:
            mode = self.mode

        text = sep.join(str(a) for a in args)
        return stylize.stylize(
            text=text,
            mode=mode,
            fg=self.fg,
            bg=self.bg,
            attrs=self.attrs,
            only_visible_if_colors_enabled=self.only_visible_if_colors_enabled,
            url=self.url,
        )

    def color_mode(self, mode: types.ColorMode) -> StyleBuilder:
        return dataclasses.replace(self, mode=mode)

    @property
    def on(self) -> StyleBuilder:
        return dataclasses.replace(self, next_color_for_bg=True)

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
        color: Union[int, str, Tuple[int, int, int]],
        g: Optional[int] = None,
        b: Optional[int] = None,
    ) -> StyleBuilder:
        """
        Adds RGB color.

        Possible calls of this method looks like:
        - `rgb('#f0f8ff')`
        - `rgb(0, 255, 255)`
        - `rgb((127, 255, 212))`
        - `rgb('mediumaquamarine')`

        Note, that `g` and `b` matter only when the first argument has type of `int`.
        Otherwise, they are ignored.

        Parameters
        ----------
        color : Union[int, str, Tuple[int, int, int]]
            One of:
            - a three-component tuple `(r, g, b)` with integer components in 0–255,
            - an `int` interpreted as the red component (in this case `g` and `b`
              must be supplied),
            - a CSS/hex color string (for example `'#ff00aa'`, `'fuchsia'`, or
              other CSS named colors).
        g : Optional[int]
            Green component when `color` is provided as an `int`. Ignored otherwise.
        b : Optional[int]
            Blue component when `color` is provided as an `int`. Ignored otherwise.

        Returns
        -------
        StyleBuilder
            A new StyleBuilder instance with the specified RGB color applied.

        Raises
        ------
        ValueError
            If `color` is an `int` but either `g` or `b` is not provided.
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

    def __getattr__(self, color: str) -> StyleBuilder:
        """
        Treat unknown attributes as colors or registered extensions.

        Lookup order:
        1. If `self.extensions` contains `color`, use that value:
           - `str` or `tuple` -> forwarded to `rgb` and returns a StyleBuilder.
           - `callable` -> returned as-is (allowing custom helpers).
        2. Otherwise treat `color` as a CSS/named/hex color and return `self.rgb(color)`.

        Notes
        -----
        - Attribute names must be valid Python identifiers; use :meth:`rgb` for
          names containing characters like `#`.
        - Registered callables should accept the same kinds of arguments as other
          style helpers if you plan to call them directly.

        Example
        -------
        >>> s = StyleBuilder().extend(primary='blue', shout=StyleBuilder().red.bold)
        >>> s.primary('ok')   # -> styled via rgb('blue')
        >>> s.shout('hey')    # -> calls the registered callable
        """
        possible_extension = (self.extensions or {}).get(color)
        if possible_extension is not None:
            if isinstance(possible_extension, (str, tuple)):
                return self.rgb(possible_extension)
            return possible_extension

        return self.rgb(color)

    def hex(self, color_code: str) -> StyleBuilder:
        warnings.warn(
            "`hex` is deprecated. Use `rgb` instead.", DeprecationWarning, stacklevel=2
        )
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
        return dataclasses.replace(self, only_visible_if_colors_enabled=True)

    def link(self, url: str) -> StyleBuilder:
        return dataclasses.replace(self, url=url)

    def extend(
        self,
        style_dict: Optional[
            Dict[str, Union[str, Tuple[int, int, int], StyleBuilder]]
        ] = None,
        **styles,
    ) -> StyleBuilder:
        """
        Extends `StyleBuilder` with new styles.

        Example:

        ```python
        from coloredstrings import StyleBuilder

        # Let's make a Bootstrap-like colored scheme
        style = StyleBuilder()
        style = style.extends(
            primary="blue",
            secondary=(169, 169, 169),
            success=style.green,
        )

        print(style.success("Complete!"))
        ```

        Parameters
        ----------
        style_dict :
            Optional dict of style-name -> color. Colors can be CSS/named
            strings (e.g. `'fuchsia'` or `'#ff00aa'`), RGB tuples like (r, g, b)
            or `StyleBuilder` instances.
        **styles :
            Additional styles provided as keyword arguments (same value types
            as ``style_dict``).

        Returns
        -------
        StyleBuilder
            A new `StyleBuilder` instance with the merged extensions.
        """
        return dataclasses.replace(
            self,
            extensions={
                **self.extensions,
                **(style_dict or {}),
                **styles,
            },
        )

    def _with_attrs(self, *attrs: types.Attribute) -> StyleBuilder:
        return dataclasses.replace(self, attrs=self.attrs.union(attrs))

    def _with_color(
        self, color: Union[types.Ansi16Color, types.Extended256, types.Rgb]
    ) -> StyleBuilder:
        fg = self.fg
        bg = self.bg
        next_color_for_bg = self.next_color_for_bg

        if next_color_for_bg:
            bg = color
            next_color_for_bg = False
        else:
            fg = color

        return dataclasses.replace(
            self, fg=fg, bg=bg, next_color_for_bg=next_color_for_bg
        )
