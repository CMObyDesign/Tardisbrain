from googleapiclient.discovery import build
from app.clients.google_auth import get_credentials
from app.models.sync import DriveDoc


def list_recent_docs(max_results: int = 10) -> list[DriveDoc]:
    service = build("drive", "v3", credentials=get_credentials())
    result = service.files().list(
        q="mimeType='application/vnd.google-apps.document'",
        orderBy="modifiedTime desc",
        pageSize=max_results,
        fields="files(id,name,modifiedTime,webViewLink)",
    ).execute()
    return [
        DriveDoc(id=f["id"], name=f["name"],
                 modified=f.get("modifiedTime", ""),
                 url=f.get("webViewLink", ""))
        for f in result.get("files", [])
    ]


def create_doc(title: str, content: str) -> dict:
    drive = build("drive", "v3", credentials=get_credentials())
    docs = build("docs", "v1", credentials=get_credentials())
    meta = drive.files().create(
        body={"name": title, "mimeType": "application/vnd.google-apps.document"}
    ).execute()
    doc_id = meta["id"]
    docs.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": [{"insertText": {"location": {"index": 1}, "text": content}}]},
    ).execute()
    return {"doc_id": doc_id, "title": title,
            "url": f"https://docs.google.com/document/d/{doc_id}/edit"}


def append_to_doc(doc_id: str, content: str) -> dict:
    docs = build("docs", "v1", credentials=get_credentials())
    doc = docs.documents().get(documentId=doc_id).execute()
    end_index = doc["body"]["content"][-1]["endIndex"] - 1
    docs.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": [{"insertText": {"location": {"index": end_index}, "text": f"\n{content}"}}]},
    ).execute()
    return {"doc_id": doc_id, "appended": True}
