"""Services (queries) for the ServiceCategory model"""

from sqlalchemy.orm import Session
from sqlalchemy import select, func, delete

from db.models import ServiceCategory

from schemas.admin import ServiceCategoryModel


async def get_service_categories(session: Session) -> list[ServiceCategory]:
    """Select all service categories"""

    q = select(ServiceCategory)

    res = await session.execute(q)

    return res.scalars().all()


async def get_service_categories_count(session: Session) -> int:
    """Get count of service categories"""

    q = select(func.count(ServiceCategory.id))

    res = await session.execute(q)

    return res.scalar()


async def get_service_category(
    session: Session, service_category_id: int
) -> ServiceCategory:
    """Get ServiceCategory instance"""

    q = select(ServiceCategory).where(ServiceCategory.id == service_category_id)
    res = await session.execute(q)

    return res.scalar()


async def create_service_category(
    session: Session, service_category_obj: ServiceCategoryModel
) -> None:
    """Create the ServiceCategory instance"""

    service_category = ServiceCategory(title=service_category_obj.title)

    session.add(service_category)
    await session.commit()


async def delete_service_category(session: Session, service_category_id: int) -> None:
    """Delete service category by id"""

    q = delete(ServiceCategory).where(ServiceCategory.id == service_category_id)
    await session.execute(q)

    await session.commit()
