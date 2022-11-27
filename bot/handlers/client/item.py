"""Item detail client-side handlers"""

from typing import Any
from aiogram import types

from aiogram_dialog import Window, Dialog, DialogManager

from aiogram_dialog.widgets.kbd import Cancel, Button
from aiogram_dialog.widgets.text import Const, Format

from dialog.dialog_state import ItemSG, ItemShopsSG, CreateItemOrderSG

from db.services.items import get_item

from sqlalchemy.orm import Session


async def item_shops(call: types.CallbackQuery, widget: Any, manager: DialogManager):
    """Item shops"""

    await manager.start(
        ItemShopsSG.item_shops, {"item_id": manager.start_data.get("item_id")}
    )


async def item_order_create(
    call: types.CallbackQuery, widget: Any, manager: DialogManager
):
    """Item order create"""

    await manager.start(
        CreateItemOrderSG.create_item_order,
        {"item_id": manager.start_data.get("item_id")},
    )


async def item_photos(call: types.CallbackQuery, widget: Any, manager: DialogManager):
    """Item order create"""

    item_id: int = manager.start_data.get("item_id")
    db_session: Session = manager.middleware_data.get("db_session")

    item = await get_item(db_session, item_id)
    item_photos: list[types.InputMediaPhoto] = [
        types.InputMediaPhoto(media=photo.file_id) for photo in item.photos
    ]

    await call.message.answer_media_group(item_photos)


async def get_item_data(db_session: Session, dialog_manager: DialogManager, **kwargs):
    """Get item window data getter"""

    item_id: int = dialog_manager.start_data.get("item_id")

    item = await get_item(db_session, item_id)

    return {"item": item}


item_window = Window(
    Const("Информация о товаре:\n"),
    Format("Артикул: {item.id}"),
    Format("Название: {item.title}"),
    Format("Категория {item.category.title}"),
    Const("Описание:"),
    Format("{item.description}\n"),
    Format("Цена: {item.price} руб."),
    Button(Const("Где есть товар?"), id="item_shops", on_click=item_shops),
    Button(Const("Купить"), id="item_order_create", on_click=item_order_create),
    Button(Const("Фото товара"), id="item_photos", on_click=item_photos),
    Cancel(Const("Назад")),
    state=ItemSG.item_detail,
    getter=get_item_data,
)

item_dialog = Dialog(item_window)
