import pytest
from src.resources.tools import Tools
from src.pages.general.login_page import LoginPage
from src.pages.admin.distributor_admin_page import DistributorAdminPage

@pytest.mark.regression
def test_distributor_crud(ui):
    ui.testrail_case_id = 1917

    lp = LoginPage(ui)
    dp = DistributorAdminPage(ui)
    distributor_body = dp.distributor_body.copy()
    edit_distributor_body = dp.distributor_body.copy()
    table_cells_checkbox = dp.table_cells_checkbox.copy()
    edit_table_cells_checkbox = dp.table_cells_checkbox.copy()

    #-------------------
    distributor_body["name"] = "my First"
    distributor_body["externalDistributorNumber"] = Tools.random_string_u(5)
    distributor_body["invoiceEmail"] = Tools.random_email()
    distributor_body["address.line1"] = "my adress line 1"
    distributor_body["address.line2"] = "my adress line 2"
    distributor_body["address.city"] = "Boston"
    distributor_body["address.zipCode"] = "02101"
    distributor_body["country"] = "Canada"
    distributor_body["state"] = "Manitoba"
    distributor_body["ship_to_level"] = "Level 3"
    checkbox_list = ["Processing Fee", "Supply Force", "Bill by all Ship-tos", "Use the Distributor Catalog in the Universal Catalog data"]

    #-------------------
    edit_distributor_body["name"] = "my Edit First"
    edit_distributor_body["externalDistributorNumber"] = Tools.random_string_u(5)
    edit_distributor_body["invoiceEmail"] = Tools.random_email()
    edit_distributor_body["address.line1"] = "my Edit adress line 1"
    edit_distributor_body["address.line2"] = "my Edit adress line 2"
    edit_distributor_body["address.city"] = "Fairbanks"
    edit_distributor_body["address.zipCode"] = "99703"
    edit_distributor_body["country"] = "USA"
    edit_distributor_body["state"] = "Manitoba"
    edit_distributor_body["ship_to_level"] = "Level 3"
    edit_checkbox_list = ["Processing Fee", "Supply Force"]
    edit_table_cells_checkbox["Process.Fee"] = False
    edit_table_cells_checkbox["SupplyForce"] = False
    #-------------------

    lp.log_in_admin_portal()
    dp.sidebar_distributors()
    dp.wait_until_page_loaded()
    dp.open_last_page()
    check_mark = dp.create_distributor(distributor_body.copy(), checkbox_list=checkbox_list)
    dp.check_last_distributor(distributor_body.copy(), state_short_code="MB", table_cells_checkbox=table_cells_checkbox, check_mark=check_mark)
    dp.update_last_distributor(edit_distributor_body.copy(), checkbox_list=edit_checkbox_list)
    dp.check_last_distributor(edit_distributor_body.copy(), "AK", table_cells_checkbox=edit_table_cells_checkbox, check_mark=check_mark)
    dp.delete_last_distributor()
