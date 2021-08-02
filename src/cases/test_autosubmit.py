import copy
import pytest
from src.api.mobile.mobile_transaction_api import MobileTransactionApi
from src.api.setups.setup_location import SetupLocation
from src.api.distributor.location_api import LocationApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.distributor.settings_api import SettingsApi

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
def test_immediately_autosubmit_by_create_active_item(api, conditions, delete_shipto):
    api.testrail_case_id = conditions["testrail_case_id"]

    la = LocationApi(api)
    ta = TransactionApi(api)

    setup_location = SetupLocation(api)
    setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True})
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
def test_autosubmit_when_create_location(api, delete_shipto, conditions):
    api.testrail_case_id = conditions["testrail_case_id"]

    la = LocationApi(api)

    setup_location = SetupLocation(api)
    setup_location.setup_shipto.add_option("autosubmit_settings", {"enabled": conditions["shipto"]})
    setup_location.add_option("autosubmit", conditions["location"])
    response_location = setup_location.setup()

    locations = la.get_locations(response_location["shipto_id"])

    assert locations[0]["autoSubmit"] == conditions["result"], f"Auto-Submit location flag should be equal to '{conditions['result']}', now: '{locations[0]['autoSubmit']}'"

@pytest.mark.regression
def test_cannot_disable_location_autosabmit_if_enabled_for_shipto(api, delete_shipto):
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
def test_update_location_when_update_shipto(api, delete_shipto, conditions):
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
def test_immediately_autosubmit_for_reorder_control_transaction(api, delete_shipto):
    api.testrail_case_id = 2059

    la = LocationApi(api)
    ta = TransactionApi(api)

    setup_location = SetupLocation(api)
    setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
    setup_location.setup_shipto.add_option("autosubmit_settings", {"enabled": True, "immediately": True, "as_order": True})
    setup_location.setup_product.add_option("issue_quantity", 1)
    setup_location.add_option("autosubmit")
    response_location = setup_location.setup()

    location = la.get_locations(shipto_id=response_location["shipto_id"])[0]
    location["onHandInventory"] = response_location["location"]["orderingConfig"]["currentInventoryControls"]["min"]*0.5
    la.update_location([location], response_location["shipto_id"])
    transaction = ta.get_transaction(shipto_id=response_location["shipto_id"])["entities"]
    assert transaction[0]["status"] == "ORDERED"

@pytest.mark.regression
def test_same_order_id_after_bulk_create_with_autosubmit_immediately(api, delete_shipto):
    api.testrail_case_id = 6995

    ta = TransactionApi(api)
    mta = MobileTransactionApi(api)

    setup_location = SetupLocation(api)
    setup_location.setup_shipto.add_option("reorder_controls_settings", {"scan_to_order": True})
    setup_location.setup_shipto.add_option("autosubmit_settings", {"enabled": True, "immediately": True, "as_order": False})
    setup_location.add_option("autosubmit")
    response_location_1 = setup_location.setup()

    setup_location = SetupLocation(api)
    setup_location.add_option("shipto_id", response_location_1["shipto_id"])
    setup_location.add_option("autosubmit")
    response_location_2 = setup_location.setup()

    data = [
        {
            "partSku": response_location_1["product"]["partSku"],
            "quantity": response_location_1["product"]["roundBuy"]
        },
        {
            "partSku": response_location_2["product"]["partSku"],
            "quantity": response_location_2["product"]["roundBuy"]
        }
    ]

    mta.bulk_create(response_location_1["shipto_id"], data, status="QUOTED")
    transactions = ta.get_transaction(shipto_id=response_location_1["shipto_id"])["entities"]

    assert len(transactions) == 2, "The number of transactions should be equal to 2"
    order_id = f"SIQTE-{response_location_1['shipto']['number']}-{min(transactions[0]['id'], transactions[1]['id'])}-001"
    assert transactions[0]["orderId"] == transactions[1]["orderId"] == order_id, "Incorrect Order ID"
