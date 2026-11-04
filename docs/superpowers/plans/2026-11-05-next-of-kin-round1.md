# Next of Kin (Round 1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the Round 1 submission for the UGREEN AI NAS hackathon: a Uliya Skill package `next-of-kin` that passes the official kit checker with 0 errors and 0 warnings, backed by a synthetic test family, simulated runs, a rules audit, and a ≤500-word proposal PDF.

**Architecture:** The Skill is Markdown only (`SKILL.md` plus five `references/*.md`). It orchestrates UGREEN's registered NAS agents through `delegate` commands. Everything else lives outside the package and only proves the package works:
- pytest content tests for every package file;
- a sample-family generator (HTML → Playwright → PDF/PNG);
- LLM-run simulations whose outputs are checked by deterministic tests;
- a ZIP builder;
- a proposal PDF builder.

**Tech Stack:** Markdown (Skill) · Python 3.13 venv · pytest · Playwright for Python + Chromium · Pillow · pypdf · markdown · optional edge-tts · Node 24 (kit checker) · uliya-skill-kit 0.7.3 at `~/tools/uliya-skill-kit`.

**Spec:** `docs/superpowers/specs/2026-11-04-next-of-kin-design.md`

## Global Constraints

- Skill name `next-of-kin`. Package directory `skill/next-of-kin/`; the directory name must equal the frontmatter `name`.
- Package root holds only `SKILL.md` and `references/`. Markdown only. ≤100 files, ≤1 MB per file, ≤10 MB total. No README, no scripts.
- Frontmatter has only `name` and `description`. `description` is ≤1024 characters and contains the phrase `Use when`.
- `SKILL.md` body ≤500 lines. Top-level headings exactly, in order: `# Goal`, `# Required input`, `# Generation-time capability evidence`, `# Workflow`, `# Completion and failure`.
- Capability evidence lines, exactly:
  - ``- `ug-filesystem` → `file-agent` ``
  - ``- `ug-filemgr` → `file-agent` ``
  - ``- `ug-photo` → `photo-agent` ``
  - ``- `ug-document` → `document-agent` ``
  - ``- `ug-knowledge` → `knowledge-agent` ``
- **Delegate form:** each delegate is inline code `` `delegate --target <agent> --instruction '<task>'` `` on one line. The instruction is single-quoted and contains no apostrophes, angle brackets, backticks or pipes. Targets are limited to `file-agent`, `photo-agent`, `document-agent`, `knowledge-agent`.
- `SKILL.md` must contain all five status tokens (`completed`, `failed`, `cancelled`, `waiting_user`, `waiting_approval`), the phrase `real result`, and the phrase `empty list`.
- **Forbidden anywhere in the package** (kit checker patterns, case-insensitive):
  - code fences tagged `bash|sh|shell|python|py|javascript|js|node|typescript|ts`;
  - the words `curl`, `wget`;
  - paths starting `/nas`, `/mnt`, `/volume`, `/share`;
  - `cat `, `rm `, `mv `, `cp `, `open (`, `readFile`, `fs.` outside delegate lines;
  - `bypass|skip|disable|ignore` within 40 characters before `gateway|approval|permission|audit`;
  - `TODO`, `TBD`, `replace-with-`;
  - `password|token|secret|api key` followed by `:`/`=` and a quoted value.
- **Fact labels:** `Verified` · `Unverified` · `Conflict` · `Missing`.
- **Finding types:** `Review` · `Gap` · `Expiring` (≤30 days ahead, or passed) · `Not searched` · `Not cross-checked` · `Unreadable` · `Not translated` · `Not transcribed`.
- **What-if source labels:** `Your policy says` · `General guide suggests` · `Confirm with the institution` · `Needs professional advice`.
- **Masking:** identifiers show only their last 4 characters, e.g. `XXXX-4821`.
- **Never copied:** passwords, PINs, OTPs, CVVs, full card numbers, net-banking IDs.
- **Map files:** `Family-Map_YYYY-MM-DD.md`, with `_HHMM` appended when that name exists. Previous versions are never overwritten.
- **Destinations:** `Private Map` and `Family Continuity Map`.
- **Sample data:** fictional institutions only, watermarked `SAMPLE`. Never use real brand names (LIC, SBI, HDFC, ICICI, Axis, Kotak, PNB, Canara, Star Health, Bajaj, Tata AIA, Max Life, Aditya Birla).
- **Deadline:** submit by the evening of Sun 15 Nov 2026 IST. The hard deadline is 23:45 PT Sun 15 Nov = 13:15 IST Mon 16 Nov.
- **Proposal:** ten required items, ≤500 words in total (declarations and licence info excluded). PDF ≤1 MB.

## Review Focus

1. **Owner answers "not sure" about the AI model:** treat it as a cloud model and require explicit consent before any file is read (Task 5 static test; Task 7 S1 assertion).
2. **The same policy exists twice (PDF scan and a phone photo of page 1):** one item with two sources, and no Conflict caused by the duplicate (Task 6 adds the photo; Task 7 S1 assertion).
3. **An allowed folder is empty:** say it returned an empty list, then continue with the other folders (Task 6 creates `Empty Folder`; Task 8 S4 assertion).
4. **Mixed Hindi-English voice note:** the transcription request leaves the language unset; it is not forced to `hi` (Task 5 static test; Task 7 S1 assertion).
5. **A second map saved on the same day:** a new `_HHMM` file; the earlier map is untouched (Task 5 static test; Task 8 S6 assertion).

## Schedule (spec §12)

| Dates | Tasks |
|---|---|
| Thu 5 – Fri 6 Nov | Tasks 1–4 (references) |
| Sat 7 – Sun 8 Nov | Task 5 (`SKILL.md`, checker 0/0) |
| Sun 8 – Mon 9 Nov | Task 6 (sample family) |
| Tue 10 – Wed 11 Nov | Tasks 7–8 (simulations) |
| Thu 12 Nov | Task 9 (rules audit, ZIP) |
| Thu 12 – Fri 13 Nov | Task 10 (proposal) |
| Sat 14 – Sun 15 Nov | Task 11 (release, submission) |

---

## File map

