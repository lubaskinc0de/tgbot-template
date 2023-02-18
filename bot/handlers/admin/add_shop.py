"""Admin-side add shop handlers"""

from typing import Any

from pydantic import ValidationError

from aiogram import types

from aiogram_dialog import Window, DialogManager, Dialog

from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel

from schemas.admin import ShopModel

from db.services.shops import create_shop as create_shop_service

from sqlalchemy.exc import DBAPIError

from dialog.dialog_state import CreateShopSG


async def set_shop_closing_in(
    message: types.Message, widget: Any, manager: DialogManager, input: str
):
    """Set shop closing_in and create them"""

    manager.dialog_data["closing_in"] = input

    try:
        shop = ShopModel(**manager.dialog_data)
        await create_shop_service(
            manager.middleware_data.get("db_session"),
            shop,
        )

        await message.answer("Магазин успешно добавлен!")
    except (ValidationError, DBAPIError):
        await message.answer("Произошла ошибка при добавлении магазина!")

    await manager.done()


set_shop_closing_in_window = Window(
    Const("Укажите когда магазин закрывается\nПример: 22:00"),
    TextInput("shopclosinginp", str, on_success=set_shop_closing_in),
    state=CreateShopSG.set_shop_closing_in,
)


async def set_shop_opening_in(
    message: types.Message, widget: Any, manager: DialogManager, input: str
):
    """Set shop opening_in"""

    manager.dialog_data["opening_in"] = input

    await manager.switch_to(CreateShopSG.set_shop_closing_in)


set_shop_opening_in_window = Window(
    Const("Укажите когда магазин открывается\nПример: 10:00"),
    TextInput("shopopeninginp", str, on_success=set_shop_opening_in),
    state=CreateShopSG.set_shop_opening_in,
)


async def set_shop_phone(
    message: types.Message, widget: Any, manager: DialogManager, input: str
):
    """Set shop phone"""

    manager.dialog_data["phone"] = input

    await manager.switch_to(CreateShopSG.set_shop_opening_in)


set_shop_phone_window = Window(
    Const(
        "Введите телефон для связи с магазином, не больше 12 символов.\nПример: +7333333333"
    ),
    TextInput("shopphoneinp", str, on_success=set_shop_phone),
    state=CreateShopSG.set_shop_phone,
)


async def set_shop_address(
    message: types.Message, widget: Any, manager: DialogManager, input: str
):
    """Set shop address"""

    manager.dialog_data["address"] = input

    await manager.switch_to(CreateShopSG.set_shop_phone)


set_shop_address_window = Window(
    Const("Введите адрес магазина, не более 50 символов."),
    TextInput("shopaddrinp", str, on_success=set_shop_address),
    state=CreateShopSG.set_shop_address,
)


async def set_shop_title(
    message: types.Message, widget: Any, manager: DialogManager, input: str
):
    """Set shop title"""

    manager.dialog_data["title"] = input

    await manager.switch_to(CreateShopSG.set_shop_address)


start_create_shop_window = Window(
    Const("Введите название магазина, не более 50 символов."),
    Cancel(Const("Отмена")),
    TextInput("shopnameinp", str, on_success=set_shop_title),
    state=CreateShopSG.start_create_shop,
)

create_shop_dialog = Dialog(
    start_create_shop_window,
    set_shop_address_window,
    set_shop_phone_window,
    set_shop_opening_in_window,
    set_shop_closing_in_window,
)
