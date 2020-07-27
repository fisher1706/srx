import pytest
import random
from src.api.setups.setup_location import setup_location
from src.api.setups.setup_put_away import setup_put_away
from src.api.setups.setup_shipto import setup_shipto
from src.api.distributor.transaction_api import TransactionApi
from src.api.distributor.location_api import LocationApi
from src.api.distributor.put_away_api import PutAwayApi
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.settings_api import SettingsApi
from src.resources.locator import Locator
from src.resources.tools import Tools
import time

class TestPutAway():
    @pytest.mark.regression
    def test_put_away_for_existing_transaction(self, api, delete_shipto):
        api.testrail_case_id = 2039

        ta = TransactionApi(api)
        pa = PutAwayApi(api)

        response_put_away = setup_put_away(api, transaction=True)
        transaction_id = response_put_away["transaction_id"]
        del response_put_away["transaction_id"]
        pa.put_away([response_put_away])
        transaction = ta.get_transaction(sku=response_put_away["partSku"], shipto_id=response_put_away["shipToId"])
        status = transaction["entities"][0]["status"]
        assert transaction_id == transaction["entities"][0]["id"], f"Existing transaction should be moved to DELIVERED"
        assert f"{status}" == "DELIVERED", f"Transaction for SKU {response_put_away['partSku']} should be in status DELIVERED, but status is {status}"
    
    @pytest.mark.regression
    def test_put_away_by_SKU(self, api, delete_shipto):
        api.testrail_case_id = 2040

        ta = TransactionApi(api)
        pa = PutAwayApi(api)

        response_put_away = setup_put_away(api)

        pa.put_away([response_put_away])
        transaction = ta.get_transaction(sku=response_put_away["partSku"], shipto_id=response_put_away["shipToId"])
        status = transaction["entities"][0]["status"]
        assert f"{status}" == "DELIVERED", f"Transaction for SKU {response_put_away['partSku']} should be in status DELIVERED, but status is {status}"

    @pytest.mark.regression
    def test_put_away_by_nonexistent_SKU(self, api, delete_shipto):
        api.testrail_case_id = 2041

        pa = PutAwayApi(api)
        ta = TransactionApi(api)

        shipto_response = setup_shipto(api)
        shipToId = shipto_response["shipto_id"]

        put_away_dto = {
            "shipToId": shipToId,
            "partSku": Tools.random_string_l(20),
            "quantity": 777
        }

        pa.put_away([put_away_dto])
        transaction_count = ta.get_transaction(shipToId)["totalElements"]
        assert transaction_count == 0, f"There should be 0 transactions for shipto {shipto_response['shipto']['number']}"

    @pytest.mark.regression
    def test_put_away_for_several_transactions_same_SKU(self, api, delete_shipto):
        api.testrail_case_id = 2042

        ta = TransactionApi(api)
        pa = PutAwayApi(api)
        la = LocationApi(api)
        sa = SettingsApi(api)

        response_put_away = setup_put_away(api, transaction=True)
        sa.set_checkout_software_settings_for_shipto(response_put_away["shipToId"], enable_reorder_control=False)
        ordering_config_id = la.get_ordering_config_by_sku(response_put_away["shipToId"], response_put_away["partSku"])
        ta.create_active_item(response_put_away["shipToId"], ordering_config_id)
        transaction_2 = ta.get_transaction(sku=response_put_away["partSku"], shipto_id=response_put_away["shipToId"])
        tarnsaction_2_id = transaction_2["entities"][1]["id"]
        ta.update_replenishment_item(tarnsaction_2_id, response_put_away["quantity"], "ORDERED")

        pa.put_away([response_put_away])
        transactions = ta.get_transaction(sku=response_put_away["partSku"], shipto_id=response_put_away["shipToId"])
        status_1 = transactions["entities"][0]["status"]
        status_2 = transactions["entities"][1]["status"]
        assert f"{status_1}" == "DELIVERED", f"First transaction for SKU {response_put_away['partSku']} should be in status DELIVERED, but status is {status}"
        assert f"{status_2}" == "ORDERED", f"Second transaction for SKU {response_put_away['partSku']} should be in status ORDERED, but status is {status}"

    @pytest.mark.regression
    def test_bulk_put_away(self, api, delete_shipto):
        api.testrail_case_id = 2043

        ta = TransactionApi(api)
        pa = PutAwayApi(api)
        la = LocationApi(api)

        response_put_away_1 = setup_put_away(api, transaction=True)
        response_put_away_2 = setup_put_away(api, transaction=True, shipto_id=response_put_away_1["shipToId"])

        pa.put_away([response_put_away_1, response_put_away_2])

        transactions = ta.get_transaction(shipto_id=response_put_away_1["shipToId"])
        status_1 = transactions["entities"][0]["status"]
        status_2 = transactions["entities"][1]["status"]
        assert f"{status_1}" == "DELIVERED", f"First transaction for SKU {response_put_away_1['partSku']} should be in status DELIVERED, but status is {status}"
        assert f"{status_2}" == "DELIVERED", f"Second transaction for SKU {response_put_away_2['partSku']} should be in status DELIVERED, but status is {status}"

    @pytest.mark.regression
    def test_put_away_qnty_0(self, api, delete_shipto):
        api.testrail_case_id = 2045

        ta = TransactionApi(api)
        pa = PutAwayApi(api)
        la = LocationApi(api)

        response_put_away = setup_put_away(api, transaction=True)
        response_put_away["quantity"] = 0
        pa.put_away([response_put_away])
        transaction = ta.get_transaction(sku=response_put_away["partSku"], shipto_id=response_put_away["shipToId"])
        status = transaction["entities"][0]["status"]
        assert f"{status}" == "DO_NOT_REORDER", f"Transaction for SKU {response_put_away['partSku']} should be in status DO_NOT_REORDER, but status is {status}"

    @pytest.mark.regression
    def test_put_away_asset(self, api, delete_shipto):
        api.testrail_case_id = 2048

        ta = TransactionApi(api)
        pa = PutAwayApi(api)

        # create location with asset product
        response_put_away = setup_put_away(api, is_asset=True)

        pa.put_away([response_put_away])
        transaction = ta.get_transaction(sku=response_put_away["partSku"], shipto_id=response_put_away["shipToId"])
        assert transaction["totalElements"]==0, f"There should not be transactions for asset product"

    @pytest.mark.regression
    def test_put_away_locker_location(self, api, delete_shipto, delete_hardware):
        api.testrail_case_id = 2062

        ta = TransactionApi(api)
        pa = PutAwayApi(api)

        response_put_away = setup_put_away(api, is_asset=True, trigger_type="LOCKER")
        pa.put_away([response_put_away])
        transaction = ta.get_transaction(sku=response_put_away["partSku"], shipto_id=response_put_away["shipToId"])
        assert transaction["totalElements"]==0, f"There should not be transactions for asset product"

    @pytest.mark.regression
    def test_put_away_active_transaction(self, api, delete_shipto):
        api.testrail_case_id = 2064

        ta = TransactionApi(api)
        pa = PutAwayApi(api)

        response_put_away = setup_put_away(api, transaction=True)
        ta.update_replenishment_item(response_put_away["transaction_id"], response_put_away["quantity"], "ACTIVE")
        pa.put_away([response_put_away])
        transaction = ta.get_transaction(sku=response_put_away["partSku"], shipto_id=response_put_away["shipToId"])
        print(transaction)
        assert transaction["totalElements"]==0, f"Put Away cant be performed for ACTIVE transaction"