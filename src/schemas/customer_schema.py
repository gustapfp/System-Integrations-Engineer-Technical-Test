from typing import TypedDict
from datetime import datetime
from pydantic import BaseModel


class CustomerSystemWorkorderSchema(BaseModel):
    orderNo: int
    isActive: bool
    isCanceled: bool
    isDeleted: bool
    isDone: bool
    isOnHold: bool
    isPending: bool
    isSynced: bool
    summary: str
    creationDate: datetime
    lastUpdateDate: datetime
    deletedDate: datetime | None = None