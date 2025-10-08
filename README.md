# coloredstrings

[![Python package](https://github.com/samedit66/coloredstrings/actions/workflows/python-package.yml/badge.svg)](https://github.com/samedit66/coloredstrings/actions/workflows/python-package.yml)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/coloredstrings?period=total&units=ABBREVIATION&left_color=BLACK&right_color=MAGENTA&left_text=downloads)](https://pepy.tech/projects/coloredstrings)
[![PyPI version](https://img.shields.io/pypi/v/coloredstrings.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/coloredstrings)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/coloredstrings.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/coloredstrings)
[![Licence](https://img.shields.io/github/license/samedit66/coloredstrings.svg)](COPYING.txt)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

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

![preview image](https://github.com/samedit66/coloredstrings/blob/main/media/preview.png?raw=true)

---

## Features🔥

- No dependencies
- Composing styles in a chainable way
- Nested colors and no nested styling bug
- Support for [common envs](#force_color-no_color-clicolor_force-and-clicolor): [`FORCE_COLOR`](https://force-color.org/), [`NO_COLOR`](https://no-color.org/), [`CLICOLOR_FORCE`&`CLICOLOR`](https://bixense.com/clicolors/)
- Friendly to [CLI arguments](#cli-arguments): `--color` & `--no-color`
- Support for 16-color, 256-color, and 24-bit (truecolor / RGB / hex) modes
- Auto-detection of terminal color capabilities
- Automatically fall back to the nearest supported color if the requested color isn't supported
- Friendly auto-complete API
- Strip ANSI escape codes with `coloredstrings.strip_ansi`

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

# style(...) accepts multiple arguments and a `sep` argument like `print`:
print(style.green("That's", "great!"))
print(style.blue(1, 3.14, True, sep=", "))

# Nesting and combining styles:
print(style.red(f"Hello {style.underline.on.blue('world')}!"))
print(
    style.green(
        "I am a green line "
        + style.blue.underline.bold("with a blue substring")
        + " that becomes green again!"
    )
)

# 24-bit RGB / hex and 256-color:
print(style.rgb(123, 45, 200)("custom"))
print(style.rgb("#aabbcc")("hex is also supported"))
print(style.rgb("purple")("as well as named colors too"))
print(style.color256(37)("256-color example"))

# Note: previous versions of `coloredstrings` had a dedicated method
# to accept hex color codes. It is now successfully handled by .rgb(...).
# Do not use it - it's deprecated.
print(style.hex("#caffac")("Deprecated method."))

# Define theme helpers:
error = style.bold.red
warning = style.hex("#FFA500")

print(error("Error!"))
print(warning("Warning!"))
```

---

## Usage

All you need to use (mostly) is the global `style` object - an instance of the `StyleBuilder` class. It provides a chainable API that looks like this:

```python
style.red.on.blue("Hello", "world!")
```

Put simply: you name the style pieces dot after dot and `StyleBuilder` handles the rest. The final pair of parentheses is a call that styles the given strings (or any sequence of values). Arguments are converted to strings and joined using an optional `sep` argument (which defaults to a single space):

```python
style.<style1>.[<style2>...](v1, [v2...], sep=' ')
```

### `style` object

`style` is an immutable builder object used to construct composite styles and themes.
Because style is immutable, creating a new style from an existing one doesn't modify the original. This avoids accidental cross-contamination of styles presented in `yachalk`:

```python
from yachalk import chalk
from coloredstrings import style

# With yachalk
s1 = chalk.italic
s2 = s1.red

print(s1("Chalk, am I red?"))
print(s2("Yes, you are!"))

print("-" * 8)

# With coloredstrings
s3 = style.italic
s4 = s3.red

print(s3("Style, am I still red?"))
print(s4("Sure not, but I am!"))

```

![yachalk bug image](https://github.com/samedit66/coloredstrings/blob/main/media/yachalk_bug.png?raw=true)

In this example, `s1/s2` and `s3/s4` behave different: `s1/s2` are actually the same style, while `s3/s4` are truly independent styles.

### Chaining and gotchas

`coloredstrings` - like `yachalk` and several other libraries - is built around chaining styles. Unlike some libraries, it does not provide separate background helpers such as `bg_blue`. Instead, use the `on` helper to mark that the next color in the chain should be a background color. This gives you explicit control over whether the color you add applies to the foreground or the background.

Example:

```python
from coloredstrings import style

# Red text on a blue background
print(style.red.on.blue("Hey!"))

# Don't write code like this - it's hard to read!
# It's equivalent to `style.white.on.black(...)` but much less clear
print(style.white.on.on.black("Do not write code like that."))

# Green background with default foreground
print(style.on.green("Text on a green background"))
```

A few important gotchas:

- If you chain multiple foreground colors, only the last foreground color takes effect:

  ```python
  print(style.red.green.blue("Blue text")) # result: blue foreground
  ```

- `on` affects only the next color in the chain. For example:


  ```python
  print(style.on.magenta.cyan("Cyan text on magenta background"))
  ```

  Here `magenta` becomes the background (because of `on`) and `cyan` is the foreground.

- Repeated calls to `on` without an intervening color are redundant and hurt readability; prefer the simpler, clearer form.

### Supported color modes

`coloredstrings` tries its best to detect terminal color capabilities automatically (see `coloredstrings.color_support.detect_color_support()`), but detection can occasionally miss. You can explicitly set the color mode using the pseudo-style method `color_mode(mode)`.

`mode` is a member of the `coloredstrings.ColorMode` enum with these values:
- `ColorMode.NO_COLORS` - disable styling; no escape sequences are emitted
- `ColorMode.ANSI_16` - 16 basic ANSI colors
- `ColorMode.EXTENDED_256` - 256 color mode
- `ColorMode.TRUE_COLOR` - 24-bit RGB / truecolor support

Example:

```python
from coloredstrings import style, ColorMode

# Force no colors
just_text = style.color_mode(ColorMode.NO_COLORS)
print(just_text.red("It isn't red"))

# Force truecolor
rgb_default = style.color_mode(ColorMode.TRUE_COLOR)
print(rgb_default.hex("#ca7e8d")("Hi!"))
```

#### `FORCE_COLOR`, `NO_COLOR`, `CLICOLOR_FORCE` and `CLICOLOR`

With a wide variety of options to force terminal color or not, `coloredstrings` respects common environment conventions (in order of precedence - higher precedence goes first):

- **`FORCE_COLOR`** or : if set, this variable can be used to force color output even when detection would otherwise disable it (for example, when output is being piped).
Following values are supported:
  - `FORCE_COLOR<=0` - same as `ColorMode.NO_COLOR` or `NO_COLOR` environment variable
  - `FORCE_COLOR=1` - same as `ColorMode.ANSI_16`
  - `FORCE_COLOR=2` - same as `ColorMode.EXTENDED_256`
  - `FORCE_COLOR>=3` - same as `ColorMode.TRUE_COLOR`

- **`NO_COLOR`**: if this environment variable is present (with any value beside empty string), coloredstrings will avoid emitting color escape sequences. This is the community-standard way for users to opt out of colored output.

- **`CLICOLOR_FORCE`**: same as `FORCE_COLOR`.

- **`CLICOLOR`**: same as `ColorMode.ANSI_16`.

You can still programmatically override detection by calling `style.color_mode(...)` as shown above.

#### CLI arguments

> [!NOTE]
> CLI arguments take precedence over any environment variable.

You can also specify command-line flags like `--no-color` to disable colars and `--color` to enable them.

Example with a file `cool.py`:

```python
from coloredstrings import style

print(style.red(f'Hello {style.blue('world')}!'))
```

```bash
# Run with python
python cool.py --no-color

# Run with uv
uv run cool.py --color
```

## Fallback behavior

Many terminals do not support full truecolor (`ColorMode.TRUE_COLOR`). When a requested color cannot be represented in the current color mode, `coloredstrings` automatically maps the requested color into the best available color space and emits the closest supported color. In short: you will still get colored output, though the result may be an approximation of the original color.

## Styles

### Attributes

- `reset` - Reset the current style chain. Widely supported.
- `bold` - Make the text bold (increases weight). Widely supported.
- `dim` (aliases: `faint`, `dark`) - Render the text with lower intensity / brightness. Support varies.
- `italic` - Render text in italic. *Support varies across terminals.*
- `underline` - Draw a horizontal line **below** the text. *Support varies.*
- `double_underline` - Draw a double underline under the text. *Not widely supported.*
- `overline` - Draw a horizontal line **above** the text. *Not widely supported.*
- `inverse` (alias: `reverse`) - Swap foreground and background colors (invert colors).
- `hidden` (alias: `concealed`) - Do not display the text (it is still present in the output stream).
- `strike` (alias: `strikethrough`) - Draw a horizontal line through the center of the text. *Support varies.*
- `blink` (alias: `slow_blink`) - Make the text blink. **Often unsupported** in modern terminals; avoid depending on it.
- `rapid_blink` - Faster blink. **Often unsupported** in modern terminals; avoid depending on it.
- `framed` - Draw a frame around the text. *Rarely supported.*
- `encircle` (alias: `circle`) - Draw a circle/encircle the text. *Rarely supported.*
- `visible` - Show text only when a color mode is enabled (anything other than `ColorMode.NO_COLOR`). Mainly used for cosmetic things.

> **Note on attributes:** Most attributes stack (they combine instead of overriding). Terminal support for many of these attributes is spotty - prefer basic attributes (`bold`, `underline`, `inverse`) for portability.

### Colors (both foreground and background)

- `black`
- `red`
- `green`
- `yellow`
- `blue`
- `magenta`
- `cyan`
- `white`
- `bright_black` (aliases: `gray`, `grey`)
- `bright_red`
- `bright_green`
- `bright_yellow`
- `bright_blue`
- `bright_magenta`
- `bright_cyan`
- `bright_white`
- `color256(index)` - 256 color
- `rgb(r, g, b)`, `hex(color_code)` - 24-bit RGB color

---

## Contributing

I’d love your help to make coloredstrings even better!

- 💡 Got an idea or found a bug? [Open an issue](https://github.com/samedit66/coloredstrings/issues) and let’s talk about it
- 🔧 Want to improve the code? PRs are always welcome! Please include tests for any new behavior.
- ♻️ Try to keep changes backward-compatible where possible
- 🎨 Adding new styles or helpers? Don’t forget to update the README and include tests to ensure ANSI - sequences open and close correctly
-  ⭐ If you like this project, consider giving it a star - it really helps others discover it!
