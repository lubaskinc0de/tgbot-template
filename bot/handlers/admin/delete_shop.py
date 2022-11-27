"""Admin-side delete shop handlers"""

from typing import Any

from aiogram import types

from aiogram_dialog import DialogManager, Window, Dialog
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Cancel
from aiogram_dialog.widgets.text import Const, Format

from dialog.dialog_state import DeleteShopSG
from dialog.data_getters import get_shops_data

from db.services.shops import delete_shop as delete_shop_service

from sqlalchemy.exc import DBAPIError


async def delete_shop(
    call: types.CallbackQuery, widget: Any, manager: DialogManager, shop_id: str
):
    """Delete shop"""

    try:
        await delete_shop_service(
            manager.middleware_data.get("db_session"), int(shop_id)
        )
        await call.answer("Магазин успешно удален!")
    except DBAPIError:
        await call.answer("Произошла ошибка при удалении магазина!")

    await manager.done()


select_shop_to_delete_window = Window(
    Const("Выберите магазин для удаления"),
    Cancel(Const("Отмена")),
    ScrollingGroup(
        Select(
            Format("{item.title}"),
            "selshoptodelsel",
            lambda shop: shop.id,
            "shops",
            on_click=delete_shop,
        ),
        width=2,
        height=4,
        id="selshoptodel",
    ),
    state=DeleteShopSG.list_of_shops_to_delete,
    getter=get_shops_data,
)


delete_shop_dialog = Dialog(select_shop_to_delete_window)
