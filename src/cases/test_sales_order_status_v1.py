
import copy
import pytest
from src.api.customer.replenishment_list_api import ReplenishmentListApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.mocks_api import MocksApi

@pytest.mark.parametrize("conditions", [
    {
        "status": "ORDERED",
        "quantity": 70,
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
    },
    {
        "status": "DO_NOT_REORDER",
        "quantity": 40,
        "testrail_case_id": 10067
    }
    ])
@pytest.mark.erp
@pytest.mark.regression
def test_sales_order_status_update_status_and_quantity(ilx_api, sync_order_location_preset, conditions, delete_shipto):
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

    assert transactions["totalElements"] == 2
    assert transactions["entities"][0]["erpOrderId"] == f"{transaction_id}-0"
    assert transactions["entities"][0]["status"] == conditions["status"]
    assert transactions["entities"][1]["erpOrderId"] == None
    assert transactions["entities"][1]["status"] == "ACTIVE"
    assert transactions["entities"][1]["shippedQuantity"] == None
    if conditions["status"] in ("SHIPPED", "DELIVERED"):
        assert transactions["entities"][0]["reorderQuantity"] == 100
        assert transactions["entities"][0]["shippedQuantity"] == conditions["quantity"]
        assert transactions["entities"][1]["reorderQuantity"] == 100-conditions["quantity"]
    elif conditions["status"] == "ORDERED":
        assert transactions["entities"][0]["reorderQuantity"] == conditions["quantity"]
        assert transactions["entities"][0]["shippedQuantity"] == None
        assert transactions["entities"][1]["reorderQuantity"] == 100-conditions["quantity"]
    else:
        assert transactions["entities"][0]["reorderQuantity"] == conditions["quantity"]
        assert transactions["entities"][0]["shippedQuantity"] == 0
        assert transactions["entities"][1]["reorderQuantity"] == 100

@pytest.mark.erp
@pytest.mark.regression
def test_sales_order_status_update_with_simulated_order_close_logic(ilx_api, sync_order_location_preset, delete_shipto):
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

@pytest.mark.parametrize("conditions", [
    {
        "status_1": "SHIPPED", #1
        "status_2": "SHIPPED",
        "quantity_1": 60,
        "quantity_2": 10,
        "testrail_case_id": 10063
    },
    {
        "status_1": "SHIPPED", #2
        "status_2": "SHIPPED",
        "quantity_1": 100,
        "quantity_2": 10,
        "testrail_case_id": 10064
    },
    {
        "status_1": "SHIPPED", #3
        "status_2": "SHIPPED",
        "quantity_1": 150,
        "quantity_2": 10,
        "testrail_case_id": 10065
    },
    {
        "status_1": "DELIVERED", #4
        "status_2": "DELIVERED",
        "quantity_1": 150,
        "quantity_2": 10,
        "testrail_case_id": 10068
    },
    {
        "status_1": "QUOTED", #5
        "status_2": "ORDERED",
        "quantity_1": 10,
        "quantity_2": 10,
        "testrail_case_id": 10069
    },
    {
        "status_1": "ORDERED", #6
        "status_2": "DELIVERED",
        "quantity_1": 20,
        "quantity_2": 20,
        "testrail_case_id": 10070
    },
    {
        "status_1": "SHIPPED", #7
        "status_2": "QUOTED",
        "quantity_1": 150,
        "quantity_2": 10,
        "testrail_case_id": 10071
    },
    {
        "status_1": "DO_NOT_REORDER", #8
        "status_2": "DO_NOT_REORDER",
        "quantity_1": 150,
        "quantity_2": 10,
        "testrail_case_id": 10072
    },
    {
        "status_1": "DO_NOT_REORDER", #9
        "status_2": "SHIPPED",
        "quantity_1": 150,
        "quantity_2": 10,
        "testrail_case_id": 10073
    },
    {
        "status_1": "DELIVERED", #10
        "status_2": "DO_NOT_REORDER",
        "quantity_1": 150,
        "quantity_2": 10,
        "testrail_case_id": 10074
    }
    ])
