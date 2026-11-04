from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

DEPARTMENT = Literal["Unassigned","IT","Finance"]
ROLE = Literal["admin", "employee", "team_lead"]

class EmployeeCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name:str = Field(min_length=3,max_length=50)
    email:EmailStr
    phone:str |None= Field(pattern=r"^[0-9]{10}$")
    department:DEPARTMENT
    role: ROLE = "employee"
    password :str= Field(min_length=8, max_length=16,
                        pattern=r"^[A-Za-z0-9@$!%*?&]+$" )
    joining_date: date 

class EmployeeDetailsResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    employee_id: int
    full_name:str
    email:EmailStr
    phone:str |None = None 
    department:DEPARTMENT
    role: ROLE 

class EmployeeUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: str | None = Field( default=None, min_length=3, max_length=50)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, pattern=r"^[0-9]{10}$")
    department: DEPARTMENT | None = None


class PaginatedEmployeeResponse(BaseModel):
    pages: int
    employees: list[EmployeeDetailsResponse]