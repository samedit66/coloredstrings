import re


_ANSI_ESCAPE = re.compile(r'''
    \x1B  # ESC
    (?:   # 7-bit C1 Fe (except CSI)
        [@-Z\\-_]
    |     # or [ for CSI, followed by a control sequence
        \[
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    )
''', re.VERBOSE)


def strip_ansi(colored_text: str) -> str:
    """
    Removes from the given text all ANSI escape sequences.
    These include: cursor positioning, erasing, scroll-region, cursor movement, and the usual SGR color/style codes.
    """
    # Taken from:
    # https://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python
    return _ANSI_ESCAPE.sub('', colored_text)
