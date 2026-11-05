# Finalist day run-book (one remote NAS day, 22–28 Nov 2026)

Goal for the day: install the Skill, run the six scenarios on real hardware, fix what breaks, and record the ≤3-minute demo before access ends.

## Before the day

1. Regenerate the sample family dated for the test day: `.venv/Scripts/python sample-family/generate.py --out sample-family/out --today <test-day YYYY-MM-DD> --with-audio`. The premium notice then falls 12 days after the test day, so it is Expiring.
2. Rebuild and check the package: `.venv/Scripts/python scripts/build_zip.py`, then `node ~/tools/uliya-skill-kit/scripts/check-skill.mjs skill/chaabi`.
3. Have screen recording ready. Write the demo voice-over (English) in advance.

## Upload order on the NAS

1. Create the folders `Papa Documents`, `Phone Backup/WhatsApp Images`, `Voice Notes`, `Empty Folder` and `Family/Chaabi`.
2. Upload the generated files into the matching folders. Add the WhatsApp Images folder to the photo library so UGOS indexes the text in its photos, and wait for indexing to finish before running anything.
3. Install the Skill from `dist/chaabi.zip`.
4. Set Uliya to the local model, so the demo shows the privacy story honestly.

## Scenario checklist

| # | Run | Pass when |
|---|---|---|
| 1 | Set up with Ramesh (S1) | Map saved, 10+ items with sources, nominee Conflict, village land Missing, premium Expiring, no full ID number or password |
| 2 | What if Papa is in hospital (S2) | Plan quotes the cashless steps and TPA number from health-policy.pdf p.6 |
| 3 | Priya without access (S3) | Explains and stops; nothing saved |
| 4 | Failure injection (S4) | Unreadable and Not searched labels; no invented Missing |
| 5 | Hindi translation (S5 path) | Pension sentence kept in Hindi with a labelled translation, or Not translated if declined |
| 6 | Change check (S6) | New file reported; new map saved with _HHMM; old map untouched |

## Known unknowns and what to try

| If this happens | Try |
|---|---|
| `search-picture --ocr-contains` returns nothing | Check photo indexing finished; try English terms only; as a last resort ask the owner to name the document photos one by one. Never open all photos. |
| `extract` cannot read images or scans | The Skill already sends images to `vision-vlm`; confirm the scans are in a folder the photo search covers. |
| `translate` asks for approval every time | Expected; approve once in the demo and mention the approval gate as a privacy feature. |
| `save-text` rejects a long map | Save the map in two parts (map, then sources and changes), or use `content-ref` if the agent offers it. |
| Mixed Hindi-English transcription is poor | Re-run with language `hi`; note the result honestly. |

## Demo video (≤3 minutes, English)

1. **0:00–0:30 · The problem:** one person knows where everything is; the family has papers but not context.
2. **0:30–1:20 · Zero-form discovery:** run setup on the messy folders. Show the photo search finding the premium notice among the decoys, the Hindi pension order and the voice note.
3. **1:20–2:00 · The unexpected discovery:** show the nominee Conflict and the village land papers Missing (mentioned in the voice note, not in any folder).
4. **2:00–2:45 · The plan:** Priya asks what to do while Papa is in hospital; the plan quotes their own policy, page 6.
5. **2:45–3:00 · Close:** privacy (local model, masked IDs, consent) and the tagline.
