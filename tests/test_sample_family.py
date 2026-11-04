import re, sys
from datetime import date
from pathlib import Path
import pytest
from pypdf import PdfReader
sys.path.insert(0, str(Path(__file__).parents[1] / "sample-family"))
import family, generate
from package_rules import REAL_BRANDS

@pytest.fixture(scope="session")
def out(tmp_path_factory):
    root = tmp_path_factory.mktemp("fam")
    generate.generate(root, date(2026, 11, 10))
    return root

def pdf_text(path): return "".join(page.extract_text() for page in PdfReader(path).pages)

def test_all_documents_exist(out):
    for doc in family.DOCUMENTS:
        assert (out / doc.relpath).exists(), doc.relpath

def test_pdfs_are_sample_and_fictional(out):
    for pdf in out.rglob("*.pdf"):
        text = pdf_text(pdf)
        assert "SAMPLE" in text, pdf
        for brand in REAL_BRANDS:
            assert not re.search(rf"\b{re.escape(brand)}\b", text), (pdf, brand)

def test_planted_conflict_review_and_gap(out):
    docs = out / "Papa Documents"
    policy, letter = pdf_text(docs / "life-policy.pdf"), pdf_text(docs / "nomination-change-letter.pdf")
    assert family.LIFE_POLICY_NO in policy and "Sunita Sharma" in policy
    assert family.LIFE_POLICY_NO in letter and "Priya Sharma" in letter
    assert "Not registered" in pdf_text(docs / "mutual-fund-statement.pdf")
    assert not list(out.rglob("*will*"))

def test_premium_notice_date_and_hindi_ppo():
    assert "22 Nov 2026" in generate.render_html("premium_notice", date(2026, 11, 10))
    assert re.search(r"[ऀ-ॿ]", generate.render_html("pension_order_hi", date(2026, 11, 10)))

def test_health_policy_has_cashless_section(out):
    text = pdf_text(out / "Papa Documents" / "health-policy.pdf")
    assert "Cashless claim" in text and family.TPA_PHONE in text

def test_photos_decoys_duplicate_and_secrets(out):
    photos = out / "Phone Backup" / "WhatsApp Images"
    assert len(list(photos.glob("decoy-*.jpg"))) == 30
    assert (photos / "life-policy-page1-photo.jpg").exists()
    assert family.PASSWORD_SECRET in (out / "Papa Documents" / "passwords.txt").read_text()
    assert list((out / "Empty Folder").iterdir()) == []
