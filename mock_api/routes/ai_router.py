
import os
import json
from datetime import date
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from groq import Groq

from db import get_db
from models import LeaveRequest
from auth import get_current_user
import dotenv


dotenv.load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_1")

router = APIRouter(prefix="/ai", tags=["AI Assistant"])


# Request model
class AIChatRequest(BaseModel):
    message: str


# AI extracted leave details
class LeaveDraft(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    reason: str | None = None
    leave_type: str | None = None


@router.post("/chat")
def ai_chat(
    request: AIChatRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):

    # Check API key
    api_key = GROQ_API_KEY

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Groq API key missing"
        )

    if not request.message.strip():
        raise HTTPException(
            status_code=422,
            detail="Message cannot be empty"
        )

    client = Groq(api_key=api_key)

    employee_id = user["user_id"]
    today = date.today()

    # Get employee's sick leave records
    leaves = db.query(LeaveRequest).filter(
        LeaveRequest.employee_id == employee_id,
        LeaveRequest.leave_type == "sick",
        LeaveRequest.status.in_(["pending", "approved"])
    ).all()

    approved_days = 0
    pending_days = 0

    for leave in leaves:

        start = max(
            leave.start_date,
            date(today.year, 1, 1)
        )

        end = min(
            leave.end_date,
            date(today.year, 12, 31)
        )

        if start <= end:
            days = (end - start).days + 1

            if leave.status == "approved":
                approved_days += days
            else:
                pending_days += days

    # AI instructions
    system_prompt = f"""
    You are an AI Leave Management Assistant.

    Today's date: {today}

    Company Leave Policy:

    1. Maximum 20 leave days per calendar year.
    2. Supported leave types: casual, sick, earned.
    3. Start date and end date are required.
    4. End date cannot be before start date.
    5. Reason is required.
    6. Leave requests are pending until approved by a manager.
    7. Only approved leave is deducted from the balance.
    8. Sick leave entitlement: 10 days per year.
    9. Casual leave entitlement: 5 days per year.
    10. Earned leave entitlement: 5 days per year.

    Employee sick leave information:
    Approved days: {approved_days}
    Pending days: {pending_days}

    Instructions:

    1. Extract start_date, end_date, reason and leave_type
       when the employee requests leave.

    2. Understand dates like tomorrow and next Monday.

    3. Do not guess missing or unclear information.

    4. Ask the employee for missing details.

    5. Answer policy questions using the policy above.

    6. Never approve a leave request.

    7. Never expose another employee's private information.

    8. For unrelated questions, use intent out_of_scope.

    9. Do not claim that a leave request has been saved.

    Return JSON only:

    {{
        "intent": "leave_draft, policy_question or out_of_scope",
        "reply": "Your response",
        "draft": {{
            "start_date": null,
            "end_date": null,
            "reason": null,
            "leave_type": null
        }},
        "needs_clarification": false
    }}
    """

    try:

        # Call Groq AI
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )

        result = json.loads(
            response.choices[0].message.content
        )

        # Policy question or unrelated question
        if result.get("intent") != "leave_draft":
            return result

        # Validate AI extracted details
        draft = LeaveDraft(**(result.get("draft") or {}))

        # Check missing details
        if (
            not draft.start_date
            or not draft.end_date
            or not draft.reason
            or not draft.leave_type
        ):
            result["needs_clarification"] = True
            result["draft"] = draft.model_dump(mode="json")

            return result

        # Validate leave type
        if draft.leave_type not in ["casual", "sick", "earned"]:
            raise HTTPException(
                status_code=422,
                detail="Invalid leave type"
            )

        # Validate date range
        if draft.end_date < draft.start_date:
            raise HTTPException(
                status_code=422,
                detail="End date cannot be before start date"
            )

        # Calculate requested leave days
        leave_days = (
            draft.end_date - draft.start_date
        ).days + 1

        if leave_days > 20:
            raise HTTPException(
                status_code=400,
                detail="Maximum 20 leave days allowed"
            )

        # Check overlapping leave requests
        existing_leave = db.query(LeaveRequest).filter(
            LeaveRequest.employee_id == employee_id,
            LeaveRequest.status.in_(["pending", "approved"]),
            LeaveRequest.start_date <= draft.end_date,
            LeaveRequest.end_date >= draft.start_date
        ).first()

        if existing_leave:
            raise HTTPException(
                status_code=400,
                detail="Leave request overlaps with an existing request"
            )

        # Save leave request in database
        new_leave = LeaveRequest(
            employee_id=employee_id,
            start_date=draft.start_date,
            end_date=draft.end_date,
            reason=draft.reason,
            leave_type=draft.leave_type,
            status="pending"
        )

        db.add(new_leave)
        db.commit()
        db.refresh(new_leave)

        # Return saved request
        return {
            "intent": "leave_draft",
            "message": "Leave request saved successfully",
            "leave_id": new_leave.id,
            "employee_id": new_leave.employee_id,
            "start_date": new_leave.start_date,
            "end_date": new_leave.end_date,
            "reason": new_leave.reason,
            "leave_type": new_leave.leave_type,
            "status": new_leave.status
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=502,
            detail="AI service or database operation failed"
        )
