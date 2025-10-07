from .style_builder import StyleBuilder
from .types import ColorMode
from .utils import strip_ansi


style = StyleBuilder()

__all__ = [
    "strip_ansi",
    "style",
    "ColorMode",
    "StyleBuilder",
]
