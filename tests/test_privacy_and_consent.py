from package_rules import REFS_DIR, read, checker_violations
DOC = REFS_DIR / "privacy-and-consent.md"
CLAUSES = ("2.4", "4.1", "4.2", "4.3", "4.5", "4.6", "5.3", "6.3", "6.4", "7.1", "7.3", "9.3", "10.1", "11.4")


def test_every_clause_mapped():
    text = read(DOC)
    for clause in CLAUSES:
        assert f"| {clause}" in text or f", {clause}" in text, clause


def test_consent_script_questions():
    text = read(DOC)
    for phrase in ("present and consenting", "local model", "cloud model", "which folders",
                   "voice notes", "Private Map", "Family Continuity Map"):
        assert phrase in text, phrase


def test_not_sure_treated_as_cloud():
    assert 'Treat "not sure" the same as a cloud model' in read(DOC)


def test_three_honest_limits():
    text = read(DOC)
    for phrase in ("cannot verify where the AI runs", "cannot check which other users can read a folder",
                   "existing photo text index"):
        assert phrase in text, phrase


def test_no_workaround_rule_and_clean():
    text = read(DOC)
    assert "no workaround" in text
    assert checker_violations(text) == []


def test_recommends_local_model():
    assert "recommend switching to the local model" in read(DOC)
