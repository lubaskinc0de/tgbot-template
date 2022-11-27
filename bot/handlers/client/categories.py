"""Categories client-side handlers"""

from typing import Any

from aiogram import types

from aiogram_dialog import DialogManager, Window, Dialog

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Cancel
from aiogram_dialog.widgets.text import Const, Format

from dialog.dialog_state import CategoriesSG, ItemsSG
from dialog.data_getters import get_categories_data


async def list_of_category_items(
    call: types.CallbackQuery, widget: Any, manager: DialogManager, category_id: str
):
    """Get list of category items"""

    await manager.start(
        ItemsSG.list_of_category_items, {"category_id": int(category_id)}
    )


categories_window = Window(
    Const("Выберите нужную категорию"),
    ScrollingGroup(
        Select(
            Format("{item.title}"),
            "catselsel",
            lambda category: category.id,
            "categories",
            on_click=list_of_category_items,
        ),
        width=2,
        height=4,
        id="catsel",  # category select
    ),
    Cancel(Const("Назад")),
    state=CategoriesSG.list_of_categories,
    getter=get_categories_data,
)

categories_dialog = Dialog(categories_window)
