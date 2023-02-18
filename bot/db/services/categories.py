"""Services (queries) for the Category model"""

from sqlalchemy.orm import Session
from sqlalchemy import select, func, delete

from db.models import Category
from schemas.admin import CategoryModel


async def get_categories(session: Session) -> list[Category]:
    """Select all categories"""

    q = select(Category)

    res = await session.execute(q)

    return res.scalars().all()


async def get_categories_count(session: Session) -> int:
    """Get count of categories"""

    q = select(func.count(Category.id))

    res = await session.execute(q)

    return res.scalar()


async def get_category(session: Session, category_id: int) -> Category:
    """Get Category instance"""

    q = select(Category).where(Category.id == category_id)
    res = await session.execute(q)

    return res.scalar()


async def create_category(session: Session, category_obj: CategoryModel) -> None:
    """Create the Category instance"""

    category = Category(title=category_obj.title)

    session.add(category)
    await session.commit()


async def delete_category(session: Session, category_id: int) -> None:
    """Delete category by id"""

    q = delete(Category).where(Category.id == category_id)
    await session.execute(q)

    await session.commit()
