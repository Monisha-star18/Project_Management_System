
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Role = Literal["admin","team_lead","employee"]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str