import pytest
from src.api.distributor.location_api import LocationApi
from src.api.customer.replenishment_list_api import ReplenishmentListApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.mocks_api import MocksApi
from src.resources.complex_assert import ComplexAssert
from src.entities.transaction import Transaction

@pytest.mark.parametrize("conditions", [
    {
        "init": Transaction("QUOTED", 100),
        "new": Transaction("ORDERED", 80, 70),
        "additional": Transaction("ACTIVE", 20),
        "testrail_case_id": 11342
    },
    {
        "init": Transaction("QUOTED", 100),
        "new": Transaction("SHIPPED", 30, 20),
        "additional": Transaction("BACKORDERED", 80),
        "testrail_case_id": 11343
    },
    {
        "init": Transaction("QUOTED", 100),
        "new": Transaction("DELIVERED", 90, 80),
        "additional": Transaction("BACKORDERED", 20),
        "testrail_case_id": 11344
    },
    {
        "init": Transaction("QUOTED", 100),
        "new": Transaction("DO_NOT_REORDER", 50, 40),
        "additional": Transaction("ACTIVE", 100),
        "testrail_case_id": 11345
    },
    {
        "init": Transaction("SHIPPED", 100, 100),
        "new": Transaction("DELIVERED", 100, 90),
        "additional": Transaction("BACKORDERED", 10),
        "testrail_case_id": 11358
    }
    ])
@pytest.mark.erp
def test_sales_orders_status_v2_update_status_and_quantity(srx_integration_api, sync_order_location_preset, conditions, delete_shipto):
    srx_integration_api.testrail_case_id = conditions["testrail_case_id"]
    init = conditions["init"]
    new = conditions["new"]
    additional = conditions["additional"]

    LOCATION_MAX = 100

    ta = TransactionApi(srx_integration_api)
    rla = ReplenishmentListApi(srx_integration_api)
    ma = MocksApi(srx_integration_api)
    la = LocationApi(srx_integration_api)

    preset = sync_order_location_preset(srx_integration_api, sync_endpoint="salesOrdersStatusV2")
    transaction_id = preset["transaction"]["transaction_id"]
    sku = preset["product"]["partSku"]
    items = [{
        "id": transaction_id,
        "reorderQuantity": preset["transaction"]["reorder_quantity"],
        "status": "QUOTED"
    }]
    rla.submit_replenishment_list(items)

    if init.status != "QUOTED" or init.quantity_ordered != LOCATION_MAX:
        ta.update_replenishment_item(transaction_id, init.quantity_ordered, init.status, init.quantity_shipped)

    transactions = ta.get_transaction(shipto_id=preset["shipto_id"])
    locations = la.get_locations(preset["shipto_id"], customer_id=preset["customer_id"])

    assert locations[0]["onHandInventory"] == 0
    assert transactions["totalElements"] == 1, "Only 1 transaction should be present"
    ComplexAssert.transaction(transactions["entities"][0], init.status, init.quantity_ordered, init.quantity_shipped, transaction_id)
    #------------ILX response-------------------
    items_list = [
            {
                "transactionType": new.status,
                "id": f"{transaction_id}",
                "release": 1,
                "items": [
                    {
                        "dsku": sku,
                        "quantityShipped": new.quantity_shipped,
                        "quantityOrdered": new.quantity_ordered
                    }
                ]
            }
        ]
    #-------------------------------------------
    ma.set_list_of_sales_orders_v2_items(items_list)
    ta.refresh_order_status(transaction_id, True)
    transactions = ta.get_transaction(shipto_id=preset["shipto_id"])
    locations = la.get_locations(preset["shipto_id"], customer_id=preset["customer_id"])

    assert locations[0]["onHandInventory"] == 0
    assert transactions["totalElements"] == 2
    ComplexAssert.transaction(transactions["entities"][0], new.status, new.quantity_ordered, new.quantity_shipped, transaction_id, 1, transactions["entities"][1]["id"])
    additional_erp_order_id = transaction_id if additional.status == "BACKORDERED" else None
    ComplexAssert.transaction(transactions["entities"][1], additional.status, additional.quantity_ordered, additional.quantity_shipped, additional_erp_order_id)

