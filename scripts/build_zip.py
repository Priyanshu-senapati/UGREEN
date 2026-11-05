"""Build the Round 1 Skill package ZIP: dist/next-of-kin.zip.

The ZIP holds one top folder, next-of-kin/, with SKILL.md and references/*.md only,
in sorted order with fixed timestamps so the same sources always give the same bytes.
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOP_FOLDER = "next-of-kin"
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def _allowed(relative: Path) -> bool:
    parts = relative.parts
    if parts == ("SKILL.md",):
        return True
    return len(parts) == 2 and parts[0] == "references" and relative.suffix == ".md"


def build_zip(skill_dir: Path, out_zip: Path) -> Path:
    skill_dir, out_zip = Path(skill_dir), Path(out_zip)
    files = sorted(path for path in skill_dir.rglob("*") if path.is_file())
    refused = [path.relative_to(skill_dir).as_posix() for path in files if not _allowed(path.relative_to(skill_dir))]
    if refused:
        raise ValueError(f"not allowed in the Skill package: {refused}")
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_zip, "w") as archive:
        for path in files:
            info = zipfile.ZipInfo(f"{TOP_FOLDER}/{path.relative_to(skill_dir).as_posix()}", FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    return out_zip


def main() -> int:
    out = build_zip(ROOT / "skill" / TOP_FOLDER, ROOT / "dist" / f"{TOP_FOLDER}.zip")
    print(f"Built {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
