from datetime import date, datetime

from sqlalchemy import DateTime, Integer,String,Identity,UniqueConstraint,Date,Boolean, text,Index,CheckConstraint,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column

from app.database.base import Base

class EmployeeData(Base):

    __tablename__="employee"

    __table_args__=(

        UniqueConstraint("email",
                        name="unique_email"),

        UniqueConstraint("phone",
                        name="unique_phone_number"),

        Index("ix_employee_dept_email", "department", "email"),

        Index("ix_employee_is_active", "is_active"),

    )

    employee_id:Mapped[int] = mapped_column(Integer,
                                            Identity(start=101,always=True),
                                            primary_key=True
                                            )

    full_name :Mapped[str] = mapped_column(String(50),
                                           nullable=False 
                                           )

    email:Mapped[str] = mapped_column(String(300),
                                    nullable=False
                                    )

    phone:Mapped[str] = mapped_column(String(10),
                                    nullable=False
                                    )

    department :Mapped[str] = mapped_column(String(30),
                                            default="Unassigned",
                                            server_default="Unassigned",
                                            nullable=False
                                            )

    employee_type:Mapped[str] = mapped_column(String(9),
                                              default="employee",
                                              server_default="employee",
                                              nullable=False
                                              )

    joining_date:Mapped[date] = mapped_column(Date,
                                            nullable=False
                                            )

    is_active:Mapped[bool] = mapped_column(Boolean,
                                        server_default=text("true"),
                                        nullable=False
                                        )

    created_at :Mapped[datetime] = mapped_column(DateTime,
                                                server_default=text("NOW()"),
                                                nullable=False
                                                )