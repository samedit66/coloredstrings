import math


def rgb_to_ansi_256(r: int, g: int, b: int) -> int:
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))

    gray_tol = 1
    is_gray = (r == g == b) or (abs(r - g) <= gray_tol and abs(r - b) <= gray_tol)

    if is_gray:
        if r < 8:
            return 16
        if r > 248:
            return 231

        val = ((r - 8) / 247.0) * 24.0
        return int(math.floor(val + 0.5)) + 232

    r6 = int(math.floor((r / 255.0) * 5.0 + 0.5))
    g6 = int(math.floor((g / 255.0) * 5.0 + 0.5))
    b6 = int(math.floor((b / 255.0) * 5.0 + 0.5))

    r6 = max(0, min(5, r6))
    g6 = max(0, min(5, g6))
    b6 = max(0, min(5, b6))

    return 16 + (36 * r6) + (6 * g6) + b6


def ansi_256_to_ansi_16(code: int, eps: float = 1e-9) -> int:
    if code < 8:
        return 30 + code
    if code < 16:
        return 90 + (code - 8)

    if code >= 232:
        v = (((code - 232) * 10) + 8) / 255.0
        r = g = b = v
    else:
        t = code - 16
        r6 = int(math.floor(t / 36))
        rem = t % 36
        g6 = int(math.floor(rem / 6))
        b6 = rem % 6

        r = r6 / 5.0
        g = g6 / 5.0
        b = b6 / 5.0

    value = max(r, g, b) * 2.0

    if value < eps:
        return 30

    r_bit = int(math.floor(r + 0.5))
    g_bit = int(math.floor(g + 0.5))
    b_bit = int(math.floor(b + 0.5))

    bits = (b_bit << 2) | (g_bit << 1) | r_bit
    result = 30 + bits

    if abs(value - 2.0) < eps:
        result += 60

    return result


def rgb_to_ansi_16(r: int, g: int, b: int) -> int:
    return ansi_256_to_ansi_16(rgb_to_ansi_256(r, g, b))