```
.gitignore  requirements-dev.txt  pytest.ini
skill/next-of-kin/SKILL.md
skill/next-of-kin/references/{family-map-format,privacy-and-consent,execution-contract,situations,disclosures}.md
tests/package_rules.py   tests/output_checks.py
tests/test_family_map_format.py  tests/test_privacy_and_consent.py  tests/test_execution_contract.py
tests/test_situations.py  tests/test_skill_md.py  tests/test_sample_family.py  tests/test_simulations.py
tests/test_rules_audit.py  tests/test_zip.py  tests/test_proposal.py
tests/simulations/harness.md  tests/simulations/scenarios/S1..S6-*.md  tests/simulations/results/S1..S6.md
sample-family/family.py  sample-family/generate.py  sample-family/templates/*.html  sample-family/voice-notes.md
scripts/build_zip.py   docs/rules-audit.md   docs/finalist-day.md
proposal/proposal.md   proposal/build_pdf.py
```

Generated, git-ignored: `.venv/`, `sample-family/out/`, `dist/`, `proposal/*.pdf`.

---

### Task 1: Scaffold, shared test rules, and `family-map-format.md`

**Files:**
- Create: `.gitignore`, `requirements-dev.txt`, `pytest.ini`, `tests/package_rules.py`, `tests/test_family_map_format.py`, `skill/next-of-kin/references/family-map-format.md`

**Interfaces:**
- Produces, in `tests/package_rules.py`:
  - `ROOT: Path`, `SKILL_DIR: Path` (`skill/next-of-kin`), `REFS_DIR: Path`;
  - `read(path: Path) -> str` (UTF-8);
  - `LABELS = ("Verified", "Unverified", "Conflict", "Missing")`;
  - `FINDING_TYPES = ("Review", "Gap", "Expiring", "Not searched", "Not cross-checked", "Unreadable", "Not translated", "Not transcribed")`;
  - `SOURCE_LABELS = ("Your policy says", "General guide suggests", "Confirm with the institution", "Needs professional advice")`;
  - `MAP_SECTIONS = ("Header", "Setup record", "At a glance", "Item cards", "People and contacts", "Open findings", "Sources and changes")`;
  - `REAL_BRANDS` (tuple from Global Constraints);
  - `checker_violations(text: str) -> list[str]`, which returns `"<rule>: line <n>"` strings;
  - `run_kit_checker(skill_dir: Path) -> dict`, which runs `node <kit>/scripts/check-skill.mjs <skill_dir>` (kit = env `UGREEN_KIT_DIR` or `~/tools/uliya-skill-kit`) and returns the parsed JSON stdout.

- [ ] **Step 1: Create the environment**

  `py -V:Astral/CPython3.13.13 -m venv .venv`, then `.venv/Scripts/python -m pip install -r requirements-dev.txt`, then `.venv/Scripts/python -m playwright install chromium`.
  - `requirements-dev.txt`: `pytest>=8`, `playwright>=1.48`, `pillow>=11`, `pypdf>=5`, `markdown>=3.7`, `edge-tts>=7`.
  - `pytest.ini`: `testpaths = tests`.
  - `.gitignore`: `.venv/`, `sample-family/out/`, `dist/`, `proposal/*.pdf`, `__pycache__/`.

- [ ] **Step 2: Write `tests/package_rules.py`**

  `checker_violations` applies these patterns line by line with `re.I`. It does not apply the `direct file api` and `nas path` rules to lines containing `delegate --`. The patterns are copied from `check-lib.mjs`:

```python
CHECKER_PATTERNS = {
    "runtime fence": r"^```\s*(?:bash|sh|shell|python|py|javascript|js|node|typescript|ts)\b",
    "remote download": r"\b(?:curl|wget)\b|https?://\S+\s*\|\s*(?:sh|bash)\b",
    "direct file api": r"\b(?:readFile|writeFile|unlink|pathlib|fs\.|open\s*\(|cp\s+|mv\s+|rm\s+|cat\s+)\b",
    "nas path": r"(?:^|[\s\"'])/(?:nas|mnt|volume\d*|shares?)(?:/|\b)",
    "bypass": r"\b(?:bypass|skip|disable|ignore)\b[^\n]{0,40}\b(?:gateway|approval|permission|audit)\b",
    "placeholder": r"replace-with-|\bTODO\b|\bTBD\b",
    "credential": r"\b(?:password|passwd|token|api[_-]?key|secret)\s*[:=]\s*[\"'][^\"'\n]+[\"']",
}
```

- [ ] **Step 3: Write the failing test `tests/test_family_map_format.py`**

```python
from package_rules import REFS_DIR, read, LABELS, FINDING_TYPES, MAP_SECTIONS, REAL_BRANDS, checker_violations
import re
DOC = REFS_DIR / "family-map-format.md"

def test_seven_sections_in_order():
    text = read(DOC)
    positions = [text.index(f"## {i}. {name}") for i, name in enumerate(MAP_SECTIONS, 1)]
    assert positions == sorted(positions)

def test_defines_labels_and_findings():
    text = read(DOC)
    for word in LABELS + FINDING_TYPES:
        assert f"**{word}**" in text, word

def test_masking_and_never_copied():
    text = read(DOC)
    assert "last 4 characters" in text and "XXXX-4821" in text
    for item in ("passwords", "PINs", "OTPs", "CVVs", "full card numbers", "net-banking IDs"):
        assert item in text, item

def test_versioned_file_naming():
    text = read(DOC)
    assert "Family-Map_YYYY-MM-DD.md" in text and "_HHMM" in text and "never overwritten" in text

def test_expiring_window_and_gap_wording():
    text = read(DOC)
    assert "30 days" in text and "not found in the folders you shared" in text

def test_card_title_format_and_voice_only_items():
    text = read(DOC)
    assert "**A3 · Life insurance: Jeevan Suraksha Life**" in text
    assert "Items mentioned only in a voice note get their own card" in text

def test_fictional_institutions_only():
    text = read(DOC)
    for brand in REAL_BRANDS:
        assert not re.search(rf"\b{re.escape(brand)}\b", text), brand

def test_kit_checker_patterns_clean():
    assert checker_violations(read(DOC)) == []
