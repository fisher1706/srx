import pytest
import copy
import time
from src.resources.tools import Tools
from src.resources.permissions import Permissions
from src.api.setups.setup_location import SetupLocation
from src.api.distributor.location_api import LocationApi
from src.api.distributor.serial_number_api import SerialNumberApi
from src.api.distributor.product_api import ProductApi
from src.pages.general.login_page import LoginPage
from src.pages.distributor.serialization_page import SerializationPage

@pytest.mark.regression
def test_cannot_create_sn_for_not_serialized_location(api, delete_shipto):
    api.testrail_case_id = 2105

    response_location = SetupLocation(api).setup()
    sna = SerialNumberApi(api)

    sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], Tools.random_string_u(), expected_status_code=400)

@pytest.mark.regression
def test_cannot_create_2_same_SNs(api, delete_shipto):
    api.testrail_case_id = 2117
    
    setup_location = SetupLocation(api)
    setup_location.add_option("serialized")
    setup_location.setup_product.add_option("round_buy", 1)
    response_location_1 = setup_location.setup()

    setup_location.add_option("product", response_location_1["product"])
    response_location_2 = setup_location.setup()

    sna = SerialNumberApi(api)
    sn = Tools.random_string_u()

    sna.create_serial_number(response_location_1["location_id"], response_location_1["shipto_id"], sn)
    sna.create_serial_number(response_location_2["location_id"], response_location_2["shipto_id"], sn, expected_status_code=400)

@pytest.mark.regression
def test_ohi_serialized_location_equal_to_sn_in_available_status(api, delete_shipto):
    api.testrail_case_id = 2106

    setup_location = SetupLocation(api)
    setup_location.add_option("serialized")
    setup_location.setup_product.add_option("round_buy", 1)
    response_location = setup_location.setup()

    sna = SerialNumberApi(api)
    la = LocationApi(api)
    sn = Tools.random_string_u()
    sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)

    locations = la.get_locations(response_location["shipto_id"])
    assert locations[0]["onHandInventory"] == 0, "Serialized location should be created with OHI = 0"

    sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
    sn_dto["status"] = "AVAILABLE"
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
    assert sn_dto["status"] == "AVAILABLE"

    locations = la.get_locations(response_location["shipto_id"])
    assert locations[0]["onHandInventory"] == 1

@pytest.mark.regression
def test_ohi_serialized_product_location_equal_to_sn_in_available_status(api, delete_shipto):
    api.testrail_case_id = 2109

    setup_location = SetupLocation(api)
    setup_location.setup_product.add_option("serialized")
    setup_location.setup_product.add_option("round_buy", 1)
    response_location = setup_location.setup()

    sna = SerialNumberApi(api)
    la = LocationApi(api)
    sn = Tools.random_string_u()
    sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)

    locations = la.get_locations(response_location["shipto_id"])
    assert locations[0]["onHandInventory"] == 0, "Serialized location should be created with OHI = 0"

    sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
    sn_dto["status"] = "AVAILABLE"
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
    assert sn_dto["status"] == "AVAILABLE"

    locations = la.get_locations(response_location["shipto_id"])
    assert locations[0]["onHandInventory"] == 1

@pytest.mark.regression
def test_ohi_serialized_location_is_not_reseted_when_update_product(api, delete_shipto):
    api.testrail_case_id = 2145

    setup_location = SetupLocation(api)
    setup_location.setup_product.add_option("serialized")
    setup_location.setup_product.add_option("round_buy", 1)
    response_location = setup_location.setup()

    sna = SerialNumberApi(api)
    la = LocationApi(api)
    pa = ProductApi(api)
    sn = Tools.random_string_u()
    sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)

    locations = la.get_locations(response_location["shipto_id"])
    assert locations[0]["onHandInventory"] == 0, "Serialized location should be created with OHI = 0"

    sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
    sn_dto["status"] = "AVAILABLE"
    sna.update_serial_number(sn_dto)

    locations = la.get_locations(response_location["shipto_id"])
    assert locations[0]["onHandInventory"] == 1

    product_dto = response_location["product"]
    product_id = product_dto.pop("id")
    product_dto["image"] = sn
    pa.update_product(product_dto, product_id)

    locations = la.get_locations(response_location["shipto_id"])
    assert locations[0]["onHandInventory"] == 1

@pytest.mark.regression
def test_sn_created_in_assigned_status_for_serialized_location(api, delete_shipto):
    api.testrail_case_id = 2108

    setup_location = SetupLocation(api)
    setup_location.add_option("serialized")
    setup_location.setup_product.add_option("round_buy", 1)
    response_location = setup_location.setup()

    sna = SerialNumberApi(api)
    sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], Tools.random_string_u())

    sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"

