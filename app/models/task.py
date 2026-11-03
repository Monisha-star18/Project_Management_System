from datetime import date, datetime

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.employee import EmployeeData
from app.models.project_allotment import ProjectAllotment


class TaskDetails(Base):
    __tablename__ = "tasks"

    # Database Check Constraints
    __table_args__ = (
        CheckConstraint(
            "status IN ('todo', 'in_progress', 'completed', 'on_hold')",
            name="ck_tasks_status",
        ),
        CheckConstraint(
            "priority IN ('low', 'medium', 'high', 'urgent')", name="ck_tasks_priority"
        ),
        CheckConstraint(
            "progress_percentage BETWEEN 0 AND 100", name="ck_tasks_progress_percentage"
        ),
        CheckConstraint("due_date >= start_date", name="ck_tasks_due_date"),
        Index("ix_tasks_allotment_id", "allotment_id"),
        Index("ix_tasks_assigned_by", "assigned_by"),
    )

    task_id: Mapped[int] = mapped_column(
        Integer, Identity(start=101, always=True), primary_key=True
    )

    allotment_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("project_allotments.allotment_id", ondelete="CASCADE"),
        nullable=False,
    )

    task_title: Mapped[str] = mapped_column(String(150), nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    assigned_by: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "employee.employee_id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    priority: Mapped[str] = mapped_column(
        String(10), nullable=False, server_default="medium"
    )

    start_date: Mapped[date] = mapped_column(Date, nullable=False)

    due_date: Mapped[date] = mapped_column(Date, nullable=False)

    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="todo"
    )

    progress_percentage: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )

    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Project membership receiving this task
    allotment: Mapped["ProjectAllotment"] = relationship(
        "ProjectAllotment",
        back_populates="tasks",
    )

    # Team lead who assigned the task
    assigner: Mapped["EmployeeData"] = relationship(
        "EmployeeData",
        foreign_keys=[assigned_by],
        back_populates="assigned_tasks",
    )
