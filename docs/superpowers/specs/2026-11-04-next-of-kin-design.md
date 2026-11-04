# Next of Kin: Design Spec

- **Date:** 2026-11-04
- **Status:** Design approved section by section in conversation; this written spec awaits review
- **Event:** UGREEN Hackathon 2026 on AI NAS (Devpost), track **Open Innovation**
- **Builder:** solo
- **Skill name:** `next-of-kin`

> When the person who knows everything becomes unavailable, the family shouldn't be left knowing nothing.

---

## 1. Summary

Next of Kin is a Uliya Skill for UGREEN AI NAS. It turns the documents, document photos and voice notes a family **already** keeps on its NAS into a source-linked **Family Map**. It then uses that map to answer two questions: *"How ready are we?"* and *"What do we do if ___ is unavailable tomorrow?"*

**Problem.** In most families, one person (the "owner") knows where the insurance policies, bank papers, property deeds, pension orders and contacts are, and how they connect. That person is the least likely to sit down and document it. When they become unavailable (hospital, memory loss, or death), the family usually still has the papers but has lost the context that makes them usable. In India alone, more than ₹72,000 crore sits unclaimed in the RBI's DEA Fund (Rajya Sabha reply, Jan 2026).

**Core innovation: zero-form.** Existing family-vault apps (NammaPetti, Soult, Family Vault, SafeLoop) depend on someone typing everything in. Next of Kin reads what is already on the NAS (scans, phone photos of documents, WhatsApp images, voice notes), on a device in the family's home, and builds the map from that.

**Why the NAS is essential.** These are the most sensitive documents a family owns. They already sit on the NAS (phone backups, scans), and they should never need to be uploaded to a cloud AI to be understood. The Skill combines four NAS capability domains: files, photos, documents and knowledge.

## 2. Goals and non-goals

**Goals (Round 1, due 15 Nov 2026):**
1. A `SKILL.md` package that follows the Uliya Skill Development Standard and passes the kit's static checker with 0 errors and 0 warnings.
2. Three conversations: Set up · Check readiness · What if ___ is unavailable.
3. Every fact in every output is labelled and linked to its source.
4. Privacy and consent are built into the workflow, not added as notes.
5. A 500-word proposal PDF (≤1 MB) that answers all ten required items.

**Non-goals (explicitly out of scope):**
- Storing passwords, PINs, OTPs, CVVs, full card numbers or net-banking IDs.
- Legal, financial or medical advice; prescribing succession or legal procedures.
- Granting, changing, unlocking or sharing access (the kit has no permission actions).
- Continuous or scheduled monitoring (the kit has no scheduler or notifications).
- A "knowledge graph" engine (the kit has no graph store; the Family Map is a structured Markdown file).
- Mobile app, cloud sync, external messaging.
- Medical record processing beyond the *location* of medical files and health-insurance details.
- Incremental re-processing of only changed files (planned for the finals).

## 3. Users and principles

**Owner** (example: Ramesh, 62): gives informed consent, chooses folders, contributes documents and voice notes, reviews and approves the map, and chooses where it is saved and who can read it.

**Family member** (example: Priya, his daughter): reads the map through NAS permissions the owner already set, runs readiness checks and "what if" plans, and can trace every step to its source. She cannot silently change the owner's records.

**Access principle.** Next of Kin never grants access. It works only within access the NAS already allows. If a user cannot open the folder that holds the map, the Skill explains this and stops; there is no workaround.

**Product principles:**
1. **Zero-form first.** Discover existing information; never require data entry.
2. **Consent first.** The owner authorises processing before any discovery.
3. **Local first.** Sensitive processing stays local wherever the chosen model allows. A cloud model requires explicit informed consent.
4. **Read-only originals.** Never move, edit, rename or delete original files.
5. **Evidence-backed.** Every important fact links to its source file and page or timestamp.
6. **Uncertainty-aware.** Never present an assumption as a verified fact.
7. **Permission-respecting.** Never bypass NAS access controls.
8. **Human-approved.** Nothing is saved before the owner reviews and approves.

## 4. The three conversations

### 4.1 Conversation 1: Set up Next of Kin (run with the owner)

1. **Consent and privacy.** The Skill explains what it will read, process and save, then asks:
   - whose records these are, and whether that person is present and consenting;
   - whether Uliya is using a local model. If the answer is "cloud" or "not sure", the Skill explains that extracted text would be sent to that provider and continues only after a separate explicit yes;
   - which folders it may read (e.g. `Papa Documents`, `Phone Backup/WhatsApp Images`, `Voice Notes`); it never scans the whole NAS by default;
   - the language of the voice notes: Hindi, English, or mixed/not sure.
