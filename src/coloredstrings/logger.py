import logging
from typing import Literal, Optional

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
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: Literal["%", "{", "$"] = "%",
        colorize_level: bool = True,
        colorize_msg: bool = False,
    ) -> None:
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.colorize_level = colorize_level
        self.colorize_msg = colorize_msg

    def format(self, record: logging.LogRecord) -> str:
        levelname = record.levelname
        if self.colorize_level and record.levelno in _DEFAULT_LEVEL_COLORS:
            level_rgb = _DEFAULT_LEVEL_COLORS[record.levelno]
            record.levelname = level_rgb(levelname)

        msg = record.getMessage()
        if self.colorize_msg:
            if record.levelno in _DEFAULT_LEVEL_COLORS:
                msg_rgb = _DEFAULT_LEVEL_COLORS[record.levelno]
                record.msg = msg_rgb(msg)
                record.args = ()

        return super().format(record)
