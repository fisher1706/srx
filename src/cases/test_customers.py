import random
import pytest
from src.resources.tools import Tools
from src.resources.locator import Locator
from src.resources.permissions import Permissions
from src.pages.general.login_page import LoginPage
from src.pages.distributor.customers_page import CustomersPage
from src.pages.distributor.shipto_page import ShiptoPage
from src.pages.distributor.usage_history_page import UsageHistoryPage
from src.pages.distributor.distributor_customer_users_page  import DistributorCustomerUsersPage
from src.pages.customer.allocation_codes_page import AllocationCodesPage
from src.api.distributor.customer_api import CustomerApi
from src.api.distributor.shipto_api import ShiptoApi
from src.api.setups.setup_shipto import SetupShipto
from src.api.setups.setup_customer import SetupCustomer

@pytest.mark.parametrize("permissions", [
    {
        "user": None,
        "testrail_case_id": 31
    },
    {
        "user": Permissions.customers("EDIT"),
        "testrail_case_id": 2241
    }
    ])
@pytest.mark.acl
@pytest.mark.regression
def test_customer_crud(ui, permission_ui, permissions, delete_distributor_security_group):
    ui.testrail_case_id = permissions["testrail_case_id"]
    context = Permissions.set_configured_user(ui, permissions["user"], permission_context=permission_ui)

    lp = LoginPage(context)
    cp = CustomersPage(context)
    customer_body = cp.customer_body.copy()
    edit_customer_body = cp.customer_body.copy()

    #-------------------
    customer_body["name"] = "Customer Name"
    customer_body["number"] = f"NUMBER {Tools.random_string_u()}"
    customer_body["customerType"] = "Not specified"
    customer_body["marketType"] = "Not specified"
    customer_body["warehouse"] = "A_Warehouse (1138)"
    #-------------------
    edit_customer_body["name"] = "Customer Edit Name"
    edit_customer_body["number"] = f"EDIT NUMBER {Tools.random_string_u()}"
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
    cp.last_page(wait=False)
    cp.check_last_customer(edit_customer_body.copy())
    cp.delete_last_customer(edit_customer_body["name"])

@pytest.mark.regression
def test_customer_unique_number(api, delete_customer):
    api.testrail_case_id = 6544

    ca = CustomerApi(api)

    response_customer = SetupCustomer(api).setup()
    customer = ca.get_customers(name=response_customer["customer"]["name"])[-1]

    customer["name"] = "Customer Edit name"
    customer["number"] = response_customer["customer"]["number"]

    ca.update_customer(dto=customer, customer_id=response_customer["customer_id"])

    not_unique_data = customer.copy()
    not_unique_data["name"] = "Name"
    not_unique_data["number"] = customer["number"]

    ca.create_customer(dto=not_unique_data, expected_status_code=400) #cannot create customer with exists number

@pytest.mark.acl
@pytest.mark.regression
def test_customer_crud_view_permission(api, permission_api, delete_distributor_security_group, delete_customer):
    api.testrail_case_id = 2242

    Permissions.set_configured_user(api, Permissions.customers("VIEW"))

    ca = CustomerApi(permission_api)

    failed_setup = SetupCustomer(permission_api)
    failed_setup.add_option("expected_status_code", 400)
    failed_setup.setup() #cannot create customer

    response_customer = SetupCustomer(api).setup()
    customer = ca.get_customers(name=response_customer["customer"]["name"])[0] #can read customer
    assert response_customer["customer"]["number"] == customer["number"] #--//--//--

    customer["id"] = response_customer["customer_id"]
    ca.update_customer(dto=customer, customer_id=response_customer["customer_id"], expected_status_code=400) #cannot update customer
    ca.delete_customer(customer_id=response_customer["customer_id"], expected_status_code=400) #cannot delete customer

@pytest.mark.parametrize("permissions", [
    {
        "user": None,
        "testrail_case_id": 241
    },
    {
        "user": Permissions.shiptos("EDIT"),
        "testrail_case_id": 2274
    }
    ])