2. **Check access** to each named folder, and check whether a Family Map already exists (if so, this becomes an update).
3. **Discover** documents and audio in the allowed folders only, and find **document photos by their indexed text**, so non-document photos are never opened.
4. **Read:**
   - extract facts from documents;
   - read document photos;
   - translate Hindi sentences (keeping the original);
   - transcribe voice notes with timestamps.
5. **Cross-check** documents about the same item, and search for items that are mentioned but not present.
6. **Preview and approval.** For example: "11 items found · 2 conflicts · 3 missing · 4 voice-note facts unverified." The owner then chooses the destination:
   - **Private Map**: a folder only the owner (and users they have already authorised) can read;
   - **Family Continuity Map**: a folder that designated family members can already read. The kit cannot check other users' permissions, so the Skill asks the owner to confirm and suggests a test ("ask Priya to open that folder once").
7. **Save** a new dated map file (previous versions are kept), confirm the save, and optionally tag the original files.

### 4.2 Conversation 2: Check our readiness (owner or permitted family member)

1. Find and read the latest Family Map. If there is no access, explain and stop. If there is no map, offer setup.
2. Check the allowed folders for files that are new, modified or deleted since the map's date.
3. Recalculate date-based findings against today, and re-search items marked Missing.
4. Report, stamped with the date and map version:
   - **Findings, in priority order:** Conflicts → Expiring soon → Missing → Unverified → Review → Gaps (e.g. "no nominee found").
   - **Change types:** new file · file modified · fact changed · conflict resolved · new conflict.
5. If anything changed, offer to update the map. In Round 1, an update re-reads the whole allowed scope and saves a new version.
6. Optionally save the report.

### 4.3 Conversation 3: What if ___ is unavailable? (permitted family member)

1. Ask which situation applies:
   - **Temporarily unavailable**: hospitalisation, temporary incapacity, difficulty communicating.
   - **Long-term memory or decision-making difficulty**: some actions may need legal authority, such as a power of attorney; the plan recommends professional advice.
   - **Passed away**: the plan identifies documents, contacts and possible next steps, never legal procedure.
2. Read the latest map. The plan header shows "Map last updated: <date>, version <n>".
3. Build a plan in four phases: **First 24 hours → First week → First 30 days → Later.** Each step states:
   - what to do and why;
   - the supporting document (NAS file plus page) and where the paper original reportedly is;
   - whom to contact;
   - the deadline;
   - the fact's status label;
   - **one source label**: *Your policy says* · *General guide suggests* · *Confirm with the institution* · *Needs professional advice*.
4. For details that only the original holds (e.g. the cashless-claim procedure or TPA number), ask the document directly and quote it with a page reference. If the document does not say, the Skill says "Your policy didn't state this; confirm with the insurer."
5. End with "Gaps to fill now, while ___ can still help," and a statement that the plan informs the family but confers no legal or financial authority.
6. Optionally save the plan.

## 5. Family Map format

**File:** one Markdown file per version, `Family-Map_<YYYY-MM-DD>.md` (a time suffix is added if a file with that name exists), saved in the chosen destination. Previous versions are never overwritten. The file is human-readable and is also the Skill's memory between runs.

**Sections:**

