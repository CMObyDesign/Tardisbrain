from pydantic import BaseModel
from typing import List, Optional


class EmailItem(BaseModel):
    id: str
    subject: str
    sender: str
    snippet: str
    date: str
    thread_id: str
    needs_reply: bool = False


class CalendarEvent(BaseModel):
    id: str
    title: str
    start: str
    end: str
    attendees: List[str] = []
    meeting_link: Optional[str] = None


class DriveDoc(BaseModel):
    id: str
    name: str
    modified: str
    url: str


class HighLevelContact(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    tags: List[str] = []
    source: Optional[str] = None


class SyncMeta(BaseModel):
    synced_at: str
    errors: List[str] = []


class NormalizedData(BaseModel):
    emails: List[EmailItem] = []
    events: List[CalendarEvent] = []
    docs: List[DriveDoc] = []
    contacts: List[HighLevelContact] = []
    meta: SyncMeta
