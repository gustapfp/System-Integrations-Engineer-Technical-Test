import pytest
from datetime import datetime, timezone
from bson import ObjectId
from src.services.tracos_service import TracOsService
from src.schemas.tracos_schema import TracOSWorkorderSchema

@pytest.fixture
async def tracos_service():
    service = TracOsService()
    yield service
    # Cleanup: Drop the collection after tests
    await service.collection.drop()

@pytest.fixture
def sample_workorder():
    return TracOSWorkorderSchema(
        _id=ObjectId(),
        number=12345,
        status="pending",
        title="Test Workorder",
        description="This is a test workorder",
        createdAt=datetime.now(timezone.utc),
        updatedAt=datetime.now(timezone.utc),
        isSynced=False,
        syncedAt=None
    )

@pytest.mark.asyncio
async def test_insert_workorder_success(tracos_service, sample_workorder):

    result = await tracos_service.insert_workorder(sample_workorder)
    assert result is not None
    assert result.number == sample_workorder.number
    assert result.title == sample_workorder.title

    db_workorder = await tracos_service.get_workorder_by_number(sample_workorder.number)
    assert db_workorder is not None
    assert db_workorder.number == sample_workorder.number



@pytest.mark.asyncio
async def test_update_workorder_success(tracos_service, sample_workorder):

    await tracos_service.insert_workorder(sample_workorder)
    
    await tracos_service.update_workorder(sample_workorder.number)

    updated_workorder = await tracos_service.get_workorder_by_number(sample_workorder.number)
    assert updated_workorder is not None
    assert updated_workorder.isSynced is True

    assert hasattr(updated_workorder, "syncedAt")
    assert updated_workorder.syncedAt is not None

@pytest.mark.asyncio
async def test_update_nonexistent_workorder(tracos_service):
    # Try to update a workorder that doesn't exist
    result = await tracos_service.update_workorder(99999)
    assert result is None
