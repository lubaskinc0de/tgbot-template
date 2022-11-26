from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from sqlalchemy.orm import sessionmaker

class DBSessionMiddleware(BaseMiddleware):
    '''Middleware that pass the database session to the handler'''

    def __init__(self, sessionmaker: sessionmaker) -> None:
        self.sessionmaker = sessionmaker

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        async with self.sessionmaker() as session:
            data['db_session'] = session

            result = await handler(event, data)
            return result