@pytest.mark.regression
def test_sn_created_in_assigned_status_for_serialized_product_location(api, delete_shipto):
    api.testrail_case_id = 2110

    setup_location = SetupLocation(api)
    setup_location.setup_product.add_option("serialized")
    setup_location.setup_product.add_option("round_buy", 1)
    response_location = setup_location.setup()

    sna = SerialNumberApi(api)
    sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], Tools.random_string_u())

    sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
    assert sn_dto["status"] == "ASSIGNED"

@pytest.mark.parametrize("conditions", [
    {
        "status": "ISSUED",
        "testrail_case_id": 2111
    },
    {
        "status": "DISPOSED",
        "testrail_case_id": 2189
    }
    ])
@pytest.mark.regression
def test_serialized_ohi_decreased_when_available_in_issued(api, conditions, delete_shipto):
    api.testrail_case_id = conditions["testrail_case_id"]

    setup_location = SetupLocation(api)
    setup_location.add_option("serialized")
    setup_location.setup_product.add_option("round_buy", 1)
    response_location = setup_location.setup()

    sna = SerialNumberApi(api)
    la = LocationApi(api)
    sn = Tools.random_string_u()
    sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)

    locations = la.get_locations(response_location["shipto_id"])
    sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
    sn_dto["status"] = "AVAILABLE"
    sna.update_serial_number(sn_dto)
    locations = la.get_locations(response_location["shipto_id"])
    assert locations[0]["onHandInventory"] == 1

    sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
    sn_dto["status"] = conditions["status"]
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
    assert sn_dto["status"] == conditions["status"]

    locations = la.get_locations(response_location["shipto_id"])
    assert locations[0]["onHandInventory"] == 0

@pytest.mark.regression
def test_serialized_ohi_decreased_when_available_in_expired(api, delete_shipto):
    api.testrail_case_id = 2112

    setup_location = SetupLocation(api)
    setup_location.add_option("serialized")
    setup_location.setup_product.add_option("round_buy", 1)
    setup_location.setup_shipto.add_option("serialization_settings", "OFF")
    response_location = setup_location.setup()

    sna = SerialNumberApi(api)
    la = LocationApi(api)
    sn = Tools.random_string_u()
    sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)

    locations = la.get_locations(response_location["shipto_id"])
    sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
    sn_dto["status"] = "AVAILABLE"
    sna.update_serial_number(sn_dto)
    locations = la.get_locations(response_location["shipto_id"])
    assert locations[0]["onHandInventory"] == 1

    sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
    sn_dto["dateExpiration"] = time.time()*1000
    sna.update_serial_number(sn_dto)

    sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
    assert sn_dto["status"] == "EXPIRED"

    locations = la.get_locations(response_location["shipto_id"])
    assert locations[0]["onHandInventory"] == 0

@pytest.mark.regression
def test_delete_sn_when_delete_location(api, delete_shipto):
    api.testrail_case_id = 2114

    setup_location = SetupLocation(api)
    setup_location.add_option("serialized")
    setup_location.setup_product.add_option("round_buy", 1)
    response_location = setup_location.setup()

    sna = SerialNumberApi(api)
    la = LocationApi(api)
    sn = Tools.random_string_u()
    sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)
    serial_number_count = sna.get_serial_number_count(shipto_id=response_location["shipto_id"])
    assert serial_number_count == 1

    la.location_bulk_update("REMOVE_ALL", response_location["shipto_id"], ids=[response_location["location_id"]])
    time.sleep(5)
    serial_number_count = sna.get_serial_number_count(shipto_id=response_location["shipto_id"])
    assert serial_number_count == 0, "Serial Numbers should be deleted when you delete their location"

@pytest.mark.regression
def test_delete_sn_when_turn_off_serialization_for_location(api, delete_shipto):
    api.testrail_case_id = 2115

    setup_location = SetupLocation(api)
    setup_location.add_option("serialized")
    setup_location.setup_product.add_option("round_buy", 1)
    response_location = setup_location.setup()

    sna = SerialNumberApi(api)
    la = LocationApi(api)
    sn = Tools.random_string_u()
    sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)
    serial_number_count = sna.get_serial_number_count(shipto_id=response_location["shipto_id"])
    assert serial_number_count == 1

    location_dto = copy.deepcopy(response_location["location"])
    location_dto["id"] = response_location["location_id"]
    location_dto["serialized"] = False
    location_list = [copy.deepcopy(location_dto)]
    la.update_location(location_list, response_location["shipto_id"])

    serial_number_count = sna.get_serial_number_count(shipto_id=response_location["shipto_id"])
    assert serial_number_count == 0, "Serial Numbers should be deleted when you turn off serialization for their location"

