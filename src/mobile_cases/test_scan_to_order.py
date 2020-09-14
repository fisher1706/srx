from src.api.mobile.mobile_transaction_api import MobileTransactionApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.setups.setup_location import SetupLocation
import pytest
import json


class TestScanToOrder():
    @pytest.mark.regression
    def test_bulk_create_transaction(self, mobile_api, delete_shipto):
        mobile_api.testrail_case_id = 2215

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

        mta = MobileTransactionApi(mobile_api)
        mta.bulk_create(response_location_1["shipto_id"], data)

        ta = TransactionApi(mobile_api)
        transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"],status="ACTIVE")["entities"]

        assert len(transactions) == 2, "There should be 2 transactions"
        assert transactions[0]["product"]["partSku"] == response_location_1["product"]["partSku"], f"Sku of product should be equal to {response_location_1['product']['partSku']}"
        assert transactions[0]["reorderQuantity"] == (response_location_1["product"]["roundBuy"]*3), f"Reorder quantity of transaction should be equal to {response_location_1['product']['roundBuy']*3}"
        assert transactions[1]["product"]["partSku"] == response_location_2["product"]["partSku"], f"Sku of product should be equal to {response_location_2['product']['partSku']}"
        assert transactions[1]["reorderQuantity"] == (response_location_2["product"]["roundBuy"]*3), f"Reorder quantity of transaction should be equal to {response_location_2['product']['roundBuy']*3}"