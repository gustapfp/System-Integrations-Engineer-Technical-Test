import pytest
from datetime import datetime
import os
import json
from src.routes.costumer_routes import CostumerERPRoute
from src.schemas.customer_schema import CustomerSystemWorkorderSchema
from pathlib import Path




@pytest.fixture
def sample_workorder():
    return CustomerSystemWorkorderSchema(
        orderNo=123,
        isActive=True,
        isCanceled=False,
        isDeleted=False,
        isDone=False,
        isOnHold=False,
        isPending=True,
        isSynced=False,
        summary="Test workorder",
        creationDate=datetime.now(),
        lastUpdateDate=datetime.now()
    )




@pytest.fixture
def costumer_route(monkeypatch):



    return CostumerERPRoute()


@pytest.mark.asyncio
async def test_get_costumer_workorder_by_order_number(costumer_route):
    """Test fetching a workorder by order number."""

    result = await costumer_route.get_costumer_workorder_by_order_number(1)
    assert result is not None
    assert isinstance(result, dict)
    assert "orderNo" in result
    assert "summary" in result

    result = await costumer_route.get_costumer_workorder_by_order_number(99999)
    assert result is None

@pytest.mark.asyncio
async def test_post_costumer_workorder(costumer_route, sample_workorder):
    """Test posting a workorder."""

    result = await costumer_route.post_costumer_workorder(sample_workorder)
    assert result is not None
    assert isinstance(result, dict)
    assert result["orderNo"] == sample_workorder.orderNo
    assert result["summary"] == sample_workorder.summary
    

    expected_file_path = os.path.join(os.getenv("DATA_OUTBOUND_DIR", "data/outbound"), f"{sample_workorder.orderNo}.json")
    assert os.path.exists(expected_file_path)
    

    try:
        os.remove(expected_file_path)
    except:
        pass  # Ignore cleanup errors

    invalid_result = await costumer_route.post_costumer_workorder(None)
    assert invalid_result is None
