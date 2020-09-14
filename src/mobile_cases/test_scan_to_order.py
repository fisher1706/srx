from src.api.mobile.mobile_transaction_api import MobileTransactionApi
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

        url = "https://api-staging.storeroomlogix.com/distributor-portal/distributor/replenishments/list/items?status=ACTIVE"
        token = mta.get_distributor_token()

        response = mta.send_get(url, token)
        list_active_transaction = response.json()['data']['entities']
        list_active_transaction_sku = []
        for sku in list_active_transaction:
            list_active_transaction_sku.append(sku['product']['partSku'])
        
        assert response_location_1["product"]["partSku"] in list_active_transaction_sku and response_location_2["product"]["partSku"] in list_active_transaction_sku , "Transactions not created"
         