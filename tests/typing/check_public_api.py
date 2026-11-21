from collections.abc import Mapping
from typing import assert_type

import coloredstrings as cs
from coloredstrings import StyleBuilder


def check_public_api() -> None:
    style = StyleBuilder()
    colors: Mapping[str, str] = {"accent": "coral"}
    assert_type(style.extend(colors), StyleBuilder)
    assert_type(style.rgb(255, 0, 0), StyleBuilder)
    assert_type(style.rgb((255, 0, 0)), StyleBuilder)
    assert_type(style.rgb("coral"), StyleBuilder)
    assert_type(style.rgb("coral", 1, 2), StyleBuilder)
    assert_type(style.strikethrough.bold, StyleBuilder)
    assert_type(cs.rgb(255, 0, 0), StyleBuilder)
    assert_type(cs.strikethrough.bold, StyleBuilder)

    # Unused-ignore checking makes these fail if invalid calls stop being rejected.
    style.rgb(255)  # type: ignore[call-overload]
    style.rgb(255, 0)  # type: ignore[call-overload]
    style.extend(accent=123)  # type: ignore[arg-type]
    style.strikethrough.rgb(object())  # type: ignore[call-overload]
