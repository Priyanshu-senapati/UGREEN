import re
from package_rules import ROOT, SKILL_DIR, read
from test_privacy_and_consent import CLAUSES

def test_every_clause_has_evidence_that_exists():
    rows = re.findall(r"^\| ([\d.]+) \| [^|]+ \| `([^`#]+)#([^`]+)` \|$", read(ROOT / "docs" / "rules-audit.md"), re.M)
    assert {clause for clause, _, _ in rows} == set(CLAUSES)
    for _, file, heading in rows:
        assert heading in read(SKILL_DIR / file), (file, heading)
