from typing import List
from uuid import uuid4, UUID
from application import database, ps
from schemas.customer import (
    CustomerInResp,
    CustomerBase,
    CustomerUpdate
)
from models.Customer import (
    Customer
)
from crud.user import (
    delete_user_in_db
)
from sqlalchemy import select


async def get_all_customers_in_db(
        offset: int = 0, limit: int = 10) -> List[CustomerInResp]:
    query = select([Customer, ps.User]).select_from(
        Customer.join(ps.User)
    ).offset(offset).limit(limit)
    customers = await database.fetch_all(query)
    return customers


async def get_all_customers_count_in_db() -> int:
    query = Customer.count()
    count = await database.execute(query)
    return count


async def find_customer_by_id(_id: UUID) -> CustomerInResp:
    query = select([Customer, ps.User]).select_from(
        Customer.join(ps.User)
    ).where(
        Customer.columns.customer_id == _id
    )
    customer = await database.fetch_one(query)
    return customer


async def create_new_customer(obj_in: CustomerBase) -> UUID:
    query = Customer.insert()
    values = obj_in.dict()
    await database.execute(query=query, values=values)
    customer = await find_customer_by_id(obj_in.customer_id)
    return customer


async def update_customer_record_in_db(
        _id: UUID,
        values: dict) -> CustomerInResp:
    query = Customer.update().where(
        Customer.columns.customer_id == _id
    )
    await database.execute(query, values)
    customer = await find_customer_by_id(_id)
    return customer


async def delete_customer_by_id(_id: UUID) -> bool:
    exists = await delete_user_in_db(_id)
    return exists
