
from pydantic import BaseModel, ConfigDict, Field


class AllotmentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    employee_id: int = Field(gt=0)


class AllottedEmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    employee_id: int
    full_name: str
    role: str


class AllotmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    allotment_id: int
    project_id: int
    employee_id: int
    employee_name : str
    role: str


class AllotmentListResponse(BaseModel):
    project_id: int
    total: int
    members: list[AllotmentResponse]
