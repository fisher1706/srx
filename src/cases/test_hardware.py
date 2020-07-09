import pytest
from src.api.distributor.distributor_hardware_api import DistributorHardwareApi
from src.api.admin.admin_hardware_api import AdminHardwareApi
from src.api.distributor.location_api import LocationApi
from src.api.distributor.shipto_api import ShiptoApi
from src.api.setups.setup_locker_location import setup_locker_location
from src.api.setups.setup_locker import setup_locker
from src.pages.admin.hardware_page import HardwarePage
from src.pages.general.login_page import LoginPage

class TestHardware():
    @pytest.mark.smoke
    def test_smoke_get_device_list(self, smoke_api):
        smoke_api.testrail_case_id = 2003

        ha = DistributorHardwareApi(smoke_api)
        response = ha.get_device_list()
        count = len(response)
        assert count != 0, "Device list is empty"

    @pytest.mark.regression
    def test_delete_location_by_change_doortype(self, api, delete_shipto, delete_hardware):
        api.testrail_case_id = 1852

        sa = ShiptoApi(api)
        ha = AdminHardwareApi(api)
        la = LocationApi(api)

        response_location = setup_locker_location(api)
        original_location_count = len(la.get_locations(response_location["shipto_id"]))
        assert original_location_count == 1, "The number of location should be 1"
        ha.update_locker_configuration(response_location["locker"]["id"], True)
        new_location_count = len(la.get_locations(response_location["shipto_id"]))
        assert new_location_count == 0, "The number of location should be 0"

    @pytest.mark.regression
    def test_change_locker_doortype(self, ui, delete_hardware):
        ui.testrail_case_id = 1851

        lp = LoginPage(ui)
        hp = HardwarePage(ui)
        ha = AdminHardwareApi(ui)

        response_locker = setup_locker(ui)
        locker_body = response_locker["locker"]
        iothub_body = response_locker["iothub"]

        lp.log_in_admin_portal()
        hp.sidebar_hardware()
        hp.check_last_hardware(serial_number=locker_body["value"], device_type="LOCKER", iothub=str(iothub_body["id"]), device_subtype=locker_body["lockerType"]["name"])
        doors_data = hp.configure_locker_door()
        hp.check_locker_door(doors_data)

    @pytest.mark.regression
    def test_common_set_of_hubs_for_locker_and_vending(self, ui, delete_hardware):
        ui.testrail_case_id = 1839

        lp = LoginPage(ui)
        hp = HardwarePage(ui)
        ha = AdminHardwareApi(ui)

        lp.log_in_admin_portal()

        iothub_dto = ha.create_iothub() #create IoT Hub via rest api
        iothub_name = f"{iothub_dto['id']} ({iothub_dto['value']}) / {ui.data.distributor_name}"
        
        hp.sidebar_hardware()
        hp.wait_until_page_loaded()
        hp.iothub_should_be_available("Locker", iothub_name)
        hp.iothub_should_be_available("Vending", iothub_name)
        hp.iothub_should_be_available("IP Camera", iothub_name)

        locker_serial_number = hp.create_locker(ui.data.distributor_name, iothub_name) #create locker
        hp.check_last_hardware(device_type="LOCKER", distributor=ui.data.distributor_name)

        hp.iothub_should_not_be_available("Locker", iothub_name)
        hp.iothub_should_not_be_available("Vending", iothub_name)
        hp.iothub_should_be_available("IP Camera", iothub_name)

        hp.remove_last_hardware("LOCKER") #remove locker

        hp.iothub_should_be_available("Locker", iothub_name)
        hp.iothub_should_be_available("Vending", iothub_name)
        hp.iothub_should_be_available("IP Camera", iothub_name)

        locker_serial_number = hp.create_vending(ui.data.distributor_name, iothub_name) #create vending
        hp.check_last_hardware(device_type="VENDING", distributor=ui.data.distributor_name)

        hp.iothub_should_not_be_available("Locker", iothub_name)
        hp.iothub_should_not_be_available("Vending", iothub_name)
        hp.iothub_should_be_available("IP Camera", iothub_name)

        hp.remove_last_hardware("VENDING") #remove vending

        hp.iothub_should_be_available("Locker", iothub_name)
        hp.iothub_should_be_available("Vending", iothub_name)
        hp.iothub_should_be_available("IP Camera", iothub_name)

    @pytest.mark.regression
    @pytest.mark.t
    def test_iothub_crud(self, ui):
        ui.testrail_case_id = 32

        lp = LoginPage(ui)
        hp = HardwarePage(ui)

        lp.log_in_admin_portal()
        hp.sidebar_hardware()
        serial_number = hp.create_iothub(ui.data.distributor_name)
        hp.check_last_hardware(serial_number=serial_number, device_type="IOTHUB", distributor=ui.data.distributor_name)
        hp.update_last_iothub(ui.data.sub_distributor_name)
        hp.check_last_hardware(serial_number=serial_number, device_type="IOTHUB", distributor=ui.data.sub_distributor_name)
        hp.remove_last_hardware("IOTHUB")

