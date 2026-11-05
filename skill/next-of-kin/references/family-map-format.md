# Family Map format

The Family Map is one Markdown file per version. It is the only memory Next of Kin keeps between conversations, and family members read it as an ordinary document.

## File naming and versions

- Name each new map `Family-Map_YYYY-MM-DD.md`, using the date it is saved.
- If a file with that name already exists in the destination folder, add the time: `Family-Map_YYYY-MM-DD_HHMM.md`.
- Previous versions are never overwritten. Every update is a new file, and the header of the new file names the previous version.
- The map is saved only after the owner approves it, in the destination the owner chose: a **Private Map** folder or a **Family Continuity Map** folder.

## 1. Header

- Owner name.
- `Map last updated:` date and time, and `Version:` number (1 for the first map, then 2, 3, …).
- Previous version file name, or "none".
- This line, verbatim: "Next of Kin is an organiser, not legal or financial advice. It does not give anyone legal or financial authority."

## 2. Setup record

- Who confirmed consent, and when.
- Allowed folders, listed by name.
- Model setting as the owner stated it: *local*, or *cloud, explicitly approved*.
- Destination type: Private Map or Family Continuity Map.
- Voice-note languages: Hindi, English, or mixed.

## 3. At a glance

One table row per item:

| ID | Type | Institution | Reference | Holder | Nominee | Key date | Paper original | Status |
|---|---|---|---|---|---|---|---|---|

- **Reference** shows only the last 4 characters (`XXXX-4821`).
- **Key date** is the next date that matters: premium due, maturity, renewal, EMI.
- **Paper original** is where the physical document is kept, only if a source says so. Otherwise write "—" and raise no finding: not knowing where a paper is kept is normal, not a gap.
- **Status** is the item's most serious label or finding.

Items covered: life insurance, health insurance, bank accounts, fixed deposits, property (deeds, land records), investments (mutual funds, demat, PPF, EPF, NPS), pension, loans, bank locker, will, vehicle. Identity documents are recorded by **location only**.

## 4. Item cards

One card per item. The title line uses exactly this form:

`**A<n> · <Item type>: <Institution>** · <masked reference> · <status>`

Each card lists the facts for that item, one per line. Every fact line ends with its label and its source: the source ID from section 7 plus a page (`S2 p.1`) or a voice-note timestamp (`S9 00:14–00:22`).

Items mentioned only in a voice note get their own card, with status **Missing**, **Unverified** or **Not searched**. An example is village land papers that are mentioned but not found.

A **Missing** or **Not searched** fact line cites the source that mentions the item, then the search outcome. For example: "- Village land papers: with Suresh · Missing · S8 00:31–00:40; searched 2026-11-10, empty list".

For a fact read from a Hindi source, the card keeps the original sentence (at most 2 sentences around the fact) and a translation labelled "Translation:". The original is never replaced.

Example (synthetic family, fictional institutions):

> **A3 · Life insurance: Jeevan Suraksha Life** · XXXX-4821 · **Conflict**
> - Policyholder: Ramesh Sharma · Verified · S2 p.1
> - Nominee: Sunita Sharma · Verified · S2 p.2, S6 (photo of page 1)
> - Nominee: Priya Sharma · Verified · S4 p.1 (nomination change letter) · Conflict with S2: check which nomination is current
> - Next premium due: 22 Nov 2026 · Verified · S5 (photo of premium notice) · Expiring
> - Paper original: Bharat National Bank locker, key with Suresh · Unverified · S9 00:14–00:22
>   - Original (Hindi): "असली कागज़ बैंक के लॉकर में हैं, चाबी सुरेश के पास है।"
>   - Translation: "The original papers are in the bank locker; Suresh has the key."
> - Contact: agent R. Kulkarni · Verified · S2 p.4

## 5. People and contacts

- Owner, family members and their roles (spouse, daughter, son, brother-in-law).
- Useful contacts (insurance agent, bank branch, lawyer, TPA helpline), included only when they appear in the shared files. Each contact cites its source.

## 6. Open findings

Every finding names the item ID, what was found, its source IDs, and a suggested next step. Findings are listed in this order:

1. **Conflict**: the same item disagrees across sources.
2. **Expiring**: a date falls within 30 days of today, or has already passed.
3. **Missing**: something is referred to but was not found.
4. **Unverified**: a fact comes only from a voice note, or the text was hard to read.
5. **Review**: different items differ in a way worth checking. This is not an error.
6. **Gap**: an expected detail is absent.
7. Step failures: **Not searched**, **Not cross-checked**, **Unreadable**, **Not translated** and **Not transcribed**, each naming the file or item affected.

## 7. Sources and changes

- **Sources:** a numbered list, `S1`, `S2`, …, each with the file path relative to its allowed folder, the file type and the last-modified date. Change checks compare against this list.
- **Skipped:** counts only (for example "212 photos without matching text"), never names of personal photos.
- **Changes since the previous version**, grouped as: new file · file modified · fact changed · conflict resolved · new conflict.

## Fact labels

- **Verified**: read clearly from a document or a document photo.
- **Unverified**: stated only in a voice note, or the text was hard to read.
- **Conflict**: the same item (the same reference number or the same property) disagrees across sources.
- **Missing**: referred to somewhere, and a search of the allowed folders ran and found nothing.

## Finding types

- **Review**: different items differ in a way worth checking, for example a bank nominee who differs from an insurance nominee on a different product.
- **Gap**: an expected detail is absent, for example no nominee on a mutual fund statement. Wording is always "not found in the folders you shared", never "you have none".
- **Expiring**: a deadline within 30 days of today, or one that has passed: a premium or renewal due date, a maturity, a policy end date, or a submission such as a pension life certificate. Routine recurring payments such as monthly EMIs and bills are recorded as facts, never as Expiring. The raw date is always shown next to this label.
- **Not searched**: the search for a mentioned item failed, so nothing is known. It is never shown as Missing.
- **Not cross-checked**: comparing documents about the same item failed, so no agreement is claimed.
- **Unreadable**: a file or photo could not be read.
- **Not translated**: the original sentence is kept because translation failed or was declined.
- **Not transcribed**: the audio is kept because transcription failed.

## Privacy rules inside the map

- Policy, account, folio, loan, PAN and Aadhaar numbers show only the last 4 characters, for example `XXXX-4821`. The full number stays in the original document, which the map points to.
- Never copied into the map: passwords, PINs, OTPs, CVVs, full card numbers, net-banking IDs. If a file appears to contain any of these, list a **Review** finding: "S7 appears to contain passwords; not copied. Consider storing them securely."
- Health: no diagnoses or medical details. Only health-insurance details and the location of medical records are kept.
- Photos of people are never described or stored.
- Amounts are kept only where they help (sum assured, loan outstanding) and always carry an "as of" date.
- Original-language text is limited to at most 2 sentences around the fact it supports.
