from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status
)
from typing import List
from utils.dependencies import (
    UserHasResourcePermission
)
from schemas.customer import (
    CustomerBase,
    CustomersInResp,
    CustomerCreation,
    CustomerInResp,
    CustomerUpdate
)
from schemas.user import (
    UserInDB
)
from schemas.common import (
    DeleteResp
)
from crud.customer import (
    get_all_customers_in_db,
    get_all_customers_count_in_db,
    create_new_customer,
    find_customer_by_id,
    update_customer_record_in_db,
    delete_customer_by_id
)
from crud.user import (
    create_new_user,
    find_user_by_username
)
from permissions_system.constants import (
    PermissionTypesEnum
)
from models.Customer import(
    _customer_table_name
)
from uuid import UUID

router = APIRouter()

user_has_create_perms = UserHasResourcePermission(
    _customer_table_name, PermissionTypesEnum.create)
user_has_read_perms = UserHasResourcePermission(
    _customer_table_name, PermissionTypesEnum.read)
user_has_update_perms = UserHasResourcePermission(
    _customer_table_name, PermissionTypesEnum.update)
user_has_delete_perms = UserHasResourcePermission(
    _customer_table_name, PermissionTypesEnum.delete)


@router.get("/", response_model=CustomersInResp)
async def get_all_customers(
    offset: int = 0,
    limit: int = 10,
    has_perm=Depends(user_has_read_perms)
):
    """
    Returns the list of all customers, and
    total count of items for this resource in DB.
    """
    customers = await get_all_customers_in_db(
        offset,
        limit
    )
    count = await get_all_customers_count_in_db()
    return CustomersInResp(customers=customers, total_count=count)


@router.get("/{customer_id}", response_model=CustomerInResp)
async def get_customer_by_id(
    customer_id: UUID,
    has_perm=Depends(user_has_read_perms)
):
    """
    Returns a customer object for the specified ID.
    """
    customer = await find_customer_by_id(customer_id)
    return customer


@router.post("/", response_model=CustomerInResp)
async def create_customer_account(customer_in: CustomerCreation):
    """
    Create new customer.
    """
    user_name_exists = await find_user_by_username(customer_in.user_name)
    if user_name_exists:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail="User exists with that user_name."
        )
    user_in = UserInDB(**customer_in.dict(), group="customer")
    user_id = await create_new_user(user_in)
    customer = await create_new_customer(CustomerBase(
        **customer_in.dict(),
        customer_id=user_id,
        is_active=False
    ))
    return customer


@router.put("/{customer_id}", response_model=CustomerInResp)
async def update_customer_details(
    customer_id: UUID,
    update_customer: CustomerUpdate,
    has_perm=Depends(user_has_update_perms)
):
    """
    Update customer details for the specified customer ID.
    """

    customer_exists = await find_customer_by_id(customer_id)
    if not customer_exists:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            "Customer with specified ID does not exists.")

    update_data = update_customer.dict()
    update_data = {k: v for k, v in update_data.items()
                   if v is not None and k != "id"}
    updated_customer = await update_customer_record_in_db(
        customer_id, update_data)
    return updated_customer


@router.delete("/{customer_id}", response_model=DeleteResp)
async def delete_customer(
    customer_id: UUID,
    has_perm=Depends(user_has_delete_perms)
):
    """
    Delete customer record from DB by specified customer ID.
    """
    resp = {
        "deleted": None
    }
    customer_exists = await find_customer_by_id(customer_id)
    if not customer_exists:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            "Customer with specified ID does not exists.")

    deleted = await delete_customer_by_id(customer_id)
    resp.update(deleted=deleted)
    return resp
