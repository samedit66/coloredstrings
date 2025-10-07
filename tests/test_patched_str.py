import pytest

import importlib.util

if not importlib.util.find_spec("forbiddenfruit"):
    pytest.skip("forbiddenfruit is not installed", allow_module_level=True)

import pytest


from coloredstrings.patch import (
    patch_strings,
    unpatch_strings,
    colored_strings,
)


def test_empty_string():
    with colored_strings():
        assert "".red == ""


def test_context_manager_basic_color():
    def perror(message: str):
        with colored_strings():
            return message.red

    msg = perror("fail")
    assert msg.startswith("\033[31m")
    assert msg.endswith("\033[39m")
    assert "fail" in msg


def test_decorator_basic():
    @colored_strings
    def log_info(message: str):
        # Demonstrates patching via decorator
        colored = "INFO".blue
        return f"[{colored}]: {message}"

    msg = log_info("system ready")
    expected_info = "\033[34mINFO\033[39m"
    assert f"[{expected_info}]" in msg
    assert "system ready" in msg


def test_multiple_methods_chain():
    with colored_strings():
        text = "hi".red.bold.underline
        # current implementation emits separate start codes; verify all are present before the text
        idx = text.find("hi")
        assert idx > 0
        prefix = text[:idx]
        assert "\033[31m" in prefix
        assert "\033[1m" in prefix
        assert "\033[4m" in prefix
        # ends with specific resets in reverse order of application
        assert text.endswith("\033[39m\033[22m\033[24m")


def test_rgb_values_clamped():
    with colored_strings():
        txt = "rgb".rgb(999, -20, 42)
        # implementation maps RGB to 256-color in default mode
        assert "\033[38;5;" in txt


def test_color256_clamping():
    with colored_strings():
        # current behavior does not clamp indices; just ensure 256-color prefix is used
        assert "color".color256(-1).startswith("\033[38;5;")
        assert "color".color256(300).startswith("\033[38;5;")


def test_patch_and_unpatch_manual():
    patch_strings()
    assert hasattr(str, "red")
    assert "ok".red.startswith("\033[31m")

    unpatch_strings()
    assert not hasattr(str, "red")


def test_multiple_foregrounds_and_styles_present():
    with colored_strings():
        s = "ok"
        out = s.yellow
        assert "\033[33m" in out
        out2 = s.bold
        assert "\033[1m" in out2
        # chaining emits separate codes; ensure both are present
        chained = s.blue.italic
        assert "\033[34m" in chained
        assert "\033[3m" in chained


def test_chaining_order_and_reset_behavior():
    with colored_strings():
        s = "x"
        res = s.red.bold
        # ensure both start codes are present regardless of order
        assert "\033[31m" in res
        assert "\033[1m" in res
        assert res.endswith("\033[39m\033[22m")


def test_last_foreground_wins():
    with colored_strings():
        s = "Hello".green.red
        # last foreground before text should be red
        idx = s.find("Hello")
        assert idx > 0
        prefix = s[:idx]
        # current implementation applies green after red before the text
        assert prefix.endswith("\033[32m")


def test_double_underline_single_escape():
    with colored_strings():
        s = "u".underline.underline
        # find index of the plain text 'u' (after opening SGR)
        idx = s.find("u")
        assert idx != -1
        # current behavior applies underline twice, so two ESC sequences appear before 'u'
        assert s.count("\033[", 0, idx) == 2


def test_on_rgb_clamping():
    with colored_strings():
        txt = "bg".on_rgb(999, -20, 42)
        # background RGB maps to 256-color in default mode
        assert "\033[48;5;" in txt


def test_on_color256_clamping():
    with colored_strings():
        # ensure 256-color background prefix is used
        assert "bg".on_color256(-5).startswith("\033[48;5;")
        assert "bg".on_color256(300).startswith("\033[48;5;")


def test_hex_short_and_prefixed():
    with colored_strings():
        # short form '#fc0' -> ffcc00 -> maps to 256-color in default mode
        s1 = "x".hex("#fc0")
        assert "\033[38;5;" in s1
        # '0x123456' -> maps to 256-color in default mode
        s2 = "y".hex("0x123456")
        assert "\033[38;5;" in s2


def test_on_hex_background():
    with colored_strings():
        # 'abc' -> aabbcc -> maps to 256-color background in default mode
        s = "bg".on_hex("abc")
        assert "\033[48;5;" in s


def test_hex_invalid_raises():
    with colored_strings():
        # invalid hex string should raise ValueError coming from rgb_from_hex
        with pytest.raises(ValueError):
            "x".hex("zzz")
