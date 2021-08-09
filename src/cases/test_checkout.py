import pytest
from src.api.checkout.checkout_api import CheckoutApi
from src.api.customer.checkout_group_api import CheckoutGroupApi
from src.api.setups.setup_location import SetupLocation
from src.api.distributor.location_api import LocationApi
from src.api.customer.customer_user_api import CustomerUserApi

@pytest.mark.parametrize("conditions", [
    {
        "issue_product": True,
        "return_product":None,
        "action": "ISSUE",
        "testrail_case_id": 4550
    },
    {
        "issue_product": None,
        "return_product":True,
        "action": "RETURN",
        "testrail_case_id": 4551
    }
    ])
@pytest.mark.regression
def test_label_transactions(api, conditions, delete_shipto):

    api.testrail_case_id = conditions["testrail_case_id"]

    la = LocationApi(api)
    ca = CheckoutApi(api)
    cua = CustomerUserApi(api)

    setup_location = SetupLocation(api)
    setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
    setup_location.add_option("ohi", "MAX")
    setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
    response_location = setup_location.setup()
    shipto_id = response_location["shipto_id"]
    product = response_location["product"]["partSku"]
    location_response = la.get_location_by_sku(shipto_id, product)
    location = location_response[0]
    location_type = location_response[0]["orderingConfig"]["type"]

    ca.checkout_add_to_cartv2(location, location_type, quantity=1, issue_product=conditions["issue_product"], \
    return_product=conditions["return_product"], passcode=None, action=conditions["action"])
    assert  ca.get_cartv2(passcode=None)["status"] == "OPEN"

    cart_id_list = ca.get_cartv2(passcode=None)["items"]
    for item in cart_id_list:
        ca.checkout_close_cart(location, cart_id=item['id'], actual_quantity=1, planned_quantity=1, passcode=None, action=conditions["action"])

    assert  ca.get_cartv2(passcode=None)["status"] == "CLOSED"

    transaction = cua.get_customer_user_transactions()[0]
    assert transaction["hardwareType"] == "LABEL"
    assert transaction["transactionType"] == conditions["action"]
    assert transaction["partSku"] == product
    expected_discrepancy_status = False
    assert transaction["discrepancy"] == expected_discrepancy_status
    assert transaction["oldOnHandInventory"] == location["onHandInventory"]
    if conditions["issue_product"] is None:
        assert transaction["onHandInventory"] == location["onHandInventory"]+1
    else:
        assert transaction["onHandInventory"] == location["onHandInventory"]-1

@pytest.mark.parametrize("conditions", [
    {
        "issue_product": True,
        "return_product":None,
        "action": "ISSUE",
        "testrail_case_id": 4552
    },
    {
        "issue_product": None,
        "return_product":True,
        "action": "RETURN",
        "testrail_case_id": 4553
    }
    ])
@pytest.mark.regression
def test_label_transactions_checkout_group(api, conditions, delete_shipto):

    api.testrail_case_id = conditions["testrail_case_id"]

    la = LocationApi(api)
    ca = CheckoutApi(api)
    cha = CheckoutGroupApi(api)
    cua = CustomerUserApi(api)

    setup_location = SetupLocation(api)
    setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
    setup_location.add_option("ohi", "MAX")
    setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
    response_location = setup_location.setup()

    shipto_id = response_location["shipto_id"]
    product = response_location["product"]["partSku"]
    location_response = la.get_location_by_sku(shipto_id, product)
    location = location_response[0]
    location_type = location_response[0]["orderingConfig"]["type"]

    cha.add_shipto_to_checkout_group(shipto_id=shipto_id)

    ca.checkout_add_to_cartv2(location, location_type, quantity=1, issue_product=conditions["issue_product"], \
    return_product=conditions["return_product"], passcode=api.data.passcode, action=conditions["action"])
    assert  ca.get_cartv2(passcode=api.data.passcode)["status"] == "OPEN"

    cart_id_list = ca.get_cartv2(passcode=api.data.passcode)["items"]
    for item in cart_id_list:
        ca.checkout_close_cart(location, cart_id=item['id'], actual_quantity=1, planned_quantity=1, passcode=api.data.passcode, action=conditions["action"])
    assert  ca.get_cartv2(passcode=api.data.passcode)["status"] == "CLOSED"

    transaction = cua.get_customer_user_transactions()[0]
    assert transaction["hardwareType"] == "LABEL"
    assert transaction["transactionType"] == conditions["action"]
    assert transaction["partSku"] == product
    expected_discrepancy_status = False
    assert transaction["discrepancy"] == expected_discrepancy_status
    assert transaction["oldOnHandInventory"] == location["onHandInventory"]
    if conditions["issue_product"] is None:
        assert transaction["onHandInventory"] == location["onHandInventory"]+1
    else:
        assert transaction["onHandInventory"] == location["onHandInventory"]-1

@pytest.mark.regression
def test_label_issue_with_discrepancy_status(api, delete_shipto):

    api.testrail_case_id = 4586

    la = LocationApi(api)
    ca = CheckoutApi(api)
    cua = CustomerUserApi(api)

    setup_location = SetupLocation(api)
    setup_location.setup_shipto.add_option("reorder_controls_settings", "DEFAULT")
    setup_location.add_option("ohi", "MAX")
    setup_location.setup_shipto.add_option("checkout_settings", "DEFAULT")
    response_location = setup_location.setup()
    shipto_id = response_location["shipto_id"]
    product = response_location["product"]["partSku"]
    location_response = la.get_location_by_sku(shipto_id, product)
    location = location_response[0]
    location_type = location_response[0]["orderingConfig"]["type"]

    ca.checkout_add_to_cartv2(location, location_type, quantity=location["onHandInventory"]+1, issue_product=True, \
    return_product=None, passcode=None, action="ISSUE")
    assert  ca.get_cartv2(passcode=None)["status"] == "OPEN"

    cart_id_list = ca.get_cartv2(passcode=None)["items"]
    for item in cart_id_list:
        ca.checkout_close_cart(location, cart_id=item['id'], actual_quantity=location["onHandInventory"]+1, planned_quantity=location["onHandInventory"]+1, passcode=None, action="ISSUE")

    assert  ca.get_cartv2(passcode=None)["status"] == "CLOSED"

    transaction = cua.get_customer_user_transactions()[0]
    assert transaction["hardwareType"] == "LABEL"
    assert transaction["transactionType"] == "ISSUE"
    assert transaction["partSku"] == product
    expected_discrepancy_status = True
    assert transaction["discrepancy"] == expected_discrepancy_status
    assert transaction["oldOnHandInventory"] == location["onHandInventory"]
    assert transaction["onHandInventory"] == 0
