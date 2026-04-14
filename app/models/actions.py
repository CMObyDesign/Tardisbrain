from pydantic import BaseModel
from typing import Optional


class DraftEmailPayload(BaseModel):
    to: str
    subject: str
    body: str
    cc: Optional[str] = None


class CreateCalendarEventPayload(BaseModel):
    title: str
    start_time: str   # ISO 8601
    end_time: str
    attendee_emails: list[str] = []
    description: Optional[str] = None


class CreateDocPayload(BaseModel):
    title: str
    content: str


class AppendDocPayload(BaseModel):
    doc_id: str
    content: str


class ActionRequest(BaseModel):
    type: str  # draft_email | create_calendar_event | create_doc | append_doc_notes
    owner: str
    reason: str
    approval_required: bool = True
    payload: dict = {}


class ActionResult(BaseModel):
    type: str
    success: bool
    result: dict = {}
    error: Optional[str] = None
    skipped: bool = False
    skip_reason: Optional[str] = None
