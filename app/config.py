import os
from functools import lru_cache
from typing import Optional

try:
    from google.cloud import secretmanager
    _SM_AVAILABLE = True
except ImportError:
    _SM_AVAILABLE = False


def _get_secret(project: str, name: str) -> Optional[str]:
    if not _SM_AVAILABLE:
        return None
    try:
        client = secretmanager.SecretManagerServiceClient()
        path = f"projects/{project}/secrets/{name}/versions/latest"
        resp = client.access_secret_version(name=path)
        return resp.payload.data.decode("utf-8").strip()
    except Exception:
        return None


def _load(env_key: str, secret_name: str, project: str, use_sm: bool) -> str:
    val = os.getenv(env_key, "")
    if val:
        return val
    if use_sm:
        val = _get_secret(project, secret_name) or ""
    return val


@lru_cache(maxsize=1)
def get_config() -> dict:
    project = os.getenv("GCP_PROJECT_ID", "durable-river-477504-v9")
    use_sm = os.getenv("USE_SECRET_MANAGER", "false").lower() == "true"
    return {
        "google_client_id":     _load("GOOGLE_CLIENT_ID",     "google-oauth-client-id",     project, use_sm),
        "google_client_secret": _load("GOOGLE_CLIENT_SECRET",  "google-oauth-client-secret", project, use_sm),
        "google_refresh_token": _load("GOOGLE_REFRESH_TOKEN",  "google-oauth-refresh-token", project, use_sm),
        "google_user_email":    _load("GOOGLE_USER_EMAIL",     "google-user-email",          project, use_sm),
        "highlevel_token":      _load("HIGHLEVEL_TOKEN",       "highlevel-token",            project, use_sm),
        "highlevel_location_id":_load("HIGHLEVEL_LOCATION_ID", "highlevel-location-id",      project, use_sm),
        "tardis_system_prompt": _load("TARDIS_SYSTEM_PROMPT",  "tardis-system-prompt",       project, use_sm),
        "gcp_project_id":       project,
    }


def config_status() -> dict:
    c = get_config()
    return {
        "google_oauth":     bool(c["google_client_id"] and c["google_refresh_token"]),
        "google_user_email":bool(c["google_user_email"]),
        "highlevel":        bool(c["highlevel_token"]),
        "vertex_ai":        bool(c["gcp_project_id"]),
    }
