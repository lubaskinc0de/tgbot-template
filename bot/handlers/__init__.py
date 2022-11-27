"""Package of bot handlers, in __init__.py the function of registering all handlers and dialogs is included"""

from . import admin
from . import client

from aiogram import Dispatcher

from aiogram_dialog import DialogRegistry


def register_handlers(dp: Dispatcher):
    client.register_handlers(dp)
    admin.register_handlers(dp)


def register_dialogs(registry: DialogRegistry):
    client.register_dialogs(registry)
    admin.register_dialogs(registry)
