"""Services (queries) for the Item model"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func, delete

from db.models import Item, ItemShop, ItemPhoto
from db.services.categories import get_category

from schemas.admin import ItemModel


async def create_item(
    session: Session,
    item_obj: ItemModel,
) -> None:
    """
    Create the Item instance, shops are list of (shop_id, quantity), photos are list of (file_id)
    """

    category = await get_category(session, item_obj.category_id)

    item = Item(
        title=item_obj.title,
        description=item_obj.description,
        price=item_obj.price,
    )

    item.category = category

    item_shop_objects = []
    item_photo_objects = []

    for shop_id, quantity in item_obj.shops:
        obj = ItemShop(quantity=quantity)
        obj.shop_id = shop_id

        item_shop_objects.append(obj)

    for photo_id in item_obj.photos:
        obj = ItemPhoto(file_id=photo_id)
        item_photo_objects.append(obj)

    item.shops.extend(item_shop_objects)
    item.photos.extend(item_photo_objects)

    session.add(item)

    await session.commit()


async def get_items_by_category(session: Session, category_id: int) -> list[Item]:
    """Select items by category_id"""

    q = select(Item).where(Item.category_id == category_id)

    res = await session.execute(q)

    return res.scalars().all()


async def get_items_by_category_count(session: Session, category_id: int) -> int:
    """Select COUNT items by category_id"""

    q = select(func.count(Item.id)).where(Item.category_id == category_id)

    res = await session.execute(q)

    return res.scalar()


async def get_items(session: Session) -> list[Item]:
    """Select all items"""

    q = select(Item)

    res = await session.execute(q)

    return res.scalars().all()


async def get_item(session: Session, item_id: int, joined: bool = True) -> Item:
    """Get Item instance"""

    q = select(Item).where(Item.id == item_id)

    if joined:
        q = q.options(joinedload(Item.category), joinedload(Item.photos))

    res = await session.execute(q)

    return res.scalar()


async def get_item_shops(
    session: Session, item_id: int, show_empty: bool = False
) -> list[ItemShop]:
    """
    Get item shops
    """

    q = (
        select(ItemShop)
        .where(ItemShop.item_id == item_id)
        .options(joinedload(ItemShop.shop))
    )

    if not show_empty:
        q = q.where(ItemShop.quantity > 0)

    res = await session.execute(q)

    return res.scalars().all()


async def get_item_shops_count(
    session: Session, item_id: int, show_empty: bool = False
) -> list[ItemShop]:
    """
    Get item shops count
    """

    q = select(func.count(ItemShop.item_id)).where(ItemShop.item_id == item_id)

    if not show_empty:
        q = q.where(ItemShop.quantity > 0)

    res = await session.execute(q)

    return res.scalar()


async def get_item_shop(session: Session, item_id: int, shop_id: int) -> ItemShop:
    """Get ItemShop instance"""

    q = (
        select(ItemShop)
        .where(ItemShop.shop_id == shop_id)
        .where(ItemShop.item_id == item_id)
    )
    res = await session.execute(q)

    return res.scalar()


async def get_items_count(session: Session) -> int:
    """Select COUNT items"""

    q = select(func.count(Item.id))

    res = await session.execute(q)

    return res.scalar()


async def delete_item(session: Session, item_id: int) -> None:
    """Delete item by id"""

    q = delete(Item).where(Item.id == item_id)
    await session.execute(q)

    await session.commit()


async def set_item_shop_quantity(
    session: Session, item_id: int, shop_id: int, quantity: int
) -> None:
    """Set ItemShop quantity"""

    item_shop = await get_item_shop(session, item_id, shop_id)

    item_shop.quantity = quantity

    await session.commit()