@pytest.mark.erp
@pytest.mark.regression
def test_split_single_transaction_with_by_two_items(ilx_api, sync_order_location_preset, conditions, delete_shipto): #cases_1-2
    ilx_api.testrail_case_id = conditions["testrail_case_id"]

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
                "transactionType": conditions["status_1"],
                "id": f"{transaction_id}-1",
                "items": [
                    {
                        "dsku": sku,
                        "quantity": conditions["quantity_1"]
                    }
                ]
            },
            {
                "transactionType": conditions["status_2"],
                "id": f"{transaction_id}-2",
                "items": [
                    {
                        "dsku": sku,
                        "quantity": conditions["quantity_2"]
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
    assert transactions["entities"][1]["erpOrderId"] == f"{transaction_id}-2"
    assert transactions["entities"][0]["status"] == conditions["status_1"]
    assert transactions["entities"][1]["status"] == conditions["status_2"]
    if (conditions["status_1"] in ("SHIPPED", "DELIVERED") and conditions["status_2"] in ("SHIPPED", "DELIVERED")):
        assert transactions["entities"][0]["reorderQuantity"] == 100
        assert transactions["entities"][0]["shippedQuantity"] == conditions["quantity_1"]
        second_reorder_quantity = (100 - conditions["quantity_1"]) if 100 - conditions["quantity_1"] >= 0 else 0
        assert transactions["entities"][1]["reorderQuantity"] == second_reorder_quantity
        assert transactions["entities"][1]["shippedQuantity"] == conditions["quantity_2"]
    elif (conditions["status_1"] in ("QUOTED", "ORDERED") and conditions["status_2"] in ("QUOTED", "ORDERED")):
        assert transactions["entities"][0]["reorderQuantity"] == conditions["quantity_1"]
        assert transactions["entities"][0]["shippedQuantity"] == None
        assert transactions["entities"][1]["reorderQuantity"] == conditions["quantity_2"]
        assert transactions["entities"][1]["shippedQuantity"] == None
    elif (conditions["status_1"] in ("QUOTED", "ORDERED") and conditions["status_2"] in ("SHIPPED", "DELIVERED")):
        assert transactions["entities"][0]["reorderQuantity"] == conditions["quantity_1"]
        assert transactions["entities"][0]["shippedQuantity"] == None
        assert transactions["entities"][1]["reorderQuantity"] == 0
        assert transactions["entities"][1]["shippedQuantity"] == conditions["quantity_2"]
    elif (conditions["status_1"] in ("SHIPPED", "DELIVERED") and conditions["status_2"] in ("QUOTED", "ORDERED")):
        assert transactions["entities"][0]["reorderQuantity"] == 100
        assert transactions["entities"][0]["shippedQuantity"] == conditions["quantity_1"]
        assert transactions["entities"][1]["reorderQuantity"] == conditions["quantity_2"]
        assert transactions["entities"][1]["shippedQuantity"] == None
    elif (conditions["status_1"] == "DO_NOT_REORDER" and conditions["status_2"] == "DO_NOT_REORDER"):
        assert transactions["entities"][0]["reorderQuantity"] == conditions["quantity_1"]
        assert transactions["entities"][0]["shippedQuantity"] == 0
        assert transactions["entities"][1]["reorderQuantity"] == conditions["quantity_2"]
        assert transactions["entities"][1]["shippedQuantity"] == 0
    elif (conditions["status_1"] == "DO_NOT_REORDER" and conditions["status_2"] in ("SHIPPED", "DELIVERED")):
        assert transactions["entities"][0]["reorderQuantity"] == conditions["quantity_1"]
        assert transactions["entities"][0]["shippedQuantity"] == 0
        assert transactions["entities"][1]["reorderQuantity"] == 0
        assert transactions["entities"][1]["shippedQuantity"] == conditions["quantity_2"]
    elif (conditions["status_1"] in ("SHIPPED", "DELIVERED") and conditions["status_2"] == "DO_NOT_REORDER"):
        assert transactions["entities"][0]["reorderQuantity"] == 100
        assert transactions["entities"][0]["shippedQuantity"] == conditions["quantity_1"]
        assert transactions["entities"][1]["reorderQuantity"] == conditions["quantity_2"]
        assert transactions["entities"][1]["shippedQuantity"] == 0
    else:
        ilx_api.logger.error("No such statuses combination. Please add")