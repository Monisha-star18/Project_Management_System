from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    Integer,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.employee import EmployeeData
    from app.models.project import ProjectDetails
    from app.models.task import TaskDetails


class ProjectAllotment(Base):
    __tablename__ = "project_allotments"

    __table_args__ = (
        UniqueConstraint("project_id", "employee_id", name="uq_project_employee"),
        Index(
            "ix_project_allotments_employee_id",
            "employee_id",
        ),
    )

    allotment_id: Mapped[int] = mapped_column(
        Integer, Identity(start=100, always=True), primary_key=True
    )

    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.project_id", ondelete="CASCADE")
    )

    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employee.employee_id", ondelete="RESTRICT"),
    )

    allotted_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("NOW()"), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("NOW()"), onupdate=text("NOW()"), nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, server_default=text("true"), nullable=False
    )

    remark_on_remove: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Each allotment belongs to one employee
    employee: Mapped["EmployeeData"] = relationship(
        "EmployeeData",
        back_populates="project_allotments",
    )

    # Each allotment belongs to one project
    project: Mapped["ProjectDetails"] = relationship(
        "ProjectDetails",
        back_populates="allotments",
    )

    # An allotment can have multiple tasks
    tasks: Mapped[list["TaskDetails"]] = relationship(
        "TaskDetails",
        back_populates="allotment",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