```

- [ ] **Step 4: Run it and confirm it fails**

  Run: `.venv/Scripts/python -m pytest tests/test_family_map_format.py -v`. Expected: FAIL (`FileNotFoundError`).

- [ ] **Step 5: Write `references/family-map-format.md` from spec §5**

  Use numbered sections `## 1. Header` … `## 7. Sources and changes`. Define each label and finding type in bold. Include the masking and never-copied rules, the health and photo limits, the "as of" rule for amounts, and the original-language rule (≤2 sentences plus a labelled translation). Use the synthetic A3 card from spec §5 with `Jeevan Suraksha Life` and `Bharat National Bank`. Write action names only in backticks.

- [ ] **Step 6: Run the test and confirm it passes**

  Item card titles use exactly `**A<n> · <Item type>: <Institution>**`, followed by ` · <masked reference> · <status>`. Items mentioned only in a voice note (e.g. village land papers) get their own card, with status Missing, Unverified or Not searched.

  Run: `.venv/Scripts/python -m pytest tests/test_family_map_format.py -v`. Expected: 8 passed.

- [ ] **Step 7: Commit**

  `git add .gitignore requirements-dev.txt pytest.ini tests skill && git commit -m "feat: add Family Map format reference and test scaffold"`

---

### Task 2: `privacy-and-consent.md`

**Files:**
- Create: `skill/next-of-kin/references/privacy-and-consent.md`, `tests/test_privacy_and_consent.py`

**Interfaces:**
- Consumes: `package_rules.read`, `checker_violations`, `REFS_DIR`.
- Produces: the clause list `CLAUSES` (defined in this test file and reused by Task 9).

- [ ] **Step 1: Write the failing test**

```python
from package_rules import REFS_DIR, read, checker_violations
DOC = REFS_DIR / "privacy-and-consent.md"
CLAUSES = ("2.4", "4.1", "4.2", "4.3", "4.5", "4.6", "5.3", "6.3", "6.4", "7.1", "7.3", "9.3", "10.1", "11.4")

def test_every_clause_mapped():
    text = read(DOC)
    for clause in CLAUSES:
        assert f"| {clause}" in text or f", {clause}" in text, clause

def test_consent_script_questions():
    text = read(DOC)
    for phrase in ("present and consenting", "local model", "cloud model", "which folders",
                   "voice notes", "Private Map", "Family Continuity Map"):
        assert phrase in text, phrase

def test_not_sure_treated_as_cloud():
    assert 'Treat "not sure" the same as a cloud model' in read(DOC)

def test_three_honest_limits():
    text = read(DOC)
    for phrase in ("cannot verify where the AI runs", "cannot check which other users can read a folder",
                   "existing photo text index"):
        assert phrase in text, phrase

def test_no_workaround_rule_and_clean():
    text = read(DOC)
    assert "no workaround" in text
    assert checker_violations(text) == []
```

- [ ] **Step 2: Run it and confirm it fails.** `.venv/Scripts/python -m pytest tests/test_privacy_and_consent.py -v` → FAIL.

- [ ] **Step 3: Write the reference from spec §3, §4.1 step 1, §8**

  Use exactly these headings: `## Consent script` (the exact questions the Skill asks), `## Clause map` (`| Clause | Rule |` rows using the clause numbers above), `## Honest limits`, `## Access principle`.

  Phrase the access principle as "no workaround". Never write "bypass … permission", because the checker flags it.

- [ ] **Step 4: Run it and confirm it passes.** Expected: 5 passed.

- [ ] **Step 5: Commit.** `git add skill tests && git commit -m "feat: add privacy and consent reference"`

---

### Task 3: `execution-contract.md`

**Files:**
- Create: `skill/next-of-kin/references/execution-contract.md`, `tests/test_execution_contract.py`

**Interfaces:**
- Consumes: `package_rules`.
- Produces: `OPERATIONS`, a dict from operation number to the action substring it must name. Task 5 reuses it to check that `SKILL.md` delegates cover the same actions.

- [ ] **Step 1: Write the failing test**

```python
import re
from package_rules import REFS_DIR, read, checker_violations
DOC = REFS_DIR / "execution-contract.md"
FIELDS = ("Precondition", "Permissions", "Agent and action", "Expected output",
          "Approval", "Failure condition", "Recovery", "Continue")
OPERATIONS = {
    1: "Skill", 2: "`ug-filesystem` `stat`", 3: "`ug-filesystem` `find`", 4: "`ug-photo` `search-picture`",
    5: "`ug-document` `extract`", 6: "`ug-photo` `vision-vlm`", 7: "`ug-document` `translate`",
    8: "`ug-knowledge` `audio-transcription`", 9: "`ug-document` `reconcile`",
    10: "`ug-knowledge` `collect-evidence`", 11: "Skill", 12: "`ug-knowledge` `save-text`",
    13: "`ug-filesystem` `stat`", 14: "`ug-filemgr` `tag-add-file`", 15: "`ug-filesystem` `find`",
    16: "`ug-filesystem` `find`", 17: "`ug-knowledge` `collect-evidence`", 18: "`ug-document` `qa`",
    19: "`ug-knowledge` `save-text`",
}

def blocks(text):
    parts = re.split(r"^### (\d+)\. ", text, flags=re.M)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}

def test_nineteen_operations_with_eight_fields():
    found = blocks(read(DOC))
    assert sorted(found) == list(range(1, 20))
    for number, body in found.items():
        for field in FIELDS:
            assert f"**{field}:**" in body, (number, field)

def test_each_operation_names_its_action():
    found = blocks(read(DOC))
    for number, action in OPERATIONS.items():
        assert action in found[number], (number, action)

def test_ground_rules_statuses_and_not_searched():
    text = read(DOC)
    for token in ("completed", "failed", "cancelled", "waiting_user", "waiting_approval", "Not searched", "Partial"):
        assert token in text, token
    assert "done · failed · not checked" in text

def test_eight_approval_points():
    section = read(DOC).split("## Approval points", 1)[1]
    assert len(re.findall(r"^\d+\. ", section, flags=re.M)) == 8

def test_clean():
    assert checker_violations(read(DOC)) == []
```

- [ ] **Step 2: Run it and confirm it fails.**

