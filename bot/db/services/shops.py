from sqlalchemy.orm import Session
from sqlalchemy import select, func, delete

from db.models import Shop

async def create_shop(session: Session, **kwargs: dict) -> None:
    '''Create the Shop instance, **kwargs are directly instance fields'''

    shop = Shop(**kwargs)
    session.add(shop)
    await session.commit()

async def get_shops(session: Session) -> list[Shop]:
    '''Select all shops'''

    q = select(Shop)
        
    res = await session.execute(q)

    return res.scalars().all()

async def get_shop(session: Session, shop_id: int) -> Shop:
    '''Get Shop instance'''

    q = select(Shop).where(Shop.id == shop_id)

    res = await session.execute(q)

    return res.scalar()

async def get_shops_count(session: Session) -> int:
    '''Get count of shops'''

    q = select(func.count(Shop.id))
            
    res = await session.execute(q)

    return res.scalar()

async def delete_shop(session: Session, shop_id: int) -> None:
    '''Delete shop by id'''

    q = delete(Shop).where(Shop.id == shop_id)
    await session.execute(q)

    await session.commit()