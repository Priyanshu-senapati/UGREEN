## Inspiration

In most families, one person knows where everything is: the insurance policies and who the nominee is, the fixed deposits, the property deed in the bank locker, the pension order, which agent to call. When that person is in hospital, losing their memory, or gone, the family usually still has the papers. What they lose is the context that makes the papers useful.

The cost is real. More than ₹72,000 crore sits unclaimed in the RBI's Depositor Education and Awareness Fund (Rajya Sabha reply, January 2026). Government recovery portals exist, but they only help if you already know what to search for.

Family-vault apps try to solve this by asking someone to type everything in. That is exactly the person who never gets round to it. So I wanted something that needs **zero forms**: it should read what the family already keeps on its NAS and build the picture from that.

## What it does

**Chaabi** (चाबी, Hindi for "key") is a Uliya Skill for UGREEN AI NAS with three conversations:

1. **Set up, with the owner.** After consent, it reads only the folders the owner names: documents, scans, phone photos (found by their indexed text, so personal photos are never opened) and voice notes. It extracts facts with identifiers masked to the last 4 characters, transcribes the owner's voice, translates Hindi while keeping the original, cross-checks documents about the same item, and saves an approved **Family Map**.
2. **Check our readiness.** It reports conflicts, deadlines about to pass, papers that are mentioned but missing, facts that only a voice note supports, and what changed since the last map.
3. **What if someone is unavailable?** For a hospital stay, long-term memory loss, or a death, it builds a plan for the first 24 hours, week, 30 days and later. Each step quotes the family's own documents, such as the cashless-claim steps and TPA helpline from page 6 of their own health policy, and is kept separate from general guidance.

Every fact is labelled **Verified**, **Unverified**, **Conflict** or **Missing** and linked to its source file and page, or to the voice-note timestamp.

## How I built it

- **Started from UGREEN's Skill Developer Package** (uliya-skill-kit 0.7.3). I read its capability catalog (78 actions across 9 command groups) and the source of its static checker, so the Skill uses only real actions and follows the checker's exact rules.
- **Designed privacy first.** I mapped every rule to a clause of UGREEN's Skill Content Safety Guidelines:
  - the owner's consent comes before anything is read;
  - a cloud model (or a "not sure") needs a separate explicit yes;
  - only the folders the owner names are read;
  - nothing is copied that should not be (passwords, PINs, OTPs);
  - originals are read-only, and every map is a new version.
- **Wrote the Skill as pure Markdown:** `SKILL.md` plus five references, including a 19-operation execution contract that fixes preconditions, approvals and recovery for every step. The Skill delegates to UGREEN's file-, photo-, document- and knowledge-agents.
- **Built a synthetic test family, the Sharmas.** A Python generator renders realistic documents with Playwright: policies, a Hindi pension order, "phone photos" of premium notices, a passwords file, an ID card, 30 decoy photos and two voice notes. Every institution is fictional and every page is watermarked SAMPLE.
- **Rehearsed without a NAS.** Round 1 has no hardware, so I built a rehearsal harness. A fresh AI agent plays the Uliya runtime, follows the Skill literally, and gets scripted responses from the NAS agents. Deterministic pytest checks then verify the output: no full ID numbers, no passwords, the right findings, and consent before any file is read. There are six scenarios and 76 automated tests.
- **Finished with an independent review.** A separate reviewer checked the whole build, and I fixed every important finding test-first.

## Challenges I ran into

- **No NAS until the finals.** The rehearsal harness was my answer. It turned "it should work" into something I could test.
- **The rehearsals found real bugs:**
  - the Hindi pension scan sat in a documents folder that the photo search never covered;
  - an Aadhaar photo was being sent to the vision model even though only its location was needed;
  - a second save on the same day could have collided with the first map;
  - a missing will was never flagged;
  - every card was flagged "paper original not found", which buried the real findings.
- **Honesty about privacy.** The Skill cannot verify whether Uliya runs a local or a cloud model, so it does not pretend to. It asks, explains what a cloud model would receive, and requires explicit consent.
- **"Missing" has to mean missing.** If a search fails, the item is labelled *Not searched*, never *Missing*. Otherwise a family could be told a deed is lost when the Skill simply could not look.

## Accomplishments that I'm proud of

- The package passes UGREEN's official checker with **0 errors and 0 warnings**.
- The best moment in the rehearsals: the owner says in a voice note that the village land papers are with his brother-in-law. Chaabi searches every shared folder, finds nothing, and flags it, before anyone needs those papers.

## What I learned

- In AI orchestration, the hard part is not the happy path but failure handling. What does the Skill say when a folder is offline, a scan is unreadable, or a translation is declined? Writing that contract first made everything else simpler.
- Privacy is a design input, not a disclaimer: minimum data, masked identifiers, consent before reading, and labelled uncertainty.

## What's next for Chaabi

- Test on a real UGREEN AI NAS iDX6011 Pro during the finals: photo text search, scan extraction, translation approval and mixed Hindi-English transcription.
- Re-process only the files that changed, and track photo modification dates.
- Add more Indian languages, starting with Kannada and Tamil.
