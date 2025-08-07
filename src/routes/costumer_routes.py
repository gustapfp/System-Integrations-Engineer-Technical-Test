from datetime import datetime
import os
import json
import logging
from typing import List, Union
import asyncio
from schemas.customer_schema import CustomerSystemWorkorderSchema # Changed this line

from pydantic import ValidationError
from services.tracos_service import TracOsService
logger = logging.getLogger(__name__)

 
class CostumerERPRoute:
    def __init__(self):
        self.client_get_url = str(os.getenv("DATA_INBOUND_DIR", "data/inbound"))
        self.client_post_url =  str(os.getenv("DATA_OUTBOUND_DIR", "data/outbound"))
        self.IOHelper = IOHelper()
        self.tracos_service = TracOsService()

    async def get_costumer_workorder_by_order_number(
        self, orderNo: int
    ) -> CustomerSystemWorkorderSchema:
        """Fetch a workorder from the customer system."""
        logger.info(f"Getting the workorder {orderNo} from Client's ERP.")
        full_path = os.path.join(self.client_get_url, f"{orderNo}.json")
        json_file = await self.IOHelper.read_json(full_path)
        if json_file is None:
            logger.error(f"Workorder with orderNo {orderNo} not found.")
            return None
        return json_file.model_dump()

    async def post_costumer_workorder(
        self, workorder: CustomerSystemWorkorderSchema
    ) -> dict: 
        if workorder is None:
            logger.error(f"Workorder not found.")
            return None

        try:
            full_path = os.path.join(self.client_post_url, f"{workorder.orderNo}.json")
            logger.info("Inserting json file in Client's ERP...")
            await self.IOHelper.write_json(
                file_path=full_path,
                data=workorder
            )
            await self.tracos_service.update_workorder(
                number=workorder.orderNo
            )
            return workorder.model_dump(mode="json")
        except Exception as e:
            logger.error(f"Error inserting json file: {str(e)}")
            return None



class IOHelper:
    @staticmethod
    async def read_json(file_path: str) -> CustomerSystemWorkorderSchema:
        """Read JSON data from a file."""
        try:
            with open(file_path, "r") as json_file:
                logger.info(f"Reading file: {file_path}")
                data = json.load(json_file)
                return CustomerSystemWorkorderSchema(
                    orderNo=data.get("orderNo", 0),
                    isActive=data.get("isActive", True),
                    isCanceled=data.get("isCanceled", False),
                    isDeleted=data.get("isDeleted", False),
                    isDone=data.get("isDone", False),
                    isOnHold=data.get("isOnHold", False),
                    isPending=data.get("isPending", False),
                    isSynced=False,
                    summary=data.get("summary", ""),
                    creationDate=data.get("creationDate", ""),
                    lastUpdateDate=data.get("lastUpdateDate", ""),
                    deletedDate=None if "deletedDate" not in data else data.get("deletedDate", None)
                )
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_path}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error reading {file_path}: {str(e)}")
            return None
        except ValidationError as e:
            logger.error(f"Validation error in {file_path}: {str(e)}")
    
    @staticmethod
    def convert_to_payload_json(
        data: Union[CustomerSystemWorkorderSchema, List[CustomerSystemWorkorderSchema]]
    ) -> Union[dict, list]:
        if isinstance(data, list):
            return [item.model_dump(mode="json") for item in data]
        return data.model_dump(mode="json")
    
    async def write_json(self, 
        file_path: str, data: List[CustomerSystemWorkorderSchema] | CustomerSystemWorkorderSchema
    ) -> bool:
        """Write JSON data to a file."""
        payload = self.convert_to_payload_json(data)
        try:
            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump(payload, json_file, ensure_ascii=False, indent=4)
                logging.info("Workorder inserted in Client's ERP")
                return True
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_path}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error reading {file_path}: {str(e)}")
            return None
        except ValidationError as e:
            logger.error(f"Validation error in {file_path}: {str(e)}")


if __name__ == "__main__":
    route = CostumerERPRoute()
    # asyncio.run(route.get_costumer_workorder_by_order_number(orderNo=2))
    asyncio.run(
        route.post_costumer_workorder(
            workorder=CustomerSystemWorkorderSchema(
                orderNo=123,
                isActive=True,
                isCanceled=False,
                isDeleted=False,
                isDone=False,
                isOnHold=False,
                isPending=False,
                isSynced=False,
                summary="Example workorder",
                creationDate=datetime.now(),
                lastUpdateDate=datetime.now(),
            
            )
        )
    )
