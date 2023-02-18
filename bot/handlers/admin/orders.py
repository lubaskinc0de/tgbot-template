"""Admin-side orders handlers"""

import operator

from typing import Any

from aiogram import Bot, types

from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Cancel
from aiogram_dialog.widgets.text import Const, Format

from dialog.dialog_state import OrdersSG, OrderSG

from sqlalchemy.orm import Session

from db.services.orders import get_unpaid_orders, get_unpaid_orders_count

from config_loader import Config

from ..utils import get_user_username


async def get_order_details(
    call: types.CallbackQuery, widget: Any, manager: DialogManager, order_id: int
):
    """Get order details"""

    await manager.start(OrderSG.order_details, {"order_id": int(order_id)})


async def get_orders_data(db_session: Session, bot: Bot, config: Config, **kwargs):
    """Orders data getter"""

    orders = [
        (
            "Товар" if order.item_id else "Услуга",
            order.item.title if order.item_id else order.service.title,
            await get_user_username(order.user_id, bot),
            order.id,
            order.summ or "(договорная)",
            order.quantity,
        )
        for order in await get_unpaid_orders(db_session)
    ]

    return {
        "orders": orders,
        "count": await get_unpaid_orders_count(db_session),
    }


orders_window = Window(
    Const("Неоплаченные заказы:"),
    Cancel(Const("Назад")),
    ScrollingGroup(
        Select(
            Format(
                '{item[0]} "{item[1]}" x{item[5]}\nЗаказчик {item[2]} На сумму {item[4]} руб.'
            ),
            id="orderselsel",
            item_id_getter=operator.itemgetter(3),
            items="orders",
            on_click=get_order_details,
        ),
        width=2,
        height=4,
        id="ordersel",
    ),
    state=OrdersSG.list_of_orders,
    getter=get_orders_data,
)

orders_dialog = Dialog(orders_window)
