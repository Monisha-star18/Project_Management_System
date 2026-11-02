from datetime import date, datetime
from sqlalchemy import CheckConstraint, DateTime, Integer,String,Identity,UniqueConstraint,Date,Boolean, text,Index,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column

from app.database.base import Base


class UsersDetails(Base):

    __tablename__="users"

    __table_args__=(

        CheckConstraint(
            "role IN ('admin', 'team_lead', 'employee')",
            name="ck_users_role"),
                    
        UniqueConstraint("user_name",
                         name="uq_user_name"),
                
    )

    user_id:Mapped[int] = mapped_column(Integer,
                                        Identity(start=1,always=True),
                                        primary_key=True
                                    )

    employee_id:Mapped[int| None] = mapped_column(Integer,
                                            ForeignKey("employee.employee_id",ondelete="CASCADE"),
                                            nullable=True,
                                            unique=True
                                        )

    user_name:Mapped[str] = mapped_column(String(10),
                                          nullable=False
                                        )

    password_hash:Mapped[str] = mapped_column(String(255),
                                               nullable=False
                                            )
    
    role: Mapped[str] = mapped_column(String(20),
                                    nullable=False,
                                    server_default="employee"
                                    )

    is_active:Mapped[bool] = mapped_column(Boolean,
                                            server_default=text("true"),
                                            nullable=False
                                            )
    
    created_at :Mapped[datetime] = mapped_column(DateTime,
                                                server_default=text("NOW()"),
                                                nullable=False
                                                )

    