import pytest
import copy
from src.api.setups.setup_location import SetupLocation
from src.api.distributor.location_api import LocationApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.distributor.settings_api import SettingsApi

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
    def test_immediately_autosubmit_by_create_active_item(self, api, conditions, delete_shipto):
        api.testrail_case_id = conditions["testrail_case_id"]

        la = LocationApi(api)
        ta = TransactionApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
        setup_location.setup_shipto.add_option("autosubmit_settings", {"enabled": True, "immediately": True, "as_order": conditions["as_order"]})
        setup_location.add_option("autosubmit")
        response_location = setup_location.setup()

        shipto_id = response_location["shipto_id"]

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

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("autosubmit_settings", {"enabled": conditions["shipto"]})
        setup_location.add_option("autosubmit", conditions["location"])
        response_location = setup_location.setup()

        locations = la.get_locations(response_location["shipto_id"])

        assert locations[0]["autoSubmit"] == conditions["result"], f"Auto-Submit location flag should be equal to '{conditions['result']}', now: '{locations[0]['autoSubmit']}'"

    @pytest.mark.regression
    def test_cannot_disable_location_autosabmit_if_enabled_for_shipto(self, api, delete_shipto):
        api.testrail_case_id = 2057

        la = LocationApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("autosubmit_settings", {"enabled": True})
        response_location = setup_location.setup()

        locations = la.get_locations(response_location["shipto_id"])

        assert locations[0]["autoSubmit"], "Auto_submit flag of the location should be TRUE"

        location_id = la.get_location_by_sku(response_location["shipto_id"], response_location["product"]["partSku"])[0]["id"]
        location_dto = copy.deepcopy(response_location["location"])
        location_dto["id"] = location_id
        location_dto["autoSubmit"] = False
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"])

        assert locations[0]["autoSubmit"], "Auto_submit flag of the location should be TRUE"

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

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("autosubmit_settings", {"enabled": conditions["shipto"]})
        response_location = setup_location.setup()
        locations = la.get_locations(response_location["shipto_id"])

        assert locations[0]["autoSubmit"] == conditions["shipto"], f"Auto_submit flag of the location should be {conditions['shipto']}"

        sa.set_autosubmit_settings_shipto(shipto_id=response_location["shipto_id"], enabled=bool(not conditions["shipto"]))
        locations = la.get_locations(response_location["shipto_id"])

        assert locations[0]["autoSubmit"] == bool(not conditions["shipto"]), f"Auto_submit flag of the location should be {bool(not conditions['shipto'])}"

    @pytest.mark.regression
    def test_immediately_autosubmit_by_reorder_control_order(self, api, delete_shipto):
        api.testrail_case_id = 2059
        la = LocationApi(api)
        ta = TransactionApi(api)

        setup_location = SetupLocation(api)
        setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
        setup_location.setup_shipto.add_option("autosubmit_settings", {"enabled": True, "immediately": True, "as_order": True})
        setup_location.add_option("autosubmit")
        response_location = setup_location.setup()

        location_dto = copy.deepcopy(response_location["location"])
        location_dto["onHandInventory"] = response_location["location"]["orderingConfig"]["currentInventoryControls"]["min"]*0.5
        location_dto["id"] = response_location["location_id"]
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"])
        transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
        assert transaction[0]["status"]== "ORDERED"