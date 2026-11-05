"""Generate the synthetic Sharma family dataset used to test Chaabi.

Usage:
    python sample-family/generate.py --out sample-family/out --today 2026-11-10 [--with-audio]
"""
from __future__ import annotations

import argparse
import asyncio
import random
import sys
from datetime import date, timedelta
from pathlib import Path
from string import Template

from PIL import Image, ImageDraw, ImageFilter
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import family  # noqa: E402

TEMPLATES = HERE / "templates"
ACCENTS = {
    "life_policy": "#0b6e4f", "life_policy_page1": "#0b6e4f", "nomination_change_letter": "#0b6e4f",
    "premium_notice": "#0b6e4f", "health_policy": "#1d4e89", "property_sale_deed": "#5c3d2e",
    "mutual_fund_statement": "#7a2e8e", "home_loan_statement": "#b4580c", "pension_order_hi": "#8a1c1c",
    "fd_receipt": "#173f5f",
}
TTS_VOICE = "hi-IN-MadhurNeural"


def _fmt(day: date) -> str:
    return day.strftime("%d %b %Y")


def _values(today: date) -> dict[str, str]:
    return {
        "owner": family.OWNER,
        "wife": family.FAMILY["wife"],
        "daughter": family.FAMILY["daughter"],
        "son": family.FAMILY["son"],
        "inst_life": family.INSTITUTIONS["life"],
        "inst_bank": family.INSTITUTIONS["bank"],
        "inst_health": family.INSTITUTIONS["health"],
        "inst_mf": family.INSTITUTIONS["mf"],
        "inst_loan": family.INSTITUTIONS["home_loan"],
        "life_policy_no": family.LIFE_POLICY_NO,
        "health_policy_no": family.HEALTH_POLICY_NO,
        "fd_no": family.FD_NO,
        "loan_no": family.LOAN_NO,
        "mf_folio": family.MF_FOLIO,
        "aadhaar": family.AADHAAR_FAKE,
        "tpa_phone": family.TPA_PHONE,
        "agent": family.AGENT,
        "agent_phone": family.AGENT_PHONE,
        "today": _fmt(today),
        "premium_due": _fmt(family.premium_due(today)),
        "statement_date": _fmt(today - timedelta(days=10)),
    }


def render_html(template: str, today: date) -> str:
    """Return the full HTML page for one sample document."""
    body = Template((TEMPLATES / f"{template}.html").read_text(encoding="utf-8")).substitute(_values(today))
    base = Template((TEMPLATES / "_base.html").read_text(encoding="utf-8"))
    return base.substitute(
        title=template.replace("_", " ").title(),
        accent=ACCENTS.get(template, "#334e68"),
        body=body,
    )


