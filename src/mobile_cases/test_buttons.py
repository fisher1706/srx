from src.resources.permissions import Permissions
from src.api.setups.setup_location import SetupLocation
from src.api.distributor.location_api import LocationApi
from src.resources.tools import Tools
import pytest
import copy

class TestButtons():
    @pytest.mark.parametrize("permissions", [
        {
            "user": None,
            "testrail_case_id": None
        },
        { 
            "user": Permissions.mobile_buttons("ENABLE", True),
            "testrail_case_id": None
        }
        ])
    @pytest.mark.regression
    def test_assign_dsn_to_button(self, mobile_api, permission_api, permissions, delete_shipto):
        #ui.testrail_case_id = permissions["testrail_case_id"]
        context = Permissions.set_configured_user(mobile_api, permissions["user"], permission_context=permission_api)
        la = LocationApi(context)

        setup_location = SetupLocation(mobile_api)
        setup_location.add_option("type", "BUTTON")
        response_location = setup_location.setup()
        dsn = Tools.random_string_u()

        location_id = la.get_location_by_sku(response_location["shipto_id"], response_location["product"]["partSku"], mobile=True)[0]["id"]
        location_dto = copy.deepcopy(response_location["location"])
        location_dto["id"] = location_id
        location_dto["orderingConfig"]["dsn"] = dsn
        location_list = [copy.deepcopy(location_dto)]
        la.update_location(location_list, response_location["shipto_id"], mobile=True)

        locations = la.get_locations(response_location["shipto_id"], mobile=True)
        assert locations[0]["orderingConfig"]["dsn"] == dsn, f"Button DSN should be {dsn}, but it is {locations[0]['orderingConfig']['dsn']}"
