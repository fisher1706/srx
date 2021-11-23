
import pytest
from src.api.customer.replenishment_list_api import ReplenishmentListApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.mocks_api import MocksApi

@pytest.mark.erp
@pytest.mark.regression
def test_sales_order_status_update_status_and_quantity(ilx_api, sync_order_location_preset):
    ilx_api.testrail_case_id = 10057

    ta = TransactionApi(ilx_api)
    rla = ReplenishmentListApi(ilx_api)
    ma = MocksApi(ilx_api)

    preset = sync_order_location_preset(ilx_api, sync_endpoint="salesOrdersStatus")
    transaction_id = preset["transaction"]["transaction_id"]
    sku = preset["product"]["partSku"]
    items = [{
        "id": transaction_id,
        "reorderQuantity": preset["transaction"]["reorder_quantity"],
        "status": "QUOTED"
    }]
    rla.submit_replenishment_list(items)
    transactions = ta.get_transaction(shipto_id=preset["shipto_id"])

    assert transactions["totalElements"] == 1, "Only 1 transaction should be present"
    assert transactions["entities"][0]["erpOrderId"] == f"{transaction_id}"
    assert transactions["entities"][0]["status"] == "QUOTED"
    assert transactions["entities"][0]["reorderQuantity"] == 100
    #------------ILX response-------------------
    items_list = [
            {
                "transactionType": "ORDERED",
                "id": f"{transaction_id}-0",
                "items": [
                    {
                    "dsku": sku,
                    "quantity": 200
                    }
                ]
            }
        ]
    #-------------------------------------------
    ma.set_list_of_sales_orders_v1_items(items_list)
    ta.refresh_order_status(transaction_id, False)
    transactions = ta.get_transaction(shipto_id=preset["shipto_id"])

    assert transactions["totalElements"] == 1, "Only 1 transaction should be present"
    assert transactions["entities"][0]["erpOrderId"] == f"{transaction_id}-0"
    assert transactions["entities"][0]["status"] == "ORDERED"
    assert transactions["entities"][0]["reorderQuantity"] == 200
