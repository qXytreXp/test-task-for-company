from peewee import Model, CharField
from src.db import mysql_db


class BaseModel(Model):
    class Meta:
        database = mysql_db


class User(BaseModel):
    username = CharField()
    hashed_password = CharField(max_length=555)
