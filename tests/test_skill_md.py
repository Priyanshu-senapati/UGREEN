import re
from package_rules import SKILL_DIR, REFS_DIR, read, checker_violations, run_kit_checker
SKILL = SKILL_DIR / "SKILL.md"
HEADINGS = ["# Goal", "# Required input", "# Generation-time capability evidence", "# Workflow", "# Completion and failure"]
EVIDENCE = ["- `ug-filesystem` → `file-agent`", "- `ug-filemgr` → `file-agent`", "- `ug-photo` → `photo-agent`",
            "- `ug-document` → `document-agent`", "- `ug-knowledge` → `knowledge-agent`"]
REFS = ["family-map-format", "privacy-and-consent", "execution-contract", "situations", "disclosures"]
AGENTS = {"file-agent", "photo-agent", "document-agent", "knowledge-agent"}
DELEGATE = re.compile(r"`delegate --target (\S+) --instruction '([^']*)'`")

def frontmatter(text):
    head = text.split("---", 2)[1]
    return dict(line.split(": ", 1) for line in head.strip().splitlines())

def test_kit_checker_static_pass():
    result = run_kit_checker(SKILL_DIR)
    assert result["status"] == "static-pass", result["diagnostics"]
    assert result["summary"]["errors"] == 0 and result["summary"]["warnings"] == 0

def test_frontmatter():
    fm = frontmatter(read(SKILL))
    assert set(fm) == {"name", "description"} and fm["name"] == "next-of-kin"
    assert len(fm["description"]) <= 1024 and "Use when" in fm["description"]

def test_headings_evidence_and_links():
    text = read(SKILL)
    assert [line for line in text.splitlines() if line.startswith("# ")] == HEADINGS
    assert [line for line in text.splitlines() if line.startswith("- `ug-")] == EVIDENCE
    for name in REFS:
        assert f"](references/{name}.md)" in text, name

def test_delegates_are_clean_and_cover_every_agent():
    found = DELEGATE.findall(read(SKILL))
    assert {target for target, _ in found} == AGENTS
    for target, instruction in found:
        assert not re.search(r"[<>`|]", instruction), instruction

def test_consent_before_first_delegate_and_not_sure_rule():
    text = read(SKILL)
    assert text.index("explicit consent") < text.index("delegate --")
    assert 'Treat "not sure" the same as a cloud model' in text

def test_review_focus_rules():
    text = read(SKILL)
    assert "leave the language unset" in text
    assert "Family-Map_YYYY-MM-DD" in text and "_HHMM" in text and "never overwrite" in text
    assert "batches of at most 60 files" in text
    assert "empty list" in text and "real result" in text

def test_transcribe_before_translate():
    text = read(SKILL)
    assert text.index("**Transcribe voice notes.**") < text.index("**Translate Hindi sentences.**")


def test_readiness_change_types_and_freshness_header():
    text = read(SKILL)
    for change in ("new file", "file modified", "fact changed", "conflict resolved", "new conflict"):
        assert change in text, change
    assert text.count("Map last updated") >= 2 and "Gaps to fill now" in text

def test_three_conversations_three_situations_and_scope():
    text = read(SKILL)
    for heading in ("## Conversation 1: Set up Next of Kin", "## Conversation 2: Check our readiness",
                    "## Conversation 3: What if someone is unavailable"):
        assert heading in text
    for situation in ("Temporarily unavailable", "Long-term memory or decision-making difficulty", "Passed away"):
        assert situation in text
    for out_of_scope in ("does not store passwords", "not legal or financial advice", "does not change who can access"):
        assert out_of_scope in text

def test_body_length_and_clean():
    text = read(SKILL)
    assert len(text.split("---", 2)[2].splitlines()) <= 500
    for path in [SKILL, *REFS_DIR.glob("*.md")]:
        assert checker_violations(read(path)) == [], path

def test_disclosures():
    text = read(REFS_DIR / "disclosures.md")
    for heading in ("## Third-party components", "## Licences", "## AI tools used", "## Work done during the hackathon"):
        assert heading in text
    assert "uliya-skill-kit 0.7.3" in text and "Claude Code" in text
