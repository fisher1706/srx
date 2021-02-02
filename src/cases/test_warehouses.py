import pytest
from src.resources.tools import Tools
from src.resources.locator import Locator
from src.resources.permissions import Permissions
from src.pages.general.login_page import LoginPage
from src.pages.distributor.warehouses_page import WarehousesPage

class TestWarehouses():
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
    def test_warehouses_crud(self, ui, permission_ui, permissions, delete_distributor_security_group):
        ui.testrail_case_id = permissions["testrail_case_id"]
        context = Permissions.set_configured_user(ui, permissions["user"], permission_context=permission_ui)

        lp = LoginPage(context)
        wp = WarehousesPage(context)

        warehouse_body = wp.warehouse_body.copy()
        edit_warehouse_body = wp.warehouse_body.copy()

        #-------------------
        warehouse_body["name"] = "Warehouse Name"
        warehouse_body["number"] = "Warehouse Number"
        warehouse_body["address.zipCode"] = "77777"
        warehouse_body["address.line1"] = "test_address 1"
        warehouse_body["address.city"] = "test city"
        warehouse_body["state"] = "Georgia"
        warehouse_body["timezone"] = "America/Halifax (-04:00)"
        warehouse_body["contactEmail"] = Tools.random_email()
        warehouse_body["invoiceEmail"] = Tools.random_email()
        #-------------------
        edit_warehouse_body["name"] = "Warehouse Edit Name"
        edit_warehouse_body["number"] = "Warehouse Edit Number"
        edit_warehouse_body["address.zipCode"] = "EDIT 77777"
        edit_warehouse_body["address.line1"] = "edit test_address 1"
        edit_warehouse_body["address.line2"] = "edit test_address 1"
        edit_warehouse_body["address.city"] = "edit test city"
        edit_warehouse_body["state"] = "Colorado"
        edit_warehouse_body["timezone"] = "America/Atka (-10:00)"
        edit_warehouse_body["contactEmail"] = Tools.random_email()
        edit_warehouse_body["invoiceEmail"] = Tools.random_email()
        #-------------------

        lp.log_in_distributor_portal()
        wp.sidebar_warehouses()
        wp.create_warehouse(warehouse_body.copy())
        wp.check_last_warehouse(warehouse_body.copy())
        wp.update_last_warehouse(edit_warehouse_body.copy())
        wp.check_last_warehouse(edit_warehouse_body.copy())
        wp.delete_last_warehouse()