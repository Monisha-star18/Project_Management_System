
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependency.auth import (
    get_auth_service,
    get_current_user
)
from app.services.auth_service import AuthService
from app.models.employee import EmployeeData
from app.schemas.auth import TokenResponse
from app.schemas.employee import EmployeeDetailsResponse

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login user"
)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
    description="Authenticate a registered user using their email address and password. Returns a JWT access token for accessing protected APIs."
) -> TokenResponse:

    token = await service.login(email_id=form.username , password=form.password)

    return TokenResponse( access_token=token, token_type="bearer")


@router.get(
    "/me",
    response_model= EmployeeDetailsResponse,
    summary="Get current user",
    description="Retrieve the authenticated user's profile details using a valid JWT access token."
)
async def get_me(
    current_user: EmployeeData = Depends(get_current_user) ) -> EmployeeData:

    return current_user