- [ ] **Step 3: Write the reference from spec §7**

  Structure: `## Ground rules` (five numbered rules), then `### 1.` … `### 19.`, each with the eight bold fields. Use the spec §7 table for values. In operation 14 name `` `ug-filemgr` `tag-add-file` `` (with `tag-list`/`tag-set` for creating the tag). Operations 15 and 16 name `` `ug-filesystem` `find` `` (op 15 also `` `ug-filesystem` `cat` ``, written with the backtick directly after `cat`). End with `## Approval points` listing the eight from spec §7.

- [ ] **Step 4: Run it and confirm it passes.** Expected: 5 passed.

- [ ] **Step 5: Commit** — `feat: add execution contract reference`.

---

### Task 4: `situations.md`

**Files:**
- Create: `skill/next-of-kin/references/situations.md`, `tests/test_situations.py`

- [ ] **Step 1: Write the failing test**

```python
import re
from package_rules import REFS_DIR, read, SOURCE_LABELS, checker_violations
DOC = REFS_DIR / "situations.md"
SITUATIONS = ("Temporarily unavailable", "Long-term memory or decision-making difficulty", "Passed away")
PHASES = ("First 24 hours", "First week", "First 30 days", "Later")
ITEM_TYPES = ("life insurance", "health insurance", "bank account", "fixed deposit", "property",
              "mutual fund", "pension", "loan", "bank locker", "will", "vehicle")

def situation(text, name):
    return text.split(f"## {name}", 1)[1].split("\n## ", 1)[0]

def test_three_situations_four_phases():
    text = read(DOC)
    for name in SITUATIONS:
        body = situation(text, name)
        positions = [body.index(f"### {p}") for p in PHASES]
        assert positions == sorted(positions), name

def test_every_step_has_exactly_one_source_label():
    text = read(DOC)
    for name in SITUATIONS:
        for line in situation(text, name).splitlines():
            if line.startswith("- "):
                assert sum(label in line for label in SOURCE_LABELS) == 1, line

def test_item_types_covered():
    text = read(DOC).lower()
    for item in ITEM_TYPES:
        assert item in text, item

def test_legal_boundaries():
    text = read(DOC)
    assert "general guide, not legal or financial advice" in text
    assert "power of attorney" in situation(text, SITUATIONS[1])
    passed = situation(text, SITUATIONS[2])
    assert passed.count("Needs professional advice") >= 3
    assert "does not give anyone legal or financial authority" in text

def test_clean():
    assert checker_violations(read(DOC)) == []
```

- [ ] **Step 2: Run it and confirm it fails.**

- [ ] **Step 3: Write the reference from spec §4.3**

  Each step is one bullet ending with exactly one source label in italics. `Your policy says` is reserved for runtime `qa` answers; the guide itself uses the other three labels. Keep it India-relevant but generic (family pension, nominee claims, joint holders, TPA for cashless claims). Never prescribe court or succession procedure.

- [ ] **Step 4: Run it and confirm it passes.** Expected: 5 passed.

- [ ] **Step 5: Commit** — `feat: add situations guide reference`.

---

### Task 5: `SKILL.md` and `disclosures.md` pass the kit checker

**Files:**
- Create: `skill/next-of-kin/SKILL.md`, `skill/next-of-kin/references/disclosures.md`, `tests/test_skill_md.py`

**Interfaces:**
- Consumes: `run_kit_checker` (Task 1); `OPERATIONS` (Task 3, import from `test_execution_contract`).
- Produces: the conversation headings that Tasks 7–8 scenarios cite:
  - `## Conversation 1: Set up Next of Kin`
  - `## Conversation 2: Check our readiness`
  - `## Conversation 3: What if someone is unavailable`

- [ ] **Step 1: Write the failing test `tests/test_skill_md.py`**

```python
import re
from package_rules import SKILL_DIR, REFS_DIR, read, checker_violations, run_kit_checker
SKILL = SKILL_DIR / "SKILL.md"
HEADINGS = ["# Goal", "# Required input", "# Generation-time capability evidence", "# Workflow", "# Completion and failure"]
EVIDENCE = ["- `ug-filesystem` → `file-agent`", "- `ug-filemgr` → `file-agent`", "- `ug-photo` → `photo-agent`",
            "- `ug-document` → `document-agent`", "- `ug-knowledge` → `knowledge-agent`"]
REFS = ["family-map-format", "privacy-and-consent", "execution-contract", "situations", "disclosures"]
AGENTS = {"file-agent", "photo-agent", "document-agent", "knowledge-agent"}
DELEGATE = re.compile(r"`delegate --target (\S+) --instruction '([^']*)'`")

def frontmatter(text):
    head = text.split("---", 2)[1]
    return dict(line.split(": ", 1) for line in head.strip().splitlines())

def test_kit_checker_static_pass():
    result = run_kit_checker(SKILL_DIR)
    assert result["status"] == "static-pass", result["diagnostics"]
    assert result["summary"]["errors"] == 0 and result["summary"]["warnings"] == 0

def test_frontmatter():
    fm = frontmatter(read(SKILL))
    assert set(fm) == {"name", "description"} and fm["name"] == "next-of-kin"
    assert len(fm["description"]) <= 1024 and "Use when" in fm["description"]

def test_headings_evidence_and_links():
    text = read(SKILL)
    assert [line for line in text.splitlines() if line.startswith("# ")] == HEADINGS
    assert [line for line in text.splitlines() if line.startswith("- `ug-")] == EVIDENCE
    for name in REFS:
        assert f"](references/{name}.md)" in text, name

def test_delegates_are_clean_and_cover_every_agent():
    found = DELEGATE.findall(read(SKILL))
    assert {target for target, _ in found} == AGENTS
    for target, instruction in found:
        assert not re.search(r"[<>`|]", instruction), instruction

def test_consent_before_first_delegate_and_not_sure_rule():
    text = read(SKILL)
    assert text.index("explicit consent") < text.index("delegate --")
    assert 'Treat "not sure" the same as a cloud model' in text

