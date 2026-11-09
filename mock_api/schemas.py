from datetime import date
from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional


class LeaveCreate(BaseModel):
    start_date: date
    end_date: date
    reason: str = Field(min_length=5, max_length=500)
    leave_type: Literal[
        "casual",
        "sick",
        "earned"
    ]

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError(
                "End date cannot be earlier than start date"
            )
        return self


class LeaveResponse(BaseModel):
    id: int
    employee_id: str
    start_date: date
    end_date: date
    reason: str
    leave_type: str
    status: str
    approved_by: Optional[str] = None

    class Config:
        from_attributes = True