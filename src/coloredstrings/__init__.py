from .style_builder import StyleBuilder
from .types import ColorMode
from .utils import strip_ansi

style = StyleBuilder()

on = style.on

black = style.black
red = style.red
green = style.green
yellow = style.yellow
blue = style.blue
magenta = style.magenta
cyan = style.cyan
white = style.white
bright_black = style.bright_black
gray = bright_black
grey = bright_black
bright_red = style.bright_red
bright_green = style.bright_green
bright_yellow = style.bright_yellow
bright_blue = style.bright_blue
bright_magenta = style.bright_magenta
bright_cyan = style.bright_cyan
bright_white = style.bright_white

reset = style.reset
bold = style.bold
dim = style.dim
faint = style.faint
dark = style.dark
italic = style.italic
underline = style.underline
blink = style.blink
slow_blink = style.slow_blink
rapid_blink = style.rapid_blink
inverse = style.inverse
reverse = style.reverse
hidden = style.hidden
concealed = style.concealed
strike = style.strike
strikethrough = style.strikethrough
framed = style.framed
encircle = style.encircle
circle = style.circle
overline = style.overline
double_underline = style.double_underline
visible = style.visible
link = style.link

color_mode = style.color_mode
color256 = style.color256
rgb = style.rgb

extend = style.extend


def __getattr__(name: str) -> StyleBuilder:
    return style.__getattr__(name)


def __dir__() -> list[str]:
    return __all__


__all__ = [
    "ColorMode",
    "StyleBuilder",
    "black",
    "blink",
    "blue",
    "bold",
    "bright_black",
    "bright_blue",
    "bright_cyan",
    "bright_green",
    "bright_magenta",
    "bright_red",
    "bright_white",
    "bright_yellow",
    "circle",
    "color256",
    "color_mode",
    "concealed",
    "cyan",
    "dark",
    "dim",
    "double_underline",
    "encircle",
    "faint",
    "framed",
    "gray",
    "green",
    "grey",
    "hidden",
    "inverse",
    "italic",
    "link",
    "magenta",
    "on",
    "overline",
    "rapid_blink",
    "red",
    "reset",
    "reverse",
    "rgb",
    "slow_blink",
    "strike",
    "strikethrough",
    "strip_ansi",
    "style",
    "underline",
    "visible",
    "white",
    "yellow",
]
