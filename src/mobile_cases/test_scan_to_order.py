from src.api.mobile.mobile_transaction_api import MobileTransactionApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.setups.setup_location import SetupLocation
from src.api.distributor.location_api import LocationApi
from src.resources.permissions import Permissions
import pytest


class TestScanToOrder():
    @pytest.mark.parametrize("permissions", [
        {
            "user": None,
            "testrail_case_id": 2215
        },
        { 
            "user": Permissions.mobile_labels("ENABLE", True),
            "testrail_case_id": 2462
        }
        ])
    @pytest.mark.acl
    @pytest.mark.regression
    def test_bulk_create_transaction(self, mobile_api, permission_api, permissions, delete_shipto, delete_distributor_security_group):
        mobile_api.testrail_case_id = permissions["testrail_case_id"]
        context = Permissions.set_configured_user(mobile_api, permissions["user"], permission_context=permission_api)
        mta = MobileTransactionApi(context)
        ta = TransactionApi(mobile_api)

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True})
        response_location_1 = setup_location.setup()
        setup_location.add_option("shipto_id", response_location_1["shipto_id"])
        response_location_2 = setup_location.setup()

        data = [
            {
                "partSku": response_location_1["product"]["partSku"],
                "quantity": response_location_1["product"]["roundBuy"] * 3
            },
            {
                "partSku": response_location_2["product"]["partSku"],
                "quantity": response_location_2["product"]["roundBuy"] * 3
            }
        ]

        mta.bulk_create(response_location_1["shipto_id"], data, admin_context=mobile_api)

        transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"], status="ACTIVE", )["entities"]

        assert len(transactions) == 2, "There should be 2 transactions"
        assert transactions[0]["product"]["partSku"] == response_location_1["product"]["partSku"], f"Sku of product should be equal to {response_location_1['product']['partSku']}"
        assert transactions[0]["reorderQuantity"] == (response_location_1["product"]["roundBuy"]*3), f"Reorder quantity of transaction should be equal to {response_location_1['product']['roundBuy']*3}"
        assert transactions[1]["product"]["partSku"] == response_location_2["product"]["partSku"], f"Sku of product should be equal to {response_location_2['product']['partSku']}"
        assert transactions[1]["reorderQuantity"] == (response_location_2["product"]["roundBuy"]*3), f"Reorder quantity of transaction should be equal to {response_location_2['product']['roundBuy']*3}"

    @pytest.mark.acl
    @pytest.mark.regression
    def test_bulk_create_transaction_without_permission(self, mobile_api, permission_api, delete_shipto, delete_distributor_security_group):
        mobile_api.testrail_case_id = 2463
        Permissions.set_configured_user(mobile_api, Permissions.mobile_labels("ENABLE", False))
        mta = MobileTransactionApi(permission_api)
        ta = TransactionApi(mobile_api)

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True})
        response_location_1 = setup_location.setup()
        setup_location.add_option("shipto_id", response_location_1["shipto_id"])
        response_location_2 = setup_location.setup()

        data = [
            {
                "partSku": response_location_1["product"]["partSku"],
                "quantity": response_location_1["product"]["roundBuy"] * 3
            },
            {
                "partSku": response_location_2["product"]["partSku"],
                "quantity": response_location_2["product"]["roundBuy"] * 3
            }
        ]

        mta.bulk_create(response_location_1["shipto_id"], data, failed=True, admin_context=mobile_api)

    @pytest.mark.regression
    def test_bulk_create_transaction_for_non_exist_sku(self, mobile_api, delete_shipto):
        mobile_api.testrail_case_id = 2179
        mta = MobileTransactionApi(mobile_api)
        ta = TransactionApi(mobile_api)

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True})
        response_location_1 = setup_location.setup()
        setup_location.add_option("shipto_id", response_location_1["shipto_id"])
        response_location_2 = setup_location.setup()

        data = [
            {
                "partSku": "TEST SKU 1",
                "quantity": response_location_1["product"]["roundBuy"] * 3
            },
            {
                "partSku": "TEST SKU 2",
                "quantity": response_location_2["product"]["roundBuy"] * 3
            }
        ]

        mta.bulk_create(response_location_1["shipto_id"], data, repeat=3, failed=True)

        transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"], status="ACTIVE")["entities"]

        assert len(transactions) == 0, "There should be 0 transactions, SKU's don't exist in the given ShipTo"

    @pytest.mark.regression
    def test_bulk_create_transaction_with_zero_quantity(self, mobile_api, delete_shipto):
        mobile_api.testrail_case_id = 2180
        mta = MobileTransactionApi(mobile_api)
        ta = TransactionApi(mobile_api)

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True})
        response_location_1 = setup_location.setup()
        setup_location.add_option("shipto_id", response_location_1["shipto_id"])
        response_location_2 = setup_location.setup()

        data = [
            {
                "partSku": response_location_1["product"]["partSku"],
                "quantity": 0
            },
            {
                "partSku": response_location_2["product"]["partSku"],
                "quantity": 0
            }
        ]

        mta.bulk_create(response_location_1["shipto_id"], data, repeat=3, failed=True)

        transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"], status="ACTIVE")["entities"]

        assert len(transactions) == 0, "There should be 0 transactions, the Quantity parameters are missing."

    @pytest.mark.regression
    def test_bulk_create_transaction_with_asset_flag(self, mobile_api, delete_shipto):
        mobile_api.testrail_case_id = 2186
        mta = MobileTransactionApi(mobile_api)
        ta = TransactionApi(mobile_api)

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True})
        setup_location.setup_product.add_option("asset")

        response_location_1 = setup_location.setup()
        setup_location.add_option("shipto_id", response_location_1["shipto_id"])
        response_location_2 = setup_location.setup()

        data = [
            {
                "partSku": response_location_1["product"]["partSku"],
                "quantity": response_location_1["product"]["roundBuy"] * 3
            },
            {
                "partSku": response_location_2["product"]["partSku"],
                "quantity": response_location_2["product"]["roundBuy"] * 3
            }
        ]

        mta.bulk_create(response_location_1["shipto_id"], data, repeat=3, failed=True)

        transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"], status="ACTIVE")["entities"]

        assert len(transactions) == 0, "There should be 0 transactions, products cannot be ordered, these products with asset flag"

    @pytest.mark.parametrize("conditions", [
        {
            
            "testrail_case_id": 2188,
            "round_buy": 10,
            "reorder_qty_exist_1": 30,
            "reorder_qty_exist_2": 50,
            "reorder_qty_new_1": 30,
            "reorder_qty_new_2": 50,
            "result_reorder_qty_1": 30,
            "result_reorder_qty_2": 50

        },
        {
            "testrail_case_id": 7007,
            "round_buy": 4,
            "reorder_qty_exist_1": 16,
            "reorder_qty_exist_2": 28,
            "reorder_qty_new_1": 24,
            "reorder_qty_new_2": 56,
            "result_reorder_qty_1": 24,
            "result_reorder_qty_2": 56
        }
    ])
    @pytest.mark.regression
    def test_bulk_create_for_exist_transactions_in_active(self, mobile_api, conditions, delete_shipto):
        mobile_api.testrail_case_id = conditions["testrail_case_id"]
        mta = MobileTransactionApi(mobile_api)
        ta = TransactionApi(mobile_api)
        la = LocationApi(mobile_api)

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True})
        setup_location.setup_product.add_option("round_buy", conditions["round_buy"])
        response_location_1 = setup_location.setup()
        setup_location.add_option("shipto_id", response_location_1["shipto_id"])
        response_location_2 = setup_location.setup()

        data = [
            {
                "partSku": response_location_1["product"]["partSku"],
                "quantity": conditions["reorder_qty_exist_1"]
            },
            {
                "partSku": response_location_2["product"]["partSku"],
                "quantity": conditions["reorder_qty_exist_2"]
            }
        ]

        mta.bulk_create(response_location_1["shipto_id"], data)

        order_config_id_1 = la.get_ordering_config_by_sku(response_location_1["shipto_id"], response_location_1["product"]["partSku"])
        order_config_id_2 = la.get_ordering_config_by_sku(response_location_2["shipto_id"], response_location_2["product"]["partSku"])

        exist_transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"], status="ACTIVE")["entities"]
        transaction_id_1 = exist_transactions[0]["id"]
        transaction_id_2 = exist_transactions[1]["id"]

        new_data = [
            {
                "partSku": response_location_1["product"]["partSku"],
                "locationId": response_location_1["location_id"],
                "orderingConfigId": order_config_id_1,
                "quantity": conditions["reorder_qty_new_1"],
                "transactionId": transaction_id_1
            },
            {
                "partSku": response_location_2["product"]["partSku"],
                "locationId": response_location_2["location_id"],
                "orderingConfigId": order_config_id_2,
                "quantity": conditions["reorder_qty_new_2"],
                "transactionId": transaction_id_2
            }
        ]
        
        mta.bulk_create(response_location_1["shipto_id"], new_data, repeat=2, failed=True)
        transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"], status="ACTIVE")["entities"]
        assert len(transactions) == 2, "Transactions already exist in Active status and new transaction has been not created"
        total_transactions_count = ta.get_transactions_count(shipto_id = response_location_1["shipto_id"])
        assert total_transactions_count == 2, "The total transactions count should be equal 2"
        assert transactions[0]["reorderQuantity"] == conditions["result_reorder_qty_1"], f"Reorder quantity of {transactions[0]['productPartSku']} should be equal to {conditions['result_reorder_qty_1']}"
        assert transactions[1]["reorderQuantity"] == conditions["result_reorder_qty_2"], f"Reorder quantity of {transactions[1]['productPartSku']} should be equal to {conditions['result_reorder_qty_2']}"

    @pytest.mark.parametrize("conditions", [
        {
            "status": "ORDERED",
            "testrail_case_id": 2190,
            "round_buy": 10,
            "reorder_qty_exist_1": 30,
            "reorder_qty_exist_2": 50,
            "reorder_qty_new_1": 40,
            "reorder_qty_new_2": 20


        },
        {
            "status": "SHIPPED",
            "testrail_case_id": 2192,
            "round_buy": 8,
            "reorder_qty_exist_1": 32,
            "reorder_qty_exist_2": 64,
            "reorder_qty_new_1": 40,
            "reorder_qty_new_2": 56
        },
        {
            "status": "QUOTED",
            "testrail_case_id": 2193,
            "round_buy": 3,
            "reorder_qty_exist_1": 27,
            "reorder_qty_exist_2": 54,
            "reorder_qty_new_1": 36,
            "reorder_qty_new_2": 42

        }
    ])
    @pytest.mark.regression
    def test_bulk_create_for_exist_transactions_in_different_status(self, mobile_api, conditions, delete_shipto):
        mobile_api.testrail_case_id = conditions["testrail_case_id"]
        mta = MobileTransactionApi(mobile_api)
        ta = TransactionApi(mobile_api)

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True})
        setup_location.setup_product.add_option("round_buy", conditions["round_buy"])
        response_location_1 = setup_location.setup()
        setup_location.add_option("shipto_id", response_location_1["shipto_id"])
        response_location_2 = setup_location.setup()

        data = [
            {
                "partSku": response_location_1["product"]["partSku"],
                "quantity": conditions["reorder_qty_exist_1"]
            },
            {
                "partSku": response_location_2["product"]["partSku"],
                "quantity": conditions["reorder_qty_exist_2"]
            }
        ]

        mta.bulk_create(response_location_1["shipto_id"], data)

        transactions_in_active = ta.get_transaction(shipto_id=response_location_1["shipto_id"], status="ACTIVE")["entities"]

        ta.update_replenishment_item(transactions_in_active[0]["id"], conditions["reorder_qty_exist_1"], conditions["status"])
        ta.update_replenishment_item(transactions_in_active[1]["id"], conditions["reorder_qty_exist_2"], conditions["status"])

        transactions_after_update = ta.get_transaction(shipto_id=response_location_1["shipto_id"])["entities"]

        assert len(transactions_after_update) == 2, f"There are should be 2 transactions in {conditions['status']} status"
        assert transactions_after_update[0]["status"] == conditions["status"], f"Status of {transactions_after_update[0]['productPartSku']} should be equal {conditions['status']} status"
        assert transactions_after_update[1]["status"] == conditions["status"], f"Status of {transactions_after_update[1]['productPartSku']} should be equal {conditions['status']} status"

        data_for_new_transactions = [
            {
                "partSku": response_location_1["product"]["partSku"],
                "quantity": conditions["reorder_qty_new_1"]
            },
            {
                "partSku": response_location_2["product"]["partSku"],
                "quantity": conditions["reorder_qty_new_2"]
            }
        ]

        mta.bulk_create(response_location_1["shipto_id"], data_for_new_transactions)

        new_transactions_in_active = ta.get_transaction(shipto_id=response_location_1["shipto_id"], status="ACTIVE")["entities"]
        assert len(new_transactions_in_active) == 2, f"There are should be 2 transactions in ACTIVE status"
        assert new_transactions_in_active[0]["reorderQuantity"] == conditions["reorder_qty_new_1"], f"Reorder quantity of {new_transactions_in_active[0]['productPartSku']} should be equal to {conditions['reorder_qty_new_1']}"
        assert new_transactions_in_active[1]["reorderQuantity"] == conditions["reorder_qty_new_2"], f"Reorder quantity of {new_transactions_in_active[1]['productPartSku']} should be equal to {conditions['reorder_qty_new_2']}"

        transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"], status = conditions["status"])["entities"]
        assert transactions[0]["reorderQuantity"] == conditions["reorder_qty_exist_1"], f"Reorder quantity of {transactions[0]['productPartSku']} should be equal to {conditions['reorder_qty_exist_1']}"
        assert transactions[1]["reorderQuantity"] == conditions["reorder_qty_exist_2"], f"Reorder quantity of {transactions[1]['productPartSku']} should be equal to {conditions['reorder_qty_exist_2']}"
        
        total_transactions_count = ta.get_transactions_count(shipto_id = response_location_1["shipto_id"])
        assert total_transactions_count == 4, "The total transactions count should be equal 4"

    @pytest.mark.parametrize("conditions", [
        {
            "quantity": 3,
            "round_buy": 5,
            "result": 5,
            "testrail_case_id": 2187
        },
        {
            "quantity": 11,
            "round_buy": 10,
            "result": 20,
            "testrail_case_id": 2311
        },
        {
            "quantity": 19,
            "round_buy": 10,
            "result": 20,
            "testrail_case_id": 2312
        }
    ])
    @pytest.mark.regression
    def test_bulk_create_with_qnty_not_alligned_roundBuy(self, mobile_api, conditions, delete_shipto):
        mobile_api.testrail_case_id = conditions["testrail_case_id"]
        mta = MobileTransactionApi(mobile_api)
        ta = TransactionApi(mobile_api)

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True})
        setup_location.setup_product.add_option("round_buy", conditions["round_buy"])
        response_location_1 = setup_location.setup()
        setup_location.add_option("shipto_id", response_location_1["shipto_id"])
        response_location_2 = setup_location.setup()

        data = [
            {
                "partSku": response_location_1["product"]["partSku"],
                "quantity": conditions["quantity"]
            },
            {
                "partSku": response_location_2["product"]["partSku"],
                "quantity": conditions["quantity"]
            }
        ]

        mta.bulk_create(response_location_1["shipto_id"], data)

        transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"], status="ACTIVE")["entities"]

        assert transactions[0]["reorderQuantity"] == conditions["result"], f"Reorder quantity of  {transactions[0]['productPartSku']} should be equal to {conditions['result']}"
        assert transactions[1]["reorderQuantity"] == conditions["result"], f"Reorder quantity of  {transactions[1]['productPartSku']} should be equal to {conditions['result']}"
