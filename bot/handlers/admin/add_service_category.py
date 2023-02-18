"""Admin-side add service category handlers"""

from typing import Any

from pydantic import ValidationError

from aiogram import types

from aiogram_dialog import Window, DialogManager, Dialog

from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import TextInput

from schemas.admin import ServiceCategoryModel

from db.services.service_categories import (
    create_service_category as create_service_category_service,
)

from sqlalchemy.exc import DBAPIError

from dialog.dialog_state import CreateServiceCategorySG


async def create_service_category_success(
    message: types.Message, widget: Any, manager: DialogManager, input: str
):
    """Create service category success"""

    try:
        service_category = ServiceCategoryModel(title=input)
        await create_service_category_service(
            manager.middleware_data.get("db_session"), service_category
        )

        await message.answer("Категория услуг успешно добавлена!")
    except (ValidationError, DBAPIError):
        await message.answer("Произошла ошибка при добавлении категории услуг!")

    await manager.done()


start_create_service_category_window = Window(
    Const("Введите название категории услуг"),
    TextInput("servicecatnameinp", str, on_success=create_service_category_success),
    Cancel(Const("Отмена")),
    state=CreateServiceCategorySG.start_create_service_category,
)

create_service_category_dialog = Dialog(start_create_service_category_window)
