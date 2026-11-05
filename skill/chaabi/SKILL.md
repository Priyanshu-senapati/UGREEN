---
name: chaabi
description: Family continuity map built from the documents, document photos and voice notes a family already keeps on the NAS, with a readiness check and a source-linked plan for the day the person who knows everything is unavailable. Use when a family wants to set up Chaabi, check how ready they are, or asks what to do if a parent or another key person becomes unavailable.
---

# Goal

Chaabi (Hindi for "key") helps a family keep working when the person who holds all the family's paperwork knowledge (the owner) becomes unavailable through hospitalisation, memory loss or death. It reads what the family already keeps on the NAS, so nobody has to fill in forms, and turns it into a **Family Map**: every policy, account, property paper, pension order, loan and contact, with where each paper original is kept. Each fact is labelled Verified, Unverified, Conflict or Missing and linked to its source.

It supports three conversations:

1. **Set up Chaabi**, run with the owner: builds and saves the Family Map after the owner approves it.
2. **Check our readiness**: reports conflicts, items expiring soon, missing documents, unverified facts and changes since the last map.
3. **What if someone is unavailable**: builds a phased continuity plan from the map and the family's own documents.

Scope and limits:
- Chaabi is an organiser, not legal or financial advice, and it does not give anyone legal or financial authority.
- It does not store passwords, PINs, OTPs, CVVs, full card numbers or net-banking IDs. Identifiers are masked to their last 4 characters.
- It does not change who can access anything. It works only within the NAS access the person using it already has.
- It never moves, edits, renames or deletes original files, never sends anything outside the NAS, and never makes claims, payments or transfers.

# Required input

For **Set up Chaabi**, collect these through the consent script in [Privacy and consent](references/privacy-and-consent.md) before any delegation:
- the owner's name, and the owner's explicit consent, given while present;
- the model setting: local, or cloud with a separate explicit consent. Treat "not sure" the same as a cloud model;
- the folders the owner allows, named one by one;
- the voice-note language: Hindi, English, or mixed;
- at the approval step, the destination: Private Map or Family Continuity Map.

For **Check our readiness** and **What if someone is unavailable**, collect:
- the name of the person asking;
- the folder where the owner keeps the Family Map;
- for the plan, which situation applies.

# Generation-time capability evidence

Each CLI used by this Skill, with the single agent that owns it:

- `ug-filesystem` → `file-agent`
- `ug-filemgr` → `file-agent`
- `ug-photo` → `photo-agent`
- `ug-document` → `document-agent`
- `ug-knowledge` → `knowledge-agent`

# Workflow

Choose the conversation from the request: setting up goes to Conversation 1, checking readiness to Conversation 2, and any "what if" question to Conversation 3.

Rules for every conversation:
- The parent Skill only delegates. It never runs NAS actions itself.
- Pass only the real result of each delegation downstream. Never pass a guess, an example or an assumed value.
- Give each delegation only the files that its task needs.
- Follow [the execution contract](references/execution-contract.md) for preconditions, approvals, failures and recovery at every step.

## Conversation 1: Set up Chaabi

1. **Consent and privacy.** Run the consent script. Continue only after the owner's explicit consent, and a separate explicit consent if the model is cloud or "not sure". Without it, stop and explain why.
2. **Check folder access.** Delegate:
   `delegate --target file-agent --instruction 'Use ug-filesystem stat on each folder the owner allowed in this conversation and report for each folder whether it is accessible. Read no file contents and open no other folder.'`
   Drop folders that cannot be opened and tell the owner. If none can be opened, stop.
3. **Find documents and audio.** Delegate:
   `delegate --target file-agent --instruction 'Use ug-filesystem find with type documents and then with type audio in only the accessible allowed folders, and use ug-filesystem stat to report each file path, type and last-modified date. If a folder returns an empty list, report that folder as empty. Search no other folder.'`
   Number every file as a source: S1, S2, and so on. Continue to step 4 even if this finds nothing. A family may share only photos. Stop only if steps 3 and 4 both find nothing.
4. **Find document photos and scans.** Delegate:
   `delegate --target photo-agent --instruction 'Use ug-photo search-picture with ocr-contains once for each search term policy, premium, passbook, nominee, deed, receipt, Aadhaar, identity, बीमा, खाता, पेंशन, limited to the allowed folders. Return only the matching image paths, with the terms each one matched, and open, describe or analyse no other image. If every search returns an empty list, report that.'`
   If photo search is unsupported or fails, report that photos were not searched. Never open all photos instead. Identity documents: record identity images by path only and never open them. An image whose only matching terms are Aadhaar or identity goes into the map as an identity-document location and is not sent to step 6.
