from src.api.mobile.mobile_transaction_api import MobileTransactionApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.setups.setup_location import SetupLocation
from src.api.setups.setup_product import SetupProduct
import pytest


class TestScanToOrder():
    @pytest.mark.regression
    def test_bulk_create_transaction(self, mobile_api, delete_shipto):
        mobile_api.testrail_case_id = 2215
        mta = MobileTransactionApi(mobile_api)
        ta = TransactionApi(mobile_api)

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
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

        transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"],status="ACTIVE")["entities"]

        assert len(transactions) == 2, "There should be 2 transactions"
        assert transactions[0]["product"]["partSku"] == response_location_1["product"]["partSku"], f"Sku of product should be equal to {response_location_1['product']['partSku']}"
        assert transactions[0]["reorderQuantity"] == (response_location_1["product"]["roundBuy"]*3), f"Reorder quantity of transaction should be equal to {response_location_1['product']['roundBuy']*3}"
        assert transactions[1]["product"]["partSku"] == response_location_2["product"]["partSku"], f"Sku of product should be equal to {response_location_2['product']['partSku']}"
        assert transactions[1]["reorderQuantity"] == (response_location_2["product"]["roundBuy"]*3), f"Reorder quantity of transaction should be equal to {response_location_2['product']['roundBuy']*3}"

    @pytest.mark.regression
    def test_bulk_create_transaction_for_non_exist_sku(self, mobile_api, delete_shipto):
        mobile_api.testrail_case_id = 2179
        mta = MobileTransactionApi(mobile_api)
        ta = TransactionApi(mobile_api)


        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
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

        mta.bulk_create(response_location_1["shipto_id"], data, repeat=2, failed=True)

        transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"],status="ACTIVE")["entities"]

        assert len(transactions) == 0, "There should be 0 transactions, SKU's don't exist in the given ShipTo"

    @pytest.mark.regression
    def test_bulk_create_transaction_with_zero_quantity(self, mobile_api, delete_shipto):
        mobile_api.testrail_case_id = 2180
        mta = MobileTransactionApi(mobile_api)
        ta = TransactionApi(mobile_api)

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
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

        mta.bulk_create(response_location_1["shipto_id"], data, repeat=2, failed=True)

        transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"],status="ACTIVE")["entities"]

        assert len(transactions) == 0, "There should be 0 transactions, the Quantity parameters are missing."

    @pytest.mark.regression
    def test_bulk_create_transaction_with_asset_flag(self, mobile_api, delete_shipto):
        mobile_api.testrail_case_id = 2186
        mta = MobileTransactionApi(mobile_api)
        ta = TransactionApi(mobile_api)

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
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

        mta.bulk_create(response_location_1["shipto_id"], data, repeat=2, failed=True)

        transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"],status="ACTIVE")["entities"]

        assert len(transactions) == 0, "There should be 0 transactions, products cannot be ordered, these products with asset flag"

    @pytest.mark.regression
    def test_bulk_create_for_exist_transactions_in_active(self, mobile_api, delete_shipto):
        mobile_api.testrail_case_id = 2188
        mta = MobileTransactionApi(mobile_api)
        ta = TransactionApi(mobile_api)

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
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

        transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"],status="ACTIVE")["entities"]
        mta.bulk_create(response_location_1["shipto_id"], data, failed = True)
        transactions_after_re_request = ta.get_transaction(shipto_id=response_location_1["shipto_id"],status="ACTIVE")["entities"]
        
        assert len(transactions_after_re_request) == len(transactions), "Transactions already exist in Active status"

    @pytest.mark.regression
    def test_bulk_create_for_exist_transactions_in_ordered(self, mobile_api, delete_shipto):
        mobile_api.testrail_case_id = 2190
        mta = MobileTransactionApi(mobile_api)
        ta = TransactionApi(mobile_api)

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
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

        transactions_in_active = ta.get_transaction(shipto_id=response_location_1["shipto_id"],status="ACTIVE")["entities"]

        ta.update_replenishment_item(transactions_in_active[0]["id"],response_location_1['product']['roundBuy']*3,"ORDERED")
        ta.update_replenishment_item(transactions_in_active[1]["id"],response_location_2['product']['roundBuy']*3,"ORDERED")

        transactions_after_update = ta.get_transaction(shipto_id=response_location_1["shipto_id"])["entities"]

        assert transactions_after_update[0]["status"] == "ORDERED" and transactions_after_update[1]["status"] == "ORDERED", "Status of each transaction should be ORDERED"
        
        mta.bulk_create(response_location_1["shipto_id"], data)
        transactions_in_active = ta.get_transaction(shipto_id=response_location_1["shipto_id"],status="ACTIVE")["entities"]

        assert transactions_in_active[0]["reorderQuantity"] == 0 and transactions_in_active[1]["reorderQuantity"] == 0, "Reorder quantity of each transactions should be equal to 0"

        transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"])["entities"]

        assert len(transactions) == 4 , "There are should be 4 transactions in the given ShipTo "
    
    @pytest.mark.regression
    def test_bulk_create_for_exist_transactions_in_shipped(self, mobile_api, delete_shipto):
        mobile_api.testrail_case_id = 2192
        mta = MobileTransactionApi(mobile_api)
        ta = TransactionApi(mobile_api)

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
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

        transactions_in_active = ta.get_transaction(shipto_id=response_location_1["shipto_id"],status="ACTIVE")["entities"]

        ta.update_replenishment_item(transactions_in_active[0]["id"],response_location_1['product']['roundBuy']*3,"SHIPPED")
        ta.update_replenishment_item(transactions_in_active[1]["id"],response_location_2['product']['roundBuy']*3,"SHIPPED")

        transactions_after_update = ta.get_transaction(shipto_id=response_location_1["shipto_id"])["entities"]

        assert transactions_after_update[0]["status"] == "SHIPPED" and transactions_after_update[1]["status"] == "SHIPPED", "Status of each transaction should be SHIPPED"
        
        mta.bulk_create(response_location_1["shipto_id"], data)
        transactions_in_active = ta.get_transaction(shipto_id=response_location_1["shipto_id"],status="ACTIVE")["entities"]

        assert transactions_in_active[0]["reorderQuantity"] == 0 and transactions_in_active[1]["reorderQuantity"] == 0, "Reorder quantity of each transactions should be equal to 0"

        transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"])["entities"]

        assert len(transactions) == 4 , "There are should be 4 transactions in the given ShipTo "

    @pytest.mark.regression
    def test_bulk_create_for_exist_transactions_in_quoted(self, mobile_api, delete_shipto):
        mobile_api.testrail_case_id = 2193
        mta = MobileTransactionApi(mobile_api)
        ta = TransactionApi(mobile_api)

        setup_location = SetupLocation(mobile_api)
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
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

        transactions_in_active = ta.get_transaction(shipto_id=response_location_1["shipto_id"],status="ACTIVE")["entities"]

        ta.update_replenishment_item(transactions_in_active[0]["id"],response_location_1['product']['roundBuy']*3,"QUOTED")
        ta.update_replenishment_item(transactions_in_active[1]["id"],response_location_2['product']['roundBuy']*3,"QUOTED")

        transactions_after_update = ta.get_transaction(shipto_id=response_location_1["shipto_id"])["entities"]

        assert transactions_after_update[0]["status"] == "QUOTED" and transactions_after_update[1]["status"] == "QUOTED", "Status of each transaction should be QUOTED"
        
        mta.bulk_create(response_location_1["shipto_id"], data)
        transactions_in_active = ta.get_transaction(shipto_id=response_location_1["shipto_id"],status="ACTIVE")["entities"]

        assert transactions_in_active[0]["reorderQuantity"] == 0 and transactions_in_active[1]["reorderQuantity"] == 0, "Reorder quantity of each transactions should be equal to 0"

        transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"])["entities"]

        assert len(transactions) == 4 , "There are should be 4 transactions in the given ShipTo "
   













