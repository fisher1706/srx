from src.api.mobile.mobile_transaction_api import MobileTransactionApi
import pytest


class TestScanToOrder():
    @pytest.mark.regression1
    def test_bulk_create_transaction(self, api):
        data = [
            {
                "partSku": "PINEAPPLE",
                "quantity": 20
            },
            {
                "partSku": "TOMATO 1",
                "quantity": 20
            }
        ]
        mta = MobileTransactionApi(api)
        mta.bulk_create(31, 54, data)
