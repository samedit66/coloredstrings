import io
import logging

import pytest

from coloredstrings import ColorMode, StyleBuilder
from coloredstrings.logger import ColoredFormatter


@pytest.mark.parametrize("colored_first", [True, False])
def test_color_is_local_to_the_handler(monkeypatch, colored_first):
    from coloredstrings import logger

    red = StyleBuilder(mode=ColorMode.ANSI_16).red
    monkeypatch.setitem(logger._DEFAULT_LEVEL_COLORS, logging.ERROR, red)
    console, log_file = io.StringIO(), io.StringIO()
    colored = logging.StreamHandler(console)
    plain = logging.StreamHandler(log_file)
    fmt = "%(levelname)s %(message)s"
    colored.setFormatter(ColoredFormatter(fmt, colorize_msg=True))
    plain.setFormatter(logging.Formatter(fmt))
    record = logging.LogRecord("app", logging.ERROR, "", 0, "error %s", ("42",), None)
    for handler in (colored, plain) if colored_first else (plain, colored):
        handler.handle(record)
    assert console.getvalue() == f"{red('ERROR')} {red('error 42')}\n"
    assert log_file.getvalue() == "ERROR error 42\n"
    assert (record.levelname, record.msg, record.args) == ("ERROR", "error %s", ("42",))
