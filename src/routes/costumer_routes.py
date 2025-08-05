import os
import json
import logging
from typing import List
import asyncio
from src.schemas.customer_schema import CustomerSystemWorkorderSchema  # Changed this line
from src.CONSTS import PROJECT_ROOT
from pydantic import ValidationError
logger = logging.getLogger(__name__)


class CostumerERPRoute:
    def __init__(self):
        self.client_get_url =  "./" + "data/inbound"
        self.client_post_url = str(PROJECT_ROOT) + "/" + "data/outbound"
        self.IOHelper = IOHelper()

    async def get_costumer_workorder_by_order_number(
        self, orderNo: int
    ) -> CustomerSystemWorkorderSchema:
        """Fetch a workorder from the customer system."""
        full_path = os.path.join(self.client_get_url, f"{orderNo}.json")
        json_file = await self.IOHelper.read_json(full_path)
       
        if json_file is None:
            logger.error(f"Workorder with orderNo {orderNo} not found.")
            return None
        return json_file.model_dump()

    async def get_costumer_workorders() -> List[CustomerSystemWorkorderSchema]:
        """Fetch all workorders from the customer system."""
        pass


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
    async def write_json(
        file_path: str, data: List[CustomerSystemWorkorderSchema]
    ) -> None:
        """Write JSON data to a file."""
        pass


if __name__ == "__main__":
    route = CostumerERPRoute()
    asyncio.run(route.get_costumer_workorder_by_order_number(orderNo=2))