def test_review_focus_rules():
    text = read(SKILL)
    assert "leave the language unset" in text
    assert "Family-Map_YYYY-MM-DD" in text and "_HHMM" in text and "never overwrite" in text
    assert "batches of at most 60 files" in text
    assert "empty list" in text and "real result" in text

def test_readiness_change_types_and_freshness_header():
    text = read(SKILL)
    for change in ("new file", "file modified", "fact changed", "conflict resolved", "new conflict"):
        assert change in text, change
    assert text.count("Map last updated") >= 2 and "Gaps to fill now" in text

def test_three_conversations_three_situations_and_scope():
    text = read(SKILL)
    for heading in ("## Conversation 1: Set up Next of Kin", "## Conversation 2: Check our readiness",
                    "## Conversation 3: What if someone is unavailable"):
        assert heading in text
    for situation in ("Temporarily unavailable", "Long-term memory or decision-making difficulty", "Passed away"):
        assert situation in text
    for out_of_scope in ("does not store passwords", "not legal or financial advice", "does not change who can access"):
        assert out_of_scope in text

def test_body_length_and_clean():
    text = read(SKILL)
    assert len(text.split("---", 2)[2].splitlines()) <= 500
    for path in [SKILL, *REFS_DIR.glob("*.md")]:
        assert checker_violations(read(path)) == [], path

def test_disclosures():
    text = read(REFS_DIR / "disclosures.md")
    for heading in ("## Third-party components", "## Licences", "## AI tools used", "## Work done during the hackathon"):
        assert heading in text
    assert "uliya-skill-kit 0.7.3" in text and "Claude Code" in text
```

- [ ] **Step 2: Run it and confirm it fails.** `.venv/Scripts/python -m pytest tests/test_skill_md.py -v` → FAIL (`SKILL.md` missing).

- [ ] **Step 3: Write `disclosures.md`**

  - **Third-party components in the package:** none (original Markdown).
  - **Development tools:** uliya-skill-kit 0.7.3 (UGREEN, used for the static checker), Playwright, Pillow, pypdf, markdown, pytest, edge-tts.
  - **Licences:** read each from `.venv/Scripts/python -m pip show <pkg>` and record exactly what it reports. Also note that the Nirmala UI font is used only to render sample images.
  - **AI tools:** Claude Code (Anthropic), used for research, design, drafting the Markdown, tests and sample data.
  - **Work done during the hackathon:** all of it.

- [ ] **Step 4: Write `SKILL.md`**

  - **Frontmatter `description`:** a declarative noun phrase ("Family continuity map… Use when a family wants to …"). It has no save locations and no "do not" rules.
  - **`# Goal`:** the result, the three conversations, the supported scope, and the out-of-scope sentences the test checks.
  - **`# Required input`:** the consent-script fields, which link to `references/privacy-and-consent.md`.
  - **`# Generation-time capability evidence`:** the five lines.
  - **`# Workflow`:** three `## Conversation …` subsections. Each delegation step is one inline `delegate` line taken from this table:

| Contract op | Target | Instruction must state |
|---|---|---|
| 2 | file-agent | `stat` each folder the owner named in this conversation; report accessible or not; read nothing else |
| 3 | file-agent | `find` documents and audio in only those folders with their modified dates; on an empty list report it per folder |
| 4 | photo-agent | `search-picture` with `ocr-contains` for the listed terms in only the allowed photo folder; return matches only; open no other photo |
| 5 | document-agent | `extract` with schema `mixed` in batches of at most 60 files; return item type, institution, last 4 characters only, holder, nominee, dates, amounts with as-of date, contacts, page; never return passwords, PINs, OTPs or full numbers; for Hindi lines return the original sentence |
| 6 | photo-agent | `vision-vlm` with the same field list for each matched photo; fall back to `vision-ocr`; mark unreadable photos |
| 7 | document-agent | `translate` only the given original sentence to English and return it labelled as a translation |
| 8 | knowledge-agent | `audio-transcription` for each voice note with timestamps; use language `hi` or `en` as the owner said, and leave the language unset for mixed |
| 9 | document-agent | `reconcile` only the files describing the same reference number or property; report agreements and differences |
| 10 | knowledge-agent | `collect-evidence` for each mentioned item within the allowed folders; report found or an empty list |
| 12 | knowledge-agent | `save-text` the approved map to the chosen folder as `Family-Map_YYYY-MM-DD.md`, adding `_HHMM` when that name exists; never overwrite an existing file |
| 13, 15, 16 | file-agent | confirm the saved file; find and read the latest map; find files modified since the map date |
| 14 | file-agent | add the Next of Kin tag to the listed originals only after approval |
| 17 | knowledge-agent | re-run `collect-evidence` for items marked Missing |
| 18 | document-agent | `qa` the named source document for the plan question; quote the answer with its page, or say the document does not state it |
| 19 | knowledge-agent | `save-text` the report or plan when the user asks |

  - **`# Completion and failure`:** the five status tokens, the five ground rules, the three end-of-run lists, and links to `references/execution-contract.md`, `references/family-map-format.md`, `references/situations.md`, `references/disclosures.md`.
  - **Pass only real results downstream** and use the exact phrase `real result`.
  - **Plain names inside delegate instructions:** the table uses backticks for readability only. Inside delegate instructions, write names like Family-Map_YYYY-MM-DD.md and _HHMM without backticks.
  - **Freshness header:** the readiness report and the what-if plan both begin with "Map last updated: date, version n". The what-if plan ends with "Gaps to fill now".

- [ ] **Step 5: Run it and confirm it passes**

  Run: `.venv/Scripts/python -m pytest tests/test_skill_md.py -v`. Expected: 10 passed. If the checker reports diagnostics, fix the `SKILL.md` lines it names. Its suggestions are in Chinese; the `code` field identifies each rule.

- [ ] **Step 6: Run the whole suite.** `.venv/Scripts/python -m pytest -v` → all passed.

- [ ] **Step 7: Commit** — `feat: add SKILL.md and disclosures; kit checker static-pass`.

---

### Task 6: Sample family generator (the Sharmas)

**Files:**
- Create: `sample-family/family.py`, `sample-family/generate.py`, `sample-family/templates/*.html`, `sample-family/voice-notes.md`, `tests/test_sample_family.py`

