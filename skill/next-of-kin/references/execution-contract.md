# Execution contract

The parent Skill never runs NAS actions itself. It delegates each operation to the agent that owns the action and uses only the real result that agent returns. This contract fixes, for every operation, what must be true first, who does it, what comes back, and what happens when it goes wrong.

## Ground rules

1. Handle every delegation state explicitly:
   - `completed`: use the returned result.
   - `failed` or `cancelled`: mark the step failed and stop every step that depends on it.
   - `waiting_user` or `waiting_approval`: pause and ask the user. Never assume a yes.
2. Never fill a gap with a guess. Facts from a failed step are absent and labelled, never invented.
3. Label an item **Missing** only when the search for it actually ran and returned an empty list. If the search itself failed, label it **Not searched**.
4. Keep partial results and label them **Partial**. Report what is known, not more.
5. End every run with three lists: done · failed · not checked.

## Conversation 1: Set up Next of Kin

Operation numbers identify operations, not their order. `SKILL.md` sets the order. For example, voice notes are transcribed (operation 8) before their Hindi sentences are translated (operation 7).

### 1. Consent and privacy
- **Precondition:** The owner is present.
- **Permissions:** None yet. Nothing has been read.
- **Agent and action:** Skill (no delegation). Runs the consent script in `privacy-and-consent.md`.
- **Expected output:** Owner name, consent, model setting, allowed folders, voice-note language.
- **Approval:** The owner's explicit yes, plus a separate explicit yes for a cloud model or a "not sure" answer.
- **Failure condition:** No consent, or no explicit yes for a cloud model.
- **Recovery:** Explain why Next of Kin cannot continue. Nothing is read.
- **Continue:** Stop.

### 2. Check folder access
- **Precondition:** At least one folder named by the owner.
- **Permissions:** Read access to each named folder for the person running the Skill.
- **Agent and action:** file-agent, `ug-filesystem` `stat` (and `ug-filesystem` `ls` when a listing is needed).
- **Expected output:** Accessible or not accessible, per folder.
- **Approval:** None.
- **Failure condition:** A folder cannot be opened.
- **Recovery:** Tell the owner which folder could not be opened, and drop it from this run.
- **Continue:** Yes, if at least one folder is accessible. Otherwise stop.

### 3. Find documents and audio
- **Precondition:** At least one accessible folder.
- **Permissions:** Read access to the accessible folders only.
- **Agent and action:** file-agent, `ug-filesystem` `find` (types documents and audio) and `ug-filesystem` `stat` for modified dates.
- **Expected output:** Source list with path, type and last-modified date.
- **Approval:** None.
- **Failure condition:** The search fails, or a folder returns an empty list.
- **Recovery:** Report "no documents found in" that folder for an empty list. Report the failure for a failed search.
- **Continue:** Yes, if any file was found in any folder.

### 4. Find document photos
- **Precondition:** At least one accessible allowed folder. Scans and phone photos of documents can sit in any of them.
- **Permissions:** Read access to the allowed folders only.
- **Agent and action:** photo-agent, `ug-photo` `search-picture` with `ocr-contains` search terms (policy, premium, passbook, nominee, deed, receipt, Aadhaar, identity, बीमा, खाता, पेंशन), limited to the allowed folders.
- **Expected output:** List of candidate photos whose indexed text matches.
- **Approval:** None.
- **Failure condition:** The action is unsupported or fails.
- **Recovery:** Report that photos were not searched. Never open all photos instead.
- **Continue:** Yes.

### 5. Read documents
- **Precondition:** The source list from operation 3.
- **Permissions:** Read access to the listed files.
- **Agent and action:** document-agent, `ug-document` `extract` (schema mixed or contract), in batches of at most 60 files.
- **Expected output:** Per file: item type, institution, reference (last 4 characters only), holder, nominee, dates, amounts with an as-of date, contacts, page; and for Hindi lines, the original sentence.
- **Approval:** None.
- **Failure condition:** A file cannot be read, or a batch fails.
- **Recovery:** Label the file **Unreadable** and list it. Keep the facts from files that were read.
- **Continue:** Yes, with **Partial** results.

