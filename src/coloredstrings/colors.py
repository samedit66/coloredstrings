import coloredstrings.style as S


def _stylize(text: str, *args, **kwargs) -> str:
    old_style, just_text = S.parse(text)
    new_style = S.merge(old_style, S.Style(*args, **kwargs))
    return S.apply(new_style, just_text)


def bold(self: str) -> str:
    return _stylize(self, attributes={S.Attribute.BOLD})


def dim(self: str) -> str:
    return _stylize(self, attributes={S.Attribute.DIM})


def italic(self: str) -> str:
    return _stylize(self, attributes={S.Attribute.ITALIC})


def underline(self: str) -> str:
    return _stylize(self, attributes={S.Attribute.UNDERLINE})


def blink(self: str) -> str:
    return _stylize(self, attributes={S.Attribute.SLOW_BLINK})


def rapid_blink(self: str) -> str:
    return _stylize(self, attributes={S.Attribute.RAPID_BLINK})


def inverse(self: str) -> str:
    return _stylize(self, attributes={S.Attribute.INVERSE})


def hidden(self: str) -> str:
    return _stylize(self, attributes={S.Attribute.HIDDEN})


def strike(self: str) -> str:
    return _stylize(self, attributes={S.Attribute.STRIKE})


def red(self: str) -> str:
    return _stylize(self, fore=S.AnsiFore.RED)


def green(self: str) -> str:
    return _stylize(self, fore=S.AnsiFore.GREEN)


def yellow(self: str) -> str:
    return _stylize(self, fore=S.AnsiFore.YELLOW)


def blue(self: str) -> str:
    return _stylize(self, fore=S.AnsiFore.BLUE)


def magenta(self: str) -> str:
    return _stylize(self, fore=S.AnsiFore.MAGENTA)


def cyan(self: str) -> str:
    return _stylize(self, fore=S.AnsiFore.CYAN)


def white(self: str) -> str:
    return _stylize(self, fore=S.AnsiFore.WHITE)


def black(self: str) -> str:
    return _stylize(self, fore=S.AnsiFore.BLACK)


def bright_red(self: str) -> str:
    return _stylize(self, fore=S.AnsiFore.BRIGHT_RED)


def bright_black(self: str) -> str:
    return _stylize(self, fore=S.AnsiFore.BRIGHT_BLACK)


def bright_green(self: str) -> str:
    return _stylize(self, fore=S.AnsiFore.BRIGHT_GREEN)


def bright_yellow(self: str) -> str:
    return _stylize(self, fore=S.AnsiFore.BRIGHT_YELLOW)


def bright_blue(self: str) -> str:
    return _stylize(self, fore=S.AnsiFore.BRIGHT_BLUE)


def bright_magenta(self: str) -> str:
    return _stylize(self, fore=S.AnsiFore.BRIGHT_MAGENTA)


def bright_cyan(self: str) -> str:
    return _stylize(self, fore=S.AnsiFore.BRIGHT_CYAN)


def bright_white(self: str) -> str:
    return _stylize(self, fore=S.AnsiFore.BRIGHT_WHITE)


def on_red(self: str) -> str:
    return _stylize(self, back=S.AnsiBack.RED)


def on_green(self: str) -> str:
    return _stylize(self, back=S.AnsiBack.GREEN)


def on_black(self: str) -> str:
    return _stylize(self, back=S.AnsiBack.BLACK)


def on_white(self: str) -> str:
    return _stylize(self, back=S.AnsiBack.WHITE)


def on_yellow(self: str) -> str:
    return _stylize(self, back=S.AnsiBack.YELLOW)


def on_blue(self: str) -> str:
    return _stylize(self, back=S.AnsiBack.BLUE)


def on_magenta(self: str) -> str:
    return _stylize(self, back=S.AnsiBack.MAGENTA)


def on_cyan(self: str) -> str:
    return _stylize(self, back=S.AnsiBack.CYAN)


def on_bright_black(self: str) -> str:
    return _stylize(self, back=S.AnsiBack.BRIGHT_BLACK)


def on_bright_red(self: str) -> str:
    return _stylize(self, back=S.AnsiBack.BRIGHT_RED)


def on_bright_green(self: str) -> str:
    return _stylize(self, back=S.AnsiBack.BRIGHT_GREEN)


def on_bright_yellow(self: str) -> str:
    return _stylize(self, back=S.AnsiBack.BRIGHT_YELLOW)


def on_bright_blue(self: str) -> str:
    return _stylize(self, back=S.AnsiBack.BRIGHT_BLUE)


def on_bright_magenta(self: str) -> str:
    return _stylize(self, back=S.AnsiBack.BRIGHT_MAGENTA)


def on_bright_cyan(self: str) -> str:
    return _stylize(self, back=S.AnsiBack.BRIGHT_CYAN)


def on_bright_white(self: str) -> str:
    return _stylize(self, back=S.AnsiBack.BRIGHT_WHITE)


def _clamp(value: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(max_value, int(value)))


def on_rgb(self: str, r: int, g: int, b: int) -> str:
    r = _clamp(r, 0, 255)
    g = _clamp(g, 0, 255)
    b = _clamp(b, 0, 255)
    return _stylize(self, back=S.RgbColor(r, g, b))


def rgb(self: str, r: int, g: int, b: int) -> str:
    r = _clamp(r, 0, 255)
    g = _clamp(g, 0, 255)
    b = _clamp(b, 0, 255)
    return _stylize(self, fore=S.RgbColor(r, g, b))


def on_color256(self: str, idx: int) -> str:
    idx = _clamp(idx, 0, 255)
    return _stylize(self, back=S.XColor(idx))


def color256(self: str, idx: int) -> str:
    idx = _clamp(idx, 0, 255)
    return _stylize(self, fore=S.XColor(idx))


def hex(self, hex_color: str) -> str:
    color = S.rgb_from_hex(hex_color)
    return rgb(self, color.r, color.g, color.b)


def on_hex(self, hex_color: str) -> str:
    color = S.rgb_from_hex(hex_color)
    return on_rgb(self, color.r, color.g, color.b)
