"""Admin-side message filter"""

from aiogram.filters import Filter
from aiogram import types

from config_loader import Config


class IsAdminFilter(Filter):
    """A filter that checks that the user is an admin (listed in the list of admins)"""

    async def __call__(
        self, message: types.Message | types.CallbackQuery, config: Config
    ) -> bool:
        return message.from_user.id in config.bot.admins
