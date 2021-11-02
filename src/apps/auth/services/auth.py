from fastapi.exceptions import HTTPException
from fastapi import Depends

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError, InvalidHeaderError

from src.apps.auth.models import User

from passlib.context import CryptContext


class Password:
    hashing = CryptContext(schemes=['bcrypt'])

    def encode_password(self, password: str) -> str:
        return self.hashing.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.hashing.verify(password, hashed_password)


def user_exists(username: str) -> bool:
    try:
        User.get(User.username == username)
        return True
    except User.DoesNotExist:
        return False


def create_user(username: str, password: str) -> User:
    user_model = User.create(
        username=username, 
        hashed_password=Password().encode_password(password)
    )
    return user_model


def get_user_model(username: str) -> User:
    return User.get(User.username == username)


def check_user_auth(authorize: AuthJWT = Depends()) -> None:
    try:
        authorize.jwt_required()
    except MissingTokenError:
        raise HTTPException(status_code=401, detail="Token header missing")

    try:
        authorize.get_jwt_subject()
    except InvalidHeaderError:
        raise HTTPException(status_code=401, detail="Invalid token")
