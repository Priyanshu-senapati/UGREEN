"""Render the Devpost gallery images for Chaabi (1500x1000, 3:2) into media/.

Usage: .venv/Scripts/python media/make_gallery.py
"""
from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
SAMPLES = HERE.parent / "sample-family" / "out"

KEY_SVG = """<svg viewBox="0 0 220 90" width="{w}" aria-hidden="true">
<circle cx="45" cy="45" r="30" fill="none" stroke="#c9a227" stroke-width="13"/>
<rect x="73" y="38" width="138" height="14" rx="5" fill="#c9a227"/>
<rect x="168" y="50" width="13" height="26" rx="2" fill="#c9a227"/>
<rect x="192" y="50" width="13" height="18" rx="2" fill="#c9a227"/></svg>"""

BASE_CSS = """
* { box-sizing: border-box; }
body { margin: 0; width: 1500px; height: 1000px; overflow: hidden; background: #f6f1e7; color: #14213d;
       font-family: "Segoe UI", Arial, sans-serif; }
.page { position: relative; width: 1500px; height: 1000px; padding: 72px 84px; }
h1, h2 { font-family: Georgia, "Times New Roman", serif; font-weight: 700; margin: 0; letter-spacing: -0.5px; }
.hi { font-family: "Nirmala UI", "Mangal", sans-serif; }
.foot { position: absolute; left: 84px; right: 84px; bottom: 40px; display: flex; justify-content: space-between;
        font-size: 18px; color: #5b6475; border-top: 2px solid #e2d8c3; padding-top: 14px; }
.brand { font-family: Georgia, serif; font-weight: 700; color: #14213d; }
.chip { display: inline-block; padding: 5px 14px; border-radius: 999px; font-size: 18px; font-weight: 700; color: #fff; }
.Conflict { background: #b5523b; } .Missing { background: #7a2e2e; } .Gap { background: #b8860b; }
.Expiring { background: #d9772b; } .Verified { background: #2f6f4f; } .Unverified { background: #5b6b80; }
.Location { background: #8a8f98; }
"""

FOOT = '<div class="foot"><span class="brand">Chaabi · The key to everything Papa knew</span><span>{note}</span></div>'


def page(body: str, note: str = "UGREEN AI NAS Hackathon 2026 · Open Innovation") -> str:
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE_CSS}</style></head>"
            f"<body><div class='page'>{body}{FOOT.format(note=note)}</div></body></html>")


COVER = page(f"""
<div style="position:absolute;inset:0;background:#14213d"></div>
<div style="position:relative;color:#f6f1e7;margin-top:120px">
  {KEY_SVG.format(w=260)}
  <h1 style="font-size:150px;margin-top:30px;color:#f6f1e7">Chaabi <span class="hi" style="font-size:90px;color:#c9a227;font-weight:600">चाबी</span></h1>
  <div style="font-size:46px;margin-top:18px;font-family:Georgia,serif;font-style:italic;color:#e9dcb5">The key to everything Papa knew.</div>
  <div style="font-size:26px;margin-top:46px;color:#c7cbd6;max-width:1100px;line-height:1.45">
    A Uliya Skill for UGREEN AI NAS that turns a family's own documents, photos and voice notes
    into a source-linked map, a readiness check and a plan for the day the person who knows everything is unavailable.</div>
</div>""", note="Track: Open Innovation").replace('border-top: 2px solid #e2d8c3', 'border-top: 2px solid #2c3a5c')

