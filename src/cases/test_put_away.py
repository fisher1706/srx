import pytest
import random
from src.api.setups.setup_location import setup_location
from src.api.setups.setup_put_away import setup_put_away
from src.api.setups.setup_shipto import setup_shipto
from src.api.distributor.transaction_api import TransactionApi
from src.api.distributor.location_api import LocationApi
from src.api.distributor.put_away_api import PutAwayApi
from src.api.distributor.shipto_api import ShiptoApi
from src.resources.locator import Locator
from src.resources.tools import Tools

class TestPutAway():
    @pytest.mark.regression
    def test_put_away_for_existing_transaction(self, api, delete_shipto):
        api.testrail_case_id = 2039

        ta = TransactionApi(api)
        pa = PutAwayApi(api)

        response_put_away = setup_put_away(api, transaction=True)

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
    
    @pytest.mark.regression
    def test_put_away_by_SKU(self, api, delete_shipto):
        api.testrail_case_id = 2040

        ta = TransactionApi(api)
        pa = PutAwayApi(api)
        la = LocationApi(api)

        response_put_away = setup_put_away(api)
        location = la.get_location_by_sku(response_put_away["shipto_id"], response_put_away["product"])[0]

        put_away_dto = {

            "shipToId": response_put_away["shipto_id"],
            "partSku": response_put_away["product"],
            "quantity": location["orderingConfig"]["currentInventoryControls"]["max"]
        }

        pa.put_away([put_away_dto])
        transaction = ta.get_transaction(sku=response_put_away["product"], shipto_id=response_put_away["shipto_id"])
        status = transaction["entities"][0]["status"]
        assert f"{status}" == "DELIVERED", f"Transaction for SKU {response_put_away['product']} should be in status DELIVERED, but status is {status}"

    @pytest.mark.regression
    def test_put_away_by_nonexistent_SKU(self, api, delete_shipto):
        api.testrail_case_id = 2041

        pa = PutAwayApi(api)
        ta = TransactionApi(api)

        shipto_response = setup_shipto(api)
        shipto_id = shipto_response["shipto_id"]

        put_away_dto = {
            "shipToId": shipto_id,
            "partSku": Tools.random_string_l(20),
            "quantity": 777
        }

        pa.put_away([put_away_dto])
        transaction_count = ta.get_transaction(shipto_id)["totalElements"]
        assert transaction_count == 0, f"There should be 0 transactions for shipto {shipto_response['shipto']['number']}"

    @pytest.mark.regression
    def test_put_away_for_several_transactions_same_SKU(self, api, delete_shipto):
        api.testrail_case_id = 2042

        ta = TransactionApi(api)
        pa = PutAwayApi(api)
        la = LocationApi(api)

        response_put_away = setup_put_away(api, transaction=True)
        ordering_config_id = la.get_ordering_config_by_sku(response_put_away["shipto_id"], response_put_away["product"])
        ta.create_active_item(response_put_away["shipto_id"], ordering_config_id)
        transaction_2 = ta.get_transaction(sku=response_put_away["product"], shipto_id=response_put_away["shipto_id"])
        tarnsaction_2_id = transaction_2["entities"][0]["id"]
        ta.update_replenishment_item(tarnsaction_2_id, response_put_away["reorderQuantity"], "SHIPPED")

        put_away_dto = {
            "shipToId": response_put_away["shipto_id"],
            "partSku": response_put_away["product"],
            "quantity": response_put_away["reorderQuantity"]
        }

        pa.put_away([put_away_dto])
        transaction = ta.get_transaction(sku=response_put_away["product"], shipto_id=response_put_away["shipto_id"])
        print(transaction["entities"][0]["updatedAt"])
        print(transaction["entities"][1]["updatedAt"])
        # assert f"{status}" == "DELIVERED", f"Transaction for SKU {response_put_away['product']} should be in status DELIVERED, but status is {status}"


