
import copy
import pytest
from src.api.customer.replenishment_list_api import ReplenishmentListApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.mocks_api import MocksApi

@pytest.mark.parametrize("conditions", [
    {
        "status": "ORDERED", #1
        "quantity": 70,
        "testrail_case_id": 10057
    },
    {
        "status": "SHIPPED", #2
        "quantity": 20,
        "testrail_case_id": 10058
    },
    {
        "status": "DELIVERED", #3
        "quantity": 80,
        "testrail_case_id": 10059
    },
    {
        "status": "DO_NOT_REORDER", #4
        "quantity": 40,
        "testrail_case_id": 10067
    }
    ])
@pytest.mark.erp
def test_sales_order_status_update_status_and_quantity(ilx_api, sync_order_location_preset, conditions, delete_shipto):
    ilx_api.testrail_case_id = conditions["testrail_case_id"]

    LOCATION_MAX = 100

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
    assert transactions["entities"][0]["reorderQuantity"] == LOCATION_MAX
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
    assert transactions["entities"][1]["erpOrderId"] is None
    assert transactions["entities"][1]["status"] == "ACTIVE"
    assert transactions["entities"][1]["shippedQuantity"] is None
    if conditions["status"] in ("SHIPPED", "DELIVERED"):
        assert transactions["entities"][0]["reorderQuantity"] == LOCATION_MAX
        assert transactions["entities"][0]["shippedQuantity"] == conditions["quantity"]
        assert transactions["entities"][1]["reorderQuantity"] == LOCATION_MAX-conditions["quantity"]
    elif conditions["status"] == "ORDERED":
        assert transactions["entities"][0]["reorderQuantity"] == conditions["quantity"]
        assert transactions["entities"][0]["shippedQuantity"] is None
        assert transactions["entities"][1]["reorderQuantity"] == LOCATION_MAX-conditions["quantity"]
    else:
        assert transactions["entities"][0]["reorderQuantity"] == conditions["quantity"]
        assert transactions["entities"][0]["shippedQuantity"] == 0
        assert transactions["entities"][1]["reorderQuantity"] == LOCATION_MAX

