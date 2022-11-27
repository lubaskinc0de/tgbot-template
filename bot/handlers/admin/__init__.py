from aiogram import Dispatcher
from aiogram.filters import Command

from .admin import admin_dialog, admin

from .delete_category import delete_category_dialog
from .delete_service_category import delete_service_category_dialog
from .delete_item import delete_item_dialog
from .delete_shop import delete_shop_dialog

from .add_category import create_category_dialog
from .add_shop import create_shop_dialog
from .add_item import create_item_dialog
from .add_service_category import create_service_category_dialog

from .edit_item_shop_quantity import edit_item_shop_quantity_dialog

from .orders import orders_dialog
from .order_details import order_details_dialog

from aiogram_dialog import DialogRegistry

from filters.admin import IsAdminFilter


def register_handlers(dp: Dispatcher):
    """Register all admin-side handlers"""

    dp.message.register(admin, Command(commands="admin"), IsAdminFilter())


def register_dialogs(registry: DialogRegistry):
    registry.register(admin_dialog)

    registry.register(delete_category_dialog)
    registry.register(delete_service_category_dialog)
    registry.register(delete_item_dialog)
    registry.register(delete_shop_dialog)

    registry.register(create_category_dialog)
    registry.register(create_service_category_dialog)
    registry.register(create_shop_dialog)
    registry.register(create_item_dialog)

    registry.register(orders_dialog)
    registry.register(order_details_dialog)

    registry.register(edit_item_shop_quantity_dialog)
