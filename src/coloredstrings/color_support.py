import os
import platform
import re
import sys
import typing

from coloredstrings import types


def detect_color_support(stream: typing.TextIO = sys.stdout) -> types.ColorMode:
    """
    Detect the best ColorMode available for the given stream and environment.

    The function tries, in order:
     - NO_COLOR environment variable
     - explicit FORCE_COLOR environment override
     - TERM == "dumb" => NO_COLOR
     - Windows version heuristics
     - CI / TEAMCITY heuristics
     - non-tty -> NO_COLOR
     - COLORTERM / TERM_PROGRAM / TERM heuristics
     - fallback -> NO_COLOR
    """
    # 0) https://no-color.org/
    if os.environ.get("NO_COLOR"):
        return types.ColorMode.NO_COLOR

    # 1) explicit override
    forced = _get_env_force_color()
    if forced is not None:
        return forced

    # 2) quick checks
    if os.environ.get("TERM", "").lower() == "dumb":
        return types.ColorMode.NO_COLOR

    # 3) Windows heuristics
    if platform.system() == "Windows":
        # platform.version() may be something like "10.0.19041"
        try:
            parts = platform.version().split(".")
            if len(parts) >= 3:
                major = int(parts[0])
                build = int(parts[2])
                # Windows 10+ and build numbers that support features
                if major >= 10:
                    if build >= 14931:
                        return types.ColorMode.TRUE_COLOR
                    if build >= 10586:
                        return types.ColorMode.EXTENDED_256
        except Exception:
            # If parsing fails, fall back to ANSI as conservative default for Windows.
            pass
        return types.ColorMode.ANSI_16

    # 4) CI detection
    if "CI" in os.environ:
        # common CI providers that support basic color
        known_ci_vars = [
            "TRAVIS",
            "CIRCLECI",
            "APPVEYOR",
            "GITLAB_CI",
            "GITHUB_ACTIONS",
            "BUILDKITE",
            "DRONE",
        ]
        if (
            any(name in os.environ for name in known_ci_vars)
            or os.environ.get("CI_NAME") == "codeship"
        ):
            return types.ColorMode.ANSI_16
        # unknown CI - be conservative
        return types.ColorMode.NO_COLOR

    # 5) TeamCity special-case
    if "TEAMCITY_VERSION" in os.environ:
        team_city_version = os.environ["TEAMCITY_VERSION"]
        m = re.search(r"^(9\.(0*[1-9]\d*)\.|\d{2,}\.)", team_city_version)
        if m:
            return types.ColorMode.ANSI_16
        return types.ColorMode.NO_COLOR

    # 6) isatty check (if stream doesn't have isatty, assume not a tty)
    is_tty = False
    try:
        is_tty = bool(getattr(stream, "isatty", lambda: False)())
    except Exception:
        is_tty = False

    if not is_tty:
        return types.ColorMode.NO_COLOR

    # 7) COLORTERM indicating truecolor
    colorterm = os.environ.get("COLORTERM", "").lower()
    if "truecolor" in colorterm or "24bit" in colorterm:
        return types.ColorMode.TRUE_COLOR

    # 8) TERM_PROGRAM heuristics (iTerm, Apple Terminal, etc.)
    if "TERM_PROGRAM" in os.environ:
        term_program = os.environ.get("TERM_PROGRAM", "")
        term_program_version_str = os.environ.get("TERM_PROGRAM_VERSION")
        term_program_version = None
        try:
            if term_program_version_str:
                term_program_version = int(term_program_version_str.split(".")[0])
        except Exception:
            # if version parsing fails, fall back to ANSI_16
            return types.ColorMode.ANSI_16

        if term_program == "iTerm.app":
            if term_program_version is not None:
                return (
                    types.ColorMode.TRUE_COLOR
                    if term_program_version >= 3
                    else types.ColorMode.EXTENDED_256
                )
            return types.ColorMode.ANSI_16
        if term_program == "Apple_Terminal":
            return types.ColorMode.EXTENDED_256
        return types.ColorMode.ANSI_16

    # 9) TERM environment checks
    term = os.environ.get("TERM", "")
    if term and re.search(r"-256(color)?$", term):
        return types.ColorMode.EXTENDED_256

    # match common terminal names that usually support ANSI basic colors
    if term and re.search(
        r"^(screen|xterm|vt100|vt220|rxvt)|color|ansi|cygwin|linux", term
    ):
        return types.ColorMode.ANSI_16

    # 10) generic COLORTERM presence -> basic ANSI
    if "COLORTERM" in os.environ:
        return types.ColorMode.ANSI_16

    # 11) fallback
    return types.ColorMode.NO_COLOR


def _get_env_force_color() -> typing.Optional[types.ColorMode]:
    """
    Interpret FORCE_COLOR environment variable.

    Accepted values:
      - unset -> None (no forcing)
      - "" or "true" (case-insensitive) -> ANSI_16
      - "false" -> NO_COLOR
      - integer 0,1,2,3 -> NO_COLOR, ANSI_16, EXTENDED_256, TRUE_COLOR respectively
      - other -> None (ignored)
    """
    raw = os.environ.get("FORCE_COLOR")
    if raw is None:
        return None

    val = raw.strip().lower()

    # empty string or "true" => basic ANSI
    if val == "" or val == "true":
        return types.ColorMode.ANSI_16

    if val == "false":
        return types.ColorMode.NO_COLOR

    # numeric values: 0 -> none, 1 -> basic, 2 -> 256, 3+ -> truecolor
    try:
        n = int(val)
    except ValueError:
        return None

    if n <= 0:
        return types.ColorMode.NO_COLOR
    if n == 1:
        return types.ColorMode.ANSI_16
    if n == 2:
        return types.ColorMode.EXTENDED_256
    return types.ColorMode.TRUE_COLOR
