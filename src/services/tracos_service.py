from datetime import timezone, datetime
from types import CoroutineType
from typing import Any
from schemas.tracos_schema import TracOSWorkorderSchema
from motor.motor_asyncio import AsyncIOMotorClient
import logging
import os
from bson.objectid import ObjectId
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class TracOsService:
    """Service to handle operations related to TracOs."""
    def __init__(self):
        self.client = AsyncIOMotorClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
        self.db = self.client[os.getenv("MONGO_DATABASE", "tractian")]
        self.collection = self.db[os.getenv("MONGO_COLLECTION", "workorders")]
    
    async def get_workorder_by_number(self, number: int) -> TracOSWorkorderSchema | None:
        """Get workorder from the TracOs database."""
        workorder = await self.collection.find_one({"number":number})
        logger.info(f"Workorder number {number} found in the TracOs database.")
        return TracOSWorkorderSchema(**workorder)
    
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

    async def update_workorder(self, number: int) -> None:
        """Insert workorder fields isSynced and  syncedAt in the TracOs database."""
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
            
        
        






