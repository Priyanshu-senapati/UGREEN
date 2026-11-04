"""The Sharma family: synthetic test data for Next of Kin.

Every person, institution and number here is invented. Institutions are fictional
on purpose: real bank or insurer names on fake documents could read as impersonation.
"""
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Literal

OWNER = "Ramesh Sharma"
FAMILY = {
    "wife": "Sunita Sharma",
    "daughter": "Priya Sharma",
    "son": "Arjun Sharma",
    "brother_in_law": "Suresh Verma",
}
INSTITUTIONS = {
    "life": "Jeevan Suraksha Life Insurance",
    "bank": "Bharat National Bank",
    "health": "Sehat Shield Health Insurance",
    "mf": "Sahyog Mutual Fund",
    "home_loan": "Griha Setu Home Finance",
    "pension": "State Pension Office",
}

LIFE_POLICY_NO = "774019324821"
HEALTH_POLICY_NO = "SSH2025550917"
FD_NO = "30418867205"
LOAN_NO = "GSHF00933370"
MF_FOLIO = "88201546"
AADHAAR_FAKE = "2345 6789 4012"
PAN_FAKE = "ABCPS1234K"
PASSWORD_SECRET = "Ramesh@1962#nb"
TPA_PHONE = "1800-000-4455"
AGENT = "R. Kulkarni"
AGENT_PHONE = "98450 00000"

FULL_IDENTIFIERS = (
    LIFE_POLICY_NO, HEALTH_POLICY_NO, FD_NO, LOAN_NO, MF_FOLIO,
    AADHAAR_FAKE, AADHAAR_FAKE.replace(" ", ""), PAN_FAKE,
)


def premium_due(today: date) -> date:
    return today + timedelta(days=12)


@dataclass(frozen=True)
class Doc:
    relpath: str
    template: str
    kind: Literal["pdf", "scan", "photo", "text"]


PAPA = "Papa Documents"
PHOTOS = "Phone Backup/WhatsApp Images"
VOICE = "Voice Notes"
EMPTY = "Empty Folder"

DOCUMENTS = [
    Doc(f"{PAPA}/life-policy.pdf", "life_policy", "pdf"),
    Doc(f"{PAPA}/nomination-change-letter.pdf", "nomination_change_letter", "pdf"),
    Doc(f"{PAPA}/health-policy.pdf", "health_policy", "pdf"),
    Doc(f"{PAPA}/property-sale-deed.pdf", "property_sale_deed", "pdf"),
    Doc(f"{PAPA}/mutual-fund-statement.pdf", "mutual_fund_statement", "pdf"),
    Doc(f"{PAPA}/home-loan-statement.pdf", "home_loan_statement", "pdf"),
    Doc(f"{PAPA}/pension-order-hi.jpg", "pension_order_hi", "scan"),
    Doc(f"{PAPA}/passwords.txt", "passwords", "text"),
    Doc(f"{PHOTOS}/premium-notice-photo.jpg", "premium_notice", "photo"),
    Doc(f"{PHOTOS}/fd-receipt-photo.jpg", "fd_receipt", "photo"),
    Doc(f"{PHOTOS}/aadhaar-photo.jpg", "aadhaar_card", "photo"),
    Doc(f"{PHOTOS}/life-policy-page1-photo.jpg", "life_policy_page1", "photo"),
    Doc(f"{PHOTOS}/screenshot-recipe.png", "screenshot_recipe", "photo"),
    Doc(f"{PHOTOS}/screenshot-cricket.png", "screenshot_cricket", "photo"),
]
AUDIO = [f"{VOICE}/voice-note-1.mp3", f"{VOICE}/voice-note-2.mp3"]
