"""Admin-side delete category handlers"""


from typing import Any

from aiogram import types

from aiogram_dialog import DialogManager, Window, Dialog
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Cancel
from aiogram_dialog.widgets.text import Const, Format

from dialog.dialog_state import DeleteCategorySG
from dialog.data_getters import get_categories_data

from db.services.categories import delete_category as delete_category_service

from sqlalchemy.exc import DBAPIError


async def delete_category(
    call: types.CallbackQuery, widget: Any, manager: DialogManager, category_id: str
):
    """Delete category"""

    try:
        await delete_category_service(
            manager.middleware_data.get("db_session"), int(category_id)
        )
        await call.answer("Категория успешно удалена!")
    except DBAPIError:
        await call.answer("Произошла ошибка при удалении категории!")

    await manager.done()


select_category_to_delete_window = Window(
    Const("Выберите категорию для удаления"),
    Cancel(Const("Отмена")),
    ScrollingGroup(
        Select(
            Format("{item.title}"),
            "selcattodelsel",
            lambda category: category.id,
            "categories",
            on_click=delete_category,
        ),
        width=2,
        height=4,
        id="selcattodel",  # select category to delete
    ),
    state=DeleteCategorySG.list_of_categories_to_delete,
    getter=get_categories_data,
)

delete_category_dialog = Dialog(select_category_to_delete_window)
