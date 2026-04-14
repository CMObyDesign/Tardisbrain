import httpx
from app.config import get_config
from app.models.sync import HighLevelContact

HL_BASE = "https://services.leadconnectorhq.com"


def _headers() -> dict:
    cfg = get_config()
    return {
        "Authorization": f"Bearer {cfg['highlevel_token']}",
        "Version": "2021-07-28",
        "Content-Type": "application/json",
    }


def get_contacts(location_id: str = "", limit: int = 20) -> list[HighLevelContact]:
    cfg = get_config()
    loc = location_id or cfg["highlevel_location_id"]
    with httpx.Client(timeout=15) as client:
        r = client.get(
            f"{HL_BASE}/contacts/",
            headers=_headers(),
            params={"locationId": loc, "limit": limit},
        )
        r.raise_for_status()
    contacts = []
    for c in r.json().get("contacts", []):
        contacts.append(HighLevelContact(
            id=c["id"],
            name=c.get("contactName") or f"{c.get('firstName','')} {c.get('lastName','')}".strip(),
            email=c.get("email"),
            phone=c.get("phone"),
            tags=c.get("tags", []),
            source=c.get("source"),
        ))
    return contacts


def get_workflows(location_id: str = "") -> dict:
    cfg = get_config()
    loc = location_id or cfg["highlevel_location_id"]
    with httpx.Client(timeout=15) as client:
        r = client.get(f"{HL_BASE}/workflows/", headers=_headers(), params={"locationId": loc})
        r.raise_for_status()
    return r.json()
