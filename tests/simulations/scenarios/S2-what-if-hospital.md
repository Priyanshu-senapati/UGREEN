# S2: What if Papa is in hospital (temporarily unavailable)

- **Today:** 2026-11-10
- **Conversation:** What if someone is unavailable
- **Person asking:** Priya Sharma (daughter). She can read the folder Family/Chaabi.

## User turns (answers in order, as the Skill asks)

1. Opening: "I am Priya. Papa was admitted to hospital this morning. What should we do? His Family Map is in the folder Family/Chaabi."
2. Situation: "Temporarily unavailable. He is in hospital and cannot talk much right now."
3. Save the plan: "No, just show it to me."

## Mocks

### file-agent · ug-filesystem find and read the Family Map in Family/Chaabi
completed. Newest file: Family/Chaabi/Family-Map_2026-11-10.md. Its content is the full text under "## Saved artifact" in tests/simulations/results/S1.md. Use that text as the map.

### document-agent · ug-document qa
- **On health-policy.pdf, about a cashless claim, the hospital desk, pre-authorisation or the TPA:** completed. Quote from Section 9, Cashless claim (p.6):
  1. "At a network hospital, show the health card and photo identity at the insurance desk."
  2. "The hospital sends the pre-authorisation request to the TPA, Sehat Care TPA (fictional)."
  3. "For a planned admission, request pre-authorisation 48 hours in advance. For an emergency admission, request it within 24 hours of admission."
  4. "TPA helpline (24x7): 1800-000-4455"
- **On health-policy.pdf, about reimbursement or bills:** completed. Quote from Section 8 (p.5): "Submit the claim form with original bills within 30 days of discharge."
- **On life-policy.pdf, about the grace period or a missed premium:** completed. Quote from p.3: "A grace period of 30 days is allowed after the due date. If the premium is not paid within the grace period, the policy lapses."
- **On home-loan-statement.pdf, about the EMI:** completed. Quote from p.1: "EMI ₹18,450, due on the 5th of every month."
- **Any other qa:** completed. The document does not state this.

### knowledge-agent · ug-knowledge save-text
Not expected. If called: failed, "no mock for this call".
