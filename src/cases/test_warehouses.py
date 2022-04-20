import pytest
from src.resources.tools import Tools
from src.resources.permissions import Permissions
from src.pages.general.login_page import LoginPage
from src.pages.distributor.warehouses_page import WarehousesPage
from src.api.distributor.warehouse_api import WarehouseApi
from src.resources.locator import Locator

@pytest.mark.parametrize("permissions", [
    {
        "user": None,
        "testrail_case_id": 29
    },
    # {
    #     "user": Permissions.warehouses("EDIT"),
    #     "testrail_case_id": 2269
    # }
    ])
@pytest.mark.acl
@pytest.mark.regression
def test_warehouses_crud(ui, permission_ui, permissions, delete_distributor_security_group):
    ui.testrail_case_id = permissions["testrail_case_id"]
    context = Permissions.set_configured_user(ui, permissions["user"], permission_context=permission_ui)

    lp = LoginPage(context)
    wp = WarehousesPage(context)

    warehouse_body = wp.warehouse_body.copy()
    edit_warehouse_body = wp.warehouse_body.copy()

    #-------------------
    warehouse_body["name"] = "Warehouse Name"
    warehouse_body["number"] = f"NUMBER {Tools.random_string_u()}"
    warehouse_body["address.zipCode"] = "77777"
    warehouse_body["address.line1"] = "test_address 1"
    warehouse_body["address.city"] = "test city"
    warehouse_body["state"] = "Georgia"
    warehouse_body["timezone"] = "America/Adak (-09:00)"
    warehouse_body["contactEmail"] = Tools.random_email()
    warehouse_body["invoiceEmail"] = Tools.random_email()
    #-------------------
    edit_warehouse_body["name"] = "Warehouse Edit Name"
    edit_warehouse_body["number"] = f"EDIT NUMBER {Tools.random_string_u()}"
    edit_warehouse_body["address.zipCode"] = "EDIT 77777"
    edit_warehouse_body["address.line1"] = "edit test_address 1"
    edit_warehouse_body["address.line2"] = "edit test_address 1"
    edit_warehouse_body["address.city"] = "edit test city"
    edit_warehouse_body["state"] = "Colorado"
    edit_warehouse_body["timezone"] = "America/Atka (-09:00)"
    edit_warehouse_body["contactEmail"] = Tools.random_email()
    edit_warehouse_body["invoiceEmail"] = Tools.random_email()
    #-------------------

    lp.log_in_distributor_portal()
    wp.sidebar_warehouses()
    wp.create_warehouse(warehouse_body.copy())
    wp.check_last_warehouse(warehouse_body.copy())
    wp.update_last_warehouse(edit_warehouse_body.copy())
    wp.click_xpath(Locator.xpath_reload_button)
    wp.last_page(wait=False)
    wp.check_last_warehouse(edit_warehouse_body.copy())
    wp.delete_last_warehouse(edit_warehouse_body["name"])

@pytest.mark.regression
def test_warehouses_unique_number(api):
    api.testrail_case_id = 6545

    wa = WarehouseApi(api)

    warehouse_body = wa.warehouse_body.copy()
    warehouse_number = f"NUMBER {Tools.random_string_u()}"

    #-------------------
    warehouse_body["name"] = "Warehouse Name"
    warehouse_body["number"] = warehouse_number
    warehouse_body["address"]["zipCode"] = "77777"
    warehouse_body["address"]["line1"] = "test_address 1"
    warehouse_body["address"]["line2"] = ""
    warehouse_body["address"]["city"] = "test city"
    warehouse_body["address"]["state"] = "Al"
    warehouse_body["zoneId"] = "America/Adak"
    warehouse_body["contactEmail"] = Tools.random_email()
    warehouse_body["invoiceEmail"] = Tools.random_email()
    # #-------------------
    edit_warehouse_body = wa.warehouse_body.copy()
    edit_warehouse_body["name"] = "Edit Warehouse Name"
    edit_warehouse_body["number"] = warehouse_number
    edit_warehouse_body["address"]["zipCode"] = "77777"
    edit_warehouse_body["address"]["line1"] = "test_address 1"
    edit_warehouse_body["address"]["line2"] = ""
    edit_warehouse_body["address"]["city"] = "test city"
    edit_warehouse_body["address"]["state"] = "Al"
    edit_warehouse_body["zoneId"] = "America/Adak"
    edit_warehouse_body["contactEmail"] = Tools.random_email()
    edit_warehouse_body["invoiceEmail"] = Tools.random_email()
    #-------------------

    response_body = wa.create_warehouse(dto=warehouse_body)
    wa.update_warehouse(dto=edit_warehouse_body, warehouese_id=response_body["data"])
    wa.create_warehouse(dto=edit_warehouse_body, expected_status_code=400) #cannot create warhouse with exists number
    wa.delete_warehouse(warehouese_id=response_body["data"])
