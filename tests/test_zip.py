import zipfile, shutil, sys
import pytest
from package_rules import ROOT, SKILL_DIR, run_kit_checker
sys.path.insert(0, str(ROOT / "scripts"))
from build_zip import build_zip

def test_zip_layout_and_limits(tmp_path):
    z = build_zip(SKILL_DIR, tmp_path / "next-of-kin.zip")
    infos = zipfile.ZipFile(z).infolist()
    names = sorted(i.filename for i in infos)
    assert names[0] == "next-of-kin/SKILL.md" and all(n.startswith("next-of-kin/") for n in names)
    assert len(names) == 6 and all(i.file_size <= 1_048_576 for i in infos)
    assert z.stat().st_size <= 10 * 1_048_576

def test_extracted_zip_passes_kit_checker(tmp_path):
    z = build_zip(SKILL_DIR, tmp_path / "next-of-kin.zip")
    zipfile.ZipFile(z).extractall(tmp_path / "x")
    assert run_kit_checker(tmp_path / "x" / "next-of-kin")["status"] == "static-pass"

def test_refuses_non_markdown(tmp_path):
    copy = tmp_path / "next-of-kin"
    shutil.copytree(SKILL_DIR, copy)
    (copy / "notes.txt").write_text("x")
    with pytest.raises(ValueError):
        build_zip(copy, tmp_path / "bad.zip")