**Interfaces:**
- Produces, in `sample-family/family.py` (single source of truth, reused by Task 7–8 checks):
  - `OWNER = "Ramesh Sharma"` and `FAMILY = {"wife": "Sunita Sharma", "daughter": "Priya Sharma", "son": "Arjun Sharma", "brother_in_law": "Suresh Verma"}`;
  - `INSTITUTIONS = {"life": "Jeevan Suraksha Life Insurance", "bank": "Bharat National Bank", "health": "Sehat Shield Health Insurance", "mf": "Sahyog Mutual Fund", "home_loan": "Griha Setu Home Finance", "pension": "State Pension Office"}`;
  - `LIFE_POLICY_NO = "774019324821"`, `HEALTH_POLICY_NO = "SSH2025550917"`, `FD_NO = "30418867205"`, `LOAN_NO = "GSHF00933370"`, `MF_FOLIO = "88201546"`, `AADHAAR_FAKE = "2345 6789 4012"`, `PAN_FAKE = "ABCPS1234K"`, `PASSWORD_SECRET = "Ramesh@1962#nb"`, `TPA_PHONE = "1800-000-4455"`;
  - `FULL_IDENTIFIERS = (LIFE_POLICY_NO, HEALTH_POLICY_NO, FD_NO, LOAN_NO, MF_FOLIO, AADHAAR_FAKE, AADHAAR_FAKE.replace(" ", ""), PAN_FAKE)`;
  - `premium_due(today: date) -> date` (today + 12 days);
  - `DOCUMENTS: list[Doc]`, where `Doc(relpath: str, template: str, kind: Literal["pdf", "scan", "photo", "text"])`.
- Produces, in `sample-family/generate.py`:
  - `render_html(template: str, today: date) -> str`;
  - `phone_photo(src: Path, dst: Path) -> None` (rotate 2–4°, slight blur and vignette, JPEG);
  - `make_decoys(folder: Path, n: int = 30) -> list[Path]` (procedural scenery, no text);
  - `generate(out: Path, today: date, with_audio: bool = False) -> list[Path]`;
  - CLI `python sample-family/generate.py --out sample-family/out --today 2026-11-10 [--with-audio]`.
- Output folders: `Papa Documents/`, `Phone Backup/WhatsApp Images/`, `Voice Notes/`, `Empty Folder/`.

- [ ] **Step 1: Write the failing test** (session fixture: `generate(tmp_path_factory.mktemp("fam"), date(2026, 11, 10))`)

```python
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
```

- [ ] **Step 2: Run it and confirm it fails.** `ModuleNotFoundError: family`.

- [ ] **Step 3: Write `family.py` with the constants above**

  `DOCUMENTS` uses exactly these paths:
  - **`Papa Documents/`:** `life-policy.pdf`, `nomination-change-letter.pdf`, `health-policy.pdf`, `property-sale-deed.pdf`, `mutual-fund-statement.pdf`, `home-loan-statement.pdf` (all kind `pdf`); `pension-order-hi.jpg` (`scan`); `passwords.txt` (`text`).
  - **`Phone Backup/WhatsApp Images/`:** `premium-notice-photo.jpg`, `fd-receipt-photo.jpg`, `aadhaar-photo.jpg`, `life-policy-page1-photo.jpg` (Review Focus 2) (all `photo`); `screenshot-recipe.png`, `screenshot-cricket.png` (`photo`, unrelated text).
  - **Not in `DOCUMENTS`:** the decoys `decoy-01.jpg`…`decoy-30.jpg` come from `make_decoys`, and the audio files `Voice Notes/voice-note-1.mp3` and `voice-note-2.mp3` are listed separately in `AUDIO` (generated only with `--with-audio`).

- [ ] **Step 4: Write the templates and `generate.py`**

  - One HTML template per document. Every page carries a diagonal `SAMPLE` watermark and the footer "Synthetic document for testing. Fictional institution."
  - The Hindi pension order uses `font-family: "Nirmala UI"`.
  - Render via Playwright `page.pdf(format="A4")` for `pdf`, and `page.screenshot(full_page=True)` then `phone_photo` for `scan`/`photo`.
  - `passwords.txt` is plain text containing `PASSWORD_SECRET`.
  - `--with-audio` uses edge-tts voice `hi-IN-MadhurNeural` for the two scripts in `voice-notes.md`, writing `Voice Notes/voice-note-1.mp3` and `voice-note-2.mp3`.
  - Voice note 1 (mixed Hindi-English) says the locker key and the village land papers are with Suresh. Voice note 2 (English) says to call agent R. Kulkarni and that the FD is for Arjun's studies.

- [ ] **Step 5: Run it and confirm it passes.** Expected: 6 passed.

- [ ] **Step 6: Generate once and look at it**

  Run `.venv/Scripts/python sample-family/generate.py --out sample-family/out --today 2026-11-10 --with-audio`. Open two PDFs, one phone photo and the Hindi order, and confirm they look like real paperwork with the watermark visible. If edge-tts fails (no network), record the two scripts by hand instead.

- [ ] **Step 7: Commit** — `feat: add Sharma sample family generator`.

---

### Task 7: Simulated runs for the proposal cases (S1–S3)

**Files:**
- Create: `tests/output_checks.py`, `tests/test_simulations.py`, `tests/simulations/harness.md`, `tests/simulations/scenarios/S1-setup.md`, `S2-what-if-hospital.md`, `S3-no-access.md`, `tests/simulations/results/S1.md`, `S2.md`, `S3.md`

**Interfaces:**
- Produces, in `tests/output_checks.py`:
  - `section(text: str, heading: str) -> str`, the text under a `## ` heading;
  - `delegates(text: str) -> list[tuple[str, str]]` (target, instruction), from transcript lines;
  - `full_identifiers_found(text: str) -> list[str]` (any `family.FULL_IDENTIFIERS`, any 12-digit run, PAN pattern `[A-Z]{5}\d{4}[A-Z]`);
  - `fact_lines_missing_source(text: str) -> list[str]` (lines with a fact label and no `S\d+`);
  - `item_card(text: str, needle: str) -> str`, the card whose `**A<n> · …**` title line contains `needle`, up to the next title line or `## ` heading;
  - `source_id(text: str, filename_fragment: str) -> str`, the `S<n>` assigned to that file in the "Sources and changes" section.
