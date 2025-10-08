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
# Do not use it - it’s deprecated.
print(style.hex("#aabbcc"))

# Define theme helpers:
error = style.bold.red
warning = style.hex("#FFA500")

print(error("Error!"))
print(warning("Warning!"))
