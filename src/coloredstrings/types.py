import dataclasses
import enum
import typing


@dataclasses.dataclass(frozen=True)
class Ansi16Code:
    start: int
    end: int


class Attribute(enum.Enum):
    """
    ANSI escape codes for text attributes.
    Support for these attributes varies across terminals.

    BOLD: Widely supported.
    DIM: Generally supported, sometimes appears as bold or not supported on older terminals.
    ITALIC: Support varies; many terminals do not render italics.
    UNDERLINE: Widely supported.
    SLOW_BLINK: Widely supported, but can be ignored or rendered as a steady color on some terminals.
    RAPID_BLINK: Less supported than slow blink, often rendered as slow blink or steady.
    INVERSE: Widely supported.
    HIDDEN: Widely supported, but some terminals might just display black text.
    STRIKE: Support varies; many terminals do not render strikethrough.
    DOUBLE_UNDERLINE: Support varies, often rendered as single underline or not at all.
    FRAMED: Support varies; less common.
    ENCIRCLE: Support varies; less common.
    OVERLINE: Support varies; less common.
    """

    BOLD = Ansi16Code(1, 22)
    DIM = Ansi16Code(2, 22)
    ITALIC = Ansi16Code(3, 23)
    UNDERLINE = Ansi16Code(4, 24)
    SLOW_BLINK = Ansi16Code(5, 25)
    RAPID_BLINK = Ansi16Code(6, 25)
    INVERSE = Ansi16Code(7, 27)
    HIDDEN = Ansi16Code(8, 28)
    STRIKE = Ansi16Code(9, 29)
    DOUBLE_UNDERLINE = Ansi16Code(21, 24)
    FRAMED = Ansi16Code(51, 54)
    ENCIRCLE = Ansi16Code(52, 54)
    OVERLINE = Ansi16Code(53, 55)


FG_RESET = 39
BG_RESET = 49


class Ansi16Color(enum.Enum):
    BLACK = Ansi16Code(30, FG_RESET)
    RED = Ansi16Code(31, FG_RESET)
    GREEN = Ansi16Code(32, FG_RESET)
    YELLOW = Ansi16Code(33, FG_RESET)
    BLUE = Ansi16Code(34, FG_RESET)
    MAGENTA = Ansi16Code(35, FG_RESET)
    CYAN = Ansi16Code(36, FG_RESET)
    WHITE = Ansi16Code(37, FG_RESET)
    BRIGHT_BLACK = Ansi16Code(90, FG_RESET)
    BRIGHT_RED = Ansi16Code(91, FG_RESET)
    BRIGHT_GREEN = Ansi16Code(92, FG_RESET)
    BRIGHT_YELLOW = Ansi16Code(93, FG_RESET)
    BRIGHT_BLUE = Ansi16Code(94, FG_RESET)
    BRIGHT_MAGENTA = Ansi16Code(95, FG_RESET)
    BRIGHT_CYAN = Ansi16Code(96, FG_RESET)
    BRIGHT_WHITE = Ansi16Code(97, FG_RESET)

    def as_bg(self) -> Ansi16Code:
        return Ansi16Code(self.value.start + 10, BG_RESET)


@dataclasses.dataclass(frozen=True)
class Extended256:
    index: int


@dataclasses.dataclass(frozen=True)
class Rgb:
    r: int
    g: int
    b: int


Color = typing.Union[Ansi16Color, Extended256, Rgb]


class ColorMode(enum.IntEnum):
    NO_COLOR = 0
    ANSI_16 = 1
    EXTENDED_256 = 2
    TRUE_COLOR = 3


@dataclasses.dataclass(frozen=True)
class CodePair:
    start: str
    end: str
