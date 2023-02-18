from sqlalchemy.orm import Session
from sqlalchemy import select, func, delete

from db.models import Shop

from schemas.admin import ShopModel


async def create_shop(
    session: Session,
    shop_obj: ShopModel,
) -> None:

    """Create the Shop instance"""

    shop = Shop(
        title=shop_obj.title,
        address=shop_obj.address,
        phone=shop_obj.phone,
        opening_in=shop_obj.opening_in,
        closing_in=shop_obj.closing_in,
    )
    session.add(shop)
    await session.commit()


async def get_shops(session: Session) -> list[Shop]:
    """Select all shops"""

    q = select(Shop)

    res = await session.execute(q)

    return res.scalars().all()


async def get_shop(session: Session, shop_id: int) -> Shop:
    """Get Shop instance"""

    q = select(Shop).where(Shop.id == shop_id)

    res = await session.execute(q)

    return res.scalar()


async def get_shops_count(session: Session) -> int:
    """Get count of shops"""

    q = select(func.count(Shop.id))

    res = await session.execute(q)

    return res.scalar()


async def delete_shop(session: Session, shop_id: int) -> None:
    """Delete shop by id"""

    q = delete(Shop).where(Shop.id == shop_id)
    await session.execute(q)

    await session.commit()
