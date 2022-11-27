"""User items client-side handlers"""

from typing import Any

from aiogram import types

from aiogram_dialog import DialogManager, Window, Dialog

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Cancel
from aiogram_dialog.widgets.text import Const, Format

from dialog.dialog_state import UserItemsSG

from db.services.users import get_user_items, get_user_items_count

from sqlalchemy.orm import Session


async def get_user_items_data(
    db_session: Session, dialog_manager: DialogManager, **kwargs
):
    """User items data getter"""

    user_id: int = dialog_manager.start_data.get("user_id")

    user_items = await get_user_items(db_session, user_id)

    return {
        "user_items": user_items,
        "count": await get_user_items_count(db_session, user_id),
    }


user_items_window = Window(
    Const("Купленные товары"),
    ScrollingGroup(
        Select(
            Format("{item.item.title} ({item.quantity} штук/и)"),
            "useritemsselsel",
            lambda user_item: user_item.item_id,
            "user_items",
        ),
        width=2,
        height=4,
        id="useritemssel",
    ),
    Cancel(Const("Назад")),
    state=UserItemsSG.user_items,
    getter=get_user_items_data,
)

user_items_dialog = Dialog(user_items_window)


async def user_items(
    message: types.Message, widget: Any, dialog_manager: DialogManager
):
    """
    Get user items
    """

    user_id = message.from_user.id

    await dialog_manager.start(UserItemsSG.user_items, {"user_id": user_id})