PROBLEM = page("""
<h2 style="font-size:64px;max-width:1150px;line-height:1.1">In most families, one person knows where everything is.</h2>
<div style="display:flex;gap:56px;margin-top:56px">
  <div style="flex:1.1;font-size:30px;line-height:1.6">
    <div>Insurance policies and their nominees</div><div>Fixed deposits and bank lockers</div>
    <div>Property deeds and village land papers</div><div>Pension orders and life certificates</div>
    <div>Which agent to call, and which key is with whom</div>
    <div style="margin-top:34px;font-family:Georgia,serif;font-style:italic;font-size:34px;color:#b5523b">
      When that person is in hospital, losing their memory, or gone, the family still has the papers, but not the context.</div>
  </div>
  <div style="flex:0.9;background:#14213d;color:#f6f1e7;border-radius:22px;padding:44px 40px">
    <div style="font-family:Georgia,serif;font-size:78px;font-weight:700;color:#c9a227;white-space:nowrap">₹72,000+ crore</div>
    <div style="font-size:28px;line-height:1.45;margin-top:12px">sits unclaimed in the RBI's Depositor Education and Awareness Fund.</div>
    <div style="font-size:19px;color:#aab1c2;margin-top:22px">Rajya Sabha reply, January 2026. Recovery portals only help if you know what to search for.</div>
    <div style="font-size:24px;line-height:1.45;margin-top:26px;border-top:1px solid #34446a;padding-top:20px">
      Family-vault apps need someone to type everything in, and that is exactly the person who never gets round to it.</div>
  </div>
</div>""")

HOW = page("""
<h2 style="font-size:56px">Zero forms. It reads what the family already has.</h2>
<div style="font-size:26px;color:#5b6475;margin-top:14px">Documents, scans and phone photos found by their indexed text, and voice notes: all on the family's own NAS.</div>
<div style="display:flex;gap:30px;margin-top:52px">
""" + "".join(f"""
  <div style="flex:1;background:#fff;border:2px solid #e2d8c3;border-radius:22px;padding:34px 30px;min-height:420px">
    <div style="font-family:Georgia,serif;font-size:64px;color:#c9a227;font-weight:700">{n}</div>
    <div style="font-family:Georgia,serif;font-size:36px;font-weight:700;margin-top:6px">{title}</div>
    <div style="font-size:21px;color:#5b6475;margin-top:6px">{who}</div>
    <div style="font-size:24px;line-height:1.5;margin-top:22px">{body}</div>
  </div>""" for n, title, who, body in [
    ("1", "Set up", "With the owner, after consent",
     "Finds documents, photos and voice notes in the folders the owner names. Extracts masked facts, translates Hindi, transcribes the owner's voice, cross-checks, and saves an approved Family Map."),
    ("2", "Check readiness", "Owner or a permitted family member",
     "Conflicts, papers about to lapse, things mentioned but missing, facts only a voice note supports, and what changed since the last map."),
    ("3", "What if ___ is unavailable?", "Hospital · memory loss · passed away",
     "A plan for the first 24 hours, week and month, quoting the family's own policy, with the document, the contact and the deadline for every step."),
]) + """
</div>
<div style="margin-top:34px;font-size:22px;color:#5b6475">Delegates to UGREEN's file-, photo-, document- and knowledge-agents · every fact labelled
 <span class="chip Verified">Verified</span> <span class="chip Unverified">Unverified</span> <span class="chip Conflict">Conflict</span> <span class="chip Missing">Missing</span></div>
""")

