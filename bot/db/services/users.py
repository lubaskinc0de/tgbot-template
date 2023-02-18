"""Services (queries) for the User model"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, exists, func

from db.models import User, UserItem


async def is_user_exists(session: Session, user_id: int) -> bool:
    """Checks for the presence of a user with the passed id"""

    q = select(exists().where(User.id == user_id))
    res = await session.execute(q)
    return res.scalar()


async def create_user(session: Session, user_id: int) -> None:
    """Create the User instance"""

    user = User(id=user_id)
    session.add(user)
    await session.commit()


async def get_user(session: Session, user_id: int) -> User:
    """Get User instance"""

    q = select(User).where(User.id == user_id)
    res = await session.execute(q)

    return res.scalar()


async def get_user_items(session: Session, user_id: int) -> list[UserItem]:
    """Get user items"""

    q = (
        select(UserItem)
        .where(UserItem.user_id == user_id)
        .options(joinedload(UserItem.item))
    )
    res = await session.execute(q)

    return res.scalars().all()


async def get_user_items_count(session: Session, user_id: int) -> int:
    """Get user items count"""

    q = select(func.count(UserItem.item_id)).where(UserItem.user_id == user_id)
    res = await session.execute(q)

    return res.scalar()


async def get_user_item(session: Session, item_id: int, user_id: int) -> UserItem:
    """Get UserItem instance"""

    q = (
        select(UserItem)
        .where(UserItem.item_id == item_id)
        .where(UserItem.user_id == user_id)
    )
    res = await session.execute(q)

    return res.scalar()
