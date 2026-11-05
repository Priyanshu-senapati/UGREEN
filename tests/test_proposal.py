import re, sys
from pypdf import PdfReader
from package_rules import ROOT, read
sys.path.insert(0, str(ROOT / "proposal"))
from build_pdf import build_pdf
MD = ROOT / "proposal" / "proposal.md"
ITEMS = ["What does your Skill do?", "Who is your target user, and what is their problem?", "What is your solution?",
         "What is the main user flow?", "How is your idea different from existing tools or common AI solutions?",
         "Which UGREEN AI NAS features does your Skill use, and at which step?", "What is your technical approach?",
         "What have you built so far? What is not built yet? What still needs testing on a NAS?",
         "How will you test your Skill if you become a Finalist?",
         "What are the known limits, risks, or outside dependencies of your Skill?"]

def answers(text):
    body = text.split("## Declarations")[0]
    return re.sub(r"^#+ .*$", "", body, flags=re.M)

def test_ten_items_in_order():
    text = read(MD)
    positions = [text.index(f"## {i}. {item}") for i, item in enumerate(ITEMS, 1)]
    assert positions == sorted(positions)

def test_word_limit():
    assert len(re.findall(r"\b[\w'’-]+\b", answers(read(MD)))) <= 500

def test_tests_named_and_declarations_present():
    text = read(MD)
    for phrase in ("Core test 1", "Core test 2", "Edge test", "## Declarations", "## Third-party components and licences"):
        assert phrase in text

def test_pdf_size_and_content(tmp_path):
    pdf = build_pdf(MD, tmp_path / "p.pdf")
    assert pdf.stat().st_size <= 1_000_000
    text = "".join(p.extract_text() for p in PdfReader(pdf).pages)
    flat = " ".join(text.split())
    for item in ITEMS:
        assert item[:25] in flat, item


def test_claims_match_repo():
    text = read(MD)
    assert "without uploading anything" not in text
    claimed = int(re.search(r"(\d+) automated tests", text).group(1))
    actual = sum(read(p).count("\ndef test_") for p in (ROOT / "tests").glob("test_*.py"))
    assert claimed == actual, (claimed, actual)