ROWS = [
    ("A1", "Life insurance · Jeevan Suraksha Life", "XXXX-4821", "Nominee: Sunita (S1 p.2) vs Priya (S2 p.1)", "Conflict"),
    ("A7", "Pension · <span class='hi'>राज्य पेंशन कार्यालय</span>", "XXXX-2019", "Life certificate due every November", "Expiring"),
    ("A5", "Village land papers", "—", "Mentioned in a voice note (S8 00:31), not found", "Missing"),
    ("A6", "Mutual fund · Sahyog Mutual Fund", "XXXX-1546", "Nominee: not registered", "Gap"),
    ("A10", "Will", "—", "No will found in the folders you shared", "Gap"),
    ("A8", "Home loan · Griha Setu Home Finance", "XXXX-3370", "EMI on the 5th; co-borrower Sunita", "Verified"),
    ("A11", "Identity document", "—", "Location only, never opened", "Location"),
]
MAP = page("""
<h2 style="font-size:52px">The Family Map: every fact labelled and linked to its source</h2>
<table style="width:100%;border-collapse:collapse;margin-top:34px;font-size:23px;background:#fff">
<tr style="background:#14213d;color:#f6f1e7;text-align:left"><th style="padding:12px 14px">ID</th><th>Item</th><th>Ref</th><th>What the map says</th><th>Status</th></tr>
""" + "".join(f"""<tr style="border-bottom:1px solid #e2d8c3"><td style="padding:11px 14px;font-weight:700">{i}</td><td>{item}</td>
<td style="font-family:Consolas,monospace">{ref}</td><td>{what}</td><td><span class="chip {s}">{'Location only' if s == 'Location' else s}</span></td></tr>"""
                for i, item, ref, what, s in ROWS) + """
</table>
<div style="display:flex;gap:26px;margin-top:28px">
  <div style="flex:1;background:#fff;border-left:10px solid #b5523b;padding:18px 22px;font-size:22px;line-height:1.45">
    <b>Conflict on the same policy.</b> The policy names Sunita; a 2021 endorsement names Priya. Next step: ask the insurer which nomination is on record.</div>
  <div style="flex:1;background:#fff;border-left:10px solid #7a2e2e;padding:18px 22px;font-size:22px;line-height:1.45">
    <b>Found only in Papa's voice.</b> "<span class="hi">गाँव वाली ज़मीन के कागज़ भी सुरेश के पास हैं</span>": the village land papers are with Suresh. No document exists.</div>
</div>""", note="Rehearsal output · synthetic Sharma family · fictional institutions")

PLAN = page("""
<div style="display:flex;gap:40px">
  <div style="flex:0.85">
    <h2 style="font-size:50px;line-height:1.1">"What if Papa is in hospital?"</h2>
    <div style="margin-top:34px;background:#14213d;color:#f6f1e7;border-radius:22px 22px 22px 4px;padding:26px 28px;font-size:26px;line-height:1.45">
      Papa was admitted to hospital this morning. What should we do?<div style="font-size:19px;color:#aab1c2;margin-top:10px">Priya, his daughter</div></div>
    <div style="margin-top:28px;font-size:24px;line-height:1.55;color:#14213d">
      Chaabi asks which situation applies, reads the latest Family Map, and builds a plan for the first
      <b>24 hours</b>, <b>week</b>, <b>30 days</b> and <b>later</b>.
      Each step names the document and its page, where the paper original is, whom to call, the deadline,
      and whether the advice comes from <i>your policy</i> or a <i>general guide</i>.</div>
  </div>
  <div style="flex:1.15;background:#fff;border:2px solid #e2d8c3;border-radius:22px;padding:30px 34px">
    <div style="font-size:19px;color:#5b6475">Map last updated: 2026-11-10 · Version 1 · Situation: Temporarily unavailable</div>
    <div style="font-family:Georgia,serif;font-size:32px;font-weight:700;margin-top:12px">First 24 hours</div>
    <div style="font-size:23px;line-height:1.5;margin-top:12px"><b>Take the health policy to the hospital desk.</b>
      Sehat Shield Health Insurance, XXXX-0917, in force until 31 Mar 2027. <span class="chip Verified">Verified</span></div>
    <div style="margin-top:18px;background:#f6f1e7;border-left:8px solid #c9a227;padding:16px 18px;font-size:22px;line-height:1.5">
      <b>Your policy says</b> (health-policy.pdf, p.6):<br>
      "For an emergency admission, request [pre-authorisation] within 24 hours of admission."<br>
      "TPA helpline (24x7): 1800-000-4455"</div>
    <div style="font-size:22px;line-height:1.5;margin-top:18px"><b>Health card:</b> top drawer of the cupboard
      <span class="chip Unverified">Unverified</span> <span style="color:#5b6475">· Papa's voice note, 00:41</span></div>
    <div style="font-size:19px;color:#5b6475;margin-top:20px">This plan is a general guide, not legal or financial advice. It does not give anyone legal or financial authority.</div>
  </div>
</div>""", note="Rehearsal output · synthetic Sharma family · fictional institutions")

