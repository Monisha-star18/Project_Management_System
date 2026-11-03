
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Role = Literal["admin","team_lead","employee"]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CurrentUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    user_name: str
    role: Role
    is_active: bool
    employee_id: int | None

class RegisterUserRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    employee_id : int 
    user_name : str = Field(min_length=3,max_length=10)
    password : str
    role : Role = "employee"