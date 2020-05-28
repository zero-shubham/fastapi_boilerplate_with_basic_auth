from schemas.user import (
    UserBase,
    UserInDB
)
from pydantic import BaseModel
from uuid import (
    UUID
)
from typing import List, Optional


class CustomerBase(BaseModel):
    customer_id: UUID
    email: str
    phone: str
    name: str
    is_active: bool


class CustomerInResp(CustomerBase):
    user_name: str
    group: str


class CustomersInResp(BaseModel):
    customers: List[CustomerInResp]
    total_count: int


class CustomerCreation(BaseModel):
    user_name: str
    password: str
    email: str
    phone: str
    name: str


class CustomerUpdate(BaseModel):
    email: Optional[str]
    phone: Optional[str]
    name: Optional[str]
