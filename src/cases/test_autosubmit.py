import pytest
import copy
from src.api.setups.setup_location import setup_location
from src.api.setups.setup_shipto import setup_shipto
from src.api.distributor.location_api import LocationApi
from src.api.distributor.settings_api import SettingsApi
from src.api.distributor.transaction_api import TransactionApi

class TestAutosubmit():
    @pytest.mark.regression
    def test_location_of_serialized_product(self, api, delete_shipto):
        api.testrail_case_id = 2046

        la = LocationApi(api)
        sa = SettingsApi(api)
        ta = TransactionApi(api)

        response_shipto = setup_shipto(api)
        shipto_id = response_shipto["shipto_id"]
        sa.set_autosubmit_settings_shipto(shipto_id=shipto_id, enabled=True, immediately=True, as_order=True)
        sa.set_checkout_software_settings_for_shipto(shipto_id=shipto_id)
        response_location = setup_location(api, shipto_id=shipto_id, is_autosubmit=True)

        ta.create_active_item(shipto_id, la.get_ordering_config_by_sku(shipto_id, response_location["product"]["partSku"]))
        transactions = ta.get_transaction(shipto_id=shipto_id)


        assert transactions["totalElements"] == 1, "Only 1 transaction should be created"
        assert transactions["entities"][0]["productPartSku"] == response_location["product"]["partSku"]
        assert transactions["entities"][0]["status"] == "ORDERED", f"Transaction should be in 'ORDERED' status, now '{transactions['entities'][0]['status']}'"

        