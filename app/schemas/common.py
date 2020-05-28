from pydantic import BaseModel


class DeleteResp(BaseModel):
    deleted: bool
