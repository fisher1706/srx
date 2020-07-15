import pytest
import random
from src.api.setups.setup_location import setup_location
from src.api.setups.setup_put_away import setup_put_away
from src.api.distributor.transaction_api import TransactionApi
from src.api.distributor.location_api import LocationApi
from src.api.distributor.put_away_api import PutAwayApi
from src.resources.locator import Locator
from src.resources.tools import Tools

class TestPutAway():
    @pytest.mark.regression
    @pytest.mark.t
    def test_put_away_for_existing_transaction(self, api, delete_shipto):
        api.testrail_case_id = 2039

        ta = TransactionApi(api)
        pa = PutAwayApi(api)

        response_put_away = setup_put_away(api)

        put_away_dto = {

            "shipToId": response_put_away["shipto_id"],
            "partSku": response_put_away["product"],
            "transactionId": response_put_away["transaction_id"],
            "quantity": response_put_away["reorderQuantity"]
        }

        pa.put_away([put_away_dto])
        transaction = ta.get_transaction(sku=response_put_away["product"], shipto_id=response_put_away["shipto_id"])
        status = transaction["entities"][0]["status"]
        assert f"{status}" == "DELIVERED", f"Transaction for SKU {response_put_away['product']} should be in status DELIVERED, but status is {status}"


