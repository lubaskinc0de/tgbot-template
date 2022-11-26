from dataclasses import dataclass, field

import environ

env = environ.Env(
    BOT_ADMINS=(list, [])
)

environ.Env.read_env()

@dataclass
class Bot:
    '''Bot config'''

    token: str
    admins: list[int] = field(default_factory=list) # admins id's

@dataclass
class DB:
    '''Database config'''

    host: str
    db_name: str
    user: str
    password: str

@dataclass
class Config:
    '''App config'''

    bot: Bot
    db: DB

def load_config() -> Config:
    '''Get app config'''
    
    return Config(
        bot=Bot(token=env('API_TOKEN'), admins=list(map(int, env('BOT_ADMINS')))),
        db=DB(
            host=env('DB_HOST'),
            db_name=env('DB_NAME'),
            user=env('DB_USER'),
            password=env('DB_PASS')
        )
    )
