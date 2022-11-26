'''Main file'''

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram_dialog import DialogRegistry

from config_loader import load_config, Config

from handlers import register_handlers, register_dialogs

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from db import Base

from middlewares import DBSessionMiddleware

API_TOKEN = load_config().bot.token

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('sqlalchemy.engine')
logger.setLevel(logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage(), events_isolation=SimpleEventIsolation())

async def get_async_sessionmaker() -> sessionmaker:
    '''Get sessionmaker instance'''

    config: Config = load_config()

    engine = create_async_engine(
        f'postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.db_name}',
        future=True
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_sessionmaker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    return async_sessionmaker

async def main():
    '''Main coroutine'''

    async_sessionmaker: sessionmaker = await get_async_sessionmaker()
    middleware = DBSessionMiddleware(async_sessionmaker)

    dp.message.outer_middleware(middleware)
    dp.callback_query.outer_middleware(middleware)
    dp.update.outer_middleware(middleware)

    register_handlers(dp)

    registry = DialogRegistry(dp)
    register_dialogs(registry)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())