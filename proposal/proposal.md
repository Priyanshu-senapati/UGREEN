# Next of Kin · Track: Open Innovation

## 1. What does your Skill do?

Next of Kin turns the documents, document photos and voice notes a family already keeps on its NAS into a source-linked Family Map, a readiness check and a plan for when the person who knows everything is unavailable.

## 2. Who is your target user, and what is their problem?

Families where one person holds all the paperwork knowledge: policies, deposits, property papers, pensions, nominees. When that person is hospitalised, loses their memory or dies, the family has the papers but not the context. In India, over ₹72,000 crore sits unclaimed in the RBI's DEA Fund.

## 3. What is your solution?

Three conversations: Set up (with owner consent), Check our readiness, and What if someone is unavailable. Every fact is labelled Verified, Unverified, Conflict or Missing and linked to its source.

## 4. What is the main user flow?

Ramesh consents and names his folders. Next of Kin finds documents, scans and voice notes; extracts masked facts; transcribes and translates; cross-checks sources; and searches for anything mentioned but absent. Ramesh approves; the map is saved where his daughter Priya can read it. Later Priya asks "What if Papa is in hospital?" and gets a phased plan quoting their own policy.

## 5. How is your idea different from existing tools or common AI solutions?

Family vaults (NammaPetti, Soult) need someone to type everything in. Next of Kin is zero-form: it reads what already exists. Unlike a document chatbot, it detects conflicts (two nominees on one policy), finds items a voice note mentions but the folders lack, and grounds plans in the family's own policy, keeping documents at home.

## 6. Which UGREEN AI NAS features does your Skill use, and at which step?

- Files: find and stat for discovery and change checks.
- Photos: OCR-text search finds document photos without opening personal ones; vision-vlm reads them.
- Documents: extract, translate, reconcile, and qa for the cashless-claim answer.
- Knowledge: audio-transcription for voice notes, collect-evidence for missing items, save-text for versioned maps.

## 7. What is your technical approach?

A Markdown-only Skill delegating to UGREEN's four NAS agents. A 19-operation execution contract fixes preconditions, approvals and recovery; "Missing" is used only after a search ran. Inputs: owner consent, folders, model setting (cloud requires explicit consent), voice-note language. Identifiers are masked to their last four characters, passwords are never copied, originals stay read-only, and maps are versioned, never overwritten. Uliya's local model is recommended.

## 8. What have you built so far? What is not built yet? What still needs testing on a NAS?

Built: the full package (SKILL.md plus five references), passing the kit checker with zero errors and warnings; a synthetic Sharma family; six simulated runs; 76 automated tests in total. Not built: re-processing only changed files. Needs NAS testing: OCR-text search, scan extraction, translation approval, save naming, mixed Hindi-English transcription.

## 9. How will you test your Skill if you become a Finalist?

- Core test 1: set up on the Sharma family. Expect 10+ sourced items, the nominee Conflict, village land Missing, the premium Expiring, and no ID number or password copied.
- Core test 2: "What if Papa is in hospital?" quotes the cashless steps and TPA number from the policy, page 6.
- Edge test: Priya requests a Private Map she cannot open; the Skill explains and stops without a workaround.

## 10. What are the known limits, risks, or outside dependencies of your Skill?

It depends on Uliya's agents (stability unverified) and OCR quality. It cannot verify where the AI runs or who else can read a folder, so it asks and discloses. It is an organiser, not legal or financial advice, and grants no authority.

## Declarations

- Solo entrant: Priyanshu Kumar Senapati.
- Next of Kin, its Skill package and its core workflow were conceived and built during the UGREEN Hackathon 2026. Nothing was reused from earlier projects or submissions.
- AI tools used: Claude Code (Anthropic) for research, drafting, tests and synthetic test data.
- Electronic signature: Priyanshu Kumar Senapati

## Third-party components and licences

The Skill package contains no third-party components. These development tools were used, and none is distributed: uliya-skill-kit 0.7.3 (UGREEN), Playwright for Python (Apache-2.0), Pillow (MIT-CMU), pypdf (BSD-3-Clause), Markdown (BSD-3-Clause), pytest (MIT), edge-tts (LGPL-3.0). All sample data is synthetic and uses fictional institutions.
