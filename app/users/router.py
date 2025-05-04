from fastapi import APIRouter, Response
from fastapi.params import Depends

from app.exceptions import UserAlreadyExistsExceptions, IncorrectEmailOrPasswordException
from app.users.auth import get_password_hash, authenticate_user, create_access_token, create_refresh_token
from app.users.dao import UsersDao
from app.users.dependencies import get_current_user
from app.users.schemas import SUserAuth
from app.users.models import Users

router = APIRouter(
    prefix="/auth",
    tags=["Auth "]
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDao.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsExceptions
    hashed_password = get_password_hash(user_data.password)
    await UsersDao.add(email=user_data.email, hashed_password=hashed_password)


@router.post
def logout_user(response: Response):
    response.delete_cookie("token")
    return dict(
        message="Logged out successfully"
    )

@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    refresh_token = create_refresh_token({"sub": str(user.id)})
    response.set_cookie("token", value=refresh_token, httponly=True, secure=True, samesite="strict")

    access_token = create_access_token({"sub":str(user.id)})

    return access_token


@router.post("/refresh")
async def refresh_user(current_user:Users=Depends(get_current_user)):
    new_access_token = create_access_token({"sub": str(current_user.id)})
    return new_access_token