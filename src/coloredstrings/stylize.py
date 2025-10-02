import typing
import re


from coloredstrings import ansi_conversions, types


_ESC = "\x1b["
_RESET = _ESC + "0m"


_RE_NESTED_RESET = re.compile(
    rf"({re.escape(_ESC)}0m.*?{re.escape(_ESC)}0m)", flags=re.S
)
_RE_NEWLINE = re.compile(r"(\r?\n)")


def stylize(
    text: str,
    mode: types.ColorMode = types.ColorMode.EXTENDED_256,
    fg: typing.Optional[types.Color] = None,
    bg: typing.Optional[types.Color] = None,
    attrs: typing.Iterable[types.Attribute] = (),
) -> str:
    if mode == types.ColorMode.NO_COLOR:
        return text

    pairs = []
    if fg is not None:
        pairs.append(code_pair(fg, is_bg=False, mode=mode))
    if bg is not None:
        pairs.append(code_pair(bg, is_bg=True, mode=mode))
    pairs.extend(code_pair(a, False, mode) for a in attrs)

    if not pairs:
        return text

    start = "".join(p.start for p in pairs)
    # Close in reverse order to properly nest styles
    end = "".join(p.end for p in reversed(pairs))

    # For robustness: after any specific off-code in the text, re-enable by appending its on code.
    if "\u001b" in text:
        for p in pairs:
            # Replace off with off + on (keep off too - important for some terminals)
            text = text.replace(p.end, p.end + p.start)

    # Also ensure generic RESET re-enables styles (important if text contains \x1b[0m)
    if _RESET in text:
        text = text.replace(_RESET, _RESET + start)

    # Handle nested resets (segment starting+ending with RESET) by wrapping them with start/end
    text = _RE_NESTED_RESET.sub(lambda m: end + m.group(1) + start, text)
    # Close and reopen styles around newlines so styles persist across lines
    text = _RE_NEWLINE.sub(lambda m: end + m.group(1) + start, text)

    return f"{start}{text}{end}"


def code_pair(
    style: typing.Union[types.Attribute, types.Color],
    is_bg: bool = False,
    mode: types.ColorMode = types.ColorMode.EXTENDED_256,
) -> typing.Tuple[str, str]:
    assert mode != types.ColorMode.NO_COLOR

    if isinstance(style, types.Attribute):
        return types.CodePair(
            start=f"{_ESC}{style.value.start}m",
            end=f"{_ESC}{style.value.end}m",
        )

    prefix = "48" if is_bg else "38"

    if isinstance(style, types.Ansi16Color):
        code = (style.as_bg() if is_bg else style.value).start

    elif isinstance(style, types.Extended256):
        if mode == types.ColorMode.ANSI_16:
            v = ansi_conversions.ansi_256_to_ansi_16(style.index)
            code = str(v + 10 if is_bg else v)
        else:
            code = f"{prefix};5;{style.index}"

    elif isinstance(style, types.Rgb):
        if mode == types.ColorMode.TRUE_COLOR:
            code = f"{prefix};2;{style.r};{style.g};{style.b}"
        else:
            v = ansi_conversions.rgb_to_ansi_256(style.r, style.g, style.b)
            if mode == types.ColorMode.ANSI_16:
                v = ansi_conversions.ansi_256_to_ansi_16(v)
                code = str(v + 10 if is_bg else v)
            else:
                code = f"{prefix};5;{v}"

    return types.CodePair(
        start=f"{_ESC}{code}m",
        end=f"{_ESC}{'49' if is_bg else '39'}m",
    )
