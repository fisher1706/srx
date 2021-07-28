import copy
import pytest
from src.resources.permissions import Permissions
from src.api.setups.setup_location import SetupLocation
from src.api.distributor.location_api import LocationApi
from src.resources.tools import Tools

@pytest.mark.parametrize("permissions", [
    {
        "user": None,
        "testrail_case_id": 2285
    },
    {
        "user": Permissions.mobile_buttons("ENABLE", True),
        "testrail_case_id": 2286
    }
])
@pytest.mark.acl
@pytest.mark.regression
def test_assign_dsn_to_button(mobile_api, permission_api, permissions, delete_shipto, delete_distributor_security_group):
    mobile_api.testrail_case_id = permissions["testrail_case_id"]
    context = Permissions.set_configured_user(mobile_api, permissions["user"], permission_context=permission_api)
    la = LocationApi(context)

    setup_location = SetupLocation(mobile_api)
    setup_location.add_option("type", "BUTTON")
    response_location = setup_location.setup()
    dsn = Tools.random_string_u()

    la.get_location_by_sku(response_location["shipto_id"], response_location["product"]["partSku"], mobile=True)
    location_dto = copy.deepcopy(response_location["location"])
    location_dto["id"] = response_location["location_id"]
    location_dto["orderingConfig"]["dsn"] = dsn
    location_list = [copy.deepcopy(location_dto)]
    la.update_location(location_list, response_location["shipto_id"], mobile=True)

    locations = la.get_locations(response_location["shipto_id"], mobile=True)
    assert locations[0]["orderingConfig"]["dsn"] == dsn, f"Button DSN should be {dsn}, but it is {locations[0]['orderingConfig']['dsn']}"


@pytest.mark.acl
@pytest.mark.regression
def test_assign_dsn_to_button_without_permissions(mobile_api, permission_api, delete_shipto, delete_distributor_security_group):
    mobile_api.testrail_case_id = 2287
    Permissions.set_configured_user(mobile_api, Permissions.mobile_buttons("ENABLE", False))
    la = LocationApi(permission_api)

    setup_location = SetupLocation(mobile_api)
    setup_location.add_option("type", "BUTTON")
    response_location = setup_location.setup()
    dsn = Tools.random_string_u()

    la.get_location_by_sku(response_location["shipto_id"], response_location["product"]["partSku"], expected_status_code=400, mobile=True)

    location_dto = copy.deepcopy(response_location["location"])
    location_dto["id"] = response_location["location_id"]
    location_dto["orderingConfig"]["dsn"] = dsn
    location_list = [copy.deepcopy(location_dto)]
    la.update_location(location_list, response_location["shipto_id"], expected_status_code=400, mobile=True)

    locations = LocationApi(mobile_api).get_locations(response_location["shipto_id"], mobile=True)
    assert locations[0]["orderingConfig"]["dsn"] is None, f"Button DSN should be empty, but it is {locations[0]['orderingConfig']['dsn']}"


@pytest.mark.parametrize("permissions", [
    {
        "user": None,
        "testrail_case_id": 2289
    },
    {
        "user": Permissions.mobile_buttons("ENABLE", True),
        "testrail_case_id": 2290
    }
])
@pytest.mark.acl
@pytest.mark.regression
def test_unassign_dsn_from_button(mobile_api, permission_api, permissions, delete_shipto, delete_distributor_security_group):
    mobile_api.testrail_case_id = permissions["testrail_case_id"]
    context = Permissions.set_configured_user(mobile_api, permissions["user"], permission_context=permission_api)
    la = LocationApi(context)

    dsn = Tools.random_string_u()
    setup_location = SetupLocation(mobile_api)
    setup_location.add_option("type", "BUTTON")
    setup_location.add_option("dsn", dsn)
    response_location = setup_location.setup()

    location_dto = copy.deepcopy(response_location["location"])
    location_dto["id"] = response_location["location_id"]
    location_dto["orderingConfig"]["dsn"] = None
    location_list = [copy.deepcopy(location_dto)]
    la.update_location(location_list, response_location["shipto_id"], mobile=True)

    locations = LocationApi(mobile_api).get_locations(response_location["shipto_id"], mobile=True)
    assert locations[0]["orderingConfig"]["dsn"] is None, f"Button DSN should be empty, but it is {locations[0]['orderingConfig']['dsn']}"


@pytest.mark.acl
@pytest.mark.regression
def test_unassign_dsn_from_button_without_permissions(mobile_api, permission_api, delete_shipto, delete_distributor_security_group):
    mobile_api.testrail_case_id = 2291
    Permissions.set_configured_user(mobile_api, Permissions.mobile_buttons("ENABLE", False))
    la = LocationApi(permission_api)

    dsn = Tools.random_string_u()
    setup_location = SetupLocation(mobile_api)
    setup_location.add_option("type", "BUTTON")
    setup_location.add_option("dsn", dsn)
    response_location = setup_location.setup()
    locations = LocationApi(mobile_api).get_locations(response_location["shipto_id"], mobile=True)

    location_dto = copy.deepcopy(response_location["location"])
    location_dto["id"] = response_location["location_id"]
    location_dto["orderingConfig"]["dsn"] = None
    location_list = [copy.deepcopy(location_dto)]
    la.update_location(location_list, response_location["shipto_id"], expected_status_code=400, mobile=True)

    locations = LocationApi(mobile_api).get_locations(response_location["shipto_id"], mobile=True)
    assert locations[0]["orderingConfig"]["dsn"] is not None, "Button DSN should Not be empty"
