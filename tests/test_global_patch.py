import pytest

import coloredstrings

import ascii_codes


@pytest.fixture(autouse=True)
def patch_and_unpatch():
    coloredstrings.patch()
    yield
    coloredstrings.unpatch()


def strip_known_codes(s: str, *codes: str) -> str:
    """Helper to remove known ANSI codes for simple content-checking."""
    for c in codes:
        s = s.replace(c, "")
    return s.replace(ascii_codes.RESET, "")


def test_basic_red_and_reset_and_content():
    s = "hello"
    r = s.red()
    assert isinstance(r, str)
    # red code must be present and string must end with reset
    assert "\033[31m" in r
    assert r.endswith(ascii_codes.RESET)
    # after removing known codes we recover original content
    assert strip_known_codes(r, "\033[31m") == s


def test_multiple_foregrounds_and_styles_present():
    s = "ok"
    out = s.yellow()
    assert "\033[33m" in out
    out2 = s.bold()
    assert "\033[1m" in out2
    # chaining: both codes present when chained
    chained = s.blue().italic()
    assert "\033[34m" in chained
    assert "\033[3m" in chained
    assert strip_known_codes(chained, "\033[34m", "\033[3m") == s


def test_background_helpers_on_red_on_green():
    s = "bg"
    orr = s.on_red()
    og = s.on_green()
    assert "\033[41m" in orr
    assert "\033[42m" in og
    assert strip_known_codes(orr, "\033[41m") == s
    assert strip_known_codes(og, "\033[42m") == s


def test_rgb_clamping_and_formatting():
    s = "X"
    # normal values
    out = s.rgb(10, 20, 30)
    assert "\033[38;2;10;20;30m" in out
    assert strip_known_codes(out, "\033[38;2;10;20;30m") == s

    # out-of-range values should be clamped: negative -> 0, >255 -> 255
    out2 = s.rgb(-5, 300, 999)
    assert "\033[38;2;0;255;255m" in out2
    assert strip_known_codes(out2, "\033[38;2;0;255;255m") == s


def test_color256_clamping_and_formatting():
    s = "Y"
    out = s.color256(202)
    assert "\033[38;5;202m" in out
    assert strip_known_codes(out, "\033[38;5;202m") == s

    out_low = s.color256(-1)
    assert "\033[38;5;0m" in out_low
    out_high = s.color256(999)
    assert "\033[38;5;255m" in out_high


def test_chaining_order_and_reset_behavior():
    s = "x"
    res = s.red().bold()
    # both codes present somewhere in the result
    assert "\033[31m" in res
    assert "\033[1m" in res
    # and the content is still present after stripping known codes
    assert strip_known_codes(res, "\033[31m", "\033[1m") == s
    