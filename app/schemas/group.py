from pydantic import BaseModel
from uuid import UUID
from typing import List


class GroupBase(BaseModel):
    id: UUID
    group: str


class GroupsInResp(BaseModel):
    groups: List[GroupBase]
    total_count: int
