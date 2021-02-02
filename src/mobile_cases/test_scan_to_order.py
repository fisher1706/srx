from src.api.mobile.mobile_transaction_api import MobileTransactionApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.setups.setup_location import SetupLocation
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
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
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
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
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
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
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
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
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
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
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

    @pytest.mark.regression
    def test_bulk_create_for_exist_transactions_in_active(self, mobile_api, delete_shipto):
        mobile_api.testrail_case_id = 2188
        mta = MobileTransactionApi(mobile_api)
        ta = TransactionApi(mobile_api)

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
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

        mta.bulk_create(response_location_1["shipto_id"], data)

        transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"], status="ACTIVE")["entities"]
        mta.bulk_create(response_location_1["shipto_id"], data, repeat=3, failed=True)
        transactions_after_re_request = ta.get_transaction(shipto_id=response_location_1["shipto_id"], status="ACTIVE")["entities"]

        assert len(transactions_after_re_request) == len(transactions), "Transactions already exist in Active status"

    @pytest.mark.parametrize("conditions", [
        {
            "status": "ORDERED",
            "testrail_case_id": 2190
        },
        {
            "status": "SHIPPED",
            "testrail_case_id": 2192
        },
        {
            "status": "QUOTED",
            "testrail_case_id": 2193
        }
    ])
    @pytest.mark.regression
    def test_bulk_create_for_exist_transactions_in_different_status(self, mobile_api, conditions, delete_shipto):
        mobile_api.testrail_case_id = conditions["testrail_case_id"]
        mta = MobileTransactionApi(mobile_api)
        ta = TransactionApi(mobile_api)

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
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

        mta.bulk_create(response_location_1["shipto_id"], data)

        transactions_in_active = ta.get_transaction(shipto_id=response_location_1["shipto_id"], status="ACTIVE")["entities"]

        ta.update_replenishment_item(transactions_in_active[0]["id"], response_location_1['product']['roundBuy']*3, conditions["status"])
        ta.update_replenishment_item(transactions_in_active[1]["id"], response_location_2['product']['roundBuy']*3, conditions["status"])

        transactions_after_update = ta.get_transaction(shipto_id=response_location_1["shipto_id"])["entities"]

        assert transactions_after_update[0]["status"] == conditions["status"], f"Status of {transactions_after_update[0]['productPartSku']} should be equal condition status"
        assert transactions_after_update[1]["status"] == conditions["status"], f"Status of {transactions_after_update[1]['productPartSku']} should be equal condition status"

        mta.bulk_create(response_location_1["shipto_id"], data)
        transactions_in_active = ta.get_transaction(shipto_id=response_location_1["shipto_id"], status="ACTIVE")["entities"]

        assert transactions_in_active[0]["reorderQuantity"] == 0, f"Reorder quantity of {transactions_in_active[0]['productPartSku']} should be equal to 0"
        assert transactions_in_active[1]["reorderQuantity"] == 0, f"Reorder quantity of {transactions_in_active[1]['productPartSku']} should be equal to 0"

        transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"])["entities"]

        assert len(transactions) == 4, "There are should be 4 transactions in the given ShipTo "

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
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
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
