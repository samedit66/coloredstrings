# coloredstrings

**Colorize Different**

A tiny utility that patches Python's built-in str with convenient ANSI color / style helpers so you can write `"hello".red()` instead of juggling escape sequences or long constant concatenations. Inspired by the Rust [text-colorizer](https://crates.io/crates/text-colorizer) crate — ergonomic, expressive, and surprisingly pleasant to type.

---

## Why use this? — Isn't patching `str` un-Pythonic?

Patching builtins is a controversial choice, and at first glance it __may__ look un-Pythonic. Libraries like `colorama` require you to import constants and build strings by concatenation:

```python
# colorama style (typical)
from colorama import Fore, Style
print(Fore.RED + "error: " + Style.RESET_ALL + "something went wrong")
```

That works fine, but it forces you to manage constants and remember to reset, and your code quickly becomes noisy with `+` and `RESET` tokens.

With `coloredstrings` the color becomes a readable method on the string itself:

```python
import coloredstrings
coloredstrings.patch()
print("error:".red(), "something went wrong")
coloredstrings.unpatch()
```

This reads more like natural prose and keeps color usage local to the value being displayed.

---

## Quick start — example usage

To patch globally:

```python
import coloredstrings

# Attach helpers to built-in str
coloredstrings.patch()

print("ok".green())                # green text
print("warn".yellow().bold())      # chained styles (color then bold)
print("bad".red(), "on green".on_green())

# 24-bit RGB:
print("custom".rgb(123, 45, 200))

# 256-color:
print("teal-ish".color256(37))

# When you're done (optional) remove the patched methods:
coloredstrings.unpatch()
```

To patch locally (inside a function or a context):

```python
import coloredstrings

def perror(message: str):
    with coloredstrings.patched():
        print(message.red())

@coloredstrings.patched
def log_info(message: str):
    colored = "INFO".blue()
    print(f"[{colored}]: {message}")

log_info("Downloaded image.")
perror("file not found!")
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

```bash
pip install git+https://github.com/samedit66/coloredstrings.git
```

I'll soon upload it to PyPi🙃.

---

## Limitations

Under the hood `coloredstrings` uses `forbiddenfruit` package, as a result it also has the same limitations:

> Forbbiden Fruit is tested on CPython 3.7-3.13.
> Since Forbidden Fruit is fundamentally dependent on the C API, this library won't work on other python implementations, such as Jython, pypy, etc.
