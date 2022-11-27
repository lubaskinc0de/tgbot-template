from aiogram import Bot
from config_loader import Config


async def get_user_username(user_id: int, bot: Bot, config: Config) -> str:
    """Get user username by user id"""

    return f"@{(await bot.get_chat(user_id)).username}"


async def get_admins(bot: Bot, config: Config) -> list[str]:
    """Get admins username's"""

    admins: list[str] = [
        await get_user_username(admin, bot, config) for admin in config.bot.admins
    ]

    return admins
