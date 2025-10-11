"""
The tests below are a direct port of the tests found in https://github.com/bluenote10/yachalk/blob/master/tests/test_chalk.py.
"""

import pytest
from helper import r

from coloredstrings import ColorMode, StyleBuilder


@pytest.fixture
def style() -> StyleBuilder:
    return StyleBuilder(mode=ColorMode.ANSI_16)


def test_empty_str(style: StyleBuilder) -> None:
    assert style.red("") == ""


def test_visible(style: StyleBuilder) -> None:
    # When visible and some colors are enabled, return just the text
    assert r(style.visible("foo", mode=ColorMode.ANSI_16)) == r("foo")
    assert r(style.red.visible("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[31mfoo\x1b[39m"
    )

    # When no colors are enabled and the text is marked as visible, nothing is returned
    no_colors = style.color_mode(mode=ColorMode.NO_COLOR)
    assert r(no_colors.visible("foo")) == r("")
    assert r(no_colors.red.visible("foo")) == r("")


def test_reset(style: StyleBuilder) -> None:
    assert style.reset() == "\x1b[0m"


def test_basics(style: StyleBuilder) -> None:
    # attributes (ANSI 16 mode for deterministic codes)
    assert r(style.bold("foo", mode=ColorMode.ANSI_16)) == r("\x1b[1mfoo\x1b[22m")
    assert r(style.dim("foo", mode=ColorMode.ANSI_16)) == r("\x1b[2mfoo\x1b[22m")
    assert r(style.italic("foo", mode=ColorMode.ANSI_16)) == r("\x1b[3mfoo\x1b[23m")
    assert r(style.underline("foo", mode=ColorMode.ANSI_16)) == r("\x1b[4mfoo\x1b[24m")
    assert r(style.overline("foo", mode=ColorMode.ANSI_16)) == r("\x1b[53mfoo\x1b[55m")
    assert r(style.hidden("foo", mode=ColorMode.ANSI_16)) == r("\x1b[8mfoo\x1b[28m")
    assert r(style.strike("foo", mode=ColorMode.ANSI_16)) == r("\x1b[9mfoo\x1b[29m")

    # 16-color foregrounds
    assert r(style.black("foo", mode=ColorMode.ANSI_16)) == r("\x1b[30mfoo\x1b[39m")
    assert r(style.red("foo", mode=ColorMode.ANSI_16)) == r("\x1b[31mfoo\x1b[39m")
    assert r(style.green("foo", mode=ColorMode.ANSI_16)) == r("\x1b[32mfoo\x1b[39m")
    assert r(style.yellow("foo", mode=ColorMode.ANSI_16)) == r("\x1b[33mfoo\x1b[39m")
    assert r(style.blue("foo", mode=ColorMode.ANSI_16)) == r("\x1b[34mfoo\x1b[39m")
    assert r(style.magenta("foo", mode=ColorMode.ANSI_16)) == r("\x1b[35mfoo\x1b[39m")
    assert r(style.cyan("foo", mode=ColorMode.ANSI_16)) == r("\x1b[36mfoo\x1b[39m")
    assert r(style.white("foo", mode=ColorMode.ANSI_16)) == r("\x1b[37mfoo\x1b[39m")

    # bright names
    assert r(style.bright_black("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[90mfoo\x1b[39m"
    )
    assert r(style.bright_red("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[91mfoo\x1b[39m"
    )
    assert r(style.bright_green("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[92mfoo\x1b[39m"
    )
    assert r(style.bright_yellow("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[93mfoo\x1b[39m"
    )
    assert r(style.bright_blue("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[94mfoo\x1b[39m"
    )
    assert r(style.bright_magenta("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[95mfoo\x1b[39m"
    )
    assert r(style.bright_cyan("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[96mfoo\x1b[39m"
    )
    assert r(style.bright_white("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[97mfoo\x1b[39m"
    )

    # gray/grey aliases map to bright_black
    assert r(style.gray("foo", mode=ColorMode.ANSI_16)) == r("\x1b[90mfoo\x1b[39m")
    assert r(style.grey("foo", mode=ColorMode.ANSI_16)) == r("\x1b[90mfoo\x1b[39m")

    # backgrounds via .on
    assert r(style.on.black("foo", mode=ColorMode.ANSI_16)) == r("\x1b[40mfoo\x1b[49m")
    assert r(style.on.red("foo", mode=ColorMode.ANSI_16)) == r("\x1b[41mfoo\x1b[49m")
    assert r(style.on.green("foo", mode=ColorMode.ANSI_16)) == r("\x1b[42mfoo\x1b[49m")
    assert r(style.on.yellow("foo", mode=ColorMode.ANSI_16)) == r("\x1b[43mfoo\x1b[49m")
    assert r(style.on.blue("foo", mode=ColorMode.ANSI_16)) == r("\x1b[44mfoo\x1b[49m")
    assert r(style.on.magenta("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[45mfoo\x1b[49m"
    )
    assert r(style.on.cyan("foo", mode=ColorMode.ANSI_16)) == r("\x1b[46mfoo\x1b[49m")
    assert r(style.on.white("foo", mode=ColorMode.ANSI_16)) == r("\x1b[47mfoo\x1b[49m")

    assert r(style.on.bright_black("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[100mfoo\x1b[49m"
    )
    assert r(style.on.bright_red("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[101mfoo\x1b[49m"
    )
    assert r(style.on.bright_green("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[102mfoo\x1b[49m"
    )
    assert r(style.on.bright_yellow("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[103mfoo\x1b[49m"
    )
    assert r(style.on.bright_blue("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[104mfoo\x1b[49m"
    )
    assert r(style.on.bright_magenta("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[105mfoo\x1b[49m"
    )
    assert r(style.on.bright_cyan("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[106mfoo\x1b[49m"
    )
    assert r(style.on.bright_white("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[107mfoo\x1b[49m"
    )

    assert r(style.on.gray("foo", mode=ColorMode.ANSI_16)) == r("\x1b[100mfoo\x1b[49m")
    assert r(style.on.grey("foo", mode=ColorMode.ANSI_16)) == r("\x1b[100mfoo\x1b[49m")


def test_rgb_hex() -> None:
    # True color
    style = StyleBuilder(mode=ColorMode.TRUE_COLOR)
    assert r(style.rgb(20, 40, 60)("foo", mode=ColorMode.TRUE_COLOR)) == r(
        "\x1b[38;2;20;40;60mfoo\x1b[39m"
    )
    assert r(style.hex("14283c")("foo", mode=ColorMode.TRUE_COLOR)) == r(
        "\x1b[38;2;20;40;60mfoo\x1b[39m"
    )
    assert r(style.on.rgb(20, 40, 60)("foo", mode=ColorMode.TRUE_COLOR)) == r(
        "\x1b[48;2;20;40;60mfoo\x1b[49m"
    )
    assert r(style.on.hex("14283c")("foo", mode=ColorMode.TRUE_COLOR)) == r(
        "\x1b[48;2;20;40;60mfoo\x1b[49m"
    )

    # Extended 256
    style = style.color_mode(ColorMode.EXTENDED_256)
    assert r(style.rgb(20, 40, 60)("foo", mode=ColorMode.EXTENDED_256)) == r(
        "\x1b[38;5;23mfoo\x1b[39m"
    )
    assert r(style.hex("14283c")("foo", mode=ColorMode.EXTENDED_256)) == r(
        "\x1b[38;5;23mfoo\x1b[39m"
    )
    assert r(style.on.rgb(20, 40, 60)("foo", mode=ColorMode.EXTENDED_256)) == r(
        "\x1b[48;5;23mfoo\x1b[49m"
    )
    assert r(style.on.hex("14283c")("foo", mode=ColorMode.EXTENDED_256)) == r(
        "\x1b[48;5;23mfoo\x1b[49m"
    )

    # ANSI 16 fallback
    style = style.color_mode(ColorMode.ANSI_16)
    assert r(style.rgb(20, 40, 60)("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[30mfoo\x1b[39m"
    )
    assert r(style.hex("14283c")("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[30mfoo\x1b[39m"
    )
    assert r(style.on.rgb(20, 40, 60)("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[40mfoo\x1b[49m"
    )
    assert r(style.on.hex("14283c")("foo", mode=ColorMode.ANSI_16)) == r(
        "\x1b[40mfoo\x1b[49m"
    )

    # All off (no color)
    style = style.color_mode(ColorMode.NO_COLOR)
    assert r(style.rgb(20, 40, 60)("foo", mode=ColorMode.NO_COLOR)) == r("foo")
    assert r(style.hex("14283c")("foo", mode=ColorMode.NO_COLOR)) == r("foo")
    assert r(style.on.rgb(20, 40, 60)("foo", mode=ColorMode.NO_COLOR)) == r("foo")
    assert r(style.on.hex("14283c")("foo", mode=ColorMode.NO_COLOR)) == r("foo")


def test_disabled_mode() -> None:
    style = StyleBuilder(mode=ColorMode.NO_COLOR)
    assert r(style.black("foo")) == r("foo")


def test_type_support(style: StyleBuilder) -> None:
    class Custom:
        def __str__(self) -> str:
            return "custom"

    assert r(style.black(42, mode=ColorMode.ANSI_16)) == r("\x1b[30m42\x1b[39m")
    assert r(style.black(1.0, mode=ColorMode.ANSI_16)) == r("\x1b[30m1.0\x1b[39m")
    assert r(style.black(True, mode=ColorMode.ANSI_16)) == r("\x1b[30mTrue\x1b[39m")
    assert r(style.black(Custom(), mode=ColorMode.ANSI_16)) == r(
        "\x1b[30mcustom\x1b[39m"
    )


def test_vararg_support(style: StyleBuilder) -> None:
    assert r(style.black("a", "b", "c", mode=ColorMode.ANSI_16)) == r(
        "\x1b[30ma b c\x1b[39m"
    )
    assert r(style.black("a", "b", "c", sep="", mode=ColorMode.ANSI_16)) == r(
        "\x1b[30mabc\x1b[39m"
    )
    assert r(style.black(1, 2, 3, mode=ColorMode.ANSI_16)) == r("\x1b[30m1 2 3\x1b[39m")
    assert r(style.black(1, 2, 3, sep=", ", mode=ColorMode.ANSI_16)) == r(
        "\x1b[30m1, 2, 3\x1b[39m"
    )


def test_extend_style(style: StyleBuilder) -> None:
    style = style.color_mode(ColorMode.ANSI_16).extend(
        primary="blue",
        secondary=(169, 169, 169),
        success=style.green,
    )

    assert r(style.primary("foo")) == r("\x1b[94mfoo\x1b[39m")
    # rgb gray (169,169,169) should map to ANSI white (37) in ANSI_16 mode
    assert r(style.secondary("foo")) == r("\x1b[37mfoo\x1b[39m")
    assert r(style.success("foo")) == r("\x1b[32mfoo\x1b[39m")


def test_support_nesting_styles_of_same_type(style: StyleBuilder) -> None:
    # Use ANSI 16 for deterministic SGR codes
    s = r(
        style.red(
            " a "
            + StyleBuilder().yellow(
                " b " + StyleBuilder().green(" c ", mode=ColorMode.ANSI_16) + " b ",
                mode=ColorMode.ANSI_16,
            )
            + " a ",
            mode=ColorMode.ANSI_16,
        )
    )
    assert s == r(
        "\x1b[31m a \x1b[33m b \x1b[32m c \x1b[39m\x1b[31m\x1b[33m b \x1b[39m\x1b[31m a \x1b[39m"
    )


def test_line_breaks_should_close_and_open_colors(style: StyleBuilder) -> None:
    assert r(style.grey("hello\nworld", mode=ColorMode.ANSI_16)) == r(
        "\u001b[90mhello\u001b[39m\n\u001b[90mworld\u001b[39m"
    )


def test_line_breaks_should_close_and_open_colors_with_crlf(
    style: StyleBuilder,
) -> None:
    assert r(style.grey("hello\r\nworld", mode=ColorMode.ANSI_16)) == r(
        "\u001b[90mhello\u001b[39m\r\n\u001b[90mworld\u001b[39m"
    )


def test_line_breaks_should_close_and_open_colors_multiple_occurrences(
    style: StyleBuilder,
) -> None:
    assert r(style.grey(" a \r\n b \n c \r\n d ", mode=ColorMode.ANSI_16)) == r(
        "\u001b[90m a \u001b[39m\r\n\u001b[90m b \u001b[39m\n\u001b[90m c \u001b[39m\r\n\u001b[90m d \u001b[39m"
    )
