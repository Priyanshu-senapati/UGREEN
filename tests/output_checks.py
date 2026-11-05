"""Deterministic checks over simulated Chaabi run results."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "sample-family"))
import family  # noqa: E402

RESULT_HEADINGS = ("Transcript", "Saved artifact", "End-of-run lists")
LABEL_WORDS = re.compile(r"\b(?:Verified|Unverified|Conflict|Missing)\b")
DELEGATE = re.compile(r"delegate --target (\S+) --instruction '([^']*)'")
CARD_TITLE = re.compile(r"^>?\s*\*\*A\d+ · ")


def section(text: str, heading: str) -> str:
    """Text under one of the result-file headings, up to the next result-file heading."""
    pattern = r"^## (" + "|".join(map(re.escape, RESULT_HEADINGS)) + r")\s*$"
    parts = re.split(pattern, text, flags=re.M)
    for index in range(1, len(parts), 2):
        if parts[index] == heading:
            return parts[index + 1]
    raise KeyError(heading)


def delegates(text: str) -> list[tuple[str, str]]:
    return DELEGATE.findall(text)


def full_identifiers_found(text: str) -> list[str]:
    found = [ident for ident in family.FULL_IDENTIFIERS if ident in text]
    found += re.findall(r"(?<!\d)\d{12}(?!\d)", text)
    found += re.findall(r"(?<!\d)\d{4} \d{4} \d{4}(?!\d)", text)
    found += re.findall(r"\b[A-Z]{5}\d{4}[A-Z]\b", text)
    return sorted(set(found))


def _map_section(text: str, number: int) -> str:
    match = re.search(rf"^## {number}\. .*?$(.*?)(?=^## \d+\. |\Z)", text, flags=re.M | re.S)
    return match.group(1) if match else ""


def fact_lines_missing_source(text: str) -> list[str]:
    """Fact lines in the Item cards section that carry a label but no S-number source."""
    missing = []
    for line in _map_section(text, 4).splitlines():
        stripped = line.lstrip("> ").strip()
        if stripped.startswith("- ") and LABEL_WORDS.search(stripped) and not re.search(r"\bS\d+\b", stripped):
            missing.append(stripped)
    return missing


def item_card(text: str, needle: str) -> str:
    lines = text.splitlines()
    for start, line in enumerate(lines):
        if CARD_TITLE.match(line) and needle.lower() in line.lower():
            end = start + 1
            while end < len(lines) and not CARD_TITLE.match(lines[end]) and not lines[end].startswith("## "):
                end += 1
            return "\n".join(lines[start:end])
    return ""


def source_id(text: str, filename_fragment: str) -> str:
    for line in _map_section(text, 7).splitlines():
        if filename_fragment in line:
            match = re.search(r"\bS\d+\b", line)
            if match:
                return match.group(0)
    return ""
