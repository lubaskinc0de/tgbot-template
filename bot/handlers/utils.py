from aiogram import Bot


async def get_user_username(user_id: int, bot: Bot) -> str:
    """Get user username by user id"""

    return f"@{(await bot.get_chat(user_id)).username}"


async def get_admins(bot: Bot, admins: list[int]) -> list[str]:
    """Get admins username's"""

    admins: list[str] = [await get_user_username(admin, bot) for admin in admins]

    return admins