@pytest.mark.regression
def test_create_serial_number_with_lot(api, delete_shipto):
    api.testrail_case_id = 2141

    setup_location = SetupLocation(api)
    setup_location.add_option("serialized")
    setup_location.add_option("lot")
    setup_location.setup_product.add_option("round_buy", 1)
    response_location = setup_location.setup()

    sna = SerialNumberApi(api)
    sn = Tools.random_string_u()
    lot = Tools.random_string_u()
    sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn, lot=lot)

    sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
    assert sn_dto["number"] == sn
    assert sn_dto["lot"] == lot

@pytest.mark.regression
def test_cannot_create_sn_with_lot_if_lot_turned_off_for_location(api, delete_shipto):
    api.testrail_case_id = 2142

    setup_location = SetupLocation(api)
    setup_location.add_option("serialized")
    setup_location.setup_product.add_option("round_buy", 1)
    response_location = setup_location.setup()

    sna = SerialNumberApi(api)
    sn = Tools.random_string_u()
    lot = Tools.random_string_u()
    sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn, lot=lot, expected_status_code=400)

@pytest.mark.parametrize("permissions", [
    {
        "user": None,
        "testrail_case_id": 2143
    },
    { 
        "user": Permissions.serialization("EDIT"),
        "testrail_case_id": 2256
    }
    ])
@pytest.mark.acl
@pytest.mark.regression
def test_serial_number_crud(ui, permission_ui, permissions, delete_shipto, delete_distributor_security_group):
    ui.testrail_case_id = permissions["testrail_case_id"]
    context = Permissions.set_configured_user(ui, permissions["user"], permission_context=permission_ui)

    lp = LoginPage(context)
    sp = SerializationPage(context)

    serial_number_body = sp.serial_number_body.copy()
    edit_serial_number_body = sp.serial_number_body.copy()

    #-------------------
    serial_number_body["number"] = Tools.random_string_u()
    serial_number_body["lot"] = Tools.random_string_u()
    #-------------------
    edit_serial_number_body["number"] = Tools.random_string_u()
    edit_serial_number_body["lot"] = Tools.random_string_u()
    edit_serial_number_body["dateManufacture"] = "08/01/2020"
    edit_serial_number_body["dateShipment"] = "08/02/2020"
    edit_serial_number_body["dateExpiration"] = "08/01/2025"
    edit_serial_number_body["dateWarrantyExpires"] = "08/02/2025"
    #-------------------

    setup_location = SetupLocation(ui)
    setup_location.add_option("serialized")
    setup_location.add_option("lot")
    setup_location.setup_product.add_option("round_buy", 1)
    response_location = setup_location.setup()

    shipto_text = f"{context.data.customer_name} - {response_location['shipto']['number']}"
    product_sku = response_location["product"]["partSku"]

    lp.log_in_distributor_portal()
    sp.sidebar_serialization()
    sp.select_shipto_sku(shipto_text, product_sku)

    ohi_path = "//div[text()='OHI']/../div[2]"

    sp.add_serial_number(serial_number_body)
    serial_number_body["status"] = "ASSIGNED"
    sp.check_last_serial_number(serial_number_body)
    assert sp.get_element_text(ohi_path) == "0"
    sp.update_last_serial_number(edit_serial_number_body)
    edit_serial_number_body["status"] = "ASSIGNED"
    sp.check_last_serial_number(edit_serial_number_body)
    sp.update_last_serial_number_status("AVAILABLE")
    edit_serial_number_body["status"] = "AVAILABLE"
    sp.check_last_serial_number(edit_serial_number_body)
    assert sp.get_element_text(ohi_path) == "1"
    sp.delete_last_serial_number(edit_serial_number_body["number"])
    assert sp.get_element_text(ohi_path) == "0"

@pytest.mark.acl
@pytest.mark.regression
def test_serial_number_crud_view_permission(api, permission_api, delete_distributor_security_group, delete_shipto):
    api.testrail_case_id = 2262

    Permissions.set_configured_user(api, Permissions.serialization("VIEW"))

    sna = SerialNumberApi(permission_api)

    setup_location = SetupLocation(api)
    setup_location.add_option("serialized")
    setup_location.setup_product.add_option("round_buy", 1)
    response_location = setup_location.setup()

    sn_failed = Tools.random_string_u()
    sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn_failed, expected_status_code=400) #cannot create Serial Number

    sn = Tools.random_string_u()
    sn_id = SerialNumberApi(api).create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)

    sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0] #can read Serial Number
    assert sn_dto["number"] == sn #--//--//--

    sna.update_serial_number(sn_dto, expected_status_code=400) #cannot update Serial Number
    sna.delete_serial_number(sn_id, expected_status_code=400) #cannot delete Serial Number

