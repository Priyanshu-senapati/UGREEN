# Rules audit: UGREEN Skill Content Safety and Publishing Guidelines

Each clause that applies to Chaabi, the requirement it sets, and where the package meets it. Every "Where" cell names a file in `skill/chaabi/` and a heading or passage that exists in that file.

| Clause | Requirement | Where |
|---|---|---|
| 2.4 | Disclose core actions such as reading local files and sending data out | `references/privacy-and-consent.md#Consent script` |
| 4.1 | Request only the minimum permissions | `SKILL.md#Conversation 1: Set up Chaabi` |
| 4.2 | Access only isolated or explicitly authorised paths | `references/privacy-and-consent.md#Consent script` |
| 4.3 | Use permissions only after explicit consent | `SKILL.md#Required input` |
| 4.5 | Use granted permissions only for the declared function | `references/privacy-and-consent.md#Clause map` |
| 4.6 | Confirm high-impact operations with the user | `references/execution-contract.md#Approval points` |
| 5.3 | No hardcoded credentials or keys | `references/privacy-and-consent.md#Clause map` |
| 6.3 | Protect sensitive data; never collect passwords or tokens | `references/family-map-format.md#Privacy rules inside the map` |
| 6.4 | No undisclosed transmission of personal information | `SKILL.md#Goal` |
| 7.1 | No personal information in packages or examples | `references/family-map-format.md#4. Item cards` |
| 7.3 | No real financial operations without secondary confirmation | `SKILL.md#Goal` |
| 9.3 | Disclose risks and boundaries in high-risk areas | `references/situations.md#Situations guide` |
| 10.1 | Inform the user and get consent before handling personal information | `references/privacy-and-consent.md#Consent script` |
| 11.4 | Disclose the permissions and data flows of third-party content | `references/disclosures.md#AI tools used` |

Audit notes:
- The official kit checker reports static-pass with 0 errors and 0 warnings, so no credential literal, remote download, script, direct file access or unregistered agent is present.
- The examples use the synthetic Sharma family and fictional institutions only.
