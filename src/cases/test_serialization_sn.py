import pytest
import copy
import time
from src.resources.tools import Tools
from src.api.setups.setup_location import SetupLocation
from src.api.distributor.location_api import LocationApi
from src.api.distributor.serial_number_api import SerialNumberApi
from src.api.distributor.product_api import ProductApi
from src.pages.general.login_page import LoginPage
from src.pages.distributor.serialization_page import SerializationPage

class TestSerializationSN():
    @pytest.mark.regression
    def test_cannot_create_sn_for_not_serialized_location(self, api, delete_shipto):
        api.testrail_case_id = 2105

        response_location = SetupLocation(api).setup()
        sna = SerialNumberApi(api)

        sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], Tools.random_string_u(), expected_status_code=400)

    @pytest.mark.regression
    def test_cannot_create_2_same_SNs(self, api, delete_shipto):
        api.testrail_case_id = 2117
        
        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        response_location_1 = setup_location.setup()

        setup_location.add_option("product", response_location_1["product"])
        response_location_2 = setup_location.setup()

        sna = SerialNumberApi(api)
        sn = Tools.random_string_u()

        sna.create_serial_number(response_location_1["location_id"], response_location_1["shipto_id"], sn)
        sna.create_serial_number(response_location_2["location_id"], response_location_2["shipto_id"], sn, expected_status_code=400)

    @pytest.mark.regression
    def test_ohi_serialized_location_equal_to_sn_in_available_status(self, api, delete_shipto):
        api.testrail_case_id = 2106

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
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
    def test_ohi_serialized_product_location_equal_to_sn_in_available_status(self, api, delete_shipto):
        api.testrail_case_id = 2109

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("serialized")
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
    def test_ohi_serialized_location_is_not_reseted_when_update_product(self, api, delete_shipto):
        api.testrail_case_id = 2145

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("serialized")
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
    def test_sn_created_in_assigned_status_for_serialized_location(self, api, delete_shipto):
        api.testrail_case_id = 2108

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], Tools.random_string_u())

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ASSIGNED"

    @pytest.mark.regression
    def test_sn_created_in_assigned_status_for_serialized_product_location(self, api, delete_shipto):
        api.testrail_case_id = 2110

        setup_location = SetupLocation(api)
        setup_location.setup_product.add_option("serialized")
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
    def test_serialized_ohi_decreased_when_available_in_issued(self, api, conditions, delete_shipto):
        api.testrail_case_id = conditions["testrail_case_id"]

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
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
    def test_serialized_ohi_decreased_when_available_in_expired(self, api, delete_shipto):
        api.testrail_case_id = 2112

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
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
    def test_delete_sn_when_delete_location(self, api, delete_shipto):
        api.testrail_case_id = 2114

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        la = LocationApi(api)
        sn = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn)
        serial_number_count = sna.get_serial_number_count(shipto_id=response_location["shipto_id"])
        assert serial_number_count == 1

        la.location_bulk_update("REMOVE_ALL", response_location["shipto_id"], ids=[response_location["location_id"]])
        serial_number_count = sna.get_serial_number_count(shipto_id=response_location["shipto_id"])
        assert serial_number_count == 0, "Serial Numbers should be deleted when you delete their location"

    @pytest.mark.regression
    def test_delete_sn_when_turn_off_serialization_for_location(self, api, delete_shipto):
        api.testrail_case_id = 2115

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
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
    def test_create_serial_number_with_lot(self, api, delete_shipto):
        api.testrail_case_id = 2141

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        setup_location.add_option("lot")
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sn = Tools.random_string_u()
        lot = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn, lot=lot)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["number"] == sn
        assert sn_dto["lot"] == lot

    @pytest.mark.regression
    def test_cannot_create_sn_with_lot_if_lot_turned_off_for_location(self, api, delete_shipto):
        api.testrail_case_id = 2142

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sn = Tools.random_string_u()
        lot = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn, lot=lot, expected_status_code=400)

    @pytest.mark.regression
    def test_serial_number_crud(self, ui, delete_shipto):
        ui.testrail_case_id = 2143

        lp = LoginPage(ui)
        sp = SerializationPage(ui)

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
        response_location = setup_location.setup()

        shipto_text = f"{ui.data.customer_name} - {response_location['shipto']['number']}"
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

    @pytest.mark.regression
    def test_serialized_ohi_decreased_when_delete_location(self, api, delete_shipto):
        api.testrail_case_id = 2144

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
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