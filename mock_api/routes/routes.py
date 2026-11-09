from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from datetime import date

from db import get_db
from models import LeaveRequest
from schemas import LeaveCreate, LeaveResponse
from auth import get_current_user, require_manager

router = APIRouter(prefix="/leave", tags=["Leave Management"])


# POST /leave
@router.post("", response_model=LeaveResponse, status_code=201)
def create_leave(
    leave: LeaveCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):

    employee_id = user["user_id"]

    # Fetch existing pending and approved requests
    existing_requests = db.query(LeaveRequest).filter(
        LeaveRequest.employee_id == employee_id,
        LeaveRequest.status.in_(["pending", "approved"])
    ).all()

    # Check overlapping requests
    for existing in existing_requests:

        if (
            leave.start_date <= existing.end_date
            and leave.end_date >= existing.start_date
        ):
            raise HTTPException(
                status_code=400,
                detail="Leave request overlaps with an existing request"
            )

    # Calculate leave days for each calendar year
    for year in range(leave.start_date.year, leave.end_date.year + 1):

        year_start = date(year, 1, 1)
        year_end = date(year, 12, 31)

        requested_days = (
            min(leave.end_date, year_end)
            - max(leave.start_date, year_start)
        ).days + 1

        used_days = 0

        for existing in existing_requests:

            overlap_start = max(existing.start_date, year_start)
            overlap_end = min(existing.end_date, year_end)

            if overlap_start <= overlap_end:
                used_days += (overlap_end - overlap_start).days + 1

        if used_days + requested_days > 20:
            raise HTTPException(
                status_code=400,
                detail=f"Maximum 20 leave days allowed in {year}"
            )

    # Create leave request
    new_leave = LeaveRequest(
        employee_id=employee_id,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason,
        leave_type=leave.leave_type,
        status="pending"
    )

    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)

    return new_leave


# GET /leave/{id}
@router.get("/{leave_id}", response_model=LeaveResponse)
def get_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(
            status_code=404,
            detail="Leave request not found"
        )

    # Employees can only view their own requests
    if (
        user["role"] == "employee"
        and leave.employee_id != user["user_id"]
    ):
        raise HTTPException(
            status_code=403,
            detail="You cannot view another employee's leave request"
        )

    return leave


# PUT /leave/{id}/approve
@router.put("/{leave_id}/approve", response_model=LeaveResponse)
def approve_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    manager: dict = Depends(require_manager)
):

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(
            status_code=404,
            detail="Leave request not found"
        )

    if leave.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Only pending leave requests can be approved"
        )

    leave.status = "approved"
    leave.approved_by = manager["user_id"]

    db.commit()
    db.refresh(leave)

    return leave