from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List


class PermissionBase(BaseModel):
    group: str
    resource: str
    create: bool
    read: bool
    update: bool
    delete: bool


class PermissionInResp(PermissionBase):
    id: UUID


class PermissionUpdate(BaseModel):
    create: Optional[bool]
    read: Optional[bool]
    update: Optional[bool]
    delete: Optional[bool]


class PermissionsInResp(BaseModel):
    permissions: List[PermissionInResp]
    total_count: int
