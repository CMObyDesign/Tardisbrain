from googleapiclient.discovery import build
from datetime import datetime, timezone, timedelta
from app.clients.google_auth import get_credentials
from app.models.sync import CalendarEvent


def list_upcoming_events(days: int = 7) -> list[CalendarEvent]:
    service = build("calendar", "v3", credentials=get_credentials())
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=days)
    result = service.events().list(
        calendarId="primary",
        timeMin=now.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy="startTime",
        maxResults=20,
    ).execute()
    events = []
    for e in result.get("items", []):
        start = e["start"].get("dateTime", e["start"].get("date", ""))
        end_t = e["end"].get("dateTime", e["end"].get("date", ""))
        attendees = [a["email"] for a in e.get("attendees", [])]
        events.append(CalendarEvent(
            id=e["id"],
            title=e.get("summary", "(no title)"),
            start=start,
            end=end_t,
            attendees=attendees,
            meeting_link=e.get("hangoutLink"),
        ))
    return events


def create_event(title: str, start_time: str, end_time: str,
                 attendee_emails: list[str], description: str = "") -> dict:
    service = build("calendar", "v3", credentials=get_credentials())
    body = {
        "summary": title,
        "description": description,
        "start": {"dateTime": start_time, "timeZone": "America/New_York"},
        "end":   {"dateTime": end_time,   "timeZone": "America/New_York"},
        "attendees": [{"email": e} for e in attendee_emails],
    }
    event = service.events().insert(calendarId="primary", body=body).execute()
    return {"event_id": event["id"], "html_link": event.get("htmlLink")}
