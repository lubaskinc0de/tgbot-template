"""Main file"""

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

from middlewares import DBSessionMiddleware, ConfigMiddleware


async def get_async_sessionmaker(config: Config) -> sessionmaker:
    """Get sessionmaker instance"""

    engine = create_async_engine(
        f"postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.db_name}",
        future=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_sessionmaker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    return async_sessionmaker


def register_middleware(dp: Dispatcher, middleware) -> None:
    """Register middleware in 'message', 'callback' and 'update' layers of dp"""

    dp.message.outer_middleware(middleware)
    dp.callback_query.outer_middleware(middleware)
    dp.update.outer_middleware(middleware)


async def main():
    """Main coroutine"""

    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger("sqlalchemy.engine")
    logger.setLevel(logging.INFO)

    config = load_config()

    async_sessionmaker: sessionmaker = await get_async_sessionmaker(config)

    db_middleware = DBSessionMiddleware(async_sessionmaker)
    config_middleware = ConfigMiddleware(config)

    token = config.bot.token
    bot = Bot(token=token)
    dp = Dispatcher(storage=MemoryStorage(), events_isolation=SimpleEventIsolation())
    registry = DialogRegistry(dp)

    register_middleware(dp, db_middleware)
    register_middleware(dp, config_middleware)
    register_handlers(dp)
    register_dialogs(registry)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
