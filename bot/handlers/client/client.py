"""Main client-side handlers"""

from aiogram import types

from db.services.users import is_user_exists, create_user

from aiogram_dialog import Window, Dialog, DialogManager, StartMode

from aiogram_dialog.widgets.kbd import Start, Row, Button
from aiogram_dialog.widgets.text import Const, Format

from dialog.dialog_state import ClientSG, CategoriesSG, CreateServiceOrderSG

from .user_items import user_items

from sqlalchemy.orm import Session

start_window = Window(
    Format(
        "Здравствуйте, {event.from_user.username}.\nЯ - бот консультант по продаже товаров.\nВыберите нужную опцию"
    ),
    Row(
        Start(Const("Товары"), id="items", state=CategoriesSG.list_of_categories),
        Start(
            Const("Заказать услугу"),
            id="service_order",
            state=CreateServiceOrderSG.set_service_category,
        ),
    ),
    Button(Const("Купленные товары"), id="user_items", on_click=user_items),
    state=ClientSG.start,
)


async def start(
    message: types.Message, dialog_manager: DialogManager, db_session: Session
):
    """
    This handler will be called when user sends `/start` command
    Main menu.
    """

    user_id = message.from_user.id

    is_user_register = await is_user_exists(db_session, user_id)

    if not is_user_register:
        await create_user(db_session, user_id=user_id)

    await dialog_manager.start(ClientSG.start, mode=StartMode.RESET_STACK)


start_dialog = Dialog(start_window)
