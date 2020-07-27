import pytest
import copy
from src.api.setups.setup_location import setup_location
from src.api.setups.setup_shipto import setup_shipto
from src.api.distributor.location_api import LocationApi
from src.api.distributor.settings_api import SettingsApi
from src.api.distributor.transaction_api import TransactionApi

class TestAutosubmit():
    @pytest.mark.parametrize("conditions", [
        {
            "as_order": False,
            "result": "QUOTED",
            "testrail_case_id": 2058
        },
        {
            "as_order": True,
            "result": "ORDERED",
            "testrail_case_id": 2046
        }
        ])
    @pytest.mark.regression
    def test_immediately_autosubmit_by_create_active_item(self, api, delete_shipto, conditions):
        api.testrail_case_id = conditions["testrail_case_id"]

        la = LocationApi(api)
        sa = SettingsApi(api)
        ta = TransactionApi(api)

        response_shipto = setup_shipto(api)
        shipto_id = response_shipto["shipto_id"]
        sa.set_autosubmit_settings_shipto(shipto_id=shipto_id, enabled=True, immediately=True, as_order=conditions["as_order"])
        sa.set_checkout_software_settings_for_shipto(shipto_id=shipto_id)
        response_location = setup_location(api, shipto_id=shipto_id, is_autosubmit=True)

        ta.create_active_item(shipto_id, la.get_ordering_config_by_sku(shipto_id, response_location["product"]["partSku"]))
        transactions = ta.get_transaction(shipto_id=shipto_id)

        assert transactions["totalElements"] == 1, "Only 1 transaction should be created"
        assert transactions["entities"][0]["productPartSku"] == response_location["product"]["partSku"]
        assert transactions["entities"][0]["status"] == conditions["result"], f"Transaction should be in '{conditions['result']}' status, now '{transactions['entities'][0]['status']}'"

    @pytest.mark.parametrize("conditions", [
        {
            "shipto": False,
            "location": None,
            "result": False,
            "testrail_case_id": 2055
        },
        {
            "shipto": True,
            "location": None,
            "result": True,
            "testrail_case_id": 2056
        },
        {
            "shipto": True,
            "location": False,
            "result": True,
            "testrail_case_id": 2065
        },
        {
            "shipto": False,
            "location": True,
            "result": True,
            "testrail_case_id": 2066
        }
        ])
    @pytest.mark.regression
    def test_autosubmit_when_create_location(self, api, delete_shipto, conditions):
        api.testrail_case_id = conditions["testrail_case_id"]

        la = LocationApi(api)
        sa = SettingsApi(api)

        response_shipto = setup_shipto(api)
        shipto_id = response_shipto["shipto_id"]
        sa.set_autosubmit_settings_shipto(shipto_id=shipto_id, enabled=conditions["shipto"])
        response_location = setup_location(api, shipto_id=shipto_id, is_autosubmit=conditions["location"])

        locations = la.get_locations(shipto_id)

        assert locations[0]["autoSubmit"] == conditions["result"], f"Auto-Submit location flag should be equal to '{conditions['result']}', now: '{locations[0]['autoSubmit']}'"

    @pytest.mark.regression
    def test_cannot_disable_location_autosabmit_if_enabled_for_shipto(self, api, delete_shipto):
        api.testrail_case_id = 2057

        la = LocationApi(api)
        sa = SettingsApi(api)

        response_shipto = setup_shipto(api)
        shipto_id = response_shipto["shipto_id"]
        sa.set_autosubmit_settings_shipto(shipto_id=shipto_id, enabled=True)
        response_location = setup_location(api, shipto_id=shipto_id)

        locations = la.get_locations(shipto_id)

        assert locations[0]["autoSubmit"] == True, "Auto_submit flag of the location should be TRUE"

        location_id = la.get_location_by_sku(response_location["shipto_id"], response_location["product"]["partSku"])[0]["id"]
        location_dto = copy.deepcopy(response_location["location"])
        location_dto["id"] = location_id
        location_dto["autoSubmit"] = False
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"])

        assert locations[0]["autoSubmit"] == True, "Auto_submit flag of the location should be TRUE"

    @pytest.mark.parametrize("conditions", [
        {
            "shipto": False,
            "testrail_case_id": 2060
        },
        {
            "shipto": True,
            "testrail_case_id": 2061
        }
        ])
    @pytest.mark.regression
    def test_update_location_when_update_shipto(self, api, delete_shipto, conditions):
        api.testrail_case_id = conditions["testrail_case_id"]

        la = LocationApi(api)
        sa = SettingsApi(api)

        response_shipto = setup_shipto(api)
        shipto_id = response_shipto["shipto_id"]
        sa.set_autosubmit_settings_shipto(shipto_id=shipto_id, enabled=conditions["shipto"])
        response_location = setup_location(api, shipto_id=shipto_id)
        locations = la.get_locations(shipto_id)

        assert locations[0]["autoSubmit"] == conditions["shipto"], f"Auto_submit flag of the location should be {conditions['shipto']}"

        sa.set_autosubmit_settings_shipto(shipto_id=shipto_id, enabled=bool(not conditions["shipto"]))
        locations = la.get_locations(shipto_id)

        assert locations[0]["autoSubmit"] == bool(not conditions["shipto"]), f"Auto_submit flag of the location should be {bool(not conditions['shipto'])}"