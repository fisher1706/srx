import pytest
import copy
import time
from src.resources.tools import Tools
from src.api.setups.setup_location import SetupLocation
from src.api.distributor.location_api import LocationApi
from src.api.distributor.serial_number_api import SerialNumberApi

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

    @pytest.mark.regression
    def test_serialized_ohi_decreased_when_available_in_issued(self, api, delete_shipto):
        api.testrail_case_id = 2111

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
        sn_dto["status"] = "ISSUED"
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "ISSUED"

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["onHandInventory"] == 0

    @pytest.mark.regression
    def test_serialized_ohi_decreased_when_available_in_expired(self, api, delete_shipto):
        api.testrail_case_id = 2112

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
        sn_dto["dateExpiration"] = time.time()*1000
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "EXPIRED"

        locations = la.get_locations(response_location["shipto_id"])
        assert locations[0]["onHandInventory"] == 0

    @pytest.mark.regression
    def test_cannot_update_sn_available_to_assigned(self, api, delete_shipto):
        api.testrail_case_id = 2113

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

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "AVAILABLE"
        sn_dto["status"] = "ASSIGNED"
        sna.update_serial_number(sn_dto)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "AVAILABLE"

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
    def test_create_sn_in_expired_status(self, api, delete_shipto):
        api.testrail_case_id = 2140

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sn = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn, additional_options={"dateExpiration":time.time()*1000})

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["status"] == "EXPIRED"

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
    def test_cannot_create_serial_number_with_lot_if_lot_turned_off_for_location(self, api, delete_shipto):
        api.testrail_case_id = 2142

        setup_location = SetupLocation(api)
        setup_location.add_option("serialized")
        response_location = setup_location.setup()

        sna = SerialNumberApi(api)
        sn = Tools.random_string_u()
        lot = Tools.random_string_u()
        sn_id = sna.create_serial_number(response_location["location_id"], response_location["shipto_id"], sn, lot=lot)

        sn_dto = sna.get_serial_number(shipto_id=response_location["shipto_id"])[0]
        assert sn_dto["number"] == sn
        assert sn_dto.get("lot") == None