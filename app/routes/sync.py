from fastapi import APIRouter
from app.services.sync_service import run_sync

router = APIRouter()

@router.post("/sync")
def sync():
    data = run_sync()
    return data.model_dump()
