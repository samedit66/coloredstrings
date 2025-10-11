import coloredstrings as cs

print(cs.bold.underline.red("Error:"), "Something went wrong.")
print(cs.blue.bold("Info:"), "Everything is OK")
print(cs.italic.green("Success!"))

# styles accepts multiple arguments and a `sep` argument like `print`:
print(cs.green("That's", "great!"))
print(cs.blue(1, 3.14, True, sep=", "))

# Nesting and combining styles:
print(cs.red(f"Hello {cs.underline.on.blue('world')}!"))
print(
    cs.green(
        "I am a green line "
        + cs.blue.underline.bold("with a blue substring")
        + " that becomes green again!"
    )
)

# 24-bit RGB / hex and 256-color:
print(cs.rgb(123, 45, 200)("custom"))
print(cs.rgb("#aabbcc")("hex is also supported"))
print(cs.rgb("purple")("as well as named colors too"))
print(cs.rgb((169, 169, 169))("tuples can be also used"))
print(cs.color256(37)("256-color example"))

# Define theme helpers:
error = cs.bold.red
warning = cs.rgb("#FFA500")

print(error("Error!"))
print(warning("Warning!"))

# Or extend with your own styles:
bootstrap = cs.extend(
    primary="blue",
    secondary=(169, 169, 169),
    success=cs.green,
)

print(bootstrap.primary("Click me!"))
print(bootstrap.italic.secondary("You can combine builtin styles with your own!"))
print(bootstrap.success("Complete."))
