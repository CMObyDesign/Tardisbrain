import json
import os
from pathlib import Path
from app.models.sync import NormalizedData
from app.models.plan import PlanningOutput
from app.config import get_config
from app.utils.logging import get_logger

log = get_logger()

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "tardis_planner.txt"


def _load_prompt() -> str:
    cfg = get_config()
    override = cfg.get("tardis_system_prompt", "")
    if override:
        return override
    if PROMPT_PATH.exists():
        return PROMPT_PATH.read_text()
    return "You are TARDIS, an AI project manager. Analyze the data and return a structured plan."


def run_plan(data: NormalizedData) -> PlanningOutput:
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel, GenerationConfig
    except ImportError:
        raise RuntimeError("vertexai SDK not installed")

    cfg = get_config()
    vertexai.init(project=cfg["gcp_project_id"], location="us-central1")
    model = GenerativeModel("gemini-1.5-pro-002")

    prompt = _load_prompt()
    user_content = f"""
Operational data (JSON):
{data.model_dump_json(indent=2)}

Return a JSON object matching this schema exactly:
{{
  "priorities_liz": [{{"title":"","reason":"","owner":"liz","urgency":"","suggested_action":""}}],
  "priorities_lily": [{{"title":"","reason":"","owner":"lily","urgency":"","suggested_action":""}}],
  "handoffs": [{{"description":"","from_owner":"liz","to_owner":"lily","blocked_by":""}}],
  "risks": [{{"description":"","impact":"","mitigation":""}}],
  "proposed_actions": [{{"type":"","owner":"liz","reason":"","approval_required":true,"payload":{{}}}}],
  "summary": ""
}}
"""
    response = model.generate_content(
        [prompt, user_content],
        generation_config=GenerationConfig(
            response_mime_type="application/json",
            temperature=0.2,
            max_output_tokens=4096,
        ),
    )
    raw = response.candidates[0].content.parts[0].text
    parsed = json.loads(raw)
    return PlanningOutput(**parsed)
