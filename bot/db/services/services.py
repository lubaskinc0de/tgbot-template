"""Services (queries) for the Service model"""

from sqlalchemy.orm import Session
from sqlalchemy import select

from db.models import Service
from db.services.service_categories import get_service_category

from schemas.client import ServiceModel


async def create_service(session: Session, service_obj: ServiceModel) -> Service:
    """Create the ServiceCategory instance"""

    service = Service(title=service_obj.title, description=service_obj.description)

    category = await get_service_category(session, service_obj.category_id)
    service.category = category

    session.add(service)

    await session.commit()

    return service


async def get_service(session: Session, service_id: int) -> Service:
    """Get Service instance"""

    q = select(Service).where(Service.id == service_id)
    res = await session.execute(q)

    return res.scalar()