@pytest.mark.parametrize("conditions", [
    {
        "init": Transaction.several(("SHIPPED", 100, 20), ("ORDERED", 80, 80)),
        "new": Transaction.several(("SHIPPED", 80, 40), ("SHIPPED", 80, 80)),
        "additional": Transaction(),
        "testrail_case_id": 11346
    }
    ])
@pytest.mark.erp
def test_sales_orders_status_v2_update_several_transactions(srx_integration_api, sync_order_location_preset, conditions, delete_shipto):
    srx_integration_api.testrail_case_id = conditions["testrail_case_id"]
    init = conditions["init"]
    new = conditions["new"]

    LOCATION_MAX = 100

    ta = TransactionApi(srx_integration_api)
    rla = ReplenishmentListApi(srx_integration_api)
    ma = MocksApi(srx_integration_api)

    preset = sync_order_location_preset(srx_integration_api, sync_endpoint="salesOrdersStatusV2", disable_reorder_controls=True)
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
                "transactionType": init[0].status,
                "id": f"{transaction_id}",
                "release": 1,
                "items": [
                    {
                        "dsku": sku,
                        "quantityShipped": init[0].quantity_shipped,
                        "quantityOrdered": init[0].quantity_ordered
                    }
                ]
            },
            {
                "transactionType": init[1].status,
                "id": f"{transaction_id}",
                "release": 2,
                "items": [
                    {
                        "dsku": sku,
                        "quantityShipped": init[1].quantity_shipped,
                        "quantityOrdered": init[1].quantity_ordered
                    }
                ]
            }
        ]
    #-------------------------------------------
    ma.set_list_of_sales_orders_v2_items(items_list)
    ta.refresh_order_status(transaction_id, True)
    transactions = ta.get_transaction(shipto_id=preset["shipto_id"])

    additional_transactions = ComplexAssert.v2_backorder_or_active(transactions, [Transaction("QUOTED", LOCATION_MAX)], init)
    ComplexAssert.transaction(transactions["entities"][0], init[0].status, init[0].quantity_ordered, init[0].quantity_shipped, transaction_id, 1)
    ComplexAssert.transaction(transactions["entities"][1], init[1].status, init[1].quantity_ordered, init[1].quantity_shipped, transaction_id, 2)
    assert transactions["totalElements"] == 2 + additional_transactions
    # #------------ILX response-------------------
    # items_list = [
    #         {
    #             "transactionType": new[0].status,
    #             "id": f"{transaction_id}",
    #             "release": 1,
    #             "items": [
    #                 {
    #                     "dsku": sku,
    #                     "quantityShipped": new[0].quantity_shipped,
    #                     "quantityOrdered": new[0].quantity_ordered
    #                 }
    #             ]
    #         },
    #         {
    #             "transactionType": new[1].status,
    #             "id": f"{transaction_id}",
    #             "release": 2,
    #             "items": [
    #                 {
    #                     "dsku": sku,
    #                     "quantityShipped": new[1].quantity_shipped,
    #                     "quantityOrdered": new[1].quantity_ordered
    #                 }
    #             ]
    #         }
    #     ]
    # #-------------------------------------------
    # ma.set_list_of_sales_orders_v2_items(items_list)
    # ta.refresh_order_status(transaction_id, True)
    # transactions = ta.get_transaction(shipto_id=preset["shipto_id"])

    # assert transactions["totalElements"] == 2
    # ComplexAssert.transaction(transactions["entities"][0], new[0].status, new[0].quantity_ordered, new[0].quantity_shipped, transaction_id, 1)
    # ComplexAssert.transaction(transactions["entities"][1], new[1].status, new[1].quantity_ordered, new[1].quantity_shipped, transaction_id, 2)