PRIVACY = page("""
<h2 style="font-size:56px">Private by design: the family's most sensitive papers stay at home</h2>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:22px 40px;margin-top:46px;font-size:25px;line-height:1.45">
""" + "".join(f"""<div style="background:#fff;border:2px solid #e2d8c3;border-radius:18px;padding:22px 26px">
<div style="font-family:Georgia,serif;font-weight:700;font-size:28px;color:#14213d">{t}</div><div style="color:#3d4659;margin-top:6px">{d}</div></div>"""
              for t, d in [
                  ("Owner consent first", "Set up with the person whose papers they are, never behind their back."),
                  ("Local model recommended", "A cloud model, or a \"not sure\", needs a separate, explicit yes."),
                  ("Only folders the owner names", "Photos are found by their indexed text; personal photos are never opened."),
                  ("Masked and minimal", "Identifiers show the last 4 characters only. Passwords, PINs and OTPs are never copied."),
                  ("Read-only, versioned", "Originals are never moved or edited. Each map is a new version; nothing is overwritten."),
                  ("No workaround", "It never grants or changes access. No access means it explains and stops."),
              ]) + """
</div>""", note="Every rule is mapped to a clause of UGREEN's Skill Content Safety Guidelines")


def _data_uri(path: Path, height: int = 540) -> str:
    """Downscale an image and inline it, because set_content pages cannot load file:// images."""
    import base64
    import io

    from PIL import Image

    img = Image.open(path).convert("RGB")
    img = img.resize((round(img.width * height / img.height), height))
    buffer = io.BytesIO()
    img.save(buffer, "JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode()


def samples_html() -> str | None:
    notice_path = SAMPLES / "Phone Backup" / "WhatsApp Images" / "premium-notice-photo.jpg"
    pension_path = SAMPLES / "Papa Documents" / "pension-order-hi.jpg"
    if not (notice_path.exists() and pension_path.exists()):
        return None
    notice, pension = _data_uri(notice_path), _data_uri(pension_path)
    return page(f"""
<h2 style="font-size:52px">Tested on a synthetic family, not real people</h2>
<div style="font-size:24px;color:#5b6475;margin-top:12px">The Sharmas: 14 documents and photos, 30 decoy photos, 2 voice notes. Fictional institutions; every page watermarked SAMPLE.</div>
<div style="display:flex;gap:36px;margin-top:34px;align-items:flex-start">
  <img src="{notice}" style="height:540px;border-radius:12px;box-shadow:0 10px 30px rgba(20,33,61,.25)">
  <img src="{pension}" style="height:540px;border-radius:12px;box-shadow:0 10px 30px rgba(20,33,61,.25)">
  <div style="font-size:22px;line-height:1.5">
    <div><b>Planted on purpose:</b></div>
    <div>• a nominee change on the same policy</div><div>• a premium due in 12 days</div>
    <div>• a Hindi pension order</div><div>• a mutual fund with no nominee</div>
    <div>• a passwords file that must not be copied</div><div>• an ID card that must never be opened</div>
    <div>• land papers mentioned only in a voice note</div>
    <div style="margin-top:22px;color:#5b6475">Six rehearsals and 76 automated tests check what the Skill does with them.</div>
  </div>
</div>""", note="Synthetic data only")


def main() -> int:
    pages = {"01-cover": COVER, "02-problem": PROBLEM, "03-how-it-works": HOW,
             "04-family-map": MAP, "05-what-if-plan": PLAN, "06-privacy": PRIVACY}
    sample = samples_html()
    if sample:
        pages["07-synthetic-family"] = sample
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        tab = browser.new_page(viewport={"width": 1500, "height": 1000})
        for name, html in pages.items():
            tab.set_content(html, wait_until="load")
            out = HERE / f"{name}.png"
            tab.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": 1500, "height": 1000})
            print(out.name, out.stat().st_size)
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
