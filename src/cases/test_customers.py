import pytest
import random
from src.resources.tools import Tools
from src.resources.locator import Locator
from src.pages.general.login_page import LoginPage
from src.pages.general.activity_log_page import ActivityLogPage
from src.pages.distributor.customers_page import CustomersPage
from src.pages.distributor.shipto_page import ShiptoPage
from src.pages.distributor.usage_history_page import UsageHistoryPage
from src.pages.customer.allocation_codes_page import AllocationCodesPage
from src.api.distributor.activity_log_api import ActivityLogApi
import time

class TestCustomers():
    @pytest.mark.regression
    def test_customer_crud(self, ui):
        ui.testrail_case_id = 31

        lp = LoginPage(ui)
        cp = CustomersPage(ui)
        customer_body = cp.customer_body.copy()
        edit_customer_body = cp.customer_body.copy()

        #-------------------
        customer_body["name"] = "Customer Name"
        customer_body["customerType"] = "Not specified"
        customer_body["marketType"] = "Not specified"
        customer_body["warehouse"] = "A_Warehouse (1138)"
        #-------------------
        edit_customer_body["name"] = "Customer Edit Name"
        edit_customer_body["number"] = "Customer Edit Number"
        edit_customer_body["customerType"] = "Not specified"
        edit_customer_body["marketType"] = "Not specified"
        edit_customer_body["notes"] = "any note"
        edit_customer_body["supplyForce"] = "true"
        #-------------------

        lp.log_in_distributor_portal()
        cp.sidebar_customers()
        cp.create_customer(customer_body.copy())
        cp.check_last_customer(customer_body.copy())
        cp.update_last_customer(edit_customer_body.copy())
        cp.sidebar_customers()
        cp.wait_until_page_loaded()
        cp.check_last_customer(edit_customer_body.copy())
        cp.delete_last_customer()

    @pytest.mark.regression
    def test_shipto_crud(self, ui):
        ui.testrail_case_id = 241

        lp = LoginPage(ui)
        sp = ShiptoPage(ui)
        shipto_body = sp.shipto_body.copy()
        edit_shipto_body = sp.shipto_body.copy()

        #-------------------
        shipto_body["number"] = Tools.random_string_l(12)
        shipto_body["poNumber"] = Tools.random_string_l(10)
        shipto_body["address.zipCode"] = "77777"
        shipto_body["address.line1"] = "test_address 1"
        shipto_body["address.city"] = "test city"
        shipto_body["state"] = "Alaska"
        #-------------------
        edit_shipto_body["number"] = Tools.random_string_l(12)
        edit_shipto_body["name"] = Tools.random_string_l(10)
        edit_shipto_body["poNumber"] = Tools.random_string_l(10)
        edit_shipto_body["address.zipCode"] = "77777"
        edit_shipto_body["address.line1"] = "test_address 1"
        edit_shipto_body["address.line2"] = "test_address 2"
        edit_shipto_body["address.city"] = "test city"
        edit_shipto_body["state"] = "Alaska"
        edit_shipto_body["notes"] = "some notes"
        edit_shipto_body["contactId"] = "11111"
        #-------------------

        lp.log_in_distributor_portal()
        sp.follow_shipto_url()
        sp.create_shipto(shipto_body.copy())
        sp.check_last_shipto(shipto_body.copy())
        sp.update_last_shipto(edit_shipto_body.copy())
        sp.should_be_disabled_xpath(Locator.xpath_submit_button)
        sp.driver.find_element_by_link_text('Shiptos').click()
        sp.wait_until_page_loaded()
        sp.check_last_shipto(edit_shipto_body.copy())
        sp.delete_last_shipto()

    @pytest.mark.regression
    def test_usage_history_import(self, ui):
        ui.testrail_case_id = 1842

        lp = LoginPage(ui)
        uhp = UsageHistoryPage(ui)
        usage_history_body = uhp.usage_history_body.copy()

        #-------------------
        usage_history_body["Order Number"] = Tools.random_string_u(10)
        usage_history_body["Customer Number"] = Tools.random_string_u(10)
        usage_history_body["ShipTo Number"] = Tools.random_string_u(10)
        usage_history_body["ShipTo Name"] = Tools.random_string_u(10)
        usage_history_body["Distributor SKU"] = Tools.random_string_u(10)
        usage_history_body["Quantity"] = str(random.choice(range(1, 100)))
        usage_history_body["Date"] = "Sun, Dec 30, 2018"
        #-------------------
        usage_history = [
            [usage_history_body["Order Number"], usage_history_body["Customer Number"], usage_history_body["ShipTo Number"], usage_history_body["ShipTo Name"], usage_history_body["Distributor SKU"], usage_history_body["Quantity"], "2018/12/30 10:15:30"]
        ]
        lp.log_in_distributor_portal()
        uhp.follow_usage_history_url()
        uhp.import_usage_history(usage_history)
        uhp.check_last_usage_history(usage_history_body.copy())

    @pytest.mark.regression
    def test_allocation_code_crud(self, ui):
        ui.testrail_case_id = 42

        lp = LoginPage(ui)
        acp = AllocationCodesPage(ui)
        alp = ActivityLogPage(ui)
        ala = ActivityLogApi(ui)
        allocation_code_body = acp.allocation_code_body.copy()
        edit_allocation_code_body = acp.allocation_code_body.copy()

        #-------------------
        allocation_code_body["name"] = Tools.random_string_u(10)
        allocation_code_body["type"] = "Dropdown"
        allocation_code_body["values"] = [Tools.random_string_u(7), Tools.random_string_u(7)]
        allocation_code_body["isRequired"] = True
        allocation_code_body["shiptos"] = [ui.data.shipto_number]
        #-------------------
        edit_allocation_code_body["name"] = Tools.random_string_u(10)
        edit_allocation_code_body["values"] = [Tools.random_string_u(7)]
        edit_allocation_code_body["isRequired"] = False
        #-------------------
        activity_log_main_body = {
            "Type": "AllocationCodes",
            "Action": "ALLOCATION_CODES_CREATE",
            "User": ui.customer_email,
            "User Type": "USER",
            "Result": "SUCCESS"
        }
        #-------------------
        activity_log_expanded_body = {
            "codeType": "DROP_DOWN",
            "name": allocation_code_body["name"]
        }
        #-------------------
        options = {
            "action": None,
            "event_type": "AllocationCodes",
            "name": None
        }

        lp.log_in_customer_portal()
        acp.sidebar_allocation_codes()
        acp.add_allocation_code(allocation_code_body.copy())

        acp.check_allocation_code(allocation_code_body.copy())
        allocation_code_event = ala.get_activity_log(size=1, shiptos=[f"{ui.data.shipto_id}"], wait=5)
        options["action"] = "ALLOCATION_CODES_CREATE"
        options["name"] = allocation_code_body["name"]
        ala.check_event(allocation_code_event, options)

        acp.update_allocation_code(allocation_code_body["name"], edit_allocation_code_body.copy())
        options["action"] = "ALLOCATION_CODES_UPDATE"
        options["name"] = edit_allocation_code_body["name"]
        allocation_code_event = ala.get_activity_log(size=1, shiptos=[f"{ui.data.shipto_id}"], wait=5)
        ala.check_event(allocation_code_event, options)

        acp.sidebar_allocation_codes()
        acp.wait_until_page_loaded()
        acp.check_allocation_code(edit_allocation_code_body.copy())
        acp.delete_allocation_code(edit_allocation_code_body["name"])
        allocation_code_event = ala.get_activity_log(size=1, shiptos=[f"{ui.data.shipto_id}"], wait=5)
        options["action"] = "ALLOCATION_CODES_DELETE"
        options["name"] = edit_allocation_code_body["name"]
        ala.check_event(allocation_code_event, options)
