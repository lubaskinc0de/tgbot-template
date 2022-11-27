"""Admin-side edit item shop quantity handlers"""

from typing import Any

from aiogram import types

from aiogram_dialog import DialogManager, Window, Dialog
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Cancel
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput

from dialog.dialog_state import EditItemShopQuantity
from dialog.data_getters import get_categories_data, get_category_items_data

from db.services.items import (
    get_item_shops,
    get_item_shops_count,
    set_item_shop_quantity as set_item_shop_quantity_service,
)

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session


async def set_item_shop_quantity(
    message: types.Message, widget: Any, manager: DialogManager, input: str
):
    """Set shop_id"""

    manager.dialog_data["quantity"] = int(input)

    try:
        item_id = manager.dialog_data.get("item_id")
        shop_id = manager.dialog_data.get("shop_id")
        quantity = manager.dialog_data.get("quantity")

        db_session = manager.middleware_data.get("db_session")

        await set_item_shop_quantity_service(db_session, item_id, shop_id, quantity)
        await message.answer("Остатки успешно изменены!")

    except DBAPIError:
        await message.answer("Произошла ошибка!")

    finally:
        await manager.done()


set_item_shop_quantity_window = Window(
    Const("Введите новое кол-во товара"),
    TextInput("itemshopquantityinp", int, on_success=set_item_shop_quantity),
    Cancel(Const("Отмена")),
    state=EditItemShopQuantity.set_item_shop_quantity,
)


async def set_shop_id(
    call: types.CallbackQuery, widget: Any, manager: DialogManager, shop_id: str
):
    """Set shop_id"""

    manager.dialog_data["shop_id"] = int(shop_id)

    await manager.switch_to(EditItemShopQuantity.set_item_shop_quantity)


async def get_item_shops_data(
    db_session: Session, dialog_manager: DialogManager, **kwargs
):
    """Item shops data getter"""

    item_id: int = dialog_manager.dialog_data.get("item_id")

    item_shops = await get_item_shops(db_session, item_id, True)

    return {
        "item_shops": item_shops,
        "count": await get_item_shops_count(db_session, item_id, True),
    }


item_shops_window = Window(
    Const("Магазины в которых есть товар:"),
    ScrollingGroup(
        Select(
            Format("{item.shop.title} ({item.quantity} штук/и) {item.shop.address}"),
            "edititshquantshselsel",
            lambda item_shop: item_shop.shop_id,
            "item_shops",
            on_click=set_shop_id,
        ),
        width=2,
        height=4,
        id="edititshquantshsel",
    ),
    Cancel(Const("Отмена")),
    state=EditItemShopQuantity.list_of_item_shops,
    getter=get_item_shops_data,
)

item_shops_dialog = Dialog(item_shops_window)


async def list_of_item_shops(
    call: types.CallbackQuery, widget: Any, manager: DialogManager, item_id: str
):
    """Get list of item shops"""

    manager.dialog_data["item_id"] = int(item_id)

    await manager.switch_to(EditItemShopQuantity.list_of_item_shops)


select_item_window = Window(
    Const("Выберите товар которому хотите изменить остатки"),
    ScrollingGroup(
        Select(
            Format("{item.title}"),
            "edititshquantitselsel",
            lambda item: item.id,
            "category_items",
            list_of_item_shops,
        ),
        width=2,
        height=4,
        id="edititshquantitsel",
    ),
    Cancel(Const("Отмена")),
    state=EditItemShopQuantity.list_of_category_items,
    getter=get_category_items_data,
)


async def list_of_category_items(
    call: types.CallbackQuery, widget: Any, manager: DialogManager, category_id: str
):
    """Get list of category item"""

    manager.dialog_data["category_id"] = int(category_id)

    await manager.switch_to(EditItemShopQuantity.list_of_category_items)


categories_window = Window(
    Const("Выберите категорию товаров"),
    ScrollingGroup(
        Select(
            Format("{item.title}"),
            "edititshquantcatselsel",
            lambda category: category.id,
            "categories",
            on_click=list_of_category_items,
        ),
        width=2,
        height=4,
        id="edititshquantcatsel",
    ),
    Cancel(Const("Отмена")),
    state=EditItemShopQuantity.list_of_items_categories,
    getter=get_categories_data,
)

edit_item_shop_quantity_dialog = Dialog(
    categories_window,
    select_item_window,
    item_shops_window,
    set_item_shop_quantity_window,
)