@pytest.mark.acl
@pytest.mark.regression
def test_shipto_crud(ui, permission_ui, permissions, delete_distributor_security_group):
    ui.testrail_case_id = permissions["testrail_case_id"]
    context = Permissions.set_configured_user(ui, permissions["user"], permission_context=permission_ui)

    lp = LoginPage(context)
    sp = ShiptoPage(context)
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
    sp.get_element_by_xpath(Locator.xpath_table_item(1, 1))
    sp.create_shipto(shipto_body.copy())
    sp.check_last_shipto(shipto_body.copy())
    sp.update_last_shipto(edit_shipto_body.copy(), False)
    sp.should_be_disabled_xpath(Locator.xpath_submit_button)
    sp.driver.find_element_by_link_text('Shiptos').click()
    sp.wait_until_page_loaded()
    sp.check_last_shipto(edit_shipto_body.copy())
    sp.delete_last_shipto(False)

@pytest.mark.acl
@pytest.mark.regression
def test_shipto_crud_view_permission(api, permission_api, delete_distributor_security_group, delete_shipto):
    api.testrail_case_id = 2276

    Permissions.set_configured_user(api, Permissions.shiptos("VIEW"))

    sa = ShiptoApi(permission_api)

    failed_setup = SetupShipto(permission_api)
    failed_setup.add_option("expected_status_code", 400)
    failed_setup.setup() #cannot create shipto

    response_shipto = SetupShipto(api).setup()
    shipto = sa.get_shipto_by_id(response_shipto["shipto_id"]) #can read shipto
    sa.get_shipto_by_number(response_shipto["shipto"]["number"])
    assert response_shipto["shipto"]["number"] == shipto["number"] #--//--//--
    sa.update_shipto(shipto, response_shipto["shipto_id"], expected_status_code=400) #cannot update shipto
    sa.delete_shipto(response_shipto["shipto_id"], expected_status_code=400) #cannot delete shipto

@pytest.mark.parametrize("permissions", [
    {
        "user": None,
        "testrail_case_id": 1842
    },
    {
        "user": Permissions.usage_history("EDIT"),
        "testrail_case_id": 2268
    }
    ])
@pytest.mark.acl
@pytest.mark.regression
def test_usage_history_import(ui, permission_ui, permissions, delete_distributor_security_group):
    ui.testrail_case_id = permissions["testrail_case_id"]
    context = Permissions.set_configured_user(ui, permissions["user"], permission_context=permission_ui)

    lp = LoginPage(context)
    uhp = UsageHistoryPage(context)
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
        [usage_history_body["Order Number"], usage_history_body["Customer Number"], usage_history_body["ShipTo Number"], usage_history_body["ShipTo Name"], usage_history_body["Distributor SKU"], usage_history_body["Quantity"], "2018/12/30 10:15:30"] #pylint: disable=C0301
    ]
    lp.log_in_distributor_portal()
    uhp.follow_usage_history_url()
    uhp.select_pagination(10)
    uhp.import_usage_history(usage_history)
    uhp.last_page(wait=False)
    uhp.check_last_usage_history(usage_history_body.copy())

@pytest.mark.regression
def test_allocation_code_crud(ui):
    ui.testrail_case_id = 42

    lp = LoginPage(ui)
    acp = AllocationCodesPage(ui)
    # ala = ActivityLogApi(ui)
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
    # options = {
    #     "action": None,
    #     "event_type": "AllocationCodes",
    #     "name": None
    # }

    lp.log_in_customer_portal()
    acp.sidebar_allocation_codes()
    acp.add_allocation_code(allocation_code_body.copy())

    acp.check_allocation_code(allocation_code_body.copy())
    # allocation_code_event = ala.get_activity_log(size=1, shiptos=[f"{ui.data.shipto_id}"], wait=5)
    # options["action"] = "ALLOCATION_CODES_CREATE"
    # options["name"] = allocation_code_body["name"]
    # ala.check_event(allocation_code_event, options)

    acp.update_allocation_code(allocation_code_body["name"], edit_allocation_code_body.copy())
    # options["action"] = "ALLOCATION_CODES_UPDATE"
    # options["name"] = edit_allocation_code_body["name"]
    # allocation_code_event = ala.get_activity_log(size=1, shiptos=[f"{ui.data.shipto_id}"], wait=5)
    # ala.check_event(allocation_code_event, options)

    acp.sidebar_allocation_codes()
    acp.wait_until_page_loaded()
    acp.check_allocation_code(edit_allocation_code_body.copy())
    acp.delete_allocation_code(edit_allocation_code_body["name"])
    # allocation_code_event = ala.get_activity_log(size=1, shiptos=[f"{ui.data.shipto_id}"], wait=5)
    # options["action"] = "ALLOCATION_CODES_DELETE"
    # options["name"] = edit_allocation_code_body["name"]
    # ala.check_event(allocation_code_event, options)

