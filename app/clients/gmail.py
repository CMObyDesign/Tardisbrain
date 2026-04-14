import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from app.clients.google_auth import get_credentials
from app.models.sync import EmailItem


def list_recent_emails(max_results: int = 20) -> list[EmailItem]:
    service = build("gmail", "v1", credentials=get_credentials())
    result = service.users().messages().list(
        userId="me", maxResults=max_results, q="is:inbox"
    ).execute()
    messages = result.get("messages", [])
    items = []
    for m in messages:
        msg = service.users().messages().get(userId="me", id=m["id"]).execute()
        headers = {h["name"]: h["value"] for h in msg["payload"].get("headers", [])}
        items.append(EmailItem(
            id=msg["id"],
            thread_id=msg["threadId"],
            subject=headers.get("Subject", "(no subject)"),
            sender=headers.get("From", ""),
            snippet=msg.get("snippet", ""),
            date=headers.get("Date", ""),
        ))
    return items


def create_draft(to: str, subject: str, body: str, cc: str = "") -> dict:
    service = build("gmail", "v1", credentials=get_credentials())
    mime = MIMEText(body)
    mime["to"] = to
    mime["subject"] = subject
    if cc:
        mime["cc"] = cc
    raw = base64.urlsafe_b64encode(mime.as_bytes()).decode()
    draft = service.users().drafts().create(
        userId="me", body={"message": {"raw": raw}}
    ).execute()
    return {"draft_id": draft["id"], "to": to, "subject": subject}
