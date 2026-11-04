"""Shared constants and helpers for the Next of Kin package tests."""
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skill" / "next-of-kin"
REFS_DIR = SKILL_DIR / "references"

LABELS = ("Verified", "Unverified", "Conflict", "Missing")
FINDING_TYPES = (
    "Review", "Gap", "Expiring", "Not searched", "Not cross-checked",
    "Unreadable", "Not translated", "Not transcribed",
)
SOURCE_LABELS = (
    "Your policy says", "General guide suggests",
    "Confirm with the institution", "Needs professional advice",
)
MAP_SECTIONS = (
    "Header", "Setup record", "At a glance", "Item cards",
    "People and contacts", "Open findings", "Sources and changes",
)
REAL_BRANDS = (
    "LIC", "SBI", "HDFC", "ICICI", "Axis", "Kotak", "PNB", "Canara",
    "Star Health", "Bajaj", "Tata AIA", "Max Life", "Aditya Birla",
)

# Copied from uliya-skill-kit 0.7.3 scripts/check-lib.mjs.
CHECKER_PATTERNS = {
    "runtime fence": r"^```\s*(?:bash|sh|shell|python|py|javascript|js|node|typescript|ts)\b",
    "remote download": r"\b(?:curl|wget)\b|https?://\S+\s*\|\s*(?:sh|bash)\b",
    "direct file api": r"\b(?:readFile|writeFile|unlink|pathlib|fs\.|open\s*\(|cp\s+|mv\s+|rm\s+|cat\s+)\b",
    "nas path": r"(?:^|[\s\"'])/(?:nas|mnt|volume\d*|shares?)(?:/|\b)",
    "bypass": r"\b(?:bypass|skip|disable|ignore)\b[^\n]{0,40}\b(?:gateway|approval|permission|audit)\b",
    "placeholder": r"replace-with-|\bTODO\b|\bTBD\b",
    "credential": r"\b(?:password|passwd|token|api[_-]?key|secret)\s*[:=]\s*[\"'][^\"'\n]+[\"']",
}
_DELEGATE_EXEMPT = {"direct file api", "nas path"}
_COMPILED = {name: re.compile(pattern, re.I) for name, pattern in CHECKER_PATTERNS.items()}


def read(path: Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def checker_violations(text: str) -> list[str]:
    found = []
    for number, line in enumerate(text.splitlines(), 1):
        for name, pattern in _COMPILED.items():
            if name in _DELEGATE_EXEMPT and "delegate --" in line:
                continue
            if pattern.search(line):
                found.append(f"{name}: line {number}")
    return found


def run_kit_checker(skill_dir: Path) -> dict:
    kit = Path(os.environ.get("UGREEN_KIT_DIR", Path.home() / "tools" / "uliya-skill-kit"))
    completed = subprocess.run(
        ["node", str(kit / "scripts" / "check-skill.mjs"), str(skill_dir)],
        capture_output=True, text=True, encoding="utf-8",
    )
    if completed.returncode == 2:
        raise RuntimeError(completed.stderr)
    return json.loads(completed.stdout)
