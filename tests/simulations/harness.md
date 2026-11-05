# Simulation harness: the Uliya parent runtime, rehearsed

You are standing in for the Uliya parent runtime running the Next of Kin Skill. There is no NAS. Each scenario file gives the user's turns and a scripted mock result for every delegation the Skill may make. Your job is to show what the Skill would do and produce what it would save.

## Inputs

1. `skill/next-of-kin/SKILL.md` and every reference it links to under `skill/next-of-kin/references/`. Read all of them before starting.
2. One scenario file from `tests/simulations/scenarios/`.

## Rules

1. **Follow the Skill literally.** Do what `SKILL.md` and its references say, in their order. Do not improve on them, skip steps, or add steps they do not ask for. If they are silent or ambiguous, choose the most cautious reading and note it under "Not checked".
2. **User turns come only from the scenario.** When the Skill asks the user something, use the scenario's scripted answer. If the scenario gives no answer, the user has not answered: treat it as `waiting_user`, stop, and record that.
3. **Write every delegation exactly once.** Write the full inline command on its own line, with real values in plain text (no angle-bracket placeholders), for example:
   `delegate --target file-agent --instruction 'Use ug-filesystem stat on ...'`
   On the next line write `Mock:` followed by the status and the data from the scenario's matching mock. Never write the same delegate command a second time anywhere in the result file.
4. **Mocks are the only NAS data.** Use only what the matching mock returns. If no mock matches a delegation, its result is `failed` with "no mock for this call". Never invent file names, facts, dates, pages or timestamps.
5. **Dates.** Today is the date the scenario gives. Do all date arithmetic against it, and always show the raw date beside any computed status.
6. **The saved artifact** is the exact text the Skill passes to `save-text` for the Family Map, or `none` if nothing is saved. A saved readiness report or plan is not the artifact; show it in the transcript instead.
7. **Language.** Write the transcript in English. Keep Hindi exactly as the mocks give it.

## Result file contract

Write `tests/simulations/results/<scenario id>.md` with exactly these headings:

```text
# Result <scenario id>

## Transcript
(alternating **User:** and **Next of Kin:** turns; delegations as in rule 3, each followed by its Mock: line)

## Saved artifact
(the exact Family Map text passed to save-text, or the single word none)

## End-of-run lists
### Done
### Failed
### Not checked
```

Do not add any other `## ` heading outside the saved artifact. The Family Map inside the saved artifact keeps its own numbered headings, `## 1. Header` to `## 7. Sources and changes`.
