from datetime import datetime, timezone
from app.models.sync import NormalizedData, SyncMeta
from app.clients import gmail, calendar, drive, highlevel
from app.utils.logging import get_logger

log = get_logger()


def run_sync() -> NormalizedData:
    errors = []
    emails, events, docs, contacts = [], [], [], []

    def safe(label, fn):
        try:
            return fn()
        except Exception as e:
            log.error("sync_error", source=label, error=str(e))
            errors.append(f"{label}: {e}")
            return []

    emails   = safe("gmail",      lambda: gmail.list_recent_emails(20))
    events   = safe("calendar",   lambda: calendar.list_upcoming_events(7))
    docs     = safe("drive",      lambda: drive.list_recent_docs(10))
    contacts = safe("highlevel",  lambda: highlevel.get_contacts())

    return NormalizedData(
        emails=emails,
        events=events,
        docs=docs,
        contacts=contacts,
        meta=SyncMeta(
            synced_at=datetime.now(timezone.utc).isoformat(),
            errors=errors,
        ),
    )
