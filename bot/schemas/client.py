from typing import TypeVar

from pydantic import BaseModel, Field, root_validator

T = TypeVar("T", bound=dict)


class ServiceModel(BaseModel):
    """Service schema"""

    title: str = Field(max_length=50)
    description: str
    category_id: int


class OrderModel(BaseModel):
    """Order schema"""

    item_id: int = None
    service_id: int = None
    shop_id: int = None
    user_id: int
    summ: int = None
    quantity: int = 1

    @root_validator
    def check_item_id_or_order_id(cls, values: T) -> T:
        """Check that item_id and service_id are not both empty"""

        item_id, service_id = values.get("item_id"), values.get("service_id")

        if not (item_id or service_id):
            raise ValueError("Вы должны указать либо id товара либо id услуги.")

        return values

    @root_validator
    def check_not_item_id_and_service_id_together(cls, values: T) -> T:
        """Check that not item_id and service_id together"""

        item_id, service_id = values.get("item_id"), values.get("service_id")

        if item_id and service_id:
            raise ValueError(
                "Вы должны указать либо id товара либо id услуги, но не все вместе."
            )

        return values

    @root_validator
    def check_not_item_and_not_shop(cls, values: T) -> T:
        """Check not (item_id and not shop_id)"""

        item_id, shop_id = values.get("item_id"), values.get("shop_id")

        if item_id and (not shop_id):
            raise ValueError("Если вы указали id товара то укажите и id магазина.")

        return values