### 6. Read document photos
- **Precondition:** Candidate photos from operation 4.
- **Permissions:** Read access to those photos only.
- **Agent and action:** photo-agent, `ug-photo` `vision-vlm` with the same field list; `ug-photo` `vision-ocr` as a fallback.
- **Expected output:** The same fields as operation 5, per photo.
- **Approval:** None.
- **Failure condition:** A photo cannot be read by either action.
- **Recovery:** Label the photo **Unreadable**.
- **Continue:** Yes, with **Partial** results.

### 7. Translate Hindi sentences
- **Precondition:** An original Hindi sentence (at most 2 sentences) supporting a fact.
- **Permissions:** None beyond the sentence itself.
- **Agent and action:** document-agent, `ug-document` `translate` with the sentence as content and target language English.
- **Expected output:** An English translation, labelled as a translation.
- **Approval:** The NAS may ask for approval. If it does, ask the owner.
- **Failure condition:** Translation fails, or the owner declines.
- **Recovery:** Keep the original sentence and label the fact **Not translated**.
- **Continue:** Yes.

### 8. Transcribe voice notes
- **Precondition:** Audio files from operation 3.
- **Permissions:** Read access to those audio files.
- **Agent and action:** knowledge-agent, `ug-knowledge` `audio-transcription`, with timestamps. Language hi or en as the owner said; leave the language unset for mixed or unknown.
- **Expected output:** A transcript with timestamped segments for each file.
- **Approval:** None.
- **Failure condition:** Transcription fails.
- **Recovery:** Keep the audio, label it **Not transcribed**, and list it.
- **Continue:** Yes. Facts from voice notes are always **Unverified** until a document confirms them.

### 9. Cross-check the same item
- **Precondition:** At least two sources describing the same reference number or the same property.
- **Permissions:** Read access to those files.
- **Agent and action:** document-agent, `ug-document` `reconcile` on only those files.
- **Expected output:** Agreements and differences between the sources.
- **Approval:** None.
- **Failure condition:** The comparison fails.
- **Recovery:** Label the item **Not cross-checked**. Never claim the sources agree.
- **Continue:** Yes.

### 10. Search for mentioned items
- **Precondition:** A document or voice note mentions an item, such as land papers.
- **Permissions:** Read access to the allowed folders only.
- **Agent and action:** knowledge-agent, `ug-knowledge` `collect-evidence` for that item within the allowed folders.
- **Expected output:** Evidence found, or an empty list.
- **Approval:** None.
- **Failure condition:** The search fails.
- **Recovery:** Label the item **Not searched**, never **Missing**.
- **Continue:** Yes. An empty list means **Missing**.

### 11. Preview and approval
- **Precondition:** Operations 2 to 10 have finished, whatever their outcome.
- **Permissions:** None.
- **Agent and action:** Skill (no delegation). Shows the summary counts and the open findings, and asks for the destination (Private Map or Family Continuity Map).
- **Expected output:** The owner's decision and the destination.
- **Approval:** The owner's explicit yes to save, and the choice of destination.
- **Failure condition:** The owner declines.
- **Recovery:** Save nothing. The summary stays in the chat only.
- **Continue:** Stop.

### 12. Save the map
- **Precondition:** Owner approval and a destination.
- **Permissions:** Write access to the destination folder.
- **Agent and action:** knowledge-agent, `ug-knowledge` `save-text`. File name Family-Map_YYYY-MM-DD.md, with _HHMM added when that name exists. Never overwrite an existing file.
- **Expected output:** `verified=true` and the output file path.
- **Approval:** The built-in approval of the save action.
- **Failure condition:** The save fails or is not approved.
- **Recovery:** Nothing is overwritten and any previous map stays intact. Offer to retry or to choose another folder.
- **Continue:** Stop.

