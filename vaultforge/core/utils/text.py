"""Text normalization helpers for human password behavior modeling."""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

_EMPTY_VALUES = {"", "none", "null", "skip", "n/a", "na"}
_SUFFIX_RE = re.compile(r"^(?P<word>.*?)(?P<number>\d{2,8})$")
_LEET_RE = re.compile(r"[@4310$7]")


@dataclass(frozen=True)
class NormalizedSeed:
    """A user supplied seed plus metadata used to avoid seed contamination."""

    original: str
    normalized: str
    transliterated: str | None
    category: str
    priority: float
    classification: str

    def variants(self) -> tuple[str, ...]:
        values = [self.normalized]
        if self.transliterated and self.transliterated != self.normalized:
            values.append(self.transliterated)
        return tuple(values)


def normalize_optional(value: str | None) -> str | None:
    """Normalize optional CLI input and treat explicit skip values as missing."""
    if value is None:
        return None
    cleaned = value.strip()
    if cleaned.lower() in _EMPTY_VALUES:
        return None
    return cleaned


def normalize_unicode(value: str) -> str:
    """Return a lowercase, trimmed, Unicode-normalized representation."""
    return unicodedata.normalize("NFC", value.strip().lower())


def transliterate(value: str) -> str:
    """Return an ASCII-compatible version when possible."""
    decomposed = unicodedata.normalize("NFKD", value)
    return decomposed.encode("ascii", "ignore").decode("ascii")


def classify_seed(value: str) -> str:
    """Classify seeds so mutation chains do not create artifacts like Carlos123123."""
    if _LEET_RE.search(value):
        return "mixed"
    if _SUFFIX_RE.match(value):
        return "numeric_suffix"
    if value.isdigit():
        return "numeric"
    if value.isalpha():
        return "raw_word"
    return "mixed"
