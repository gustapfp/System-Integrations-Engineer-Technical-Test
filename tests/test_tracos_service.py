import pytest
from datetime import datetime, timezone
from bson import ObjectId
from src.services.tracos_service import TracOsService
from src.schemas.tracos_schema import TracOSWorkorderSchema

@pytest.fixture
async def tracos_service():
    service = TracOsService()
    yield service

    await service.collection.drop()

@pytest.fixture
def sample_workorder():
    """Create a sample workorder for testing."""
    return TracOSWorkorderSchema(
        _id=ObjectId(),
        number=12345,
        status="pending",
        title="Test Workorder",
        description="This is a test workorder",
        createdAt=datetime.now(timezone.utc),
        updatedAt=datetime.now(timezone.utc)
    )

@pytest.mark.asyncio
async def test_insert_workorder_success(tracos_service, sample_workorder):
    """Test inserting a workorder."""
    result = await tracos_service.insert_workorder(sample_workorder)
    assert result is not None
    assert result.number == sample_workorder.number
    assert result.title == sample_workorder.title
    
@pytest.mark.asyncio
async def test_insert_workorder_validation_error(tracos_service):
    """Test inserting a workorder with validation error."""
    db_workorder = await tracos_service.get_workorder(sample_workorder.number)
    assert db_workorder is not None
    assert db_workorder["number"] == sample_workorder.number



@pytest.mark.asyncio
async def test_update_workorder_success(tracos_service, sample_workorder):
    """Test updating a workorder."""
    await tracos_service.insert_workorder(sample_workorder)
    
    await tracos_service.update_workorder(sample_workorder.number)

    updated_workorder = await tracos_service.get_workorder(sample_workorder.number)
    assert updated_workorder is not None
    assert updated_workorder["isSynced"] is True
    assert "syncedAt" in updated_workorder
    assert updated_workorder["syncedAt"] is not None

@pytest.mark.asyncio
async def test_update_nonexistent_workorder(tracos_service):
    """Test updating a workorder that does not exist."""
    result = await tracos_service.update_workorder(99999)
    assert result is None
