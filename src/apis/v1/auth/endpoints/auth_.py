from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError, InvalidHeaderError

from src.apps.auth.schemas import (
    UserSchema, 
    BaseDetailAboutUserSchema, 
    SettingsSchema
)
from src.apps.auth.services.auth import (
    user_exists, 
    create_user, 
    get_user_model,
    Password
)


auth_router_ = APIRouter(tags=["Auth"])
security = HTTPBearer()


@AuthJWT.load_config
def get_config():
    return SettingsSchema()


@auth_router_.post("/auth")
async def auth(
    user: UserSchema, 
    authorize: AuthJWT = Depends()
) -> JSONResponse:
    if user_exists(user.username):
        user_model = get_user_model(user.username)

        if not Password().verify_password(
            password=user.password, hashed_password=user_model.hashed_password
        ):
            return JSONResponse({
                "detail": "Username or password incorrect"
            }, status_code=401)

        access_token = authorize.create_access_token(user.username)
        refresh_token = authorize.create_refresh_token(user.username)
        
        return JSONResponse({
            "access_token": access_token, 
            "refresh_token": refresh_token
        }, status_code=201)
    return JSONResponse({
        "detail": "Username or password incorrect"
    }, status_code=401)


@auth_router_.post("/signup")
async def signup(user: UserSchema) -> JSONResponse:
    if not user_exists(user.username):
        create_user(username=user.username, password=user.password)
        return JSONResponse({
            "detail": "User successful created"
        }, status_code=201)
    else:
        return JSONResponse({"detail": "User does exists"}, status_code=400)


@auth_router_.post("/refresh")
async def refresh(
    authorize: AuthJWT = Depends(), 
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> JSONResponse:
    try:
        authorize.jwt_required()
    except MissingTokenError:
        return JSONResponse({"detail": "Invalid token"}, status_code=401)

    try:
        current_user = authorize.get_jwt_subject()

        access_token = authorize.create_access_token(current_user)
        refresh_token = authorize.create_refresh_token(current_user)

        return JSONResponse({
            "new_access_token": access_token, 
            "new_refresh_token": refresh_token
        }, status_code=201)
    except InvalidHeaderError:
        return JSONResponse({"detail": "Invalid token"}, status_code=401)


@auth_router_.get("/user", response_model=BaseDetailAboutUserSchema)
async def base_detail_about_user(
    authorize: AuthJWT = Depends(), 
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> list[UserSchema]:
    try:
        authorize.jwt_required()
    except MissingTokenError:
        return JSONResponse({"detail": "Invalid token"}, status_code=401)

    try:
        username = authorize.get_jwt_subject()
        user_model = get_user_model(username)

        return JSONResponse(
            BaseDetailAboutUserSchema(username=user_model.username).dict(),
            status_code=200
        )
    except InvalidHeaderError:
        return JSONResponse({"detail": "Invalid token"}, status_code=401)
