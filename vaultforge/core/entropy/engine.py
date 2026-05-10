"""Entropy and resistance estimates."""
from __future__ import annotations

import math
import string


def charset_size(password: str) -> int:
    size = 0
    if any(c in string.ascii_lowercase for c in password):
        size += 26
    if any(c in string.ascii_uppercase for c in password):
        size += 26
    if any(c in string.digits for c in password):
        size += 10
    if any(c in string.punctuation for c in password):
        size += len(string.punctuation)
    if any(ord(c) > 127 for c in password):
        size += 80
    return max(size, 1)


def entropy_bits(password: str) -> float:
    return round(len(password) * math.log2(charset_size(password)), 2)