@pytest.mark.parametrize("permissions", [
    {
        "user": None,
        "testrail_case_id": 3790
    }
    # {
    #     "user": Permissions.customers("EDIT"),
    #     # "testrail_case_id": 3791
    # }
    ])
@pytest.mark.regression
def test_customer_setup_wizard_required_steps(ui, permission_ui, api, permissions, delete_distributor_security_group):
    ui.testrail_case_id = permissions["testrail_case_id"]
    context = Permissions.set_configured_user(ui, permissions["user"], permission_context=permission_ui)

    lp = LoginPage(context)
    cp = CustomersPage(context)
    ca = CustomerApi(api)
    dcp = DistributorCustomerUsersPage(context)
    customer_body = cp.customer_body.copy()

    customer_body["name"] = Tools.random_string_l(10)
    customer_body["number"] = Tools.random_string_u(10)
    customer_body["customerType"] = "Not specified"
    customer_body["marketType"] = "Not specified"
    email = Tools.random_string_l(10)+ "@agilevision.io"

    lp.log_in_distributor_portal()
    cp.sidebar_customers()
    cp.click_on_customer_setup_wizard_button()
    cp.select_warehouse()
    cp.add_customer_info(customer_body.copy())
    cp.add_customer_portal_user(email)
    cp.click_complete()
    cp.check_last_customer(customer_body.copy())
    response_customer = ca.get_customers(name=customer_body["name"])[-1]
    dcp.follow_customer_users_url(customer_id=response_customer["id"])
    cp.check_customer_portal_user(email)
    cp.sidebar_customers()
    cp.wait_until_page_loaded()
    cp.delete_last_customer(customer_body["name"])

@pytest.mark.regression
def test_customer_setup_wizard_view_permission(ui, permission_ui, delete_distributor_security_group):
    ui.testrail_case_id = 3792
    context = Permissions.set_configured_user(ui, Permissions.customers("VIEW"), permission_context=permission_ui)

    lp = LoginPage(context)
    cp = CustomersPage(context)

    lp.log_in_distributor_portal()
    cp.check_customer_setup_wizard_button()

@pytest.mark.regression
def test_customer_setup_wizard_all_steps(ui, api, delete_distributor_security_group):
    ui.testrail_case_id = 3793

    lp = LoginPage(ui)
    cp = CustomersPage(ui)
    ca = CustomerApi(api)
    dcp = DistributorCustomerUsersPage(ui)
    customer_body = cp.customer_body.copy()

    customer_body["name"] = Tools.random_string_l(10)
    customer_body["number"] = Tools.random_string_u(10)
    customer_body["customerType"] = "Not specified"
    customer_body["marketType"] = "Not specified"
    email = Tools.random_string_l(10)+ "@agilevision.io"

    lp.log_in_distributor_portal()
    cp.sidebar_customers()
    cp.click_on_customer_setup_wizard_button()
    cp.select_warehouse()
    cp.add_customer_info(customer_body.copy())
    cp.add_customer_portal_user(email)
    cp.click_next()
    cp.click_next()
    cp.change_automation_settings(email)
    cp.wait_until_page_loaded()
    cp.check_last_customer(customer_body.copy())
    response_customer = ca.get_customers(name=customer_body["name"])[-1]
    dcp.follow_customer_users_url(customer_id=response_customer["id"])
    cp.check_customer_portal_user(email)
    dcp.follow_customer_settings_url(customer_id=response_customer["id"])
    cp.check_settings_reorder_list_settings(email)
    cp.sidebar_customers()
    cp.wait_until_page_loaded()
    cp.delete_last_customer(customer_body["name"])

@pytest.mark.regression
def test_create_shipto_with_deleted_number(api, delete_shipto):
    api.testrail_case_id = 5598

    sa = ShiptoApi(api)

    shipto_name = Tools.random_string_l(21)
    setup_shipto = SetupShipto(api)
    setup_shipto.add_option("number", shipto_name)
    setup_shipto.add_option("delete", False)
    response_shipto = setup_shipto.setup()

    sa.delete_shipto(response_shipto["shipto_id"])

    setup_shipto = SetupShipto(api)
    setup_shipto.add_option("number", shipto_name)
    response_shipto = setup_shipto.setup()
