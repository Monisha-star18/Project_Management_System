from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.employee import EmployeeData
    from app.models.project_allotment import ProjectAllotment


class ProjectDetails(Base):
    __tablename__ = "projects"

    __table_args__ = (
        CheckConstraint(
            "status IN ('planning','started','pending','completed','dropped')",
            name="ck_project_status",
        ),
        CheckConstraint("expected_end_date >= start_date", name="ck_project_date"),
        UniqueConstraint("project_name", name="uq_project_name"),
        Index("ix_lead_id", "lead_id"),
        Index("ix_status", "status"),
    )

    project_id: Mapped[int] = mapped_column(
        Integer, Identity(start=1010, always=True), primary_key=True
    )

    project_name: Mapped[str] = mapped_column(String(100), nullable=False)

    project_description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    lead_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employee.employee_id", ondelete="RESTRICT"),
        nullable=False,
    )

    start_date: Mapped[date] = mapped_column(Date, nullable=False)

    expected_end_date: Mapped[date] = mapped_column(Date, nullable=False)

    status: Mapped[str] = mapped_column(
        String(10), default="planning", server_default="planning"
    )

    created_by: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employee.employee_id", ondelete="RESTRICT"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("NOW()"), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # The team lead responsible for this project
    lead: Mapped["EmployeeData"] = relationship(
        "EmployeeData",
        foreign_keys=[lead_id],
        back_populates="led_projects",
    )

    # The admin who created this project
    creator: Mapped["EmployeeData"] = relationship(
        "EmployeeData",
        foreign_keys=[created_by],
        back_populates="created_projects",
    )

    # Employees allotted to this project
    allotments: Mapped[list["ProjectAllotment"]] = relationship(
        "ProjectAllotment",
        back_populates="project",
        passive_deletes=True,
    )
