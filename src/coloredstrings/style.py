from __future__ import annotations
import dataclasses
import enum
import typing


ESC = "\033["
RESET = f"{ESC}0m"


class Attribute(enum.IntEnum):
    BOLD = 1
    DIM = 2
    ITALIC = 3
    UNDERLINE = 4
    SLOW_BLINK = 5
    RAPID_BLINK = 6
    INVERSE = 7
    HIDDEN = 8
    STRIKE = 9


class AnsiFore(enum.IntEnum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    BRIGHT_BLACK = 90
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92
    BRIGHT_YELLOW = 93
    BRIGHT_BLUE = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN = 96
    BRIGHT_WHITE = 97


class AnsiBack(enum.IntEnum):
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47
    BRIGHT_BLACK = 100
    BRIGHT_RED = 101
    BRIGHT_GREEN = 102
    BRIGHT_YELLOW = 103
    BRIGHT_BLUE = 104
    BRIGHT_MAGENTA = 105
    BRIGHT_CYAN = 106
    BRIGHT_WHITE = 107


@dataclasses.dataclass(frozen=True)
class XColor:
    index: int


@dataclasses.dataclass(frozen=True)
class RgbColor:
    r: int
    g: int
    b: int


@dataclasses.dataclass(frozen=True)
class Style:
    attributes: typing.Set[Attribute] = dataclasses.field(default_factory=set)
    fore: typing.Union[AnsiFore | XColor | RgbColor | None] = None
    back: typing.Union[AnsiBack | XColor | RgbColor | None] = None


def apply(style: Style, text: str) -> str:
    params = []

    # attributes: Attribute enum values already map to SGR codes
    params.extend(sorted(int(a) for a in style.attributes))

    # foreground
    if isinstance(style.fore, AnsiFore):
        params.append(int(style.fore))
    elif isinstance(style.fore, XColor):
        # 38;5;{index}
        params.extend([38, 5, style.fore.index])
    elif isinstance(style.fore, RgbColor):
        # 38;2;r;g;b
        params.extend([38, 2, style.fore.r, style.fore.g, style.fore.b])

    # background
    if isinstance(style.back, AnsiBack):
        params.append(int(style.back))
    elif isinstance(style.back, XColor):
        # 48;5;{index}
        params.extend([48, 5, style.back.index])
    elif isinstance(style.back, RgbColor):
        # 48;2;r;g;b
        params.extend([48, 2, style.back.r, style.back.g, style.back.b])

    if not params:
        return text

    opening = f"{ESC}{';'.join(str(p) for p in params)}m"
    return f"{opening}{text}{RESET}"


def merge(s1: Style, s2: Style) -> Style:
    attributes = s1.attributes | s2.attributes
    fore = s2.fore or s1.fore
    back = s2.back or s1.back
    return Style(attributes, fore, back)


def parse(colored_text: str) -> typing.Tuple[Style, str]:
    if not colored_text.startswith(ESC):
        return Style(), colored_text

    # strip the initial ESC[
    rest = colored_text[len(ESC) :]

    # remove trailing resets (0m) occurrences
    while rest.endswith(RESET):
        rest = rest[: -len(RESET)]

    # find the 'm' that ends the SGR parameters
    try:
        m_idx = rest.index("m")
    except ValueError:
        # no 'm' found: not a valid opening SGR - return as-is
        return Style(), colored_text

    codes_part = rest[:m_idx]
    text = rest[m_idx + 1 :]

    if codes_part == "":
        nums: typing.List[int] = []
    else:
        # parse numbers; ignore empty pieces
        nums = [int(s) for s in codes_part.split(";") if s != ""]

    attrs = set()
    fore = None
    back = None

    i = 0
    L = len(nums)
    while i < L:
        n = nums[i]
        # attribute codes 1..9
        if 1 <= n <= 9:
            try:
                attrs.add(Attribute(n))
            except ValueError:
                pass
            i += 1
            continue

        # standard 8/16 colors foreground
        if (30 <= n <= 37) or (90 <= n <= 97):
            try:
                fore = AnsiFore(n)
            except ValueError:
                fore = None
            i += 1
            continue

        # standard 8/16 colors background
        if (40 <= n <= 47) or (100 <= n <= 107):
            try:
                back = AnsiBack(n)
            except ValueError:
                back = None
            i += 1
            continue

        # extended color sequences
        if n == 38 or n == 48:
            # need at least one more token
            if i + 1 >= L:
                break
            mode = nums[i + 1]
            if mode == 5:
                # 38;5;{index} or 48;5;{index}
                if i + 2 < L:
                    idx = nums[i + 2]
                    if n == 38:
                        fore = XColor(idx)
                    else:
                        back = XColor(idx)
                    i += 3
                    continue
                else:
                    break
            elif mode == 2:
                # 38;2;r;g;b or 48;2;r;g;b
                if i + 4 < L:
                    r = nums[i + 2]
                    g = nums[i + 3]
                    b = nums[i + 4]
                    if n == 38:
                        fore = RgbColor(r, g, b)
                    else:
                        back = RgbColor(r, g, b)
                    i += 5
                    continue
                else:
                    break
            else:
                # unknown mode, skip mode token
                i += 2
                continue

        # unknown code: skip
        i += 1

    return Style(attributes=attrs, fore=fore, back=back), text