- **Result file contract** (defined in `harness.md`, read by tests): `# Result Sn`, then `## Transcript`, `## Saved artifact` (exact text passed to `save-text`, or `none`), and `## End-of-run lists` with `### Done`, `### Failed`, `### Not checked`. In the transcript, each delegation is a line holding the exact inline `delegate` command, followed by a `Mock:` line.

- [ ] **Step 1: Write the failing tests** (`tests/test_simulations.py`, S1–S3)

```python
import re, sys
from output_checks import section, delegates, full_identifiers_found, fact_lines_missing_source, item_card, source_id
from package_rules import ROOT, read, MAP_SECTIONS
sys.path.insert(0, str(ROOT / "sample-family"))
import family
R = ROOT / "tests" / "simulations" / "results"

def test_s1_consent_and_cloud_before_any_delegate():
    t = section(read(R / "S1.md"), "Transcript")
    assert t.index("cloud") < t.index("delegate --")

def test_s1_mixed_voice_note_language_unset():
    voice_calls = [i for _, i in delegates(read(R / "S1.md")) if "audio-transcription" in i]
    assert voice_calls
    for instruction in voice_calls:
        assert not re.search(r"language\s*(?:=|:)?\s*hi\b", instruction), instruction

def test_s1_map_privacy():
    m = section(read(R / "S1.md"), "Saved artifact")
    assert full_identifiers_found(m) == []
    assert family.PASSWORD_SECRET not in m and "XXXX-4821" in m
    assert fact_lines_missing_source(m) == []

def test_s1_map_structure_and_findings():
    m = section(read(R / "S1.md"), "Saved artifact")
    for name in MAP_SECTIONS:
        assert name in m, name
    assert "Conflict" in item_card(m, "Jeevan Suraksha")
    assert "Conflict" not in item_card(m, "Fixed deposit") and "Review" in m
    assert "Missing" in m and "village land" in m.lower()
    assert "Expiring" in m and "22 Nov 2026" in m
    assert "not found in the folders you shared" in m

def test_s1_duplicate_photo_is_second_source_not_conflict():
    m = section(read(R / "S1.md"), "Saved artifact")
    card = item_card(m, "Jeevan Suraksha")
    photo, letter = source_id(m, "life-policy-page1-photo"), source_id(m, "nomination-change-letter")
    assert photo in card and letter in card
    assert f"Conflict with {photo}" not in card

def test_s2_plan_grounded_in_policy():
    t = read(R / "S2.md")
    assert "Map last updated" in t and "Gaps to fill now" in t
    for phase in ("First 24 hours", "First week", "First 30 days", "Later"):
        assert phase in t
    assert "Your policy says" in t and family.TPA_PHONE in t and "p.6" in t
    assert "General guide suggests" in t
    assert "does not give anyone legal or financial authority" in t

def test_s3_no_access_stops_without_workaround():
    t = read(R / "S3.md")
    assert [target for target, _ in delegates(t)] == ["file-agent"]
    transcript = section(t, "Transcript").lower()
    assert "access" in transcript and "owner" in transcript
    assert section(t, "Saved artifact").strip() == "none"
```

- [ ] **Step 2: Run them and confirm they fail.** `FileNotFoundError` on the results.

- [ ] **Step 3: Write `harness.md`**

  The simulated runtime acts as the Uliya parent. It reads `SKILL.md` and the linked references, follows them literally, and writes each `delegate` it would issue. It then uses the scenario's scripted mock for that call, or `failed` if no mock exists. It never invents data beyond the mocks and writes the result file in the result-file contract above.

- [ ] **Step 4: Write the three scenarios** (each has: today = 2026-11-10, user turns, mocks per call, expected outcomes in prose)

  - **S1:** owner Ramesh present; model answer "not sure", then explicit yes; three folders; voice notes "mixed". Mocks return the Sharma facts from `family.py`:
    - the policy PDF and its page-1 photo carry the same policy number and nominee Sunita;
    - the letter shows nominee Priya;
    - the FD nominee is Arjun;
    - the MF has no nominee;
    - the premium is due 22 Nov 2026;
    - voice note 1 transcript segments are at 00:14–00:22 (locker) and 00:31–00:40 (village land);
    - `collect-evidence` for "village land record" returns an empty list.
    - Destination: Family Continuity Map.
  - **S2:** Priya; situation "Temporarily unavailable"; the map read returns the S1 artifact; `qa` on `health-policy.pdf` returns the cashless steps on p.6 with `TPA_PHONE`.
  - **S3:** Priya asks for a readiness check; `find` on Ramesh's Private Map folder returns `failed` with "permission denied".

- [ ] **Step 5: Run each scenario in a fresh subagent**

  Prompt: "Act as the runtime in `tests/simulations/harness.md` for scenario `<file>`; write `tests/simulations/results/<Sn>.md`." Run the three in parallel.

- [ ] **Step 6: Run the tests**

  `.venv/Scripts/python -m pytest tests/test_simulations.py -v`. For each failure, fix the cause in `SKILL.md` or a reference, never in the result file. Re-run the affected scenario and repeat until green. After any `SKILL.md` change, re-run `tests/test_skill_md.py`.

- [ ] **Step 7: Commit** — `test: add simulated runs S1-S3 (setup, what-if, no access)`.

---

### Task 8: Simulated runs for failures and changes (S4–S6)

**Files:**
- Create: `tests/simulations/scenarios/S4-failures.md`, `S5-translation-declined.md`, `S6-change-check.md`, `tests/simulations/results/S4.md`, `S5.md`, `S6.md`
- Modify: `tests/test_simulations.py` (append)

- [ ] **Step 1: Append the failing tests**

