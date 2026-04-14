from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class Owner(str, Enum):
    LIZ = "liz"
    LILY = "lily"
    BOTH = "both"


class Priority(BaseModel):
    title: str
    reason: str
    owner: Owner
    urgency: str  # high / medium / low
    suggested_action: Optional[str] = None


class Handoff(BaseModel):
    description: str
    from_owner: Owner
    to_owner: Owner
    blocked_by: Optional[str] = None


class Risk(BaseModel):
    description: str
    impact: str
    mitigation: Optional[str] = None


class ProposedAction(BaseModel):
    type: str
    owner: Owner
    reason: str
    approval_required: bool = True
    payload: dict = {}


class PlanningOutput(BaseModel):
    priorities_liz: List[Priority] = []
    priorities_lily: List[Priority] = []
    handoffs: List[Handoff] = []
    risks: List[Risk] = []
    proposed_actions: List[ProposedAction] = []
    summary: str = ""
