"""Service order create client-side handlers"""

from typing import Any

from pydantic import ValidationError

from aiogram import types, Bot

from aiogram_dialog import DialogManager, Window, Dialog

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Cancel
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format

from dialog.dialog_state import CreateServiceOrderSG
from dialog.data_getters import get_service_categories_data

from db.services.services import create_service
from db.services.orders import create_order

from schemas.client import ServiceModel, OrderModel

from sqlalchemy.exc import DBAPIError

from config_loader import Config

from ..utils import get_admins


async def get_order_data(
    dialog_manager: DialogManager, bot: Bot, config: Config, **kwargs
):
    """service_order_created_window data getter"""

    order_id: int = dialog_manager.dialog_data.get("order_id")

    admins = await get_admins(bot, config.bot.admins)

    return {"order_id": order_id, "admins": "\n".join(admins)}


service_order_created_window = Window(
    Format("Номер вашего заказа: {order_id}"),
    Format("Для уточнения деталей обратитесь к {admins}"),
    Cancel(Const("Назад")),
    state=CreateServiceOrderSG.service_order_created,
    getter=get_order_data,
)


async def set_service_description(
    message: types.Message, widget: Any, manager: DialogManager, input: str
):
    """Set service description and create them"""

    manager.dialog_data["description"] = input

    db_session = manager.middleware_data.get("db_session")

    try:
        service = ServiceModel(**manager.dialog_data)
        service_id = (
            await create_service(
                db_session,
                service,
            )
        ).id

        user_id: int = message.from_user.id

        order = OrderModel(
            service_id=service_id, user_id=user_id, **manager.dialog_data
        )

        order = await create_order(
            manager.middleware_data.get("db_session"), order
        )

        await message.answer("Заказ успешно создан!")

        manager.dialog_data["order_id"] = order.id

        await manager.switch_to(CreateServiceOrderSG.service_order_created)
    except (DBAPIError, ValidationError):
        await message.answer("Что то пошло не так..")
        await manager.done()


set_service_description_window = Window(
    Const("Полностью и в деталях опишите вашу задачу."),
    Cancel(Const("Отмена")),
    TextInput("servicedescinp", str, on_success=set_service_description),
    state=CreateServiceOrderSG.set_service_description,
)


async def set_service_title(
    message: types.Message, widget: Any, manager: DialogManager, input: str
):
    """Set service title"""

    manager.dialog_data["title"] = input

    await manager.switch_to(CreateServiceOrderSG.set_service_description)


set_service_title_window = Window(
    Const("Кратко опишите что вам нужно, не более 50 символов."),
    Cancel(Const("Отмена")),
    TextInput("servicetitleinp", str, on_success=set_service_title),
    state=CreateServiceOrderSG.set_service_title,
)


async def set_service_category(
    call: types.CallbackQuery, widget: Any, manager: DialogManager, category_id: str
):
    """Set service category"""

    manager.dialog_data["category_id"] = int(category_id)

    await manager.switch_to(CreateServiceOrderSG.set_service_title)


set_service_category_window = Window(
    Const("Выберите нужную категорию услуг"),
    ScrollingGroup(
        Select(
            Format("{item.title}"),
            "servicecatselsel",
            lambda category: category.id,
            "service_categories",
            on_click=set_service_category,
        ),
        width=2,
        height=4,
        id="servicecatsel",
    ),
    Cancel(Const("Отмена")),
    state=CreateServiceOrderSG.set_service_category,
    getter=get_service_categories_data,
)

create_service_order_dialog = Dialog(
    set_service_category_window,
    set_service_title_window,
    set_service_description_window,
    service_order_created_window,
)
