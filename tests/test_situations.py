import re
from package_rules import REFS_DIR, read, SOURCE_LABELS, checker_violations
DOC = REFS_DIR / "situations.md"
SITUATIONS = ("Temporarily unavailable", "Long-term memory or decision-making difficulty", "Passed away")
PHASES = ("First 24 hours", "First week", "First 30 days", "Later")
ITEM_TYPES = ("life insurance", "health insurance", "bank account", "fixed deposit", "property",
              "mutual fund", "pension", "loan", "bank locker", "will", "vehicle")

def situation(text, name):
    return text.split(f"## {name}", 1)[1].split("\n## ", 1)[0]

def test_three_situations_four_phases():
    text = read(DOC)
    for name in SITUATIONS:
        body = situation(text, name)
        positions = [body.index(f"### {p}") for p in PHASES]
        assert positions == sorted(positions), name

def test_every_step_has_exactly_one_source_label():
    text = read(DOC)
    for name in SITUATIONS:
        for line in situation(text, name).splitlines():
            if line.startswith("- "):
                assert sum(label in line for label in SOURCE_LABELS) == 1, line

def test_item_types_covered():
    text = read(DOC).lower()
    for item in ITEM_TYPES:
        assert item in text, item

def test_legal_boundaries():
    text = read(DOC)
    assert "general guide, not legal or financial advice" in text
    assert "power of attorney" in situation(text, SITUATIONS[1])
    passed = situation(text, SITUATIONS[2])
    assert passed.count("Needs professional advice") >= 3
    assert "does not give anyone legal or financial authority" in text

def test_clean():
    assert checker_violations(read(DOC)) == []
