from fastapi import APIRouter, HTTPException
from app.models.sync import NormalizedData
from app.services.planning_service import run_plan

router = APIRouter()

@router.post("/plan")
def plan(data: NormalizedData):
    try:
        output = run_plan(data)
        return output.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
