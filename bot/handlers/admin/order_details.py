"""Admin-side order details handlers"""

from typing import Any

from aiogram import Bot, types

from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Cancel, Button
from aiogram_dialog.widgets.text import Const, Format

from dialog.dialog_state import OrderSG

from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError

from db.services.orders import get_order, pay_order as pay_order_service

from config_loader import Config

from ..utils import get_user_username


async def pay_order(call: types.CallbackQuery, widget: Any, manager: DialogManager):
    """Pay order"""

    try:
        db_session: Session = manager.middleware_data.get("db_session")
        order_id: int = manager.start_data.get("order_id")

        await pay_order_service(db_session, order_id)

        await call.answer("Заказ успешно оплачен!")
    except DBAPIError:
        await call.answer("Произошла ошибка!")
    finally:
        await manager.done()


async def get_order_data(
    db_session: Session,
    dialog_manager: DialogManager,
    bot: Bot,
    config: Config,
    **kwargs,
):
    """Order details window data getter"""

    order_id: int = dialog_manager.start_data.get("order_id")

    order = await get_order(db_session, order_id)
    order_customer = await get_user_username(order.user_id, bot)
    order_type = "Товар" if order.item_id else "Услуга"
    order_price = f"{order.item.price} руб." if order.item_id else "Договорная"
    order_service_description = order.service.description if order.service_id else None

    return {
        "order": order,
        "order_customer": order_customer,
        "order_type": order_type,
        "order_title": order.item.title if order.item_id else order.service.title,
        "order_price": order_price,
        "order_service_description": order_service_description,
    }


order_details_window = Window(
    Format("Информация о заказе\n"),
    Format("Идентификатор: {order.id}"),
    Format("Заказчик: {order_customer}"),
    Format("Тип: {order_type}"),
    Format('Название: "{order_title}"'),
    Format(
        "Описание услуги:\n{order_service_description}",
        when="order_service_description",
    ),
    Format("Кол-во товаров в заказе: {order.quantity}"),
    Format("На сумму: {order_price}"),
    Button(Const("Заказ оплачен ✅"), id="order_paid", on_click=pay_order),
    Cancel(Const("Назад")),
    state=OrderSG.order_details,
    getter=get_order_data,
)

order_details_dialog = Dialog(order_details_window)
