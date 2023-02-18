"""Create item order client-side handlers"""

from pydantic import ValidationError

from typing import Any
from aiogram import types, Bot

from aiogram_dialog import Window, Dialog, DialogManager

from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput

from dialog.dialog_state import CreateItemOrderSG
from dialog.data_getters import get_item_shops_data

from db.services.items import get_item, get_item_shop
from db.services.orders import create_order

from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError

from schemas.client import OrderModel

from config_loader import Config

from ..utils import get_admins


async def get_order_data(
    dialog_manager: DialogManager, bot: Bot, config: Config, **kwargs
):
    """item_order_created_window data getter"""

    order_id: int = dialog_manager.dialog_data.get("order_id")
    order_summ: float = dialog_manager.dialog_data.get("order_summ")

    admins = await get_admins(bot, config)

    return {"order_id": order_id, "order_summ": order_summ, "admins": "\n".join(admins)}


item_order_created_window = Window(
    Format("Номер вашего заказа: {order_id}"),
    Format("К оплате: {order_summ} руб."),
    Format("Для оплаты обратитесь к {admins}"),
    Cancel(Const("Назад")),
    state=CreateItemOrderSG.item_order_created,
    getter=get_order_data,
)


async def set_order_quantity(
    message: types.Message, widget: Any, manager: DialogManager, quantity: str
):
    """Set order quantity and create them"""

    quantity = int(quantity)
    manager.dialog_data["quantity"] = quantity

    item_id: int = manager.start_data.get("item_id")
    shop_id: int = manager.dialog_data.get("shop_id")
    db_session = manager.middleware_data.get("db_session")

    item_in_shop_quantity = (await get_item_shop(db_session, item_id, shop_id)).quantity

    if quantity > item_in_shop_quantity:
        await message.answer(
            "Вы ввели кол-во больше чем есть в магазине. Повторите попытку."
        )
        return
    try:
        item_id: int = manager.start_data.get("item_id")
        item = await get_item(db_session, item_id, False)
        order_summ = item.price * quantity

        user_id: int = message.from_user.id

        order = OrderModel(
            item_id=item_id, user_id=user_id, summ=order_summ, **manager.dialog_data
        )

        order = await create_order(
            manager.middleware_data.get("db_session"),
            order,
        )

        await message.answer("Заказ успешно создан!")

        manager.dialog_data["order_id"] = order.id
        manager.dialog_data["order_summ"] = order_summ

        await manager.switch_to(CreateItemOrderSG.item_order_created)

    except (DBAPIError, ValidationError):
        message.answer("Что-то пошло не так..")
        await manager.done()


set_order_quantity_window = Window(
    Const("Введите желаемое кол-во товара"),
    TextInput("orderquantityinp", int, on_success=set_order_quantity),
    Cancel(Const("Отмена")),
    state=CreateItemOrderSG.set_order_quantity,
)


async def set_order_shop(
    call: types.CallbackQuery, widget: Any, manager: DialogManager, shop_id: str
):
    """Set order shop"""

    manager.dialog_data["shop_id"] = int(shop_id)

    await manager.switch_to(CreateItemOrderSG.set_order_quantity)


set_order_shop_window = Window(
    Const("Выберите из какого магазина и в каком кол-ве хотите купить товар"),
    ScrollingGroup(
        Select(
            Format("{item.shop.title} ({item.quantity} штук/и) {item.shop.address}"),
            "ordershopselsel",
            lambda item_shop: item_shop.shop_id,
            "item_shops",
            on_click=set_order_shop,
        ),
        width=2,
        height=4,
        id="ordershopsel",
    ),
    Cancel(Const("Отмена")),
    state=CreateItemOrderSG.set_order_shop,
    getter=get_item_shops_data,
)


async def get_item_data(db_session: Session, dialog_manager: DialogManager, **kwargs):
    """Get item window data getter"""

    item_id: int = dialog_manager.start_data.get("item_id")

    item = await get_item(db_session, item_id, False)

    return {"item": item}


create_item_order_window = Window(
    Const("Вы выбрали товар\n"),
    Format("Артикул {item.id}"),
    Format("Название {item.title}"),
    SwitchTo(
        Const("Продолжить?"),
        id="set_order_shop_quantity",
        state=CreateItemOrderSG.set_order_shop,
    ),
    Cancel(Const("Отмена")),
    state=CreateItemOrderSG.create_item_order,
    getter=get_item_data,
)

create_item_order_dialog = Dialog(
    create_item_order_window,
    set_order_shop_window,
    set_order_quantity_window,
    item_order_created_window,
)
