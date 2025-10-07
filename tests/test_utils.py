import pytest

from coloredstrings import utils


@pytest.mark.parametrize(
    "input_text, expected",
    [
        # no ANSI sequences -> unchanged
        ("plain text", "plain text"),

        # simple CSI color and reset sequences
        ("\x1b[31mred\x1b[0m", "red"),

        # multiple sequences interleaved with text
        ("A\x1b[1mB\x1b[22mC\x1b[4mD\x1b[24mE", "ABCDE"),

        # adjacent sequences only -> empty string
        ("\x1b[31m\x1b[0m", ""),

        # CSI sequence with multiple parameters and semicolons
        ("start\x1b[1;34;48mmid\x1b[0mend", "startmidend"),

        # sequences using final bytes other than 'm' (e.g. 'K' via CSI)
        ("line\x1b[2K\x1b[0m", "line"),

        # 7-bit C1 single-character sequence (ESC followed by a single byte in @-Z\-_)
        ("hello\x1bKworld", "helloworld"),

        # unicode and non-ASCII characters preserved
        ("привет\x1b[31mмир\x1b[0m", "приветмир"),
    ],
)
def test_strip_ansi_parametrized(input_text, expected):
    assert utils.strip_ansi(input_text) == expected


def test_incomplete_escape_sequence_is_not_removed():
    # An incomplete CSI (no final byte) should not be matched/removed by the regex,
    # so the input should remain unchanged.
    incomplete = "hello\x1b["
    assert utils.strip_ansi(incomplete) == incomplete

    # ESC at end with a single char that is not in the single-byte removal set
    # (e.g. ESC followed by a lowercase letter outside the @-Z range)
    s = "tail\x1bq"
    assert utils.strip_ansi(s) == s


def test_multiple_mixed_sequences_removed_completely():
    input_text = (
        "Start\x1b[31mred\x1b[0mMiddle\x1bKclear\x1b[1;4mstyle\x1b[0mEnd"
    )
    assert utils.strip_ansi(input_text) == "StartredMiddleclearstyleEnd"


def test_strip_ansi_accepts_empty_string():
    assert utils.strip_ansi("") == ""
