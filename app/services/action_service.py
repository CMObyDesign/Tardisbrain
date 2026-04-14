from app.models.actions import ActionRequest, ActionResult
from app.clients import gmail, calendar, drive
from app.utils.logging import get_logger

log = get_logger()


def execute_action(action: ActionRequest, force: bool = False) -> ActionResult:
    if action.approval_required and not force:
        return ActionResult(
            type=action.type,
            success=False,
            skipped=True,
            skip_reason="approval_required=True — set force=true to execute",
        )

    try:
        if action.type == "draft_email":
            result = gmail.create_draft(
                to=action.payload["to"],
                subject=action.payload["subject"],
                body=action.payload["body"],
                cc=action.payload.get("cc", ""),
            )
        elif action.type == "create_calendar_event":
            result = calendar.create_event(
                title=action.payload["title"],
                start_time=action.payload["start_time"],
                end_time=action.payload["end_time"],
                attendee_emails=action.payload.get("attendee_emails", []),
                description=action.payload.get("description", ""),
            )
        elif action.type == "create_doc":
            result = drive.create_doc(
                title=action.payload["title"],
                content=action.payload["content"],
            )
        elif action.type == "append_doc_notes":
            result = drive.append_to_doc(
                doc_id=action.payload["doc_id"],
                content=action.payload["content"],
            )
        else:
            return ActionResult(type=action.type, success=False,
                                error=f"Unknown action type: {action.type}")

        log.info("action_executed", type=action.type, owner=action.owner)
        return ActionResult(type=action.type, success=True, result=result)

    except Exception as e:
        log.error("action_failed", type=action.type, error=str(e))
        return ActionResult(type=action.type, success=False, error=str(e))
