import pytest
import random
from src.api.setups.setup_location import SetupLocation
from src.api.setups.setup_shipto import SetupShipto
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

        setup_location = SetupLocation(api)
        setup_location.add_option("transaction", "ORDERED")
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
        response_location = setup_location.setup()

        dto = response_location["put_away"]
        transaction_id = dto.pop("transactionId")
        pa.put_away([dto])
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"])
        status = transaction["entities"][0]["status"]
        assert f"{status}" == "DELIVERED", f"Transaction for SKU {response_location['product']['partSku']} should be in status DELIVERED, but status is {status}"
        assert transaction_id == transaction["entities"][0]["id"], f"Existing transaction should be moved to DELIVERED"

    @pytest.mark.regression
    def test_put_away_by_SKU(self, api, delete_shipto):
        api.testrail_case_id = 2040

        ta = TransactionApi(api)
        pa = PutAwayApi(api)

        setup_location = SetupLocation(api)
        response_location = setup_location.setup()

        dto = {
            "shipToId": response_location["shipto_id"],
            "partSku": response_location["product"]["partSku"]
        }
        pa.put_away([dto])
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"])
        status = transaction["entities"][0]["status"]
        assert f"{status}" == "DELIVERED", f"Transaction for SKU {response_location['product']['partSku']} should be in status DELIVERED, but status is {status}"

    @pytest.mark.regression
    def test_put_away_by_nonexistent_SKU(self, api, delete_shipto):
        api.testrail_case_id = 2041

        pa = PutAwayApi(api)
        ta = TransactionApi(api)

        setup_shipto = SetupShipto(api)
        response_shipto = setup_shipto.setup()
        shipto_id = response_shipto["shipto_id"]

        put_away_dto = {
            "shipToId": shipto_id,
            "partSku": Tools.random_string_l(20),
            "quantity": 777
        }

        pa.put_away([put_away_dto])
        transaction_count = ta.get_transaction(shipto_id)["totalElements"]
        assert transaction_count == 0, f"There should be 0 transactions for shipto {shipto_id}"

    @pytest.mark.regression
    def test_put_away_for_several_transactions_same_SKU(self, api, delete_shipto):
        api.testrail_case_id = 2042

        ta = TransactionApi(api)
        pa = PutAwayApi(api)
        la = LocationApi(api)
        sa = SettingsApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("transaction", "ORDERED")
        setup_location.setup_shipto.add_option("checkout_settings", {"enable_reorder_control": False})
        response_location = setup_location.setup()

        ordering_config_id = la.get_ordering_config_by_sku(response_location["shipto_id"], response_location["product"]["partSku"])
        ta.create_active_item(response_location["shipto_id"], ordering_config_id)
        transaction_2 = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"])
        tarnsaction_2_id = transaction_2["entities"][-1]["id"]
        ta.update_replenishment_item(tarnsaction_2_id, response_location["put_away"]["quantity"], "ORDERED")

        dto = response_location["put_away"]
        pa.put_away([dto])
        transactions = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"])
        status_1 = transactions["entities"][0]["status"]
        status_2 = transactions["entities"][1]["status"]
        assert f"{status_1}" == "DELIVERED", f"First transaction for SKU {response_location['product']['partSku']} should be in status DELIVERED, but status is {status}"
        assert f"{status_2}" == "ORDERED", f"Second transaction for SKU {response_location['product']['partSku']} should be in status ORDERED, but status is {status}"

    @pytest.mark.regression
    def test_bulk_put_away(self, api, delete_shipto):
        api.testrail_case_id = 2043

        ta = TransactionApi(api)
        pa = PutAwayApi(api)
        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("transaction", "ORDERED")
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
        response_location = setup_location.setup()

        setup_location.add_option("shipto_id", response_location["shipto_id"])
        setup_location.add_option("transaction", "ORDERED")
        response_location_2 = setup_location.setup()

        pa.put_away([response_location["put_away"], response_location_2["put_away"]])

        transactions = ta.get_transaction(shipto_id=response_location["shipto_id"])
        status_1 = transactions["entities"][0]["status"]
        status_2 = transactions["entities"][1]["status"]
        assert f"{status_1}" == "DELIVERED", f"First transaction for SKU {response_location['product']['partSku']} should be in status DELIVERED, but status is {status}"
        assert f"{status_2}" == "DELIVERED", f"Second transaction for SKU {response_location_2['product']['partSku']} should be in status DELIVERED, but status is {status}"

    @pytest.mark.regression
    def test_put_away_qnty_0(self, api, delete_shipto):
        api.testrail_case_id = 2045

        ta = TransactionApi(api)
        pa = PutAwayApi(api)
        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("transaction", "ORDERED")
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
        response_location = setup_location.setup()

        dto = response_location["put_away"]
        dto["quantity"] = 0
        pa.put_away([dto])
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"])
        status = transaction["entities"][0]["status"]
        assert f"{status}" == "DO_NOT_REORDER", f"Transaction for SKU {response_location['product']['partSku']} should be in status DO_NOT_REORDER, but status is {status}"

    @pytest.mark.regression
    def test_put_away_asset(self, api, delete_shipto):
        api.testrail_case_id = 2048

        ta = TransactionApi(api)
        pa = PutAwayApi(api)

        # create location with asset product
        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("asset")
        response_location = setup_location.setup()

        dto = {
            "shipToId": response_location["shipto_id"],
            "partSku": response_location["product"]["partSku"]
        }
        pa.put_away([dto])
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"])
        assert transaction["totalElements"] == 0, f"There should not be transactions for asset product"

    @pytest.mark.regression
    def test_bulk_put_away_locker_location(self, api, delete_shipto, delete_hardware):
        api.testrail_case_id = 2062

        ta = TransactionApi(api)
        pa = PutAwayApi(api)

        setup_location = SetupLocation(api)
        setup_location.add_option("locker_location")
        response_location = setup_location.setup()

        dto = {
            "shipToId": response_location["shipto_id"],
            "partSku": response_location["product"]["partSku"]
        }
        pa.put_away([dto])

        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"])
        assert transaction["totalElements"] == 0, f"There should not be transactions for asset product"

    @pytest.mark.regression
    def test_put_away_active_transaction(self, api, delete_shipto):
        api.testrail_case_id = 2064

        ta = TransactionApi(api)
        pa = PutAwayApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
        setup_location.add_option("transaction", "ACTIVE")
        response_location = setup_location.setup()

        dto = response_location["put_away"]
        pa.put_away([dto])

        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"])
        assert transaction["totalElements"] == 1, f"There should be only 1 transaction for {response_location['product']['partSku']}"
        status = transaction["entities"][-1]["status"]
        assert f"{status}" == "ACTIVE", f"Transaction for SKU {response_location['product']['partSku']} should be in status ACTIVE, but status is {status}"

    @pytest.mark.regression
    def test_put_away_by_SKU_and_unmatched_transaction(self, api, delete_shipto):
        api.testrail_case_id = 2077

        ta = TransactionApi(api)
        pa = PutAwayApi(api)

        invalid_transaction_id = 999999
        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
        setup_location.add_option("transaction", "ORDERED")
        response_location = setup_location.setup()

        dto = response_location["put_away"]
        dto["transactionId"] = invalid_transaction_id
        pa.put_away([dto])
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"])
        status = transaction["entities"][-1]["status"]
        assert f"{status}" == "ORDERED", f"Transaction for SKU {response_location['product']['partSku']} should be in status QUOTED, but status is {status}"

    @pytest.mark.regression
    def test_put_away_by_nonexistent_transaction(self, api, delete_shipto):
        api.testrail_case_id = 2078

        ta = TransactionApi(api)
        pa = PutAwayApi(api)

        invalid_transaction_id = 999999
        setup_location = SetupLocation(api)
        response_location = setup_location.setup()

        dto = {
            "shipToId": response_location["shipto_id"],
            "partSku": response_location["product"]["partSku"],
            "transactionId": invalid_transaction_id
        }
        pa.put_away([dto])
        transaction = ta.get_transaction(sku=response_location["product"]["partSku"], shipto_id=response_location["shipto_id"])
        assert transaction["totalElements"] == 0, f"There should not be transaction for {response_location['product']['partSku']}"