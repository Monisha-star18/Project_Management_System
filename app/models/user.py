from datetime import date, datetime
from sqlalchemy import DateTime, Integer,String,Identity,UniqueConstraint,Date,Boolean, text,Index,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column

from app.database.base import Base


class UsersDetails(Base):

    __tablename__="users"

    __table_args__=(
        UniqueConstraint("user_name",
                         name="uq_user_name"),
        
        Index("ix_employee_id_user_name", "employee_id","user_name"),
        
    )

    user_id:Mapped[int] = mapped_column(Integer,
                                        Identity(start=1,always=True),
                                        primary_key=True
                                    )

    employee_id:Mapped[int] = mapped_column(Integer,
                                            ForeignKey("employee",ondelete="CASCADE"),
                                            nullable=False
                                        )

    user_name:Mapped[int] = mapped_column(String(10),
                                          nullable=False
                                        )

    password_harsh:Mapped[int] = mapped_column(String(20),
                                               nullable=False
                                            )

    is_active:Mapped[bool] = mapped_column(Boolean,
                                            server_default=True,
                                            nullable=False
                                            )
    
    created_at :Mapped[datetime] = mapped_column(DateTime,
                                                server_default=text("NOW()"),
                                                nullable=False
                                                )

    