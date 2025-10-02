# coloredstrings

[![Python package](https://github.com/samedit66/coloredstrings/actions/workflows/python-package.yml/badge.svg)](https://github.com/samedit66/coloredstrings/actions/workflows/python-package.yml)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/coloredstrings?period=total&units=ABBREVIATION&left_color=BLACK&right_color=MAGENTA&left_text=downloads)](https://pepy.tech/projects/coloredstrings)
[![PyPI version](https://img.shields.io/pypi/v/coloredstrings.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/coloredstrings)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/coloredstrings.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/coloredstrings)
[![Licence](https://img.shields.io/github/license/samedit66/coloredstrings.svg)](COPYING.txt)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

<div align="center">
  <p><em>Do more. Type less. Colorize different.</em></p>
</div>

---

**coloredstrings** is a small utility for expressive terminal colors and text styles. It exposes a fluent, chainable API for styling strings - similar to the [yachalk](https://github.com/bluenote10/yachalk) package, and can act as a drop-in replacement.

Example:

```python
from coloredstrings import style

print(style.bold.underline.red("Error:"), "Something went wrong.")
print(style.blue.bold("Info:"), "Everything is OK")
print(style.italic.green("Success!"))
```

![Colored examples](https://github.com/samedit66/coloredstrings/blob/main/media/example_1.png?raw=true)

---

## Features

- No dependencies
- Composing styles in a chainable way
- Nested colors and no nested styling bug
- [`NO_COLOR`](https://no-color.org/) & `FORCE_COLOR` support
- Support for 16-color, 256-color, and 24-bit (truecolor / RGB / hex) modes
- Auto-detection of terminal color capabilities
- Friendly auto-complete API
- Ability to call style methods on strings directly (with some [black magic](https://github.com/clarete/forbiddenfruit) help)

---

## Installation

Stable release from PyPI:

```bash
pip install coloredstrings
```

Latest development version:

```bash
pip install git+https://github.com/samedit66/coloredstrings.git
```

### Optional: enable the experimental `str`-patching feature

The package includes an experimental feature that patches Python's built-in `str` type so you can call style methods directly on string literals (for example, `"text".red`). This is not enabled by default. To install the optional patched build, run:

```bash
pip install "coloredstrings[patched]"
```

This extra depends on the `forbiddenfruit` package to attach methods to `str` at runtime — see **Limitations** below.

---

## Quick start

Run the bundled demo:

```bash
python -m coloredstrings
```

Examples using the `style` object:

```python
from coloredstrings import style

print(style.bold.underline.red("Error:"), "Something went wrong.")
print(style.blue.bold("Info:"), "Everything is OK")
print(style.italic.green("Success!"))
```

Multi-argument and separator support:

```python
# style(...) accepts multiple arguments (stringable values) and a `sep` argument like `print`:
print(style.green("That's", "great!"))
print(style.blue(1, 3.14, True, sep=", "))
```

Nesting and combining styles:

```python
print(style.red(f"Hello {style.underline.on.blue('world')}!"))

print(
    style.green(
        "I am a green line " +
        style.blue.underline.bold("with a blue substring") +
        " that becomes green again!"
    )
)
```

24-bit RGB / hex and 256-color:

```python
print(style.rgb(123, 45, 200)("custom"))
print(style.hex("#aabbcc")("hex is also supported"))
print(style.color256(37)("256-color example"))
```

Define theme helpers:

```python
error = style.bold.red
warning = style.hex("#FFA500")

print(error("Error!"))
print(warning("Warning!"))
```

---

## `style` and `StyleBuilder` - API details

`style` is a convenience global instance of `StyleBuilder`. It provides a chainable API for composing foreground color, background color (via the `.on` helper), and text attributes.

**Key behaviour**

- `style` is immutable: chaining returns new `StyleBuilder` instances — no mutable global color state.
- `style(...)` (i.e. `StyleBuilder.__call__`) accepts either:
  - a single `str` argument, or
  - multiple arguments which are converted to strings and joined using `sep` (default is a single space).
- Color detection: by default the library tries to detect supported color mode (16/256/truecolor) for the current terminal. You can override it with `color_mode()`. If you want to find out what color mode is detected, use this:

```python
from coloredstrings.color_support import detect_color_support
print(detect_color_support())
```

**Important methods / properties**

- `style(...)` — apply the composed style to text; accepts `*args`, `sep` and `mode` (explicit `ColorMode`).
- `style.color_mode(mode: ColorMode)` — return a new `StyleBuilder` that uses the given color mode by default.
- `style.on` — a *property* that toggles the next color to be applied as a **background** color rather than a foreground. Example:
  ```py
  style.red.on.white("text")   # red foreground on white background
  style.on.white.red("text")   # white background with red foreground is the same if used correctly;
                               # typical usage is style.red.on.white(...)
  ```

**Foreground color builders (properties / methods)**

16-color names (properties):
```
black, red, green, yellow, blue, magenta, cyan, white,
bright_black (aliases: gray, grey),
bright_red, bright_green, bright_yellow, bright_blue, bright_magenta, bright_cyan, bright_white
```

Extended / truecolor helpers (callable methods):
```
rgb(r, g, b)        # 24-bit RGB foreground
color256(index)     # 256-color foreground (index clamped to 0..255)
hex("#RRGGBB"|"RGB"|... )  # hex shorthand supported
```

**Background selection**

Use `.on` together with a color property or method on the `style` object: e.g. `style.red.on.white("text")`, or `style.on.rgb(1,2,3)("text")`.

**Text attributes**

Properties that add text attributes (they stack; attributes combine instead of overriding):

```
bold, dim (aliases: faint, dark),
italic, underline,
blink (slow_blink), rapid_blink,
inverse (alias: reverse),
hidden (aliases: concealed),
strike,
framed, encircle (alias: circle),
overline, double_underline
```

Attribute support varies by terminal. See `types.Attribute` in the source for start/end ANSI codes and short notes on support.

**Chaining semantics (summary)**

- Attributes (bold, italic, underline, etc.) stack: calling `.bold.underline` applies both.
- Foreground/background colors are *mutually exclusive*: the last color-setting operation for foreground replaces previous foreground; same for background.
- Reapplying the same attribute does not duplicate codes - the builder ensures attributes are applied once.

---

## Isn't patching `str` un‑Pythonic?

Some time ago I was inspired by the Rust crate [text-colorizer](https://crates.io/crates/text-colorizer) — ergonomic, expressive, and pleasant to type. I later discovered [colors](https://github.com/Marak/colors.js) which uses a similar API. I couldn't find anything like that in Python, so I implemented this approach.

Patching builtins is controversial and can look un‑Pythonic. Libraries like `colorama` require you to compose ANSI sequences manually:

```python
from colorama import Fore, Style

print(Fore.RED + "error: " + Style.RESET_ALL + "something went wrong")
```

This works, but it adds visual noise (constants, concatenation, and manual resets). `termcolor` provides a simpler function-based API:

```python
from termcolor import colored

print(colored("error:", "red"), "something went wrong")
```

`coloredstrings` takes a different approach: colors and styles are first-class, readable operations on values. If you enable the optional patching feature, you can also write styles directly on string literals inside a restricted context:

```python
from coloredstrings.patch import colored_strings

# colored_strings() is a context manager that
# temporarily adds style methods to str
with colored_strings():
    print("error:".red, "something went wrong")

# colored_strings() is also a decorator with same mechanics:
# style methods are only available inside the `hello` function
@colored_strings
def hello():
    print("Hello, World!".green.bold.on_white)
```

This reads more like natural prose and keeps color usage scoped to the values that need it. Maybe it's not for everyone (and because of that the `style` object exists), but it's pleasant to type.

---

## Limitations

Under the hood `coloredstrings[patched]` uses `forbiddenfruit` package, as a result it also has the same limitations:

> Forbbiden Fruit is tested on CPython 3.7-3.13.
> Since Forbidden Fruit is fundamentally dependent on the C API, this library won't work on other python implementations, such as Jython, pypy, etc.

---

## Contributing

I’d love your help to make coloredstrings even better!

- 💡 Got an idea or found a bug? [Open an issue](https://github.com/samedit66/coloredstrings/issues) and let’s talk about it
- 🔧 Want to improve the code? PRs are always welcome! Please include tests for any new behavior.
- ♻️ Try to keep changes backward-compatible where possible
- 🎨 Adding new styles or helpers? Don’t forget to update the README and include tests to ensure ANSI - sequences open and close correctly
-  ⭐ If you like this project, consider giving it a star - it really helps others discover it!