| # | Section | Contents |
|---|---|---|
| 1 | Header | Owner, last updated, version number, previous version filename, disclaimer ("an organiser, not legal or financial advice") |
| 2 | Setup record | Who consented and when · allowed folders · model setting as stated (*local* / *cloud, explicitly approved*) · destination type (Private or Family) · voice-note languages |
| 3 | At a glance | One row per item: ID · type · institution · reference (masked) · holder · nominee · key date · paper original location · status |
| 4 | Item cards | Per item: each fact with its label and source (S#, page or timestamp); for Hindi, the original sentence(s) plus a labelled translation |
| 5 | People and contacts | Owner, family roles, useful contacts (agent, bank branch, lawyer), only as found in shared files |
| 6 | Open findings | Conflicts · Review · Missing · Expiring · Unverified · Gaps, as of this version |
| 7 | Sources and changes | Numbered source list (S1…) with path, type and last-modified date · count of skipped and unreadable files · changes since the previous version (the five change types) |

**Items covered:** life insurance, health insurance, bank accounts, fixed deposits, property (deeds, land records), investments (mutual funds, demat, PPF/EPF/NPS), pension, loans, bank locker, will, vehicle. Identity documents: **location only**.

**Privacy rules inside the file:**
- Policy, account, folio, loan, PAN and Aadhaar numbers show **only their last 4 characters** (`XXXX-4821`); the full number stays in the original, which the map points to.
- Never copied: passwords, PINs, OTPs, CVVs, full card numbers, net-banking IDs. If one is found, the finding reads: "S7 appears to contain passwords; not copied. Consider storing them securely."
- Health: no diagnoses or medical content, only health-insurance details and the location of medical records.
- Photos of people are never described or stored.
- Amounts are kept only where useful (sum assured, loan outstanding) and always with an "as of" date.
- Original-language text is limited to the sentence or two that supports a fact.

**Fact labels:**
- **Verified:** read clearly from a document or document photo.
- **Unverified:** stated only in a voice note, or the text was hard to read.
- **Conflict:** the *same* item (same reference number, same property) disagrees across sources.
- **Missing:** referred to somewhere, and a search of the allowed folders ran and found nothing.

**Finding-only categories:**
- **Review:** different items differ in a way worth checking (e.g. bank nominee ≠ insurance nominee on different products). Not an error.
- **Gap:** an expected detail is absent (e.g. no nominee on a mutual fund statement; no will found in the shared folders). Worded as "not found in the folders you shared", never "you have none".
- **Expiring:** a date falls within 30 days of today (or has passed).
- **Not searched / Not cross-checked / Unreadable / Not translated / Not transcribed:** a step failed. These are never upgraded to Missing or Verified.

**Example item card (synthetic):**

> **A3 · Life insurance: Jeevan Suraksha Life** · Policy `XXXX-4821` · **Conflict**
> - Policyholder: Ramesh Sharma · Verified · S2 p.1
> - Nominee: Sunita Sharma · Verified · S2 p.2
> - Nominee: Priya Sharma · Verified · S4 p.1 (nomination change letter): *Conflict with S2, so check which is current*
> - Next premium due: 28 Nov 2026 · Verified · S5 (photo of premium notice) · *Expiring*
> - Paper original: "Bharat National Bank locker; key with Suresh" · Unverified · S9 voice note 00:14–00:22
>   - Original (Hindi): "असली कागज़ बैंक के लॉकर में हैं, चाबी सुरेश के पास है।" Translation: "The original papers are in the bank locker; Suresh has the key."
> - Contact: agent R. Kulkarni · Verified · S2 p.4

## 6. Orchestration and capability evidence

The parent Skill only delegates (`delegate --target <agent-id> --instruction '<task>'`). It never calls `cli.invoke`. Each delegation is self-contained, carries only the files that task needs, and passes only verified results onward.

**`SKILL.md` headings (the exact wording the kit checker requires):** `# Goal` · `# Required input` · `# Generation-time capability evidence` · `# Workflow` · `# Completion and failure`.

**Capability evidence (the exact checker format, with backticks and a `→` arrow):**
- `ug-filesystem` → `file-agent`
- `ug-filemgr` → `file-agent`
- `ug-photo` → `photo-agent`
- `ug-document` → `document-agent`
- `ug-knowledge` → `knowledge-agent`

**Not used:** `file-workflow`, `ug-video`, `ug-music`, `ug-surveillance`.

**Key action usage:**

| Purpose | Agent | Action |
|---|---|---|
| Check folder access | file-agent | `ug-filesystem stat`, `ls` |
| Find documents and audio, with modified dates | file-agent | `ug-filesystem find` (type `documents` / `audio`), `stat` |
| Find document photos by indexed text | photo-agent | `ug-photo search-picture --ocr-contains <term>` (terms include policy, premium, passbook, nominee, deed, बीमा, खाता, पेंशन) |
| Read documents | document-agent | `ug-document extract` (schema `contract` / `mixed`) with masking instructions |
| Read document photos | photo-agent | `ug-photo vision-vlm` (extraction prompt); `vision-ocr` as fallback |
| Translate Hindi sentences | document-agent | `ug-document translate --content <sentence> --target-lang en` |
| Transcribe voice notes | knowledge-agent | `ug-knowledge audio-transcription` (`--language hi` / `en`, or unset for mixed) |
| Cross-check the same item | document-agent | `ug-document reconcile` |
| Search for mentioned items | knowledge-agent | `ug-knowledge collect-evidence` |
| Ask an original document | document-agent | `ug-document qa` (intent `locate_content` / `qa`) |
| Save map, report or plan | knowledge-agent | `ug-knowledge save-text` (built-in approval) |
| Confirm save; find and read map; change check | file-agent | `ug-filesystem stat`, `find`, `cat` |
| Optional tagging | file-agent | `ug-filemgr tag-list`, `tag-set`, `tag-add-file` |

## 7. Execution contract

**Ground rules:**
1. **Agent responses are handled explicitly:**
   - `completed`: use the result;
   - `failed` / `cancelled`: mark the step failed and stop dependent steps;
   - `waiting_user` / `waiting_approval`: pause and ask; never assume a yes.
2. Never fill gaps with guesses. A failed step's facts are absent and labelled.
3. "Missing" only when the search actually ran. If the search failed, the label is "Not searched".
4. Partial results are kept and labelled Partial.
5. Every run ends with three lists: done · failed · not checked.

**Contract.** The `references/execution-contract.md` file in the package expands each row into eight fields: precondition, permissions, agent and command, expected output, approval, failure condition, recovery, and whether to continue.

| # | Operation (agent · action) | Precondition | Expected output | Approval | On failure | Continue |
|---|---|---|---|---|---|---|
| 1 | Consent & privacy (Skill) | Owner present | Consent, model setting, folders, languages | Owner yes; separate yes for a cloud model | Nothing is read | Stop |
| 2 | Check folder access (file · `stat`/`ls`) | Folder named by owner | Accessible / not | — | Explain; drop that folder | Yes if ≥1 folder remains |
| 3 | Find documents & audio (file · `find`+`stat`) | ≥1 open folder | Source list with dates | — | Empty → "no documents found in X" | Yes if anything was found |
| 4 | Find document photos (photo · `search-picture --ocr-contains`) | Photo folder allowed | Candidate photo list | — | Skip photos and say so; never open all photos instead | Yes |
| 5 | Read documents (document · `extract`) | Source list | Masked facts per file, page refs | — | Mark Unreadable | Yes, Partial |
| 6 | Read document photos (photo · `vision-vlm`, then `vision-ocr`) | Candidates | Masked facts per photo | — | Mark Unreadable | Yes, Partial |
| 7 | Translate (document · `translate --content`) | Original sentence | Labelled translation | May be requested by NAS | Keep original; mark Not translated | Yes |
| 8 | Transcribe (knowledge · `audio-transcription`) | Audio files | Timestamped transcript | — | Keep audio; mark Not transcribed | Yes |
| 9 | Cross-check (document · `reconcile`) | ≥2 docs on one item | Agreements and differences | — | Mark Not cross-checked; never claim agreement | Yes |
| 10 | Search mentions (knowledge · `collect-evidence`) | A mention exists | Evidence or none | — | Mark Not searched (not Missing) | Yes |
| 11 | Preview & approval (Skill) | Steps 2–10 done | Summary; destination choice | Owner yes | Nothing saved; summary stays in chat | Stop |
| 12 | Save map (knowledge · `save-text`) | Approval + destination | `verified=true`, output file | Built-in | Nothing overwritten; offer retry or another folder | Stop |
| 13 | Confirm save (file · `stat`) | Output path | File exists | — | Report "save could not be confirmed" | — |
| 14 | Tag originals (file · `ug-filemgr`) | Owner opted in | Tags applied | Each tag | Map still valid; report | Yes |
| 15 | Find & read map (file · `find`+`cat`) | User has NAS access | Latest map text | — | No access → explain, no workaround; no map → offer setup | Stop |
| 16 | Change check (file · `find` modified-since) | Map source list | New / modified / deleted | — | Audit from saved map, warning "changes not checked" | Yes |
| 17 | Re-check Missing (knowledge · `collect-evidence`) | Missing items | Found / still missing | — | Keep "last searched <date>" | Yes |
| 18 | Policy Q&A (document · `qa`) | Source doc in map | Quoted answer with page | — | "Your policy didn't state this; confirm with the insurer" | Yes |
| 19 | Save report or plan (knowledge · `save-text`) | User asked | Output file | Built-in | Content stays in chat | — |

**Approval points:**
1. Owner consent
2. Cloud-model consent
3. Folder scope
4. Translation (if the NAS asks)
5. Map approval
6. Private vs Family destination
7. Optional tagging
8. Map update after changes

## 8. Privacy and consent

Each rule maps to a clause of UGREEN's Skill Content Safety and Publishing Guidelines:

| Rule | Clause |
|---|---|
| Owner consent before any processing; designed to run *with* the owner | 10.1, 4.3 |
| Disclose what is read, processed and saved, including cloud-model data flow | 2.4, 6.4, 11.4 |
| Only folders the owner names; no whole-NAS scan; never other users' data | 4.1, 4.2 |
| Minimum data; masking; no credentials copied | 4.1, 10.1, 6.3, 5.3 |
| Read-only originals; saves only after approval | 4.5, 4.6 |
| No external transmission, sharing or messaging | 6.4 |
| No financial operations; organiser, not advice; risks disclosed | 7.3, 9.3 |
| Package and examples use synthetic data only | 7.1 |

**Honest limits (stated in the Skill and the proposal):**
- The Skill cannot verify where the AI runs. It asks, and requires explicit consent for a cloud model.
- It cannot check other users' permissions. The owner confirms who can read the chosen folder.
- Photo search relies on the text index UGOS already maintains. Next of Kin opens only matching photos.

## 9. Testing

**Sample family (synthetic, watermarked SAMPLE, fictional institutions):** the Sharma family: Ramesh (owner), Sunita, Priya, Arjun, and Suresh (brother-in-law).

| File | Format | Expected behaviour |
|---|---|---|
| Life policy (Jeevan Suraksha Life), nominee Sunita | PDF | Verified facts |
| Nomination-change letter, same policy, nominee Priya | PDF | Conflict |
| Premium-due notice, due 12 days after the test date | Phone photo | Found by text search; Expiring |
| Health policy with cashless-claim section and TPA number | PDF | Policy Q&A in "what if" |
| Fixed deposit receipt, nominee Arjun | Phone photo | Review (different product) |
| Property sale deed | PDF scan | Verified; voice note gives paper location |
| Pension payment order, in Hindi | Scan image | Translation; family-pension step |
| Mutual fund statement, no nominee | PDF | Gap |
| Home loan statement | PDF | Outstanding "as of" date |
| `passwords.txt` | Text | Not copied; finding raised |
| Aadhaar card (fake, watermarked) | Photo | Location only |
| ~30 scenery/food photos + 2 unrelated screenshots | Photos | Ignored by text search |
| (no will) | — | Gap: "no will found in the folders you shared" |
| Voice note 1, mixed Hindi-English (locker key with Suresh; village land papers with Suresh) | Audio | Unverified facts; village land → Missing |
| Voice note 2, English (call agent Kulkarni; FD is for Arjun's studies) | Audio | Unverified facts; contact |

The dataset is generated by scripts in the repo, outside the Skill package.

**Round 1 testing (no NAS):**
1. Kit static checker: 0 errors, 0 warnings.
2. Simulated runs: scripted agent responses (completed / failed / waiting) for each contract row, walked through the Skill to check behaviour against the expected outputs above.
3. Rules audit against the clauses in §8.
4. Limits: proposal ≤500 words and PDF ≤1 MB; package ≤10 MB, ≤100 files, ≤1 MB per file.

**Proposal test cases:**
- **Core 1, Setup on the Sharma family:** ≥10 items, each with a source. Expected findings:
  - nominee Conflict;
  - FD Review;
  - village land Missing;
  - premium Expiring;
  - voice facts Unverified;
  - no password or Aadhaar number copied.
- **Core 2, "What if Papa is in hospital":** the plan quotes the cashless-claim steps and TPA number from the health policy with a page reference, labelled *Your policy says*, kept separate from *General guide suggests* steps.
- **Edge, privacy:** Priya requests a map saved in Ramesh's Private folder without access. The Skill explains and stops; no workaround.

**Finalist day (24-hour remote NAS):**
1. Upload the dataset.
2. Run the six scenarios: the three proposal cases, plus a failure-injection run (unreadable file, inaccessible folder), the Hindi translation check, and a change-check after adding a file.
3. Fix the Skill.
4. Record the ≤3-minute demo.

## 10. Deliverables and layout

**Skill package (`next-of-kin.zip`)** contains Markdown only and no scripts. The kit checker allows only `SKILL.md` and `references/` at the package root, so there is no README. The ZIP holds one top-level folder named `next-of-kin/`.
```
next-of-kin/
  SKILL.md                         # name, description, goal, input, capability evidence, orchestration, completion/failure
  references/
    execution-contract.md          # §7 expanded to eight fields per operation
    family-map-format.md           # §5
    situations.md                  # general guide per situation × item type (never legal advice)
    privacy-and-consent.md         # §8
    disclosures.md                 # third-party components and licences, AI tools used, work done during the hackathon
```

**Repository (`~/next-of-kin`):**
```
docs/superpowers/specs/            # this spec
docs/superpowers/plans/            # implementation plan
skill/next-of-kin/                 # the package source
sample-family/                     # generator scripts + generated dataset (not in the package)
tests/                             # simulated-run scenarios and expected results
proposal/                          # proposal source + PDF
dist/                              # built ZIP
```

**Where each proposal item is answered:**

| # | Item | Source |
|---|---|---|
| 1 | One-sentence description | §1 |
| 2 | Target user and problem | §1, §3 |
| 3 | Solution | §1, §4 |
| 4 | Main user flow | §4 |
| 5 | Difference from existing tools | §1 |
| 6 | NAS features used, by step | §6 |
| 7 | Technical approach | §6, §7, §8 |
| 8 | Built so far / not yet / needs NAS testing | §11, §12 |
| 9 | Two core tests and one edge test | §9 |
| 10 | Limits, risks, dependencies | §8, §11 |

**Pitch story:** taken from the builder's own family experience (caring for a parent, memory loss, loss), collected in the builder's own words while writing the proposal and never invented.

## 11. Risks and open questions (to validate on the NAS)

| Risk | Mitigation |
|---|---|
| Every action is marked "stability unknown" | Execution contract; partial results; failure labels |
| `extract` may not accept images | Document photos go through `vision-vlm` / `vision-ocr` |
| `translate` may require approval | Treated as an approval point; keep the original if declined |
| `search-picture --ocr-contains` behaviour and index coverage unknown | Skip photos and say so if unsupported; never bulk-open photos |
| `audio-transcription` auto-detection for mixed language unknown | Ask the language; leave it unset only for mixed |
| `save-text` content size limits unknown | Keep the map compact; fall back to `content-ref` if needed |
| No way to verify the model location or other users' permissions | Ask, disclose, require explicit consent |
| Date arithmetic by the orchestrator | Always show the raw date next to the computed status |
| Judges see "another document organiser" | Lead with zero-form, voice-note context, Missing discovery and policy-grounded plans |

## 12. Timeline (solo, Round 1 deadline 23:45 PT Sun 15 Nov = 13:15 IST Mon 16 Nov)

Target: submit by **evening of Sun 15 Nov IST**, keeping the PT margin as buffer.

| Date | Work |
|---|---|
| Wed 4 Nov | Spec written and reviewed |
| Thu 5 Nov | Implementation plan; repo scaffold; install kit for checking |
| Thu 5 – Sat 7 Nov | `SKILL.md` and the five references |
| Sun 8 Nov | Static checker to 0/0; fixes |
| Sun 8 – Mon 9 Nov | Sample family generator; voice notes |
| Tue 10 – Wed 11 Nov | Simulated runs; fix logic gaps |
| Thu 12 Nov | Rules audit; disclosures |
| Thu 12 – Fri 13 Nov | Proposal (with the builder's story) and PDF |
| Sat 14 Nov | Final review; build and validate ZIP |
| Sun 15 Nov | Submit |

## 13. Decision log

| Decision | Choice | Why |
|---|---|---|
| Idea | Next of Kin over Care Ledger and Remember Me | Highest on impact, feasibility and differentiation; the builder's lived experience covers all three |
| Positioning | Zero-form family continuity, not a vault | Vault apps need manual entry; that is the failure mode |
| Track | Open Innovation | Combines four NAS domains; signals originality; avoids the crowded Workflow track |
| Languages | English + Hindi | Realistic for Indian families; Hindi more reliable than Kannada on local models |
| Architecture | Map once, reuse (Approach A), with a simple change check | Fast "what if" answers; buildable solo; incremental processing deferred |
| Situations | Three (temporary, long-term memory/decision difficulty, passed away) | Different practical and consent implications |
| Access | Private vs Family Continuity destination chosen at setup | Ensures the map is reachable when needed without granting access |
| Conflict model | Conflict (same item) vs Review (different items) | Different nominees on different products are not errors |
| Setup record | Inside the map file | One file is the Skill's only memory |
| Confidence | Status labels plus agent warnings, no numeric scores | The kit does not promise confidence values |
