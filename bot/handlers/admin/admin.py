"""Admin-side main handlers"""

from aiogram import types

from aiogram_dialog import Window, Dialog, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Group, Row, Start
from aiogram_dialog.widgets.text import Const

from dialog.dialog_state import (
    AdminSG,
    DeleteCategorySG,
    DeleteItemSG,
    DeleteShopSG,
    CreateCategorySG,
    CreateShopSG,
    CreateItemSG,
    OrdersSG,
    DeleteServiceCategorySG,
    CreateServiceCategorySG,
    EditItemShopQuantity,
)

from sqlalchemy.orm import Session

admin_window = Window(
    Const("Привет админ! Вот опции которые тебе доступны:"),
    Group(
        Row(
            Start(
                Const("Удалить категорию"),
                id="deletecategory",
                state=DeleteCategorySG.list_of_categories_to_delete,
            ),
            Start(
                Const("Удалить товар"),
                id="deleteitem",
                state=DeleteItemSG.list_of_items_categories,
            ),
        ),
        Row(
            Start(
                Const("Удалить магазин"),
                id="deleteshop",
                state=DeleteShopSG.list_of_shops_to_delete,
            ),
            Start(
                Const("Удалить категорию услуг"),
                id="deleteservicecategory",
                state=DeleteServiceCategorySG.list_of_service_categories_to_delete,
            ),
        ),
        Row(
            Start(
                Const("Добавить категорию"),
                id="addcategory",
                state=CreateCategorySG.start_create_category,
            ),
            Start(
                Const("Добавить магазин"),
                id="addshop",
                state=CreateShopSG.start_create_shop,
            ),
        ),
        Row(
            Start(
                Const("Добавить товар"),
                id="additem",
                state=CreateItemSG.start_create_item,
            ),
            Start(
                Const("Добавить категорию услуг"),
                id="addservicecategory",
                state=CreateServiceCategorySG.start_create_service_category,
            ),
        ),
        Row(
            Start(Const("Заказы"), id="orders", state=OrdersSG.list_of_orders),
            Start(
                Const("Изменить остатки товара"),
                id="edititemshopquantity",
                state=EditItemShopQuantity.list_of_items_categories,
            ),
        ),
    ),
    state=AdminSG.admin,
)


async def admin(
    message: types.Message, dialog_manager: DialogManager, db_session: Session
):
    """
    This handler will be called when user sends `/admin` command

    Admin main menu.
    """

    await dialog_manager.start(AdminSG.admin, mode=StartMode.RESET_STACK)


admin_dialog = Dialog(admin_window)
