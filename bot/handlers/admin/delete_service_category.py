"""Admin-side delete service category handlers"""

from typing import Any

from aiogram import types

from aiogram_dialog import DialogManager, Window, Dialog
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Cancel
from aiogram_dialog.widgets.text import Const, Format

from dialog.dialog_state import DeleteServiceCategorySG
from dialog.data_getters import get_service_categories_data

from db.services.service_categories import (
    delete_service_category as delete_service_category_service,
)

from sqlalchemy.exc import DBAPIError


async def delete_service_category(
    call: types.CallbackQuery,
    widget: Any,
    manager: DialogManager,
    service_category_id: str,
):
    """Delete service category"""

    try:
        await delete_service_category_service(
            manager.middleware_data.get("db_session"), int(service_category_id)
        )
        await call.answer("Категория услуг успешно удалена!")
    except DBAPIError:
        await call.answer("Произошла ошибка при удалении категории услуг!")

    await manager.done()


select_service_category_to_delete_window = Window(
    Const("Выберите категорию услуг для удаления"),
    Cancel(Const("Отмена")),
    ScrollingGroup(
        Select(
            Format("{item.title}"),
            "selservicecattodelsel",
            lambda category: category.id,
            "service_categories",
            on_click=delete_service_category,
        ),
        width=2,
        height=4,
        id="selservicecattodel",
    ),
    state=DeleteServiceCategorySG.list_of_service_categories_to_delete,
    getter=get_service_categories_data,
)

delete_service_category_dialog = Dialog(select_service_category_to_delete_window)
