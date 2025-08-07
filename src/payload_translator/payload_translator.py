from schemas.customer_schema import CustomerSystemWorkorderSchema
from schemas.tracos_schema import TracOSWorkorderSchema
from bson import ObjectId
import logging
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class PayloadTranslator: 
    """Class to translate payloads between different formats."""
    def from_costumer_to_tracos(
        self, payload: CustomerSystemWorkorderSchema
    ) -> dict:
        """Translate a customer system workorder to Tracos format."""
        try: 
            logger.info(f"Translating customer system workorder to Tracos format.")
            tracos_status = self.get_tracos_status(payload = payload)
            return TracOSWorkorderSchema(
                _id=ObjectId(),
                number=payload.orderNo,
                status=tracos_status,
                title=f"Workorder {payload.orderNo}",
                description=payload.summary,
                 
                createdAt=payload.creationDate.astimezone().isoformat().replace('+00:00', 'Z'),
                updatedAt=payload.lastUpdateDate.astimezone().isoformat().replace('+00:00', 'Z'),
                deleted=True if payload.isDeleted else False,
                deletedAt=payload.deletedDate.astimezone().isoformat().replace('+00:00', 'Z') if payload.deletedDate else None,
                isSynced=payload.isSynced
            )
        except ValidationError as e:
            logger.error(f"The workorder you're trying to insert is not valid: {e}")
            return None
        else:
            logger.error(f"Error inserting workorder: {e}")
            return None

    def from_tracos_to_costumer(
        self, payload: TracOSWorkorderSchema
    )  -> CustomerSystemWorkorderSchema:
        """Translate a Tracos workorder to customer system format."""
        return CustomerSystemWorkorderSchema(
            orderNo=payload.number,
            isActive=True,
            isCanceled=payload.status == "cancelled",
            isDeleted=payload.deleted,
            isDone=payload.status == "completed",
            isOnHold=payload.status == "on_hold",
            isPending=payload.status == "pending",
            isSynced=True,
            summary=payload.description,
            creationDate=payload.createdAt,
            lastUpdateDate = payload.updatedAt
        )


    @staticmethod
    def get_tracos_status(
        payload: CustomerSystemWorkorderSchema
    ) -> str:
        """Get the Tracos status based on the customer system workorder."""
        if payload.isCanceled:
            return "cancelled"
        elif payload.isDeleted:
            return "deleted"
        elif payload.isDone:
            return "completed"
        elif payload.isOnHold:
            return "on_hold"
        elif payload.isPending:
            return "pending"
        else:
            return "in_progress"

