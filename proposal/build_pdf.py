"""Render proposal/proposal.md to an A4 PDF: proposal/next-of-kin-proposal.pdf."""
from __future__ import annotations

import sys
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
STYLE = """
@page { size: A4; margin: 14mm 15mm; }
body { font-family: "Segoe UI", Arial, sans-serif; font-size: 9.6pt; line-height: 1.38; color: #1f2933; }
h1 { font-size: 17pt; margin: 0 0 2px; color: #0b4f6c; }
h1 + p { margin-top: 0; color: #52606d; }
h2 { font-size: 11pt; margin: 10px 0 3px; color: #0b4f6c; }
p, li { margin: 2px 0; }
ul, ol { margin: 2px 0 4px 18px; padding: 0; }
table { border-collapse: collapse; width: 100%; font-size: 8.6pt; margin: 4px 0; }
th, td { border: 1px solid #cbd2d9; padding: 3px 5px; text-align: left; vertical-align: top; }
th { background: #f0f4f8; }
code { font-size: 8.6pt; background: #f0f4f8; padding: 0 2px; }
"""


def build_pdf(md_path: Path, pdf_path: Path) -> Path:
    body = markdown.markdown(Path(md_path).read_text(encoding="utf-8"), extensions=["tables"])
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{STYLE}</style></head><body>{body}</body></html>"
    pdf_path = Path(pdf_path)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.set_content(html, wait_until="load")
        page.pdf(path=str(pdf_path), format="A4", print_background=True)
        browser.close()
    return pdf_path


def main() -> int:
    out = build_pdf(HERE / "proposal.md", HERE / "next-of-kin-proposal.pdf")
    print(f"Built {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
