from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from app.config import get_config

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]


def get_credentials() -> Credentials:
    cfg = get_config()
    creds = Credentials(
        token=None,
        refresh_token=cfg["google_refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=cfg["google_client_id"],
        client_secret=cfg["google_client_secret"],
        scopes=SCOPES,
    )
    creds.refresh(Request())
    return creds
