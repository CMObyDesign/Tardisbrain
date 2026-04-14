from fastapi import APIRouter
from app.services.sync_service import run_sync
from app.services.planning_service import run_plan
from app.utils.logging import get_logger

router = APIRouter()
log = get_logger()

@router.post("/run")
def run():
    log.info("run_started")
    data = run_sync()
    log.info("sync_complete", email_count=len(data.emails))
    try:
        plan = run_plan(data)
        log.info("plan_complete")
        return {"sync": data.model_dump(), "plan": plan.model_dump()}
    except Exception as e:
        log.error("plan_failed", error=str(e))
        return {"sync": data.model_dump(), "plan_error": str(e)}
