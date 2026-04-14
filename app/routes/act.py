from fastapi import APIRouter
from app.models.actions import ActionRequest, ActionResult
from app.services.action_service import execute_action

router = APIRouter()

@router.post("/act")
def act(action: ActionRequest, force: bool = False) -> ActionResult:
    return execute_action(action, force=force)
