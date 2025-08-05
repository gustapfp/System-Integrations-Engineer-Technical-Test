from typing import Literal
from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId

class TracOSWorkorderSchema(BaseModel):
    _id: ObjectId
    number: int
    status: Literal["pending", "in_progress", "completed", "on_hold", "cancelled"]
    title: str
    description: str
    createdAt: datetime
    updatedAt: datetime
    deleted: bool
    deletedAt: datetime | None = None


