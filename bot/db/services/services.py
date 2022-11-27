"""Services (queries) for the Service model"""

from sqlalchemy.orm import Session
from sqlalchemy import select

from db.models import Service
from db.services.service_categories import get_service_category


async def create_service(
    session: Session, category_id: int, title: str, description: str
) -> Service:
    """Create the ServiceCategory instance, **kwargs are directly instance fields without category_id"""

    service = Service(title=title, description=description)

    category = await get_service_category(session, category_id)
    service.category = category

    session.add(service)

    await session.commit()

    return service


async def get_service(session: Session, service_id: int) -> Service:
    """Get Service instance"""

    q = select(Service).where(Service.id == service_id)
    res = await session.execute(q)

    return res.scalar()
