from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str


class BaseDetailAboutUserSchema(BaseModel):
    username: str


class SettingsSchema(BaseModel):
    authjwt_secret_key: str = "secret"
