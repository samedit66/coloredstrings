import copy
import logging
from typing import Literal

from coloredstrings import style_builder

_sb = style_builder.StyleBuilder()

_DEFAULT_LEVEL_COLORS = {
    logging.DEBUG: _sb.rgb(100, 200, 200),
    logging.INFO: _sb.rgb(120, 200, 120),
    logging.WARNING: _sb.rgb(220, 180, 60),
    logging.ERROR: _sb.rgb(220, 80, 80),
    logging.CRITICAL: _sb.rgb(200, 40, 40),
}


class ColoredFormatter(logging.Formatter):
    """
    Logging formatter that colorizes the levelname and optionally message.
    Example:
        handler = logging.StreamHandler()
        handler.setFormatter(ColoredFormatter("%(levelname)s: %(message)s"))
    """

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: Literal["%", "{", "$"] = "%",
        colorize_level: bool = True,
        colorize_msg: bool = False,
    ) -> None:
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.colorize_level = colorize_level
        self.colorize_msg = colorize_msg

    def format(self, record: logging.LogRecord) -> str:
        record = copy.copy(record)
        color = _DEFAULT_LEVEL_COLORS.get(record.levelno)
        if color is not None:
            if self.colorize_level:
                record.levelname = color(record.levelname)
            if self.colorize_msg:
                record.msg = color(record.getMessage())
                record.args = ()

        return super().format(record)
