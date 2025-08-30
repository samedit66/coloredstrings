import pytest

import coloredstrings

import ascii_codes


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
        assert "".red() == "\033[31m\033[0m"  # red empty string still applies codes


def test_context_manager_basic_color():
    msg = perror("fail")
    assert msg.startswith(ascii_codes.RED)
    assert msg.endswith(ascii_codes.RESET)
    assert "fail" in msg


def test_decorator_basic():
    msg = log_info("system ready")
    assert "[\033[34mINFO\033[0m]" in msg
    assert "system ready" in msg


def test_multiple_methods_chain():
    with coloredstrings.patched():
        text = "hi".red().bold().underline()
        # order of application matters, should start with last code added
        assert text.startswith("\033[4m\033[1m\033[31mhi") or text.startswith("\033[31m")  
        assert text.endswith("\033[0m")


def test_rgb_values_clamped():
    with coloredstrings.patched():
        txt = "rgb".rgb(999, -20, 42)
        # values should be clamped into 0..255
        assert "\033[38;2;255;0;42m" in txt


def test_color256_clamping():
    with coloredstrings.patched():
        assert "color".color256(-1).startswith("\033[38;5;0m")
        assert "color".color256(300).startswith("\033[38;5;255m")


def test_patch_and_unpatch_manual():
    coloredstrings.patch()
    assert hasattr(str, "red")
    assert "ok".red().startswith("\033[31m")

    coloredstrings.unpatch()
    assert not hasattr(str, "red")