### 13. Confirm the save
- **Precondition:** The output file path from operation 12.
- **Permissions:** Read access to the destination.
- **Agent and action:** file-agent, `ug-filesystem` `stat` on the output file.
- **Expected output:** The file exists, with its size and time.
- **Approval:** None.
- **Failure condition:** The file is not found.
- **Recovery:** Report "save could not be confirmed".
- **Continue:** No further steps depend on it.

### 14. Tag the original files (optional)
- **Precondition:** The owner opted in.
- **Permissions:** Tag permission on the listed originals.
- **Agent and action:** file-agent, `ug-filemgr` `tag-add-file` (with `ug-filemgr` `tag-list` and `ug-filemgr` `tag-set` to find or create the Next of Kin tag).
- **Expected output:** Tags applied.
- **Approval:** Each tag change needs approval.
- **Failure condition:** Tagging fails or is declined.
- **Recovery:** The map stays valid. Report which files were not tagged.
- **Continue:** Yes.

## Conversation 2 and Conversation 3

### 15. Find and read the latest map
- **Precondition:** The person using the Skill has NAS access to the map folder.
- **Permissions:** Read access to the map folder, granted by the owner or the NAS administrator.
- **Agent and action:** file-agent, `ug-filesystem` `find` for Family-Map files, then `ug-filesystem` `cat`, which reads the newest one.
- **Expected output:** The text of the latest map, with its version and date.
- **Approval:** None.
- **Failure condition:** No access, or no map exists.
- **Recovery:** No access: explain that the map belongs to the owner and only the owner or the NAS administrator can grant access; there is no workaround. No map: offer to run setup with the owner.
- **Continue:** Stop.

### 16. Check for changes
- **Precondition:** The source list in the map.
- **Permissions:** Read access to the allowed folders.
- **Agent and action:** file-agent, `ug-filesystem` `find` for files modified since the map date.
- **Expected output:** New, modified and deleted files.
- **Approval:** None.
- **Failure condition:** The search fails.
- **Recovery:** Run the readiness check from the saved map with the warning "changes not checked".
- **Continue:** Yes.

### 17. Re-check missing items
- **Precondition:** The map lists **Missing** items.
- **Permissions:** Read access to the allowed folders.
- **Agent and action:** knowledge-agent, `ug-knowledge` `collect-evidence` for each missing item.
- **Expected output:** Found, or still an empty list.
- **Approval:** None.
- **Failure condition:** The search fails.
- **Recovery:** Keep the item as "last searched" with the map date.
- **Continue:** Yes.

### 18. Ask the original document
- **Precondition:** The source document is listed in the map.
- **Permissions:** Read access to that document.
- **Agent and action:** document-agent, `ug-document` `qa` on that document for the plan question.
- **Expected output:** A quoted answer with its page.
- **Approval:** None.
- **Failure condition:** The document does not answer the question, or the action fails.
- **Recovery:** Say "Your policy didn't state this; confirm with the insurer" (or the relevant institution).
- **Continue:** Yes.

### 19. Save the report or plan (optional)
- **Precondition:** The user asked to save it.
- **Permissions:** Write access to the chosen folder.
- **Agent and action:** knowledge-agent, `ug-knowledge` `save-text`.
- **Expected output:** `verified=true` and the output file path.
- **Approval:** The built-in approval of the save action.
- **Failure condition:** The save fails.
- **Recovery:** The content stays in the chat.
- **Continue:** No further steps depend on it.

## Approval points

1. Owner consent.
2. Consent for a cloud model, or for a "not sure" answer.
3. Folder scope.
4. Translation, when the NAS asks.
5. Approving the map before it is saved.
6. Choosing Private Map or Family Continuity Map.
7. Each optional tag on an original file.
8. Updating the map after files changed.