5. **Read documents.** Delegate:
   `delegate --target document-agent --instruction 'Use ug-document extract with schema mixed on the listed files only, in batches of at most 60 files. For each file return the item type, institution, reference number showing only its last 4 characters, holder, nominee, key dates, amounts with their as-of date, contacts, and the page of each fact. For a fact written in Hindi also return the original sentence. Never return passwords, PINs, OTPs, CVVs, full card numbers, net-banking IDs or full identity numbers, and if a file seems to contain them report only that it does. Name each unreadable file.'`
6. **Read document photos.** Delegate:
   `delegate --target photo-agent --instruction 'Use ug-photo vision-vlm on each listed photo and ask for the item type, institution, reference number showing only its last 4 characters, holder, nominee, key dates and amounts with their as-of date shown in this document image, and describe no person. If vision-vlm fails for a photo, use ug-photo vision-ocr on that photo. Never return full identity numbers, passwords, PINs or OTPs. Name each photo that neither action can read.'`
7. **Transcribe voice notes.** Delegate:
   `delegate --target knowledge-agent --instruction 'Use ug-knowledge audio-transcription on each listed voice note with timestamped segments. Set the language to hi or en only when the owner named that language, and leave the language unset for mixed or unknown speech, and never return passwords, PINs or OTPs; for a segment that holds one, report only its timestamp and that it does. Name each file that cannot be transcribed.'`
   Facts from voice notes stay Unverified until a document confirms them, and each one cites its timestamp. In every step, never quote or translate a sentence that contains a credential. Raise a Review finding with its timestamp instead.
8. **Translate Hindi sentences.** For each fact whose original sentence is in Hindi, whether from a document, a photo or a voice-note transcript, delegate:
   `delegate --target document-agent --instruction 'Use ug-document translate on the given Hindi sentence only, with target language English, and return the translation labelled as a translation. Translate nothing else.'`
   If the NAS asks for approval, ask the owner. If translation fails or is declined, keep the original and label the fact Not translated.
9. **Cross-check the same item.** When two or more document files describe the same reference number or the same property, send those document files together in one request. Compare facts read from photos yourself.
   `delegate --target document-agent --instruction 'Use ug-document reconcile on the listed document files only, which all describe the same reference number or the same property, and report where they agree and where they differ, with pages.'`
   A difference on the same item is a Conflict. A difference between different items, such as a bank nominee and an insurance nominee, is only a Review finding. A duplicate copy of the same document adds a second source; it is not a conflict. Note that a field missing from a partial copy is not a difference. A disagreement with a hard-to-read photo makes the fact Unverified, not a Conflict.
10. **Search for mentioned items.** For each item mentioned in a document or voice note but not yet found, delegate:
   `delegate --target knowledge-agent --instruction 'Use ug-knowledge collect-evidence to look for the named item within the allowed folders only, and return the evidence with file paths, or an empty list if nothing matches.'`
   An empty list makes the item Missing. A failed search makes it Not searched.
11. **Preview and approval.** Build the map exactly as [the Family Map format](references/family-map-format.md) describes. Before the preview, check for the expected items: a will, and a nominee on each policy, account, deposit and investment. Raise a Gap for each one not found. Show the owner the counts (items, conflicts, missing, expiring, unverified) and the open findings. Ask for explicit approval, and for the destination: Private Map or Family Continuity Map. For a Family Continuity Map, ask the owner to confirm which family members can already read that folder. If the owner declines, save nothing.
12. **Save the map.** First check the destination. Delegate:
   `delegate --target file-agent --instruction 'Use ug-filesystem find for files matching Family-Map_ in the destination folder the owner chose, and report each name with its time. If there are none, report an empty list.'`
   If a map already exists there, this save is a new version: set the version number one higher and name the previous file in the header. Work out the exact file name: Family-Map_YYYY-MM-DD.md for the save date, or, if that name is taken, the same name with _HHMM added. Then delegate:
   `delegate --target knowledge-agent --instruction 'Use ug-knowledge save-text to save the full approved map text as the content, in the destination folder the owner chose, with the exact file name worked out in this step, and never overwrite an existing file. If the text is too long for one request, use a content reference instead. Return the saved file path.'`
13. **Confirm the save.** Delegate:
   `delegate --target file-agent --instruction 'Use ug-filesystem stat on the saved Family Map file path returned by the save step, and on the previous map file if there is one, and report whether each exists, with its size and time.'`
14. **Optional tags.** Only if the owner asks, delegate:
   `delegate --target file-agent --instruction 'Use ug-filemgr tag-get-by-name to find the tag named Chaabi, and add it with ug-filemgr tag-add-file to the listed original files only, after the owner approves each change. If the tag does not exist, report that and add nothing.'`
   If the tag does not exist, ask the owner to create it once in File Manager.

