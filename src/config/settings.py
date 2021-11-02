from os import environ


DEBUG = environ.get("DEBUG", default=True)

# MySQL configuration
DATABASE_NAME = environ.get("DATABASE_NAME", default="testtask1")
DATABASE_USERNAME = environ.get("DATABASE_USERNAME", default="root")
DATABASE_PASSWORD = environ.get("DATABASE_PASSWORD", default="root123passwd")
DATABASE_HOST = environ.get("DATABASE_HOST", default="127.0.0.1")
DATABASE_PORT = environ.get("DATABASE_PORT", default=3306)

# Celery configuration
CELERY_APP_NAME = "celderei"
CELERY_BROKER = environ.get("CELERY_BROKER", default="redis://127.0.0.1:6379")
CELERY_BACKEND = environ.get("CELERY_BACKEND", default="redis://127.0.0.1:6379")

CELERY_INCLUDES = ["src.celery_.tasks", ]

# JWT configuration
JWT_SECRET_KEY = "secret"
