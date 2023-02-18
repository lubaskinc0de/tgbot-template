"""Admin-side add category handlers"""

from typing import Any

from pydantic import ValidationError

from aiogram import types

from aiogram_dialog import Window, DialogManager, Dialog

from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import TextInput

from schemas.admin import CategoryModel

from db.services.categories import create_category as create_category_service

from sqlalchemy.exc import DBAPIError

from dialog.dialog_state import CreateCategorySG


async def create_category_success(
    message: types.Message, widget: Any, manager: DialogManager, input: str
):
    """Create category success"""

    try:
        category = CategoryModel(title=input)
        await create_category_service(
            manager.middleware_data.get("db_session"),
            category,
        )

        await message.answer("Категория успешно добавлена!")
    except (ValidationError, DBAPIError):
        await message.answer("Произошла ошибка при добавлении категории!")

    await manager.done()


start_create_category_window = Window(
    Const("Введите название категории"),
    TextInput("catnameinp", str, on_success=create_category_success),
    Cancel(Const("Отмена")),
    state=CreateCategorySG.start_create_category,
)

create_category_dialog = Dialog(start_create_category_window)
