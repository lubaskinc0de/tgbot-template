import logging

from pydantic import (
    BaseModel,
    BaseSettings,
)


class Bot(BaseSettings):
    """Bot config"""

    token: str
    admins: list[int]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

        fields = {
            "token": {
                "env": "API_TOKEN",
            },
            "admins": {
                "env": "BOT_ADMINS",
            },
        }


class DB(BaseSettings):
    """Database config"""

    host: str
    db_name: str
    user: str
    password: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

        fields = {
            "host": {
                "env": "DB_HOST",
            },
            "db_name": {
                "env": "DB_NAME",
            },
            "user": {
                "env": "DB_USER",
            },
            "password": {
                "env": "DB_PASS",
            },
        }


class Config(BaseModel):
    """App config"""

    bot: Bot = Bot()
    db: DB = DB()


def load_config() -> Config:
    """Get app config"""

    return Config()
