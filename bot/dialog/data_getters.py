"""Aiogram dialog getters that are used more than once"""

from typing import Optional
from aiogram_dialog import DialogManager

from db.services.categories import get_categories, get_categories_count
from db.services.service_categories import (
    get_service_categories,
    get_service_categories_count,
)
from db.services.shops import get_shops, get_shops_count
from db.services.items import (
    get_item_shops,
    get_item_shops_count,
    get_items_by_category,
    get_items_by_category_count,
)

from sqlalchemy.orm import Session


async def get_categories_data(db_session: Session, **kwargs):
    """Categories data getter"""

    categories = await get_categories(db_session)

    return {
        "categories": categories,
        "count": await get_categories_count(db_session),
    }


async def get_service_categories_data(db_session: Session, **kwargs):
    """Service categories data getter"""

    service_categories = await get_service_categories(db_session)

    return {
        "service_categories": service_categories,
        "count": await get_service_categories_count(db_session),
    }


async def get_shops_data(db_session: Session, **kwargs):
    """Shops data getter"""

    shops = await get_shops(db_session)

    return {
        "shops": shops,
        "count": await get_shops_count(db_session),
    }


async def get_item_shops_data(
    db_session: Session, dialog_manager: DialogManager, **kwargs
):
    """Item shops data getter"""

    item_id: Optional[int] = dialog_manager.dialog_data.get("item_id")

    if not item_id:
        item_id: int = dialog_manager.start_data.get("item_id")

    item_shops = await get_item_shops(db_session, item_id)

    return {
        "item_shops": item_shops,
        "count": await get_item_shops_count(db_session, item_id),
    }


async def get_category_items_data(
    db_session: Session, dialog_manager: DialogManager, **kwargs
):
    """Category items data getter"""

    category_id: Optional[int] = dialog_manager.dialog_data.get("category_id")

    if not category_id:
        category_id: int = dialog_manager.start_data.get("category_id")

    category_items = await get_items_by_category(db_session, category_id)

    return {
        "category_items": category_items,
        "count": await get_items_by_category_count(db_session, category_id),
    }
