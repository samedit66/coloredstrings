# coloredstrings [![Python package](https://github.com/samedit66/coloredstrings/actions/workflows/python-package.yml/badge.svg)](https://github.com/samedit66/coloredstrings/actions/workflows/python-package.yml) [![PyPI Downloads](https://static.pepy.tech/personalized-badge/coloredstrings?period=total&units=ABBREVIATION&left_color=BLACK&right_color=MAGENTA&left_text=downloads)](https://pepy.tech/projects/coloredstrings)

**Colorize Different**

A tiny utility that patches Python's built-in str with convenient ANSI color / style helpers so you can write `"hello".red()` instead of juggling escape sequences or long constant concatenations. Inspired by the Rust [text-colorizer](https://crates.io/crates/text-colorizer) crate — ergonomic, expressive, and surprisingly pleasant to type.

---

## Why use this? — Isn't patching `str` un-Pythonic?

Patching builtins is a controversial choice, and at first glance it __may__ look un-Pythonic. Libraries like `colorama` require you to import constants and build strings by concatenation:

```python
from colorama import Fore, Style

print(Fore.RED + "error: " + Style.RESET_ALL + "something went wrong")
```

That works fine, but it forces you to manage constants and remember to reset, and your code quickly becomes noisy with `+` and `RESET` tokens.

Another example using the `termcolor` package:
```python
from termcolor import cprint

print(colored("error:", "red"), "something went wrong")
```

`termcolor` offers a nice function `colored` with a bunch of arguments, but personally, I still find it lacking.

With `coloredstrings` the color becomes a readable method on the string itself:

```python
import coloredstrings

# `patched()` patches `str` to have awesome `red()` method
with coloredstrings.patched():
    print("error: ".red(), "something went wrong")
```

This reads more like natural prose and keeps color usage local to the value being displayed.

---

## Quick start — example usage

```python
import coloredstrings

# Patched `str` methods are available only within the context
def warn(msg: str) -> None:
    with coloredstrings.patched():
        print("warning:".yellow().bold(), msg)

# Same idea, but using a decorator
@coloredstrings.patched
def info(msg: str) -> None:
    print("[info]:".blue(), msg)

# If you're brave enough and really want it, you can patch `str` globally
coloredstrings.patch()

print("ok".green())
print("warn".yellow().bold())
print("bad".red(), "on green".on_green())

# 24-bit RGB:
print("custom".rgb(123, 45, 200))

# 256-color:
print("teal-ish".color256(37))

# And don't forget to unpatch it afterwards
coloredstrings.unpatch()
```

---

## API (high level)

- `patch()` — attach methods to `str`
- `unpatch()` — remove the attached methods
- `patched()` - automatically calls `patch()` and `unpatch()` in a given context

- Color/style methods attached to str (call on any string):
    - Foreground colors: `red()`, `green()`, `yellow()`, `blue()`, `magenta()`, `cyan()`, `white()`, `black()`, `bright_red()`
    - Styles: `bold()`, `dim()`, `italic()`, `underline()`, `inverse()`
    - Background helpers: `on_red()`, `on_green()`
    - 24-bit color: `rgb(r, g, b)`
    - 256-color: `color256(idx)`

---

## Installation

Stable:
```bash
pip install coloredstrings
```

Latest:
```bash
pip install git+https://github.com/samedit66/coloredstrings.git
```

---

## Limitations

Under the hood `coloredstrings` uses `forbiddenfruit` package, as a result it also has the same limitations:

> Forbbiden Fruit is tested on CPython 3.7-3.13.
> Since Forbidden Fruit is fundamentally dependent on the C API, this library won't work on other python implementations, such as Jython, pypy, etc.
