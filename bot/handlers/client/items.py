"""Items client-side handlers"""

from typing import Any

from aiogram import types

from aiogram_dialog import Window, Dialog, DialogManager

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Cancel
from aiogram_dialog.widgets.text import Const, Format

from dialog.dialog_state import ItemsSG, ItemSG
from dialog.data_getters import get_category_items_data


async def item_detail(
    call: types.CallbackQuery, widget: Any, manager: DialogManager, item_id: str
):
    """Item detail"""

    await manager.start(ItemSG.item_detail, {"item_id": int(item_id)})


category_items_window = Window(
    Const("Выберите нужный товар"),
    ScrollingGroup(
        Select(
            Format("{item.title}"),
            "itselsel",
            lambda item: item.id,
            "category_items",
            on_click=item_detail,
        ),
        width=2,
        height=4,
        id="itsel",  # item select
    ),
    Cancel(Const("Назад")),
    state=ItemsSG.list_of_category_items,
    getter=get_category_items_data,
)

category_items_dialog = Dialog(category_items_window)