def phone_photo(src: Path, dst: Path) -> None:
    """Turn a clean render into something that looks like a phone photo of paper."""
    rng = random.Random(src.name)
    page = Image.open(src).convert("RGB")
    pad = 70
    table = Image.new("RGB", (page.width + 2 * pad, page.height + 2 * pad), (176, 150, 120))
    table.paste(page, (pad, pad))
    angle = rng.uniform(2, 4) * rng.choice((-1, 1))
    tilted = table.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=(150, 125, 100))
    tilted = tilted.filter(ImageFilter.GaussianBlur(0.8))
    width, height = tilted.size
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).ellipse((-width * 0.15, -height * 0.15, width * 1.15, height * 1.15), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(min(width, height) // 8))
    shade = Image.new("RGB", (width, height), (40, 35, 30))
    Image.composite(tilted, shade, mask).save(dst, "JPEG", quality=82)


def make_decoys(folder: Path, n: int = 30) -> list[Path]:
    """Procedural scenery and food photos with no text in them."""
    paths = []
    for index in range(1, n + 1):
        rng = random.Random(index)
        img = Image.new("RGB", (800, 600))
        draw = ImageDraw.Draw(img)
        if index % 3:
            top = (rng.randint(60, 140), rng.randint(120, 190), rng.randint(200, 255))
            bottom = (rng.randint(200, 255), rng.randint(170, 220), rng.randint(120, 180))
            for y in range(600):
                t = y / 599
                draw.line([(0, y), (800, y)], fill=tuple(int(top[k] * (1 - t) + bottom[k] * t) for k in range(3)))
            sun_x, sun_y = rng.randint(100, 700), rng.randint(60, 200)
            draw.ellipse((sun_x - 40, sun_y - 40, sun_x + 40, sun_y + 40), fill=(255, 220, 120))
            for layer in range(3):
                base_y = 380 + layer * 70
                points = [(0, 600)] + [(x, base_y - rng.randint(0, 90)) for x in range(0, 801, 100)] + [(800, 600)]
                draw.polygon(points, fill=(40 + layer * 20, 90 + layer * 30, 50 + layer * 10))
        else:
            draw.rectangle((0, 0, 800, 600), fill=(rng.randint(90, 140), rng.randint(60, 90), rng.randint(40, 60)))
            draw.ellipse((150, 75, 650, 525), fill=(245, 245, 240))
            for _ in range(rng.randint(4, 8)):
                cx, cy, r = rng.randint(260, 540), rng.randint(190, 410), rng.randint(25, 60)
                draw.ellipse((cx - r, cy - r, cx + r, cy + r),
                             fill=(rng.randint(150, 255), rng.randint(60, 200), rng.randint(0, 80)))
        path = folder / f"decoy-{index:02d}.jpg"
        img.filter(ImageFilter.GaussianBlur(1)).save(path, "JPEG", quality=85)
        paths.append(path)
    return paths


def _passwords_text() -> str:
    return (
        f"Net banking ({family.INSTITUTIONS['bank']})\n"
        "user: rsharma64\n"
        f"password: {family.PASSWORD_SECRET}\n"
    )


def _voice_scripts() -> dict[str, str]:
    text = (HERE / "voice-notes.md").read_text(encoding="utf-8")
    scripts = {}
    for chunk in text.split("\n## ")[1:]:
        heading, _, body = chunk.partition("\n")
        scripts[heading.split()[0]] = body.strip()
    return scripts


def _make_audio(out: Path) -> list[Path]:
    import edge_tts

    paths: list[Path] = []

    async def run() -> None:
        for name, script in _voice_scripts().items():
            dst = out / family.VOICE / f"{name}.mp3"
            await edge_tts.Communicate(script, TTS_VOICE).save(str(dst))
            paths.append(dst)

    asyncio.run(run())
    return paths


def generate(out: Path, today: date, with_audio: bool = False) -> list[Path]:
    """Write the whole dataset under `out` and return the files written."""
    out = Path(out)
    for folder in (family.PAPA, family.PHOTOS, family.VOICE, family.EMPTY):
        (out / folder).mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 900, "height": 1200}, device_scale_factor=1.5)
        for doc in family.DOCUMENTS:
            dst = out / doc.relpath
            if doc.kind == "text":
                dst.write_text(_passwords_text(), encoding="utf-8")
            else:
                page.set_content(render_html(doc.template, today), wait_until="load")
                if doc.kind == "pdf":
                    page.pdf(path=str(dst), format="A4", print_background=True)
                elif dst.suffix == ".png":
                    page.screenshot(path=str(dst), full_page=True)
                else:
                    render = dst.with_suffix(".render.png")
                    page.screenshot(path=str(render), full_page=True)
                    phone_photo(render, dst)
                    render.unlink()
            written.append(dst)
        browser.close()
    written += make_decoys(out / family.PHOTOS)
    if with_audio:
        written += _make_audio(out)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE / "out")
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    parser.add_argument("--with-audio", action="store_true")
    args = parser.parse_args(argv)
    files = generate(args.out, args.today, args.with_audio)
    print(f"Wrote {len(files)} files to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
