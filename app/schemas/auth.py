
from typing import Literal

from pydantic import BaseModel, ConfigDict


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

class LoginRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_name:str
    password:str
    role:Role