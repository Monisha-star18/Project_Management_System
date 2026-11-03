from datetime import date , datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

DEPARTMENT = Literal["Unassigned","IT","HR","Finance"]
EMPLOYEE_TYPE = Literal["employee","team_lead"]

class EmployeeCreate(BaseModel):

    model_config = ConfigDict(extra="forbid")

    full_name:str = Field(min_length=3,max_length=50)
    email:EmailStr
    phone:str = Field(pattern=r"^[0-9]{10}$")
    department:DEPARTMENT
    employee_type: EMPLOYEE_TYPE = "employee"
    joining_date: date 

class EmployeeResponse(EmployeeCreate):

    model_config = ConfigDict(from_attributes=True)

    employee_id: int
    is_active: bool
    created_at: datetime
