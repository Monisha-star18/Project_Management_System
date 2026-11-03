
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependency.auth import (
    get_auth_service,
    get_current_user,
    require_roles
)
from app.services.auth_service import AuthService
from app.models.user import UsersDetails
from app.schemas.auth import TokenResponse, CurrentUserResponse


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
    service: AuthService = Depends(get_auth_service)
) -> TokenResponse:

    token = await service.login(username=form.username,password=form.password)

    return TokenResponse( access_token=token, token_type="bearer")


@router.get(
    "/me",
    response_model=CurrentUserResponse,
    summary="Get current user"
)
async def get_me(
    current_user: UsersDetails = Depends(get_current_user) ) -> UsersDetails:

    return current_user
