from datetime import datetime, timedelta, timezone


from jose import jwt
from passlib.context import CryptContext

from app.config import settings
from app.users.dao import UsersDao


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict, secret_key: str, expiration_time: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expiration_time
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, secret_key, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_access_token(data: dict) -> str:
    return create_token(data, settings.SECRET_KEY_ACCESS, timedelta(minutes=settings.ACCESS_TIME_TOKEN))


def create_refresh_token(data: dict) -> str:
    return create_token(data, settings.SECRET_KEY_REFRESH, timedelta(days=settings.REFRESH_TOKEN_EXPIRATION))




async def authenticate_user(email, password: str):
    user = await UsersDao.find_one_or_none(email=email)
    if not user and not verify_password(password, user.password):
        return None
    return user
