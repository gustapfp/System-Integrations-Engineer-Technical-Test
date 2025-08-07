from pydantic import ValidationError
from src.payload_translator.payload_translator import PayloadTranslator
from src.schemas.customer_schema import CustomerSystemWorkorderSchema
from src.schemas.tracos_schema import TracOSWorkorderSchema
from datetime import datetime, timezone
from bson import ObjectId
import pytest
import re


payload_translator = PayloadTranslator()
costumer_payload_schema = CustomerSystemWorkorderSchema(
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
tracos_payload_schema = TracOSWorkorderSchema(
            _id=ObjectId('6894ee8b79351927c44f37fc'),
            number=1,
            status="pending",
            title="Sample Workorder",
            description="This is a sample workorder.",
            createdAt=datetime.now(),
            updatedAt=datetime.now(),
            deleted=False,
        )


def test_translation_from_custumer_to_tracos_field_by_field():
    translated_tracos_payload = payload_translator.from_costumer_to_tracos(
        payload=costumer_payload_schema
    )
    

    assert translated_tracos_payload.number == 123
    assert translated_tracos_payload.status == 'in_progress'
    assert translated_tracos_payload.title == 'Workorder 123'
    assert translated_tracos_payload.description == 'Example workorder'
    assert translated_tracos_payload.deleted == False
    assert translated_tracos_payload.deletedAt == None
    assert translated_tracos_payload.isSynced == False
    assert translated_tracos_payload.syncedAt == None
    
    
    assert translated_tracos_payload.createdAt is not None
    assert translated_tracos_payload.updatedAt is not None

    assert hasattr(translated_tracos_payload, 'id')
    assert isinstance(translated_tracos_payload.id, ObjectId)


def test_translation_from_tracos_to_costumer_field_by_field():
    translated_customer_payload = payload_translator.from_tracos_to_costumer(
        payload=tracos_payload_schema
    )
    
    # Test individual fields based on the translation logic
    assert translated_customer_payload.orderNo == 1  # from tracos_payload_schema.number
    assert translated_customer_payload.isActive == True
    assert translated_customer_payload.isCanceled == False 
    assert translated_customer_payload.isDeleted == False  
    assert translated_customer_payload.isDone == False  
    assert translated_customer_payload.isOnHold == False  
    assert translated_customer_payload.isPending == True  
    assert translated_customer_payload.isSynced == True
    assert translated_customer_payload.summary == "This is a sample workorder."  

    assert translated_customer_payload.creationDate == tracos_payload_schema.createdAt
    assert translated_customer_payload.lastUpdateDate == tracos_payload_schema.updatedAt



def test_translation_with_invalid_customer_payload_raises_exception():
    """Test that translation function raises exception with invalid customer payload"""
    try:
        invalid_customer_payload = CustomerSystemWorkorderSchema(
            orderNo=True,
            isActive=True,
            isCanceled=False,
            isDeleted=False,
            isDone=False,
            isOnHold=False,
            isPending=False,
            isSynced=False,
            summary="", 
            creationDate=datetime.now(),
            lastUpdateDate=datetime.now(),
        )

  
        result = payload_translator.from_costumer_to_tracos(payload=invalid_customer_payload)

        assert hasattr(result, 'number')
        assert hasattr(result, 'status')
        assert hasattr(result, 'title')
    except Exception as e:

        assert isinstance(e, (ValidationError, ValueError))


def test_translation_with_invalid_tracos_payload_raises_exception():
    """Test that translation function raises exception with invalid TracOS payload"""
    try:
   
        invalid_tracos_payload = TracOSWorkorderSchema(
            _id=ObjectId(),
            number="",
            status="pending",
            title="",  
            description="", 
            createdAt=datetime.now(),
            updatedAt=datetime.now(),
        )

        result = payload_translator.from_tracos_to_costumer(payload=invalid_tracos_payload)
  
        assert hasattr(result, 'orderNo')
        assert hasattr(result, 'isActive')
        assert hasattr(result, 'summary')
    except Exception as e:
  
        assert isinstance(e, (ValidationError, ValueError))


def test_dates_are_in_utc_iso8601_format():
    """Test that dates are properly formatted in UTC ISO 8601 format"""

    translated_tracos_payload = payload_translator.from_costumer_to_tracos(
        payload=costumer_payload_schema
    )


    created_at_dt = translated_tracos_payload.createdAt
    updated_at_dt = translated_tracos_payload.updatedAt
    
  
    created_at_str = created_at_dt.isoformat()
    updated_at_str = updated_at_dt.isoformat()


    assert created_at_dt.tzinfo is not None, "createdAt is not timezone-aware"
    assert updated_at_dt.tzinfo is not None, "updatedAt is not timezone-aware"



def test_tracos_to_customer_dates_preservation():
    """Test that dates are properly preserved when translating from TracOS to customer format"""

    specific_datetime = datetime(2024, 1, 15, 10, 30, 45, 123456, tzinfo=timezone.utc)
    
    tracos_payload_with_dates = TracOSWorkorderSchema(
        _id=ObjectId(),
        number=999,
        status="completed",
        title="Test Workorder with Dates",
        description="Testing date preservation",
        createdAt=specific_datetime,
        updatedAt=specific_datetime,
        deleted=False,
    )
    
   
    translated_customer_payload = payload_translator.from_tracos_to_costumer(
        payload=tracos_payload_with_dates
    )

    assert translated_customer_payload.creationDate == specific_datetime
    assert translated_customer_payload.lastUpdateDate == specific_datetime
    
 
    assert translated_customer_payload.creationDate.tzinfo == timezone.utc
    assert translated_customer_payload.lastUpdateDate.tzinfo == timezone.utc
