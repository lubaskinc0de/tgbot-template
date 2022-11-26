from aiogram import Bot
from config_loader import Config, load_config

async def get_user_username(user_id: int, bot: Bot) -> str:
    '''Get user username by user id'''

    return f'@{(await bot.get_chat(user_id)).username}'

async def get_admins(bot: Bot) -> list[str]:
    '''Get admins username's'''

    config: Config = load_config()
    admins = [f'@{(await bot.get_chat(admin)).username}' for admin in config.bot.admins]

    return admins