@pytest.mark.erp
def test_sales_order_status_update_with_simulated_order_close_logic(ilx_api, sync_order_location_preset, delete_shipto):
    ilx_api.testrail_case_id = 10060

    LOCATION_MAX = 100
    TRANSACTION_QUANTITY_1 = 20 #pylint: disable=C0103
    TRANSACTION_QUANTITY_2 = 40 #pylint: disable=C0103

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
                        "quantity": TRANSACTION_QUANTITY_1
                    }
                ]
            },
            {
                "transactionType": "QUOTED",
                "id": f"{transaction_id}-2",
                "items": [
                    {
                        "dsku": sku,
                        "quantity": TRANSACTION_QUANTITY_2
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
    assert transactions["entities"][0]["reorderQuantity"] == LOCATION_MAX
    assert transactions["entities"][0]["shippedQuantity"] == TRANSACTION_QUANTITY_1
    assert transactions["entities"][1]["erpOrderId"] == f"{transaction_id}-2"
    assert transactions["entities"][1]["status"] == "QUOTED"
    assert transactions["entities"][1]["reorderQuantity"] == TRANSACTION_QUANTITY_2
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
    assert transactions["entities"][0]["reorderQuantity"] == LOCATION_MAX
    assert transactions["entities"][0]["shippedQuantity"] == TRANSACTION_QUANTITY_1
    assert transactions["entities"][1]["erpOrderId"] == f"{transaction_id}-2"
    assert transactions["entities"][1]["status"] == "QUOTED"
    assert transactions["entities"][1]["reorderQuantity"] == TRANSACTION_QUANTITY_2
    #------------ILX response-------------------
    del items_list[0]
    #-------------------------------------------
    ma.set_list_of_sales_orders_v1_items(copy.deepcopy(items_list))
    ta.refresh_order_status(f"{transaction_id}-2", False)
    transactions = ta.get_transaction(shipto_id=preset["shipto_id"])
    assert transactions["totalElements"] == 2
    assert transactions["entities"][0]["erpOrderId"] == f"{transaction_id}-1"
    assert transactions["entities"][0]["status"] == "SHIPPED"
    assert transactions["entities"][0]["reorderQuantity"] == LOCATION_MAX
    assert transactions["entities"][0]["shippedQuantity"] == TRANSACTION_QUANTITY_1
    assert transactions["entities"][1]["erpOrderId"] == f"{transaction_id}-2"
    assert transactions["entities"][1]["status"] == "SHIPPED"
    assert transactions["entities"][1]["reorderQuantity"] == TRANSACTION_QUANTITY_2
    assert transactions["entities"][1]["shippedQuantity"] == TRANSACTION_QUANTITY_2

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
def test_split_single_transaction_by_two_items(ilx_api, sync_order_location_preset, conditions, delete_shipto):
    ilx_api.testrail_case_id = conditions["testrail_case_id"]

    LOCATION_MAX = 100

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
        assert transactions["entities"][0]["reorderQuantity"] == LOCATION_MAX
        assert transactions["entities"][0]["shippedQuantity"] == conditions["quantity_1"]
        assert transactions["entities"][0]["backorderedItemId"] == transactions["entities"][1]["id"]
        second_reorder_quantity = (LOCATION_MAX - conditions["quantity_1"]) if LOCATION_MAX - conditions["quantity_1"] >= 0 else 0
        assert transactions["entities"][1]["reorderQuantity"] == second_reorder_quantity
        assert transactions["entities"][1]["shippedQuantity"] == conditions["quantity_2"]
    elif (conditions["status_1"] in ("QUOTED", "ORDERED") and conditions["status_2"] in ("QUOTED", "ORDERED")):
        assert transactions["entities"][0]["reorderQuantity"] == conditions["quantity_1"]
        assert transactions["entities"][0]["shippedQuantity"] is None
        assert transactions["entities"][0]["backorderedItemId"] == transactions["entities"][1]["id"]
        assert transactions["entities"][1]["reorderQuantity"] == conditions["quantity_2"]
        assert transactions["entities"][1]["shippedQuantity"] is None
    elif (conditions["status_1"] in ("QUOTED", "ORDERED") and conditions["status_2"] in ("SHIPPED", "DELIVERED")):
        assert transactions["entities"][0]["reorderQuantity"] == conditions["quantity_1"]
        assert transactions["entities"][0]["shippedQuantity"] is None
        assert transactions["entities"][0]["backorderedItemId"] == transactions["entities"][1]["id"]
        assert transactions["entities"][1]["reorderQuantity"] == 0
        assert transactions["entities"][1]["shippedQuantity"] == conditions["quantity_2"]
    elif (conditions["status_1"] in ("SHIPPED", "DELIVERED") and conditions["status_2"] in ("QUOTED", "ORDERED")):
        assert transactions["entities"][0]["reorderQuantity"] == LOCATION_MAX
        assert transactions["entities"][0]["shippedQuantity"] == conditions["quantity_1"]
        assert transactions["entities"][0]["backorderedItemId"] == transactions["entities"][1]["id"]
        assert transactions["entities"][1]["reorderQuantity"] == conditions["quantity_2"]
        assert transactions["entities"][1]["shippedQuantity"] is None
    elif (conditions["status_1"] == "DO_NOT_REORDER" and conditions["status_2"] == "DO_NOT_REORDER"):
        assert transactions["entities"][0]["reorderQuantity"] == conditions["quantity_1"]
        assert transactions["entities"][0]["shippedQuantity"] == 0
        assert transactions["entities"][0]["backorderedItemId"] == transactions["entities"][1]["id"]
        assert transactions["entities"][1]["reorderQuantity"] == conditions["quantity_2"]
        assert transactions["entities"][1]["shippedQuantity"] == 0
    elif (conditions["status_1"] == "DO_NOT_REORDER" and conditions["status_2"] in ("SHIPPED", "DELIVERED")):
        assert transactions["entities"][0]["reorderQuantity"] == conditions["quantity_1"]
        assert transactions["entities"][0]["shippedQuantity"] == 0
        assert transactions["entities"][0]["backorderedItemId"] == transactions["entities"][1]["id"]
        assert transactions["entities"][1]["reorderQuantity"] == 0
        assert transactions["entities"][1]["shippedQuantity"] == conditions["quantity_2"]
    elif (conditions["status_1"] in ("SHIPPED", "DELIVERED") and conditions["status_2"] == "DO_NOT_REORDER"):
        assert transactions["entities"][0]["reorderQuantity"] == LOCATION_MAX
        assert transactions["entities"][0]["shippedQuantity"] == conditions["quantity_1"]
        assert transactions["entities"][0]["backorderedItemId"] == transactions["entities"][1]["id"]
        assert transactions["entities"][1]["reorderQuantity"] == conditions["quantity_2"]
        assert transactions["entities"][1]["shippedQuantity"] == 0
    else:
        ilx_api.logger.error("No such statuses combination. Please add")

@pytest.mark.parametrize("conditions", [
    {
        "status_1": "SHIPPED", #1
        "status_2": "SHIPPED",
        "status_3": "SHIPPED",
        "testrail_case_id": 10075
    },
    {
        "status_1": "DELIVERED", #2
        "status_2": "DELIVERED",
        "status_3": "DELIVERED",
        "testrail_case_id": 10076
    },
    {
        "status_1": "DELIVERED", #3
        "status_2": "SHIPPED",
        "status_3": "ORDERED",
        "testrail_case_id": 10077
    },
    {
        "status_1": "QUOTED", #4
        "status_2": "ORDERED",
        "status_3": "SHIPPED",
        "testrail_case_id": 10078
    },
    {
        "status_1": "DO_NOT_REORDER", #5
        "status_2": "DO_NOT_REORDER",
        "status_3": "DO_NOT_REORDER",
        "testrail_case_id": 10079
    },
    {
        "status_1": "DO_NOT_REORDER", #6
        "status_2": "ORDERED",
        "status_3": "SHIPPED",
        "testrail_case_id": 10080
    },
    {
        "status_1": "DELIVERED", #7
        "status_2": "ORDERED",
        "status_3": "DO_NOT_REORDER",
        "testrail_case_id": 10081
    },
    ])
@pytest.mark.erp
def test_split_single_transaction_by_three_items_reorder_controls(ilx_api, sync_order_location_preset, conditions, delete_shipto):
    ilx_api.testrail_case_id = conditions["testrail_case_id"]

    LOCATION_MAX = 100
    TRANSACTION_QUANTITY = 10 #pylint: disable=C0103

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
    #------------ILX response-------------------
    items_list = [
            {
                "transactionType": conditions["status_1"],
                "id": f"{transaction_id}-1",
                "items": [
                    {
                        "dsku": sku,
                        "quantity": TRANSACTION_QUANTITY
                    }
                ]
            },
            {
                "transactionType": conditions["status_2"],
                "id": f"{transaction_id}-2",
                "items": [
                    {
                        "dsku": sku,
                        "quantity": TRANSACTION_QUANTITY
                    }
                ]
            },
            {
                "transactionType": conditions["status_3"],
                "id": f"{transaction_id}-3",
                "items": [
                    {
                        "dsku": sku,
                        "quantity": TRANSACTION_QUANTITY
                    }
                ]
            }
        ]
    #-------------------------------------------
    ma.set_list_of_sales_orders_v1_items(items_list)
    ta.refresh_order_status(transaction_id, False)
    transactions = ta.get_transaction(shipto_id=preset["shipto_id"])

    assert transactions["totalElements"] == 4
    transactions = transactions["entities"]
    for transaction in transactions:
        if transaction["status"] == "ACTIVE":
            count_do_not_reorder = sum(value == "DO_NOT_REORDER" for value in conditions.values())
            assert transaction["erpOrderId"] is None
            assert transaction["reorderQuantity"] == (LOCATION_MAX - TRANSACTION_QUANTITY * (3 - count_do_not_reorder))
            assert transaction["shippedQuantity"] is None
            assert transaction["backorderedItemId"] is None
            transactions.remove(transaction)
            break
    else:
        ilx_api.logger.error("There is no ACTIVE transaction")
    assert transactions[0]["erpOrderId"] == f"{transaction_id}-1"
    assert transactions[1]["erpOrderId"] == f"{transaction_id}-2"
    assert transactions[2]["erpOrderId"] == f"{transaction_id}-3"
    assert transactions[0]["status"] == conditions["status_1"]
    assert transactions[1]["status"] == conditions["status_2"]
    assert transactions[2]["status"] == conditions["status_3"]
    if (conditions["status_1"] in ("SHIPPED", "DELIVERED") and conditions["status_2"] in ("SHIPPED", "DELIVERED") and conditions["status_3"] in ("SHIPPED", "DELIVERED")):
        assert transactions[0]["reorderQuantity"] == LOCATION_MAX
        assert transactions[0]["shippedQuantity"] == TRANSACTION_QUANTITY
        assert transactions[0]["backorderedItemId"] == transactions[1]["id"]
        assert transactions[1]["reorderQuantity"] == (LOCATION_MAX - TRANSACTION_QUANTITY)
        assert transactions[1]["shippedQuantity"] == TRANSACTION_QUANTITY
        assert transactions[1]["backorderedItemId"] == transactions[2]["id"]
        assert transactions[2]["reorderQuantity"] == (LOCATION_MAX - TRANSACTION_QUANTITY * 2)
        assert transactions[2]["shippedQuantity"] == TRANSACTION_QUANTITY
        assert transactions[2]["backorderedItemId"] == None
    if (conditions["status_1"] in ("SHIPPED", "DELIVERED") and conditions["status_2"] in ("SHIPPED", "DELIVERED") and conditions["status_3"] in ("QUOTED", "ORDERED")):
        assert transactions[0]["reorderQuantity"] == LOCATION_MAX
        assert transactions[0]["shippedQuantity"] == TRANSACTION_QUANTITY
        assert transactions[0]["backorderedItemId"] == transactions[1]["id"]
        assert transactions[1]["reorderQuantity"] == (LOCATION_MAX - TRANSACTION_QUANTITY)
        assert transactions[1]["shippedQuantity"] == TRANSACTION_QUANTITY
        assert transactions[1]["backorderedItemId"] == transactions[2]["id"]
        assert transactions[2]["reorderQuantity"] == TRANSACTION_QUANTITY
        assert transactions[2]["shippedQuantity"] == None
        assert transactions[2]["backorderedItemId"] == None

@pytest.mark.erp
def test_update_external_order_id_by_sales_order_status(ilx_api, sync_order_location_preset, delete_shipto):
    ilx_api.testrail_case_id = 10082

    TRANSACTION_QUANTITY = 10 #pylint: disable=C0103

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
                "id": f"0{transaction_id}-1",
                "items": [
                    {
                        "dsku": sku,
                        "quantity": TRANSACTION_QUANTITY
                    }
                ]
            },
            {
                "transactionType": "SHIPPED",
                "id": f"0{transaction_id}-2",
                "items": [
                    {
                        "dsku": sku,
                        "quantity": TRANSACTION_QUANTITY
                    }
                ]
            }
        ]
    #-------------------------------------------
    ma.set_list_of_sales_orders_v1_items(items_list)
    ta.refresh_order_status(transaction_id, False)
    transactions = ta.get_transaction(shipto_id=preset["shipto_id"])
    assert transactions["totalElements"] == 2
    assert transactions["entities"][0]["erpOrderId"] == f"0{transaction_id}-1"
    assert transactions["entities"][1]["erpOrderId"] == f"0{transaction_id}-2"
