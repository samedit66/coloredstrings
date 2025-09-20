import pytest

import coloredstrings
from coloredstrings import style


def perror(message: str):
    # Demonstrates patching via context manager
    with coloredstrings.patched():
        return message.red()


@coloredstrings.patched
def log_info(message: str):
    # Demonstrates patching via decorator
    colored = "INFO".blue()
    return f"[{colored}]: {message}"


def test_context_manager_empty_string():
    with coloredstrings.patched():
        # red empty string still applies codes (opening + reset)
        assert "".red() == f"{style.ESC}{style.AnsiFore.RED.value}m{style.RESET}"


def test_context_manager_basic_color():
    msg = perror("fail")
    assert msg.startswith(f"{style.ESC}{style.AnsiFore.RED.value}m")
    assert msg.endswith(style.RESET)
    assert "fail" in msg


def test_decorator_basic():
    msg = log_info("system ready")
    expected_info = f"{style.ESC}{style.AnsiFore.BLUE.value}mINFO{style.RESET}"
    assert f"[{expected_info}]" in msg
    assert "system ready" in msg


def test_multiple_methods_chain():
    with coloredstrings.patched():
        text = "hi".red().bold().underline()
        # new implementation produces a single combined SGR sequence, e.g. '\033[1;4;31mhi...'
        expected_prefix = (
            f"{style.ESC}"
            f"{style.Attribute.BOLD.value};"
            f"{style.Attribute.UNDERLINE.value};"
            f"{style.AnsiFore.RED.value}mhi"
        )
        assert text.startswith(expected_prefix)
        assert text.endswith(style.RESET)


def test_rgb_values_clamped():
    with coloredstrings.patched():
        txt = "rgb".rgb(999, -20, 42)
        # values should be clamped into 0..255
        assert f"{style.ESC}38;2;255;0;42m" in txt


def test_color256_clamping():
    with coloredstrings.patched():
        assert "color".color256(-1).startswith(f"{style.ESC}38;5;0m")
        assert "color".color256(300).startswith(f"{style.ESC}38;5;255m")


def test_patch_and_unpatch_manual():
    coloredstrings.patch()
    assert hasattr(str, "red")
    assert "ok".red().startswith(f"{style.ESC}{style.AnsiFore.RED.value}m")

    coloredstrings.unpatch()
    assert not hasattr(str, "red")


def test_multiple_foregrounds_and_styles_present():
    with coloredstrings.patched():
        s = "ok"
        out = s.yellow()
        assert f"{style.ESC}{style.AnsiFore.YELLOW.value}m" in out
        out2 = s.bold()
        assert f"{style.ESC}{style.Attribute.BOLD.value}m" in out2
        # chaining: both codes present when chained; combined sequence likely '\033[3;34m' for italic+blue
        chained = s.blue().italic()
        opt1 = f"{style.ESC}{style.Attribute.ITALIC.value};{style.AnsiFore.BLUE.value}m"
        opt2 = f"{style.ESC}{style.AnsiFore.BLUE.value};{style.Attribute.ITALIC.value}m"
        assert opt1 in chained or opt2 in chained


def test_chaining_order_and_reset_behavior():
    with coloredstrings.patched():
        s = "x"
        res = s.red().bold()
        # combined sequence includes both codes (example '\033[1;31m' or '\033[31;1m')
        opt1 = f"{style.ESC}{style.Attribute.BOLD.value};{style.AnsiFore.RED.value}m"
        opt2 = f"{style.ESC}{style.AnsiFore.RED.value};{style.Attribute.BOLD.value}m"
        assert opt1 in res or opt2 in res
        assert res.endswith(style.RESET)


def test_commutativity_of_color_and_style():
    with coloredstrings.patched():
        s1 = "ok".green().bold()
        s2 = "ok".bold().green()
        # result strings should be identical (order of applying style vs color should not change combined SGR)
        assert s1 == s2


def test_last_foreground_wins():
    with coloredstrings.patched():
        s = "Hello".green().red()
        # last foreground color should be red (31); ensure red present and green absent
        red_seq = f"{style.ESC}{style.AnsiFore.RED.value}m"
        green_seq = f"{style.ESC}{style.AnsiFore.GREEN.value}m"
        assert red_seq in s
        assert green_seq not in s


def test_double_underline_single_escape():
    with coloredstrings.patched():
        s = "u".underline().underline()
        # find index of the plain text 'u' (after opening SGR)
        idx = s.find("u")
        assert idx != -1
        # there should be only one ESC sequence in the prefix before the 'u'
        assert s.count(style.ESC, 0, idx) == 1


def test_on_rgb_clamping():
    with coloredstrings.patched():
        txt = "bg".on_rgb(999, -20, 42)
        # background RGB uses 48;2;r;g;b sequence and values should be clamped into 0..255
        assert f"{style.ESC}48;2;255;0;42m" in txt


def test_on_color256_clamping():
    with coloredstrings.patched():
        assert "bg".on_color256(-5).startswith(f"{style.ESC}48;5;0m")
        assert "bg".on_color256(300).startswith(f"{style.ESC}48;5;255m")


def test_hex_short_and_prefixed():
    with coloredstrings.patched():
        # short form '#fc0' -> ffcc00 -> 255;204;0
        s1 = "x".hex("#fc0")
        assert f"{style.ESC}38;2;255;204;0m" in s1
        # '0x123456' -> 18;52;86
        s2 = "y".hex("0x123456")
        assert f"{style.ESC}38;2;18;52;86m" in s2


def test_on_hex_background():
    with coloredstrings.patched():
        # 'abc' -> aabbcc -> 170;187;204
        s = "bg".on_hex("abc")
        assert f"{style.ESC}48;2;170;187;204m" in s


def test_hex_invalid_raises():
    with coloredstrings.patched():
        # invalid hex string should raise ValueError coming from rgb_from_hex
        with pytest.raises(ValueError):
            "x".hex("zzz")
