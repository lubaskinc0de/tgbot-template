'''Services (queries) for the Order model'''

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func

from db.models import Order, UserItem

from db.services.items import get_item, get_item_shop
from db.services.users import get_user
from db.services.shops import get_shop
from db.services.services import get_service

async def get_unpaid_orders(session: Session) -> list[Order]:
    '''Get unpaid orders'''

    q = select(Order).where(Order.paid == False).options(joinedload(Order.item), joinedload(Order.service))
    res = await session.execute(q)

    return res.scalars().all()

async def get_order(session: Session, order_id: int, joined: bool = True) -> Order:
    '''Get order instance'''

    q = select(Order).where(Order.id == order_id)

    if joined:
        q = q.options(joinedload(Order.item), joinedload(Order.service))

    res = await session.execute(q)

    return res.scalar()

async def get_unpaid_orders_count(session: Session) -> list[Order]:
    '''Get unpaid orders count'''

    q = select(func.count(Order.id)).where(Order.paid == False)
    res = await session.execute(q)

    return res.scalar()

async def create_order(
    session: Session, user_id: int, shop_id: int = None, summ: float = None,
    quantity: int = None, item_id: int = None, service_id: int = None,
    ) -> Order:
    '''Create the Order instance'''

    order = Order()

    if item_id:
        item = await get_item(session, item_id)
        order.item = item
    
    if shop_id:
        shop = await get_shop(session, shop_id)
        order.shop = shop
    
    if quantity:
        order.quantity = quantity
    
    if service_id:
        service = await get_service(session, service_id)
        order.service = service
    
    user = await get_user(session, user_id)
    
    order.user = user
    order.summ = summ

    session.add(order)
    await session.commit()

    return order

async def pay_order(session: Session, order_id: int) -> None:
    '''Make order paid'''

    order = await get_order(session, order_id, joined=False)

    if order.item_id:
        user_item = UserItem(user_id=order.user_id, item_id=order.item_id, quantity=order.quantity)
        await session.merge(user_item)
        
        item_shop = await get_item_shop(session, order.item_id, order.shop_id)
        item_shop.quantity = item_shop.quantity - order.quantity

    order.paid = True

    await session.commit()
