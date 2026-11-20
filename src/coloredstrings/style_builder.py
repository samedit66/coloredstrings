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
        """Select an RGB color by name, hex string, tuple, or three integers.

        Components must be integers from 0 through 255. The optional green
        and blue arguments are used only with an integer first argument.
        """
        if isinstance(color, int):
            if g is None or b is None:
                raise ValueError("You must specify 'green' and 'blue' components also")

            rgb = types.Rgb(r=color, g=g, b=b)
        elif isinstance(color, tuple):
            if len(color) != 3:
                raise ValueError("An RGB tuple must contain exactly three components")
            rgb = types.Rgb(*color)
        elif isinstance(color, str):
            rgb = utils.rgb_from_hex_or_named_color(color)
        else:
            raise TypeError("Expected an RGB tuple, a color string, or three integers")
        return self._with_color(rgb)

    def __getattr__(self, color: str) -> StyleBuilder:
        """Resolve a theme extension or a named color in the current chain."""
        extensions = object.__getattribute__(self, "extensions")
        extension = extensions.get(color)
        if isinstance(extension, StyleBuilder):
            style = self
            if extension.fg is not None:
                style = style._with_color(extension.fg)
            return dataclasses.replace(
                style,
                bg=extension.bg if extension.bg is not None else style.bg,
                attrs=style.attrs | extension.attrs,
                next_color_for_bg=extension.next_color_for_bg
                or style.next_color_for_bg,
                only_visible_if_colors_enabled=(
                    style.only_visible_if_colors_enabled
                    or extension.only_visible_if_colors_enabled
                ),
                url=extension.url if extension.url is not None else style.url,
                extensions={**extension.extensions, **extensions},
            )
        if isinstance(extension, (str, tuple)):
            return self.rgb(extension)
        if extension is not None:
            return extension
        try:
            return self.rgb(color)
        except ValueError:
            raise AttributeError(color) from None

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
        style = style.extend(
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
