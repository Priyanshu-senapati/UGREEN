from package_rules import REFS_DIR, read, LABELS, FINDING_TYPES, MAP_SECTIONS, REAL_BRANDS, checker_violations
import re
DOC = REFS_DIR / "family-map-format.md"


def test_seven_sections_in_order():
    text = read(DOC)
    positions = [text.index(f"## {i}. {name}") for i, name in enumerate(MAP_SECTIONS, 1)]
    assert positions == sorted(positions)


def test_defines_labels_and_findings():
    text = read(DOC)
    for word in LABELS + FINDING_TYPES:
        assert f"**{word}**" in text, word


def test_masking_and_never_copied():
    text = read(DOC)
    assert "last 4 characters" in text and "XXXX-4821" in text
    for item in ("passwords", "PINs", "OTPs", "CVVs", "full card numbers", "net-banking IDs"):
        assert item in text, item


def test_versioned_file_naming():
    text = read(DOC)
    assert "Family-Map_YYYY-MM-DD.md" in text and "_HHMM" in text and "never overwritten" in text


def test_expiring_window_and_gap_wording():
    text = read(DOC)
    assert "30 days" in text and "not found in the folders you shared" in text


def test_card_title_format_and_voice_only_items():
    text = read(DOC)
    assert "**A3 · Life insurance: Jeevan Suraksha Life**" in text
    assert "Items mentioned only in a voice note get their own card" in text


def test_fictional_institutions_only():
    text = read(DOC)
    for brand in REAL_BRANDS:
        assert not re.search(rf"\b{re.escape(brand)}\b", text), brand


def test_kit_checker_patterns_clean():
    assert checker_violations(read(DOC)) == []