## Conversation 2: Check our readiness

1. **Read the latest map.** Delegate:
   `delegate --target file-agent --instruction 'Use ug-filesystem find for files matching Family-Map_*.md in the folder the user names, choose the newest one, and read the whole file with ug-filesystem cat, in parts if it is long. If the folder cannot be opened, report the access error exactly and do nothing else.'`
   If access is denied, explain that the map belongs to the owner and only the owner or the NAS administrator can grant access, then stop. There is no workaround. If no map exists, offer to run Conversation 1 with the owner.
2. **Check for changes.** Delegate:
   `delegate --target file-agent --instruction 'Use ug-filesystem find in the allowed folders listed in the map Setup record for files modified after the map date, report new and modified files, and compare with the map source list to report deleted files. If nothing changed, report an empty list.'`
   If this fails, continue from the saved map with the warning "changes not checked".
3. **Re-check missing items.** Delegate:
   `delegate --target knowledge-agent --instruction 'Use ug-knowledge collect-evidence again for each item the map marks Missing, within the allowed folders only, and report the evidence found or an empty list.'`
4. **Report.** Start with "Map last updated:" and the map date and version. Recalculate every date against today. List the findings in this order: Conflict, Expiring, Missing, Unverified, Review, Gap, each with its item ID and sources. Then list the changes since the map as new file, file modified, fact changed, conflict resolved and new conflict.
5. **Offer an update.** If files changed, offer to rerun Conversation 1 steps 1 to 14, only with the owner present, starting again from consent, with the same folders and destination unless the owner changes them. The update is saved as a new version and never overwrites the old map. If the person asking is not the owner, explain that the owner must run the update.
6. **Optional save.** Only if the user asks, delegate:
   `delegate --target knowledge-agent --instruction 'Use ug-knowledge save-text to save the readiness report as Readiness-Report_YYYY-MM-DD.md or the continuity plan as Continuity-Plan_YYYY-MM-DD.md in the folder the user chooses, with the exact file name worked out the same way as for the map, adding _HHMM when that name already exists, and never overwrite an existing file. Return the saved file path.'`

## Conversation 3: What if someone is unavailable

1. **Ask the situation.** Offer exactly three: Temporarily unavailable; Long-term memory or decision-making difficulty; Passed away. Do not assume one.
2. **Read the latest map** with the same delegation as Conversation 2 step 1, and handle a denied access the same way.
3. **Build the plan** from [the situations guide](references/situations.md). Start with "Map last updated:" and the map date and version. Group the steps under First 24 hours, First week, First 30 days and Later. Include only steps for items in the map. Each step states what to do and why, the supporting document and page, where the paper original is, whom to contact, the deadline, the fact label, and exactly one source label: Your policy says, General guide suggests, Confirm with the institution, or Needs professional advice.
4. **Ask the original document.** When a step depends on what a specific document says, such as the cashless claim procedure or the TPA helpline in a health policy, delegate:
   `delegate --target document-agent --instruction 'Use ug-document qa on the named source document only to answer the plan question, and quote the answer with its page. If the document does not state the answer, say so plainly.'`
   Label the quoted answer Your policy says. If the document does not state it, write "Your policy didn't state this; confirm with the insurer". If the call failed or the document could not be opened, write "Could not read" with the source ID and "confirm with the insurer", and list it under not checked. Never present a failed read as something the policy does not say.
5. **Close the plan** with "Gaps to fill now", listing the open findings the owner can still help resolve. Add: "This plan is a general guide, not legal or financial advice. It does not give anyone legal or financial authority."
6. **Optional save** with the same delegation as Conversation 2 step 6.

# Completion and failure

Handle every delegation state:
- `completed`: use the real result it returned.
- `failed` or `cancelled`: mark the step failed and stop every step that depends on it. Never replace the missing result with a guess.
- `waiting_user` or `waiting_approval`: pause, ask the user, and continue only on an explicit answer.

Never invent NAS data:
- An empty list is reported as empty.
- An item is Missing only when its search ran and returned an empty list; a failed search makes it Not searched.
- Unreadable files, failed translations and failed transcriptions keep their labels: Unreadable, Not translated, Not transcribed.
- Partial results are kept and labelled Partial.

End every run with three short lists: done, failed, and not checked.

Details for each operation are in [the execution contract](references/execution-contract.md). The map layout and labels are in [the Family Map format](references/family-map-format.md). The plan steps are in [the situations guide](references/situations.md). Components, licences and AI tools are in [the disclosures](references/disclosures.md).
