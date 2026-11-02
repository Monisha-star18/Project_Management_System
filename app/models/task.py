
from datetime import date, datetime

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base 


class TaskDetails(Base):
    __tablename__ = "tasks"

     # Database Check Constraints
    __table_args__ = (
            CheckConstraint(
                "status IN ('todo', 'in_progress', 'completed', 'on_hold')",
                name="ck_tasks_status"
            ),
    
            CheckConstraint(
                "priority IN ('low', 'medium', 'high', 'urgent')",
                name="ck_tasks_priority"
            ),
    
            CheckConstraint(
                "progress_percentage BETWEEN 0 AND 100",
                name="ck_tasks_progress_percentage"
            ),
    
            CheckConstraint(
                "due_date >= start_date",
                name="ck_tasks_due_date"
            ),
        )
    

    
    task_id: Mapped[int] = mapped_column(Integer,
                                        Identity(start=101,always=True),
                                        primary_key=True
                                        )

    
    allotment_id: Mapped[int] = mapped_column(Integer,
                                            ForeignKey("project_allotments.allotment_id"),
                                            nullable=False
                                            )

    
    task_title: Mapped[str] = mapped_column(String(150),
                                            nullable=False
                                            )

    description: Mapped[str | None] = mapped_column(Text,
                                                    nullable=True
                                                    )

    
    assigned_by: Mapped[int] = mapped_column(Integer,
                                            ForeignKey("users.user_id"),
                                            nullable=False
                                            )

    
    priority: Mapped[str] = mapped_column(String(10),
                                        nullable=False,
                                        server_default="medium"
                                        )

    
    start_date: Mapped[date] = mapped_column(Date,
                                            nullable=False
                                            )

    due_date: Mapped[date] = mapped_column(Date,
                                            nullable=False
                                            )

    
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default="todo"
                                        )

    
    progress_percentage: Mapped[int] = mapped_column(Integer,
                                                    nullable=False,
                                                    server_default="0"
                                                    )

    
    remarks: Mapped[str | None] = mapped_column(Text,
                                                nullable=True
                                                )

    
    created_at: Mapped[datetime] = mapped_column( DateTime(timezone=True),
                                                nullable=False,
                                                server_default=func.now()
                                                )

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                nullable=False,
                                                server_default=func.now(),
                                                onupdate=func.now()
                                                )

    