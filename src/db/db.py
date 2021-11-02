from peewee import MySQLDatabase
from src.config.settings import (
    DATABASE_NAME, 
    DATABASE_USERNAME, 
    DATABASE_PASSWORD, 
    DATABASE_HOST, 
    DATABASE_PORT
)


mysql_db = MySQLDatabase(
    DATABASE_NAME, 
    user=DATABASE_USERNAME,
    password=DATABASE_PASSWORD, 
    host=DATABASE_HOST, 
    port=DATABASE_PORT
)
