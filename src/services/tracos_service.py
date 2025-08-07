from datetime import timezone, datetime
from types import CoroutineType
from typing import Any
from schemas.tracos_schema import TracOSWorkorderSchema
from motor.motor_asyncio import AsyncIOMotorClient
import logging
import os
from bson.objectid import ObjectId
from pydantic import ValidationError
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "tractian")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "workorders")

logger = logging.getLogger(__name__)

# TODO: Add one method update the workorder to isSynced = true and set a  timestamp
# TODO: Add a method to insert many workorders
# TODO: Add a method to get all workorderstimestamp
class TracOsService:
    """Service to handle operations related to TracOs."""
    def __init__(self):
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[MONGO_DATABASE]
        self.collection = self.db[MONGO_COLLECTION]
    
    async def get_workorder(self, number: int) -> TracOSWorkorderSchema | None:
        """Get workorder from the TracOs database."""
        workorder = await self.collection.find_one({"number":number})
        logger.info(f"Workorder number {number} found in the TracOs database.")
        return workorder
    
    async def insert_workorder(self, workorder: TracOSWorkorderSchema) -> TracOSWorkorderSchema | None:
        """Insert workorder in the TracOs database."""
        try: 
            inserted_document = await self.collection.insert_one(workorder.model_dump())
            logger.info(f"Workorder number {workorder.number} inserted with id {inserted_document.inserted_id}")
            print(f"Workorder number {workorder.number} inserted successfully.")
            return workorder
        except ValidationError as e:
            logger.error(f"The workorder you're trying to insert is not valid: {e}")
            return None
        except Exception as e:
            logger.error(f"Error inserting workorder: {e}")
            return None
        else:
            logger.error(f"Error inserting workorder: {e}")
            return None
    # TODO: Improve typing here
    async def update_workorder(self, number: int) -> None:
        try:
            logger.info(f"Updating workorder number: {number}...")
            await self.collection.update_one(
                filter={
                    "number" : number
                },
                update={
                    "$set": {
                        "isSynced": True,
                        "syncedAt": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
                    }
                }          
            )
            logger.info("Workorder number {number} updated successfully.")
            
          
        except Exception as e:
            logger.error(f"Error updating workorder: {e}")
            return None
            
        
        
if __name__ == "__main__":
    from datetime import datetime
    from bson import ObjectId
    import asyncio
    tracos_service = TracOsService()
    sample_workorder = TracOSWorkorderSchema(
        _id=ObjectId(),
        number=1,
        status="pending",
        title="Sample Workorder",
        description="This is a sample workorder.",
        createdAt=datetime.now(),
        updatedAt=datetime.now(),
        deleted=False,
        isSynced=False
    )
    # asyncio.run(tracos_service.insert_workorder(sample_workorder))
    asyncio.run(tracos_service.update_workorder(
        1
    ))






