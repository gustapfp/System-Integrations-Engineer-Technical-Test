from typing import Literal, Optional, TypedDict
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from bson.objectid import ObjectId


class TracOSWorkorderSchema(BaseModel):
    id: ObjectId = Field(..., alias="_id")
    number: int
    status: Literal["pending", "in_progress", "completed", "on_hold", "cancelled"]
    title: str
    description: str
    createdAt: datetime
    updatedAt: datetime
    deleted: bool = False
    deletedAt: Optional[datetime] = None
    isSynced: bool = False
    syncedAt: Optional[datetime] = None 

    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        json_encoders = {ObjectId: str},
    )


