from aiogram import Dispatcher
from aiogram.filters import Command

from .client import start, start_dialog

from .categories import categories_dialog
from .items import category_items_dialog
from .item import item_dialog
from .item_shops import item_shops_dialog
from .item_order_create import create_item_order_dialog
from .service_order_create import create_service_order_dialog
from .user_items import user_items_dialog

from aiogram_dialog import DialogRegistry


def register_handlers(dp: Dispatcher):
    """Register all client-side handlers"""

    dp.message.register(start, Command(commands="start"))


def register_dialogs(registry: DialogRegistry):
    registry.register(start_dialog)

    registry.register(categories_dialog)
    registry.register(category_items_dialog)
    registry.register(item_dialog)
    registry.register(item_shops_dialog)
    registry.register(create_item_order_dialog)
    registry.register(create_service_order_dialog)
    registry.register(user_items_dialog)
