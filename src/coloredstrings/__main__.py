from __future__ import annotations

import os

import coloredstrings


with coloredstrings.patched():
    print(f"Current terminal type: {os.getenv('TERM')}")

    print("-" * 78)

    print("Test basic colors:")
    print("Black color".black())
    print("Red color".red())
    print("Green color".green())
    print("Yellow color".yellow())
    print("Blue color".blue())
    print("Magenta color".magenta())
    print("Cyan color".cyan())
    print("White color".white())
    print("Light grey color".bright_black())
    print("Dark grey color".black().dim())
    print("Light red color".bright_red())
    print("Light green color".bright_green())
    print("Light yellow color".bright_yellow())
    print("Light blue color".bright_blue())
    print("Light magenta color".bright_magenta())
    print("Light cyan color".bright_cyan())

    print("-" * 78)

    print("Test highlights:")
    print("On black color".on_black())
    print("On red color".on_red())
    print("On green color".on_green())
    print("On yellow color".on_yellow())
    print("On blue color".on_blue())
    print("On magenta color".on_magenta())
    print("On cyan color".on_cyan())
    print("On white color".black().on_white())
    print("On light grey color".on_bright_grey())
    print("On dark grey color".on_grey())
    print("On light red color".on_bright_red())
    print("On light green color".on_bright_green())
    print("On light yellow color".on_bright_yellow())
    print("On light blue color".on_bright_blue())
    print("On light magenta color".on_bright_magenta())
    print("On light cyan color".on_bright_cyan())

    print("-" * 78)

    print("Test attributes:")
    print("Bold black color".black().bold())
    print("Dim red color".red().dim())  # 'dark' mapped to dim()
    print("Underline green color".green().underline())
    print("Reversed blue color".blue().inverse())
    print("Bold underline inverse cyan color".cyan().bold().underline().inverse())
    print("Dim white color".white().dim())
    print("Hidden:", "you can't see it, eh?".hidden())
    print("Striked".strike())
    print("Blink hot pink color".blink().rgb(255, 105, 180))

    print("-" * 78)

    print("Test mixing:")
    print("Underline red on black color".red().on_black().underline())
    print("Reversed green on red color".green().on_red().inverse())

    print("-" * 78)

    print("Test RGB (truecolor):")
    print("Pure red text (255, 0, 0)".rgb(255, 0, 0))
    print("Default red for comparison".red())
    print("Pure green text (0, 255, 0)".rgb(0, 255, 0))
    print("Default green for comparison".green())
    print("Pure blue text (0, 0, 255)".rgb(0, 0, 255))
    print("Default blue for comparison".blue())
    print("Pure yellow text (255, 255, 0)".rgb(255, 255, 0))
    print("Default yellow for comparison".yellow())
    print("Pure cyan text (0, 255, 255)".rgb(0, 255, 255))
    print("Default cyan for comparison".cyan())
    print("Pure magenta text (255, 0, 255)".rgb(255, 0, 255))
    print("Default magenta for comparison".magenta())
    print("Light pink (255, 182, 193)".rgb(255, 182, 193))
    print("Hot pink (255, 105, 180)".rgb(255, 105, 180))
