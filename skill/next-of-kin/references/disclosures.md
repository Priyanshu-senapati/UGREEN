# Disclosures

## Third-party components

The Next of Kin package contains no third-party code, libraries, models or assets. Every file in it is original Markdown written for this hackathon.

These tools were used to build and test the package. None of them is included in it:

| Component | Version | Source | Used for |
|---|---|---|---|
| uliya-skill-kit | 0.7.3 | UGREEN Skill Developer Package (ai.ugreen.com hackathon starter kit) | Capability catalog and the official static checker |
| Playwright for Python | 1.64.1 | github.com/microsoft/playwright-python | Rendering the synthetic sample documents and the proposal PDF |
| Pillow | 13.0.0 | github.com/python-pillow/Pillow | Making phone-photo versions of the sample documents |
| pypdf | 6.21.4 | github.com/py-pdf/pypdf | Reading the sample PDFs in tests |
| Markdown | 3.11.2 | github.com/Python-Markdown/markdown | Converting the proposal to HTML before printing it as a PDF |
| pytest | 9.2.0 | github.com/pytest-dev/pytest | Running the package, sample-data and simulation tests |
| edge-tts | 7.3.1 | github.com/rany2/edge-tts | Optional text-to-speech for the two synthetic voice notes. It sends only the synthetic script text to Microsoft's online speech service. |
| Nirmala UI font | Windows system font | Microsoft Windows | Rendering Hindi text in the synthetic sample images only |

## Licences

| Component | Licence |
|---|---|
| uliya-skill-kit 0.7.3 | Provided by UGREEN for the hackathon. Used as published; not redistributed. |
| Playwright for Python | Apache-2.0 |
| Pillow | MIT-CMU |
| pypdf | BSD-3-Clause |
| Markdown | BSD-3-Clause |
| pytest | MIT |
| edge-tts | LGPL-3.0 |
| Nirmala UI font | Microsoft font licence, part of Windows. Not redistributed. |

## AI tools used

- **Claude Code (Anthropic).** Principal uses: researching the hackathon rules and the capability catalog, designing the workflow with the builder, drafting the Markdown files, writing the tests, generating the synthetic sample family, and running the simulated conversations.
- **Uliya (UGREEN), at runtime.** The Skill delegates its work to Uliya's registered NAS agents. The AI model behind Uliya is the one the family chooses, local or cloud. See [Privacy and consent](privacy-and-consent.md).

## Work done during the hackathon

All of Next of Kin was conceived and built during the UGREEN Hackathon 2026: the idea, the design, every file in the package, the synthetic test family and the tests. Nothing was reused from earlier projects or earlier submissions.

The principal functionality developed for the hackathon is:
- zero-form discovery of a family's existing documents, document photos and voice notes;
- the source-linked Family Map, with labels for verified, unverified, conflicting and missing facts;
- the readiness check;
- the "what if someone is unavailable" continuity plan grounded in the family's own documents;
- the consent and privacy rules around all three.
