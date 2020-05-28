from pydantic import BaseModel
from uuid import UUID
from typing import List


class ResourceInDB(BaseModel):
    id: UUID
    resource_table: str
    resource_name: str


class ResourcesInResp(BaseModel):
    resources: List[ResourceInDB]
    total_count: int
