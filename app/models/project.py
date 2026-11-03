from datetime import date, datetime

from sqlalchemy import DateTime, ForeignKey, Integer,String,Identity,UniqueConstraint,Date,Boolean, text,Index,CheckConstraint
from sqlalchemy.orm import Mapped,mapped_column

from app.database.base import Base

class ProjectDetails(Base):

    __tablename__="projects"

    __table_args__ =(
        CheckConstraint(
            "status IN ('planning','started','pending','completed','dropped')",
            name="ck_project_status"
        ),

        CheckConstraint(
            "expected_end_date >= start_date",
            name="ck_project_date"
        ),

        UniqueConstraint("project_name",
                        name="uq_project_name"),

        Index("ix_lead_id", "lead_id"),

        Index("ix_status", "status"),
    
    )

    project_id:Mapped[int] = mapped_column(Integer,
                                           Identity(start=1010, always=True),
                                           primary_key=True
                                           )

    project_name:Mapped[str] = mapped_column(String(100),
                                             nullable=False
                                             )

    project_description:Mapped[str|None] = mapped_column(String(500),
                                                    nullable=True
                                                    )

    lead_id:Mapped[int] = mapped_column(Integer,
                                        ForeignKey("employee.employee_id", ondelete="RESTRICT"),
                                        )

    start_date:Mapped[date]=mapped_column(Date,
                                          nullable=False
                                          )

    expected_end_date:Mapped[date] = mapped_column(Date,
                                                   nullable=False
                                                   )

    status:Mapped[str] = mapped_column(String(10),
                                       default="planning",
                                       server_default="planning"
                                       )

    created_by:Mapped[int] = mapped_column(Integer,
                                           ForeignKey("employee.employee_id", ondelete="RESTRICT"),
                                           )

    created_at :Mapped[datetime] = mapped_column(DateTime,
                                                server_default=text("NOW()"),
                                                nullable=False
                                                )
    
    updated_at:Mapped[datetime] = mapped_column(DateTime,
                                                server_default=text("NOW()"),
                                                onupdate=text("NOW()"),
                                                nullable=False
                                                )
    
    