@pytest.mark.parametrize("permissions", [
    {
        "user": None,
        "testrail_case_id": 2257
    },
    { 
        "user": Permissions.serialization("EDIT"),
        "testrail_case_id": 2258
    }
    ])
@pytest.mark.acl
@pytest.mark.regression
def test_serial_number_import(ui, permission_ui, permissions, delete_shipto, delete_distributor_security_group):
    ui.testrail_case_id = permissions["testrail_case_id"]
    context = Permissions.set_configured_user(ui, permissions["user"], permission_context=permission_ui)

    lp = LoginPage(context)
    sp = SerializationPage(context)

    serial_number_body = sp.serial_number_body.copy()

    #-------------------
    serial_number_body["number"] = Tools.random_string_u()
    serial_number_body["lot"] = Tools.random_string_u()
    serial_number_body["dateManufacture"] = "08/01/2020"
    serial_number_body["dateShipment"] = "08/02/2020"
    serial_number_body["dateExpiration"] = "08/01/2025"
    serial_number_body["dateWarrantyExpires"] = "08/02/2025"
    #-------------------

    setup_location = SetupLocation(ui)
    setup_location.add_option("serialized")
    setup_location.add_option("lot")
    setup_location.setup_product.add_option("round_buy", 1)
    response_location = setup_location.setup()

    product_sku = response_location["product"]["partSku"]
    shipto_text = f"{context.data.customer_name} - {response_location['shipto']['number']}"

    serial_numbers = [
        [serial_number_body["number"], serial_number_body["lot"], product_sku, None, serial_number_body["dateShipment"], serial_number_body["dateManufacture"], serial_number_body["dateExpiration"], serial_number_body["dateWarrantyExpires"], None]
    ]

    lp.log_in_distributor_portal()
    sp.sidebar_serialization()
    sp.select_shipto_sku(shipto_text)

    sp.import_serial_numbers(serial_numbers)
    serial_number_body["status"] = "ASSIGNED"
    sp.select_shipto_sku(shipto_text, product_sku)
    sp.check_last_serial_number(serial_number_body)

@pytest.mark.regression
def test_serialized_ohi_decreased_when_delete_location(api, delete_shipto):
    api.testrail_case_id = 2144

    setup_location = SetupLocation(api)
    setup_location.add_option("serialized")
    setup_location.setup_product.add_option("round_buy", 1)
    response_location = setup_location.setup()

    sna = SerialNumberApi(api)
    la = LocationApi(api)
    sn = Tools.random_string_u()
    sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)

    locations = la.get_locations(response_location["shipto_id"])
    sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
    sn_dto["status"] = "AVAILABLE"
    sna.update_serial_number(sn_dto)
    locations = la.get_locations(response_location["shipto_id"])
    assert locations[0]["onHandInventory"] == 1

    sna.delete_serial_number(sn_id)

    locations = la.get_locations(response_location["shipto_id"])
    assert locations[0]["onHandInventory"] == 0

@pytest.mark.parametrize("permissions", [
    {
        "user": None,
        "testrail_case_id": 2259
    },
    { 
        "user": Permissions.serialization("EDIT"),
        "testrail_case_id": 2260
    }
    ])
@pytest.mark.acl
@pytest.mark.regression
def test_create_serial_numbers_by_lot(api, permission_api, permissions, delete_shipto, delete_distributor_security_group):
    api.testrail_case_id = permissions["testrail_case_id"]
    context = Permissions.set_configured_user(api, permissions["user"], permission_context=permission_api)

    setup_location = SetupLocation(api)
    setup_location.add_option("serialized")
    setup_location.add_option("lot")
    setup_location.setup_product.add_option("round_buy", 1)
    response_location = setup_location.setup()

    sna = SerialNumberApi(context)

    sn_dto = Tools.get_dto("lot_generate_dto.json")
    sn_dto["locationId"] = response_location["location_id"]
    sn_dto["lot"] = Tools.random_string_l()
    sn_dto["numberQuantity"] = 3

    sna.create_serial_numbers_by_lot(sn_dto)
    assert len(sna.get_serial_number(shipto_id=response_location["shipto_id"])) == 3