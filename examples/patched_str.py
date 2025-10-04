from coloredstrings.patch import colored_strings


with colored_strings():
    # style methods (like .red, .green.bold, etc.) are available on all string literals here
    print("error:".red, "something went wrong")


@colored_strings
def hello():
    # style methods are available only inside this function
    print("Hello, World!".green.bold.on_white)


hello()
