
import copy
import pytest
from src.api.customer.replenishment_list_api import ReplenishmentListApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.mocks_api import MocksApi

@pytest.mark.parametrize("conditions", [
    {
        "status": "ORDERED",
        "quantity": 200,
        "testrail_case_id": 10057
    },
    {
        "status": "SHIPPED",
        "quantity": 20,
        "testrail_case_id": 10058
    },
    {
        "status": "DELIVERED",
        "quantity": 80,
        "testrail_case_id": 10059
    }
    ])
@pytest.mark.erp
@pytest.mark.regression
def test_sales_order_status_update_status_and_quantity(ilx_api, sync_order_location_preset, conditions, delete_shipto): #cases_1-2
    ilx_api.testrail_case_id = conditions["testrail_case_id"]

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
                "transactionType": conditions["status"],
                "id": f"{transaction_id}-0",
                "items": [
                    {
                    "dsku": sku,
                    "quantity": conditions["quantity"]
                    }
                ]
            }
        ]
    #-------------------------------------------
    ma.set_list_of_sales_orders_v1_items(items_list)
    ta.refresh_order_status(transaction_id, False)
    transactions = ta.get_transaction(shipto_id=preset["shipto_id"])

    assert transactions["entities"][0]["erpOrderId"] == f"{transaction_id}-0"
    assert transactions["entities"][0]["status"] == conditions["status"]
    if conditions["status"] in ("SHIPPED", "DELIVERED"):
        assert transactions["entities"][0]["reorderQuantity"] == 100
        assert transactions["entities"][0]["shippedQuantity"] == conditions["quantity"]
        assert transactions["totalElements"] == 2
        assert transactions["entities"][1]["status"] == "ACTIVE"
        assert transactions["entities"][1]["reorderQuantity"] == 100-conditions["quantity"]
    else:
        assert transactions["entities"][0]["reorderQuantity"] == 200
        assert transactions["totalElements"] == 1, "Only 1 transaction should be present"

@pytest.mark.erp
@pytest.mark.regression
def test_sales_order_status_update_with_simulated_order_close_logic(ilx_api, sync_order_location_preset, delete_shipto): #case_9
    ilx_api.testrail_case_id = 10060

    ta = TransactionApi(ilx_api)
    rla = ReplenishmentListApi(ilx_api)
    ma = MocksApi(ilx_api)

    preset = sync_order_location_preset(ilx_api, sync_endpoint="salesOrdersStatus", disable_reorder_controls=True)
    transaction_id = preset["transaction"]["transaction_id"]
    sku = preset["product"]["partSku"]
    items = [{
        "id": transaction_id,
        "reorderQuantity": preset["transaction"]["reorder_quantity"],
        "status": "QUOTED"
    }]
    rla.submit_replenishment_list(items)
    transactions = ta.get_transaction(shipto_id=preset["shipto_id"])
    #------------ILX response-------------------
    items_list = [
            {
                "transactionType": "SHIPPED",
                "id": f"{transaction_id}-1",
                "items": [
                    {
                    "dsku": sku,
                    "quantity": 20
                    }
                ]
            },
            {
                "transactionType": "QUOTED",
                "id": f"{transaction_id}-2",
                "items": [
                    {
                    "dsku": sku,
                    "quantity": 40
                    }
                ]
            }
        ]
    #-------------------------------------------
    ma.set_list_of_sales_orders_v1_items(items_list)
    ta.refresh_order_status(transaction_id, False)
    transactions = ta.get_transaction(shipto_id=preset["shipto_id"])

    assert transactions["totalElements"] == 2
    assert transactions["entities"][0]["erpOrderId"] == f"{transaction_id}-1"
    assert transactions["entities"][0]["status"] == "SHIPPED"
    assert transactions["entities"][0]["reorderQuantity"] == 100
    assert transactions["entities"][0]["shippedQuantity"] == 20
    assert transactions["entities"][1]["erpOrderId"] == f"{transaction_id}-2"
    assert transactions["entities"][1]["status"] == "QUOTED"
    assert transactions["entities"][1]["reorderQuantity"] == 40
    #------------ILX response-------------------
    items_list = [
            {
                "transactionType": "SHIPPED",
                "id": f"{transaction_id}-1",
                "items": [
                    {
                    "dsku": sku,
                    "quantity": 20
                    }
                ]
            },
            {
                "transactionType": "SHIPPED",
                "id": f"{transaction_id}-2",
                "items": [
                    {
                    "dsku": sku,
                    "quantity": 40
                    }
                ]
            }
        ]
    #-------------------------------------------
    ma.set_list_of_sales_orders_v1_items(copy.deepcopy(items_list))
    ta.refresh_order_status(f"{transaction_id}-1", False)
    transactions = ta.get_transaction(shipto_id=preset["shipto_id"])

    assert transactions["totalElements"] == 2
    assert transactions["entities"][0]["erpOrderId"] == f"{transaction_id}-1"
    assert transactions["entities"][0]["status"] == "SHIPPED"
    assert transactions["entities"][0]["reorderQuantity"] == 100
    assert transactions["entities"][0]["shippedQuantity"] == 20
    assert transactions["entities"][1]["erpOrderId"] == f"{transaction_id}-2"
    assert transactions["entities"][1]["status"] == "QUOTED"
    assert transactions["entities"][1]["reorderQuantity"] == 40
    #------------ILX response-------------------
    del items_list[0]
    #-------------------------------------------
    ma.set_list_of_sales_orders_v1_items(copy.deepcopy(items_list))
    ta.refresh_order_status(f"{transaction_id}-2", False)
    transactions = ta.get_transaction(shipto_id=preset["shipto_id"])
    assert transactions["totalElements"] == 2
    assert transactions["entities"][0]["erpOrderId"] == f"{transaction_id}-1"
    assert transactions["entities"][0]["status"] == "SHIPPED"
    assert transactions["entities"][0]["reorderQuantity"] == 100
    assert transactions["entities"][0]["shippedQuantity"] == 20
    assert transactions["entities"][1]["erpOrderId"] == f"{transaction_id}-2"
    assert transactions["entities"][1]["status"] == "SHIPPED"
    assert transactions["entities"][1]["reorderQuantity"] == 40
    assert transactions["entities"][1]["shippedQuantity"] == 40