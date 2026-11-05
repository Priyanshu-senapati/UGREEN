import re
from package_rules import REFS_DIR, read, checker_violations
DOC = REFS_DIR / "execution-contract.md"
FIELDS = ("Precondition", "Permissions", "Agent and action", "Expected output",
          "Approval", "Failure condition", "Recovery", "Continue")
OPERATIONS = {
    1: "Skill", 2: "`ug-filesystem` `stat`", 3: "`ug-filesystem` `find`", 4: "`ug-photo` `search-picture`",
    5: "`ug-document` `extract`", 6: "`ug-photo` `vision-vlm`", 7: "`ug-document` `translate`",
    8: "`ug-knowledge` `audio-transcription`", 9: "`ug-document` `reconcile`",
    10: "`ug-knowledge` `collect-evidence`", 11: "Skill", 12: "`ug-knowledge` `save-text`",
    13: "`ug-filesystem` `stat`", 14: "`ug-filemgr` `tag-add-file`", 15: "`ug-filesystem` `find`",
    16: "`ug-filesystem` `find`", 17: "`ug-knowledge` `collect-evidence`", 18: "`ug-document` `qa`",
    19: "`ug-knowledge` `save-text`",
}

def blocks(text):
    parts = re.split(r"^### (\d+)\. ", text, flags=re.M)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}

def test_nineteen_operations_with_eight_fields():
    found = blocks(read(DOC))
    assert sorted(found) == list(range(1, 20))
    for number, body in found.items():
        for field in FIELDS:
            assert f"**{field}:**" in body, (number, field)

def test_each_operation_names_its_action():
    found = blocks(read(DOC))
    for number, action in OPERATIONS.items():
        assert action in found[number], (number, action)

def test_ground_rules_statuses_and_not_searched():
    text = read(DOC)
    for token in ("completed", "failed", "cancelled", "waiting_user", "waiting_approval", "Not searched", "Partial"):
        assert token in text, token
    assert "done · failed · not checked" in text

def test_eight_approval_points():
    section = read(DOC).split("## Approval points", 1)[1]
    assert len(re.findall(r"^\d+\. ", section, flags=re.M)) == 8

def test_clean():
    assert checker_violations(read(DOC)) == []


def test_photo_only_families_still_reach_photo_search():
    assert "operations 3 and 4 both find nothing" in blocks(read(DOC))[3]


def test_failed_qa_kept_apart_from_not_stated():
    body = blocks(read(DOC))[18]
    assert "Could not read" in body and "Not checked" in body
