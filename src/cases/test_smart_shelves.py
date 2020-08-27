import pytest
from src.api.admin.smart_shelves_api import SmartShelvesApi
from src.api.admin.admin_hardware_api import AdminHardwareApi
from src.api.distributor.shipto_api import ShiptoApi
from src.api.setups.setup_locker import SetupLocker
from src.api.setups.setup_shipto import SetupShipto
from src.pages.general.login_page import LoginPage
from src.pages.distributor.locker_planogram_page import LockerPlanogramPage
from src.pages.distributor.distributor_portal_smart_shelves_page import DistributorSmartShelvesPage
from src.pages.admin.smart_shelves_page import SmartShelvesPage
from src.pages.admin.hardware_page import HardwarePage
from src.resources.locator import Locator
from src.resources.tools import Tools
import random

class TestSmartShelves():
    @pytest.mark.regression
    def test_remove_locker_from_smart_shelf(self, api, delete_smart_shelf, delete_hardware):
        api.testrail_case_id = 1924

        ssa = SmartShelvesApi(api)
        ha = AdminHardwareApi(api)

        # create smart shelf for main distributor
        setup_locker = SetupLocker(api)
        setup_locker.add_option("smart_shelf")
        response_locker = setup_locker.setup()

        locker_body = response_locker["locker"]
        locker_id = response_locker["locker_id"]
        locker = locker_body["value"]
        iothub_body = response_locker["iothub"]

        ssa.update_smart_shelf(locker_body, locker_body_second=False)
        locker_conf = ha.get_locker_configuration(locker_id)
        assert (locker_conf[0]["smartShelfHardware"] == None), f"First locker should not have smart shelf with ID {response_locker['smart_shelf_id']}"

    @pytest.mark.regression
    def test_smart_shelves_change_door(self, api, delete_smart_shelf, delete_hardware):
        api.testrail_case_id = 1923

        ssa = SmartShelvesApi(api)
        ha = AdminHardwareApi(api)

        # create smart shelf for main distributor
        setup_locker = SetupLocker(api)
        setup_locker.add_option("smart_shelf")
        response_locker_1 = setup_locker.setup()

        locker_body = response_locker_1["locker"]
        locker_id = locker_body["id"]
        locker = locker_body["value"]
        iothub_body = response_locker_1["iothub"]

        # create second locker
        setup_locker = SetupLocker(api)
        setup_locker.add_option("smart_shelf", False)
        response_locker_2 = setup_locker.setup()

        locker_body_second = response_locker_2["locker"]
        locker_id_second = locker_body_second["id"]
        locker_second = locker_body_second["value"]
        iothub_body_second = response_locker_2["iothub"]

        ssa.update_smart_shelf(locker_body, locker_body_second=locker_body_second)
        locker_1_conf = ha.get_locker_configuration(locker_id)
        locker_2_conf = ha.get_locker_configuration(locker_id_second)
        assert (locker_1_conf[0]["smartShelfHardware"] == None), f"First locker should not have smart shelf with ID {response_locker_1['smart_shelf_id']}"
        assert (locker_2_conf[0]["smartShelfHardware"]["id"] == response_locker_1["smart_shelf_id"]), f"Second locker should have smart shelf with ID {response_locker_1['smart_shelf_id']}"

    @pytest.mark.regression
    def test_smart_shelves_delete_check_locker(self, api, delete_hardware):
        api.testrail_case_id = 1928

        ssa = SmartShelvesApi(api)
        ha = AdminHardwareApi(api)

        # create smart shelf for main distributor
        setup_locker = SetupLocker(api)
        setup_locker.add_option("smart_shelf")
        response_locker = setup_locker.setup()

        locker_body = response_locker["locker"]
        locker_id = locker_body["id"]
        locker = locker_body["value"]
        iothub_body = response_locker["iothub"]

        ssa.delete_smart_shelves(response_locker["smart_shelf_id"])
        locker_conf = ha.get_locker_configuration(locker_id)
        assert (locker_conf[0]["smartShelfHardware"] == None), f"First locker should not have smart shelf with ID {response_locker['smart_shelf_id']}"

    @pytest.mark.regression
    def test_planogram_assign_smart_shelf(self, ui, delete_shipto, delete_hardware, delete_smart_shelf):
        ui.testrail_case_id = 1965

        lp = LoginPage(ui)
        lpp = LockerPlanogramPage(ui)
        ssa = SmartShelvesApi(ui)

        #create shipto
        response_shipto = SetupShipto(ui).setup()

        # create smart shelf for main distributor
        setup_locker = SetupLocker(ui)
        setup_locker.add_option("smart_shelf")
        setup_locker.add_option("shipto_id", response_shipto["shipto_id"])
        response_locker = setup_locker.setup()

        locker_body = response_locker["locker"]
        locker = locker_body["value"]
        iothub_body = response_locker["iothub"]

        # remove locker from smart shelf
        ssa.update_smart_shelf(locker_body, locker_body_second=False)

        lp.log_in_distributor_portal()
        lpp.follow_locker_planogram_url(customer_id=locker_body["customerUser"] , shipto_id=response_shipto["shipto_id"])
        lpp.assign_smart_shelf_to_locker_door(response_locker["smart_shelf_number"])

    @pytest.mark.regression
    def test_planogram_merge_split_cells(self, ui, delete_shipto, delete_hardware, delete_smart_shelf):
        ui.testrail_case_id = 1970

        lp = LoginPage(ui)
        lpp = LockerPlanogramPage(ui)
        ssp = DistributorSmartShelvesPage(ui)

        #create shipto
        response_shipto = SetupShipto(ui).setup()

        # create smart shelf for main distributor
        setup_locker = SetupLocker(ui)
        setup_locker.add_option("smart_shelf")
        setup_locker.add_option("shipto_id", response_shipto["shipto_id"])
        response_locker = setup_locker.setup()
    
        locker_body = response_locker["locker"]
        locker = locker_body["value"]

        lp.log_in_distributor_portal()
        lpp.follow_locker_planogram_url(customer_id=locker_body["customerUser"] , shipto_id=response_shipto["shipto_id"])
        ssp.merge_cells(3, is_planogram=True, door_number=1)
        ssp.check_cells_number(2, is_planogram=True, door_number=1)
        ssp.split_cells(1, is_planogram=True, door_number=1)
        ssp.check_cells_number(4, is_planogram=True, door_number=1)

    @pytest.mark.regression
    def test_planogram_without_weights_assign_smart_shelf(self, ui, delete_shipto, delete_hardware, delete_smart_shelf):
        ui.testrail_case_id = 1968

        lp = LoginPage(ui)
        lpp = LockerPlanogramPage(ui)
        ha = AdminHardwareApi(ui)
        ssa = SmartShelvesApi(ui)

        #create shipto
        response_shipto = SetupShipto(ui).setup()

        # create smart shelf for main distributor
        setup_locker = SetupLocker(ui)
        setup_locker.add_option("smart_shelf")
        setup_locker.add_option("shipto_id", response_shipto["shipto_id"])
        response_locker = setup_locker.setup()

        locker_body = response_locker["locker"]
        locker = locker_body["value"]
        iothub_body = response_locker["iothub"]

        # remove locker from smart shelf
        ssa.update_smart_shelf(locker_body=locker_body, locker_body_second=False)

        # update locker door
        ha.update_locker_configuration(locker_body["id"], True)

        lp.log_in_distributor_portal()
        lpp.follow_locker_planogram_url(customer_id=locker_body["customerUser"] , shipto_id=response_shipto["shipto_id"])
        lpp.check_first_door_is_unavaliable_planogram()

    @pytest.mark.regression
    def test_smart_shelf_move_locker_to_another_distributor(self, ui, delete_hardware, delete_smart_shelf):
        ui.testrail_case_id = 1969

        lp = LoginPage(ui)
        ha = AdminHardwareApi(ui)
        ssa = SmartShelvesApi(ui)
        ss = SmartShelvesPage(ui)

        # create smart shelf for main distributor
        setup_locker = SetupLocker(ui)
        setup_locker.add_option("smart_shelf")
        response_locker_1 = setup_locker.setup()

        locker_body = response_locker_1["locker"]
        locker = locker_body["value"]

        # create second smart shelf for main distributor
        response_locker_2 = setup_locker.setup()
        locker_body_second = response_locker_2["locker"]

        # remove locker from smart shelf
        ssa.update_smart_shelf(locker_body=locker_body_second, locker_body_second=False)

        # create iot hub for second distributor
        iothub_response = ha.create_iothub(distributor_id=ui.data.sub_distributor_id)
        ui.dynamic_context["delete_hardware_id"].append(iothub_response["id"])

        lp.log_in_admin_portal()
        ss.sidebar_hardware()
        ss.check_smart_shelf_unavailable_via_planogram(locker, response_locker_1["smart_shelf_number"], in_list=True)

        # move locker to iothub of second distributor
        first_locker_type_id = (ha.get_first_locker_type())["id"]
        ha.update_locker(locker_id=locker_body["id"], locker_type_id=first_locker_type_id, iothub_id=iothub_response["id"])

        ss.page_refresh()
        ss.wait_until_progress_bar_loaded()
        ss.sidebar_hardware()
        ss.check_smart_shelf_unavailable_via_planogram(locker, response_locker_2["smart_shelf_number"])

    @pytest.mark.regression
    def test_smart_shelves_assign_to_several_lockers(self, ui, delete_hardware, delete_smart_shelf):
        ui.testrail_case_id = 1927

        lp = LoginPage(ui)
        ss = SmartShelvesPage(ui)
        hp = HardwarePage(ui)
        ssa = SmartShelvesApi(ui)

        # create smart shelf for main distributor
        setup_locker = SetupLocker(ui)
        setup_locker.add_option("smart_shelf")
        response_locker_1 = setup_locker.setup()

        smart_shelf_number = response_locker_1["smart_shelf_number"]
        locker_body = response_locker_1["locker"]
        locker = locker_body["value"]

        # remove locker from smart shelf
        ssa.update_smart_shelf(locker_body=locker_body, locker_body_second=False)

        # create second locker
        setup_locker.add_option("smart_shelf", False)
        response_locker_2 = setup_locker.setup()

        locker_body_second = response_locker_2["locker"]
        locker_second = locker_body_second["value"]

        lp.log_in_admin_portal()
        hp.sidebar_hardware()
        ss.assign_smart_shelf_locker_planogram(locker, smart_shelf_number)
        hp.sidebar_hardware()
        ss.check_smart_shelf_unavailable_via_planogram(locker_second, smart_shelf_number)

    @pytest.mark.regression
    def test_shelves_assign_via_hardware_check_planogram(self, ui, delete_shipto, delete_hardware, delete_smart_shelf):
        ui.testrail_case_id = 1966

        lp = LoginPage(ui)
        lpp = LockerPlanogramPage(ui)
        ssp = DistributorSmartShelvesPage(ui)
        ssa = SmartShelvesApi(ui)

        #create shipto
        response_shipto = SetupShipto(ui).setup()

        # create smart shelf for main distributor
        setup_locker = SetupLocker(ui)
        setup_locker.add_option("smart_shelf")
        setup_locker.add_option("shipto_id", response_shipto["shipto_id"])
        response_locker = setup_locker.setup()

        locker_body = response_locker["locker"]
        locker = locker_body["value"]

        # remove locker from smart shelf
        ssa.update_smart_shelf(locker_body, locker_body_second=False)

        lp.log_in_distributor_portal()
        ssp.open_smart_shelves()
        ssp.assign_smart_shelf_to_locker(response_locker["smart_shelf_number"], locker, "1")
        lpp.follow_locker_planogram_url(customer_id=locker_body["customerUser"] , shipto_id=response_shipto["shipto_id"])
        lpp.check_smart_shelf_via_planogram(response_locker["smart_shelf_number"], "1")
    
    @pytest.mark.regression
    def test_smart_shelves_crud(self, ui, delete_shipto, delete_hardware):
        ui.testrail_case_id = 1920

        lp = LoginPage(ui)
        sh = SmartShelvesPage(ui)
        ha = AdminHardwareApi(ui)

        # create locker for main distributor
        setup_locker = SetupLocker(ui)
        response_locker = setup_locker.setup()
        locker_body = response_locker["locker"]
        locker = locker_body["value"]

        # create locker for second distributor
        setup_locker.add_option("distributor_id", ui.data.sub_distributor_id)
        response_second_locker = setup_locker.setup()
        locker_body_second = response_second_locker["locker"]
        edit_locker = locker_body_second["value"]

        #--------------------------------
        serial_number = random.randint(1000000, 9999999)
        smart_shelves_body = sh.smart_shelves_body.copy()
        smart_shelves_body["serialNumber"] = f"{serial_number}"
        smart_shelves_body["distributor"] = f"{ui.data.distributor_name}"
        smart_shelves_body["assign_to"] = f"{locker}"
        smart_shelves_body["door_number"] = "1"

        #--------------------------------
        edit_serial_number = f"edit{serial_number}"
        edit_smart_shelves_body = sh.smart_shelves_body.copy()
        edit_smart_shelves_body["serialNumber"] = f"{edit_serial_number}"
        edit_smart_shelves_body["distributor"] = f"{ui.data.sub_distributor_name}"
        edit_smart_shelves_body["assign_to"] = f"{edit_locker}"
        edit_smart_shelves_body["door_number"] = "2"

        lp.log_in_admin_portal()
        sh.open_smart_shelves()
        sh.create_smart_shelves(smart_shelves_body)
        sh.check_last_smart_shelf(smart_shelves_body)
        sh.update_smart_shelves(edit_smart_shelves_body)
        sh.check_last_smart_shelf(edit_smart_shelves_body)
        sh.delete_smart_shelf(edit_serial_number)

    @pytest.mark.regression
    def test_smart_shelves_edit_dist_portal(self, ui, delete_smart_shelf, delete_hardware):
        ui.testrail_case_id = 1960

        lp = LoginPage(ui)
        dss = DistributorSmartShelvesPage(ui)
        ssa = SmartShelvesApi(ui)

        # create smart shelf for main distributor
        setup_locker = SetupLocker(ui)
        setup_locker.add_option("smart_shelf")
        response_locker = setup_locker.setup()

        locker_body = response_locker["locker"]
        locker = locker_body["value"]

        # remove locker from smart shelf
        ssa.update_smart_shelf(locker_body=locker_body, locker_body_second=False)

        #--------------------------------
        smart_shelves_body = dss.smart_shelves_body.copy()
        smart_shelves_body["serialNumber"] = response_locker["smart_shelf_number"]
        smart_shelves_body["assign_to"] = locker
        smart_shelves_body["door_number"] = "1"

        lp.log_in_distributor_portal()
        dss.open_smart_shelves()
        dss.update_smart_shelves(smart_shelves_body)
        dss.check_last_smart_shelf(smart_shelves_body)

    @pytest.mark.regression
    def test_smart_shelves_merge_cells(self, ui, delete_smart_shelf, delete_hardware):
        ui.testrail_case_id = 1921

        lp = LoginPage(ui)
        ss = SmartShelvesPage(ui)
        ssa = SmartShelvesApi(ui)

        # create locker for main distributor
        setup_locker = SetupLocker(ui)
        setup_locker.add_option("smart_shelf")
        response_locker = setup_locker.setup()

        locker_body = response_locker["locker"]
        locker = locker_body["value"]
        iothub_body = response_locker["iothub"]

        lp.log_in_admin_portal()
        ss.open_smart_shelves()
        ss.merge_cells(3)
        ss.check_cells_number(2)
        ss.split_cells(0)
        ss.check_cells_number(4)

    @pytest.mark.regression
    def test_smart_shelves_merge_cells_distributor(self, ui, delete_smart_shelf, delete_hardware):
        ui.testrail_case_id = 1959

        lp = LoginPage(ui)
        dss = DistributorSmartShelvesPage(ui)
        ssa = SmartShelvesApi(ui)

        # create smart shelf for main distributor
        setup_locker = SetupLocker(ui)
        setup_locker.add_option("smart_shelf")
        response_locker = setup_locker.setup()

        locker_body = response_locker["locker"]
        locker = locker_body["value"]
        iothub_body = response_locker["iothub"]

        lp.log_in_distributor_portal()
        dss.open_smart_shelves()
        dss.merge_cells(3)
        dss.check_cells_number(2)
        dss.split_cells(0)
        dss.check_cells_number(4)

    @pytest.mark.regression
    def test_smart_shelves_remove_locker_distributor(self, ui, delete_smart_shelf, delete_hardware):
        ui.testrail_case_id = 1926
    
        lp = LoginPage(ui)
        ss = SmartShelvesPage(ui)
        ssa = SmartShelvesApi(ui)

        # create smart shelf for main distributor
        setup_locker = SetupLocker(ui)
        setup_locker.add_option("smart_shelf")
        response_locker = setup_locker.setup()

        locker_body = response_locker["locker"]
        locker = locker_body["value"]
        iothub_body = response_locker["iothub"]

        lp.log_in_admin_portal()
        ss.open_smart_shelves()
        ss.clear_fields_smart_shelves(locker=True, distributor=True)
        ss.open_smart_shelves()

    @pytest.mark.regression
    def test_smart_shelves_unavailable_door(self, ui, delete_smart_shelf, delete_hardware):
        ui.testrail_case_id = 1925

        lp = LoginPage(ui)
        ss = SmartShelvesPage(ui)
        ssa = SmartShelvesApi(ui)

        # create smart shelf for main distributor
        setup_locker = SetupLocker(ui)
        setup_locker.add_option("smart_shelf")
        response_locker = setup_locker.setup()

        locker_body = response_locker["locker"]
        locker = locker_body["value"]
        iothub_body = response_locker["iothub"]

        lp.log_in_admin_portal()
        ss.open_smart_shelves()
        ss.check_first_door_is_unavaliable(locker, create=True)
      
    @pytest.mark.regression
    def test_smart_shelves_without_weights(self, ui, delete_smart_shelf, delete_hardware):
        ui.testrail_case_id = 1922

        lp = LoginPage(ui)
        ss = SmartShelvesPage(ui)

        # create smart shelf for main distributor
        setup_locker = SetupLocker(ui)
        setup_locker.add_option("smart_shelf")
        response_locker_1 = setup_locker.setup()

        locker_body = response_locker_1["locker"]
        locker = locker_body["value"]
        iothub_body = response_locker_1["iothub"]

        # create locker with 'without weights' configuration
        setup_locker.add_option("smart_shelf", False)
        setup_locker.add_option("no_weight")
        response_locker_2 = setup_locker.setup()

        locker_body_noweights = response_locker_2["locker"]
        locker_noweights = locker_body_noweights["value"]
        iothub_body_second = response_locker_2["iothub"]

        lp.log_in_admin_portal()
        ss.open_smart_shelves()
        ss.check_first_door_is_unavaliable(locker_noweights)
