from sqlalchemy import Column, Integer, String, Date, ForeignKey
from db import Base


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(String, index=True)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    reason = Column(String, nullable=False)
    leave_type = Column(String, nullable=False)

    status = Column(String, default="pending")

    approved_by = Column(String, nullable=True)