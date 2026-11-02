from datetime import date, datetime

from sqlalchemy import DateTime, ForeignKey, Integer,String,Identity,Date,Boolean, UniqueConstraint, text,Index
from sqlalchemy.orm import Mapped,mapped_column

from app.database.base import Base

class ProjectAllotment(Base):

    __tablename__ = "project_allotments"

    __table_args__ = (
        UniqueConstraint("project_id","employee_id",
            name="uq_project_employee"
        ),
    )


    allotment_id:Mapped[int] = mapped_column(Integer,
                                             Identity(start=100,always=True),
                                             primary_key=True
                                            )

    project_id:Mapped[int] = mapped_column(Integer,
                                           ForeignKey("projects.project_id",ondelete="CASCADE")
                                           )

    employee_id:Mapped[int] = mapped_column(Integer,
                                            ForeignKey("employee.employee_id", ondelete="RESTRICT"),
                                            )

    allotted_by:Mapped[int] = mapped_column(Integer,
                                            ForeignKey("users.user_id", ondelete="RESTRICT"),
                                            )

    allotted_at :Mapped[datetime] = mapped_column(DateTime,
                                                    server_default=text("NOW()"),
                                                    nullable=False
                                                    )
    
    updated_at:Mapped[datetime] = mapped_column(DateTime,
                                                server_default=text("NOW()"),
                                                onupdate=text("NOW()"),
                                                nullable=False
                                                )
    
    is_active:Mapped[bool] = mapped_column(Boolean,
                                            server_default=text("true"),
                                            nullable=False
                                            )

    remark_on_remove:Mapped[str | None] = mapped_column(String(255),
                                                nullable=True)