```python
def test_s4_failures_are_labelled_not_invented():
    t = read(R / "S4.md")
    m = section(t, "Saved artifact")
    assert "Unreadable" in m and "home-loan-statement" in m
    assert "Not searched" in m and "village land" in m.lower()
    assert "Missing" not in item_card(m, "village land")
    assert "empty list" in section(t, "Transcript") and "Empty Folder" in t
    for heading in ("### Done", "### Failed", "### Not checked"):
        assert heading in t

def test_s5_declined_translation_keeps_original():
    m = section(read(R / "S5.md"), "Saved artifact")
    assert "Not translated" in m and "पेंशन" in m

def test_s6_change_check_and_same_day_version():
    t = read(R / "S6.md")
    assert "new file" in t and "Map last updated" in t
    saves = [i for target, i in delegates(t) if "save-text" in i]
    assert saves and all("_HHMM" in i and "never overwrite" in i for i in saves)
```

- [ ] **Step 2: Run them and confirm they fail.**

- [ ] **Step 3: Write the scenarios**

  - **S4:** the folder `Old Scans` returns `failed` on `stat`; `Empty Folder` returns an empty list; `extract` marks `home-loan-statement.pdf` unreadable; `collect-evidence` returns `failed`.
  - **S5:** `translate` returns `waiting_approval`, and the owner declines.
  - **S6:** an existing map dated 2026-11-10 09:00; `find` modified-since returns one new file, `fd-renewal-photo.jpg`; Ramesh accepts the update on the same day.

- [ ] **Step 4: Run the three scenarios in fresh subagents** (as in Task 7 Step 5).

- [ ] **Step 5: Run the tests and fix the Skill until green.** Then run the full suite: `.venv/Scripts/python -m pytest -v`.

- [ ] **Step 6: Commit** — `test: add simulated runs S4-S6 (failures, translation, change check)`.

---

### Task 9: Rules audit and ZIP build

**Files:**
- Create: `docs/rules-audit.md`, `tests/test_rules_audit.py`, `scripts/build_zip.py`, `tests/test_zip.py`

**Interfaces:**
- Produces: `build_zip(skill_dir: Path, out_zip: Path) -> Path`. The ZIP has a single top folder `next-of-kin/`, entries sorted, fixed timestamps (1980-01-01). It raises `ValueError` if any file is not `SKILL.md` or `references/*.md`. CLI: `python scripts/build_zip.py` → `dist/next-of-kin.zip`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_rules_audit.py
import re
from package_rules import ROOT, SKILL_DIR, read
from test_privacy_and_consent import CLAUSES

def test_every_clause_has_evidence_that_exists():
    rows = re.findall(r"^\| ([\d.]+) \| [^|]+ \| `([^`#]+)#([^`]+)` \|$", read(ROOT / "docs" / "rules-audit.md"), re.M)
    assert {clause for clause, _, _ in rows} == set(CLAUSES)
    for _, file, heading in rows:
        assert heading in read(SKILL_DIR / file), (file, heading)
```

```python
# tests/test_zip.py
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
```

- [ ] **Step 2: Run them and confirm they fail.**

- [ ] **Step 3: Write `docs/rules-audit.md`**

  One row per clause: `` | 10.1 | Consent before processing | `references/privacy-and-consent.md#Consent script` | ``. The heading text after `#` must exist verbatim in that file. Go through UGREEN's guidelines clause by clause against the finished package and fix any gap in the package itself.

- [ ] **Step 4: Write `scripts/build_zip.py`**

- [ ] **Step 5: Run the tests and confirm they pass.** `.venv/Scripts/python -m pytest tests/test_rules_audit.py tests/test_zip.py -v` → 4 passed.

- [ ] **Step 6: Commit** — `feat: add rules audit and deterministic ZIP build`.

---

### Task 10: Proposal and PDF

**Files:**
- Create: `proposal/proposal.md`, `proposal/build_pdf.py`, `tests/test_proposal.py`

**Interfaces:**
- Produces: `build_pdf(md_path: Path, pdf_path: Path) -> Path` (markdown → HTML with an embedded A4 stylesheet → Playwright `page.pdf`). CLI: `python proposal/build_pdf.py` → `proposal/next-of-kin-proposal.pdf`.

- [ ] **Step 1: Write the failing test**

```python
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
```

- [ ] **Step 2: Run it and confirm it fails.**

- [ ] **Step 3: Ask the builder for their story**

  Ask for 2–3 sentences in their own words about caring for a parent, memory loss and loss, plus the name to use in the declaration. Wait for the answer, and do not draft the story without it.

- [ ] **Step 4: Write `proposal.md`**

  Answer the ten items, sourcing each from the spec as mapped in spec §10. The story opens item 2. Item 6 is a step → agent → action list. Item 8 says honestly what is built (package, checker pass, simulations) and what needs NAS testing (spec §11). Item 9 contains the spec §9 tests labelled `Core test 1`, `Core test 2`, `Edge test`. After the ten items come `## Declarations` (solo entrant name, originality statement) and `## Third-party components and licences` (copied from `disclosures.md`).

- [ ] **Step 5: Write `build_pdf.py`, run the tests, and confirm they pass.** Expected: 4 passed. Open the PDF and read it once end to end.

- [ ] **Step 6: Commit** — `docs: add Round 1 proposal and PDF builder`.

---

### Task 11: Release check and submission

**Files:**
- Create: `docs/finalist-day.md`

- [ ] **Step 1: Run the full suite.** `.venv/Scripts/python -m pytest -v` → all passed.

- [ ] **Step 2: Build the artefacts**

  `.venv/Scripts/python scripts/build_zip.py && .venv/Scripts/python proposal/build_pdf.py`. Then `node ~/tools/uliya-skill-kit/scripts/check-skill.mjs skill/next-of-kin` → `"status": "static-pass"`, `"errors": 0`, `"warnings": 0`.

- [ ] **Step 3: Write `docs/finalist-day.md` from spec §9**

  Cover the dataset upload order, the six scenarios as a checklist, what to record for the demo (the three demo moments), and fixes to try when `ocr-contains`, `extract` on images, `translate` approval or `save-text` size behave unexpectedly.

- [ ] **Step 4: Tag the release.** `git tag round1-submission && git log --oneline | head -15`

- [ ] **Step 5: The builder submits on Devpost**

  Upload `proposal/next-of-kin-proposal.pdf` and `dist/next-of-kin.zip` by the evening of Sun 15 Nov IST (the hard limit is 13:15 IST Mon 16 Nov). Do not delete the Round 1 materials afterwards.
