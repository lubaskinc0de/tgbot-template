"""Admin-side delete item handlers"""

from typing import Any

from aiogram import types

from aiogram_dialog import DialogManager, Window, Dialog
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Cancel
from aiogram_dialog.widgets.text import Const, Format

from dialog.dialog_state import DeleteItemSG
from dialog.data_getters import get_categories_data, get_category_items_data

from db.services.items import delete_item as delete_item_service

from sqlalchemy.exc import DBAPIError


async def delete_item(
    call: types.CallbackQuery, widget: Any, manager: DialogManager, item_id: str
):
    """Delete item"""

    try:
        await delete_item_service(
            manager.middleware_data.get("db_session"), int(item_id)
        )
        await call.answer("Товар успешно удален!")
    except DBAPIError:
        await call.answer("Произошла ошибка при удалении товара!")

    await manager.done()


select_item_to_delete_window = Window(
    Const("Выберите товар для удаления"),
    ScrollingGroup(
        Select(
            Format("{item.title}"),
            "selittodelsel",
            lambda item: item.id,
            "category_items",
            on_click=delete_item,
        ),
        width=2,
        height=4,
        id="selittodel",
    ),
    Cancel(Const("Отмена")),
    state=DeleteItemSG.list_of_category_items_to_delete,
    getter=get_category_items_data,
)


async def list_of_category_items_to_delete(
    call: types.CallbackQuery, widget: Any, manager: DialogManager, category_id: str
):
    """Get list of category items to delete"""

    manager.dialog_data["category_id"] = int(category_id)

    await manager.switch_to(DeleteItemSG.list_of_category_items_to_delete)


categories_window = Window(
    Const("Выберите категорию товаров"),
    ScrollingGroup(
        Select(
            Format("{item.title}"),
            "itemdelcatselsel",
            lambda category: category.id,
            "categories",
            on_click=list_of_category_items_to_delete,
        ),
        width=2,
        height=4,
        id="itemdelcatsel",
    ),
    Cancel(Const("Отмена")),
    state=DeleteItemSG.list_of_items_categories,
    getter=get_categories_data,
)

delete_item_dialog = Dialog(categories_window, select_item_to_delete_window)
