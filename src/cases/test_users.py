import pytest
from src.resources.tools import Tools
from src.resources.locator import Locator
from src.resources.permissions import Permissions
from src.api.customer.customer_user_api import CustomerUserApi
from src.api.customer.checkout_user_api import CheckoutUserApi
from src.api.distributor.user_api import UserApi
from src.api.setups.setup_customer_user import setup_customer_user
from src.api.setups.setup_checkout_group import setup_checkout_group
from src.api.setups.setup_shipto import SetupShipto
from src.pages.customer.customer_users_page import CustomerUsersPage
from src.pages.customer.checkout_users_page import CheckoutUsersPage
from src.pages.customer.customer_security_groups import CustomerSecurityGroups
from src.pages.customer.checkout_groups_page import CheckoutGroupsPage
from src.pages.distributor.distributor_users_page import DistributorUsersPage
from src.pages.general.login_page import LoginPage

class TestUsers():
    @pytest.mark.regression
    def test_checkout_user_of_customer_user(self, api):
        api.testrail_case_id = 1850

        cua = CustomerUserApi(api)
        chua = CheckoutUserApi(api)

        response_customer_user = setup_customer_user(api)
        customer_user_body = response_customer_user["customerUser"]
        customer_user_id = response_customer_user["customerUserId"]

        edit_customer_user_body = Tools.get_dto("customer_user_dto.json")
        edit_customer_user_body["firstName"] = customer_user_body["firstName"]+"edit"
        edit_customer_user_body["lastName"] = customer_user_body["lastName"]+"edit"
        edit_customer_user_body["email"] = customer_user_body["email"]
        edit_customer_user_body["id"] = customer_user_id

        first_number = chua.checkout_user_should_be_present(customer_user_body.copy())
        cua.update_customer_user(edit_customer_user_body.copy())
        second_number = chua.checkout_user_should_be_present(edit_customer_user_body.copy())
        assert first_number == second_number, "The number of checkout users is changed after update"

        chua.checkout_user_should_not_be_present(customer_user_body.copy())
        cua.delete_customer_user(customer_user_id)
        third_number = chua.checkout_user_should_not_be_present(edit_customer_user_body.copy())
        assert third_number == second_number-1, "The number of checkout users after removing should be less by 1 than before"

    @pytest.mark.regression
    def test_customer_user_crud(self, ui):
        ui.testrail_case_id = 37

        lp = LoginPage(ui)
        cup = CustomerUsersPage(ui)
        customer_user_body = cup.customer_user_body.copy()
        edit_customer_user_body = cup.customer_user_body.copy()

        #-------------------
        customer_user_body["email"] = Tools.random_email()
        customer_user_body["firstName"] = f"User {Tools.random_string_l()}"
        customer_user_body["lastName"] = f"User {Tools.random_string_l()}"
        customer_user_body["role"] = "Customer User"
        customer_user_body["shiptos"] = [ui.data.shipto_number]
        #-------------------
        edit_customer_user_body["firstName"] = f"User {Tools.random_string_l()}"
        edit_customer_user_body["lastName"] = f"User {Tools.random_string_l()}"
        edit_customer_user_body["role"] = "Customer Super User"
        #-------------------

        lp.log_in_customer_portal()
        cup.sidebar_users_and_groups()
        cup.click_xpath(Locator.xpath_button_tab_by_name("Users"))
        cup.create_customer_user(customer_user_body.copy())
        cup.check_last_customer_user(customer_user_body.copy())
        cup.update_last_customer_user(edit_customer_user_body.copy())
        cup.sidebar_users_and_groups()
        cup.wait_until_page_loaded()
        cup.check_last_customer_user(edit_customer_user_body.copy())
        cup.delete_last_customer_user()

    @pytest.mark.parametrize("permissions", [
        {
            "user": None,
            "testrail_case_id": 28
        },
        { 
            "user": Permissions.distributor_users("EDIT"),
            "testrail_case_id": 2178
        }
        ])
    @pytest.mark.regression
    def test_distributor_user_crud(self, ui, permissions, delete_distributor_security_group):
        ui.testrail_case_id = permissions["testrail_case_id"]
        Permissions.set_configured_user(ui, permissions["user"])

        lp = LoginPage(ui)
        dup = DistributorUsersPage(ui)
        distributor_user_body = dup.distributor_user_body.copy()
        edit_distributor_user_body = dup.distributor_user_body.copy()

        #-------------------
        distributor_user_body["email"] = Tools.random_email()
        distributor_user_body["firstName"] = f"User {Tools.random_string_l()}"
        distributor_user_body["lastName"] = f"User {Tools.random_string_l()}"
        distributor_user_body["role"] = "User"
        distributor_user_body["warehouses"] = ["Z_Warehouse (9999)", "A_Warehouse (1138)"]
        #-------------------
        edit_distributor_user_body["firstName"] = f"User {Tools.random_string_l()}"
        edit_distributor_user_body["lastName"] = f"User {Tools.random_string_l()}"
        edit_distributor_user_body["role"] = "Static Group"
        edit_distributor_user_body["warehouses"] = ["Z_Warehouse (9999)"]
        #-------------------

        lp.log_in_distributor_portal()
        dup.sidebar_users()
        dup.create_distributor_user(distributor_user_body.copy())
        dup.check_last_distributor_user(distributor_user_body.copy())
        dup.update_last_distributor_user(edit_distributor_user_body.copy())
        dup.check_last_distributor_user(edit_distributor_user_body.copy())
        dup.delete_last_distributor_user()

    

    @pytest.mark.regression
    def test_distributor_superuser_crud(self, ui):
        ui.testrail_case_id = 30

        lp = LoginPage(ui)
        dup = DistributorUsersPage(ui)
        distributor_superuser_body = dup.distributor_superuser_body.copy()
        edit_distributor_superuser_body = dup.distributor_superuser_body.copy()

        #-------------------
        distributor_superuser_body["email"] = Tools.random_email()
        distributor_superuser_body["firstName"] = f"User {Tools.random_string_l()}"
        distributor_superuser_body["lastName"] = f"User {Tools.random_string_l()}"
        #-------------------
        edit_distributor_superuser_body["firstName"] = f"User {Tools.random_string_l()}"
        edit_distributor_superuser_body["lastName"] = f"User {Tools.random_string_l()}"
        #-------------------

        lp.log_in_distributor_portal()
        dup.sidebar_users()
        dup.click_xpath(Locator.xpath_button_tab_by_name("Super Users"))
        dup.create_distributor_super_user(distributor_superuser_body.copy())
        dup.check_last_distributor_super_user(distributor_superuser_body.copy())
        dup.update_last_distributor_super_user(edit_distributor_superuser_body.copy())
        dup.check_last_distributor_super_user(edit_distributor_superuser_body.copy())
        dup.delete_last_distributor_super_user()

    @pytest.mark.regression
    def test_checkout_user_import_without_group(self, ui):
        ui.testrail_case_id = 1849

        lp = LoginPage(ui)
        cup = CheckoutUsersPage(ui)
        checkout_user_body = cup.checkout_user_body.copy()

        #-------------------
        checkout_user_body["firstName"] = f"Checkout User {Tools.random_string_l()}"
        checkout_user_body["lastName"] = f"Checkout User {Tools.random_string_l()}"
        checkout_user_body["fob"] = Tools.random_string_u(18)
        checkout_user_body["passCode"] = Tools.random_string_u(18)
        checkout_user_body["email"] = Tools.random_email()
        checkout_user_body["phone"] = Tools.random_string_l()
        #-------------------
        checkout_users = [
            [checkout_user_body["firstName"], checkout_user_body["lastName"], checkout_user_body["email"], checkout_user_body["phone"], checkout_user_body["fob"], checkout_user_body["passCode"], None]
        ]
        #-------------------

        lp.log_in_customer_portal()
        cup.sidebar_users_and_groups()
        cup.click_xpath(Locator.xpath_button_tab_by_name("Fobs & Passcodes"))
        cup.import_checkout_user(checkout_users)
        row = cup.scan_table(checkout_user_body["firstName"], "First Name", pagination=False)
        cup.check_new_checkout_user(checkout_user_body.copy(), row)
        cup.delete_new_checkout_user(row)

    @pytest.mark.regression
    def test_checkout_user_crud(self, ui):
        ui.testrail_case_id = 1848

        lp = LoginPage(ui)
        cup = CheckoutUsersPage(ui)
        checkout_user_body = cup.checkout_user_body.copy()
        edit_checkout_user_body = cup.checkout_user_body.copy()

        #-------------------
        checkout_user_body["firstName"] = f"Checkout User {Tools.random_string_l()}"
        checkout_user_body["lastName"] = f"Checkout User {Tools.random_string_l()}"
        #-------------------
        edit_checkout_user_body["firstName"] = f"Checkout User {Tools.random_string_l()}"
        edit_checkout_user_body["lastName"] = f"Checkout User {Tools.random_string_l()}"
        edit_checkout_user_body["fob"] = Tools.random_string_u(18)
        edit_checkout_user_body["passCode"] = Tools.random_string_u(18)
        edit_checkout_user_body["email"] = Tools.random_email()
        edit_checkout_user_body["phone"] = Tools.random_string_l()
        #-------------------

        lp.log_in_customer_portal()
        cup.sidebar_users_and_groups()
        cup.click_xpath(Locator.xpath_button_tab_by_name("Fobs & Passcodes"))
        cup.create_checkout_user(checkout_user_body.copy())
        row = cup.scan_table(checkout_user_body["firstName"], "First Name", pagination=False)
        cup.check_new_checkout_user(checkout_user_body.copy(), row)
        cup.update_new_checkout_user(edit_checkout_user_body.copy(), row, first_group=True)
        cup.sidebar_users_and_groups()
        cup.click_xpath(Locator.xpath_button_tab_by_name("Fobs & Passcodes"))
        cup.wait_until_page_loaded()
        row = cup.scan_table(edit_checkout_user_body["firstName"], "First Name", pagination=False)
        cup.check_new_checkout_user(edit_checkout_user_body.copy(), row)
        cup.delete_new_checkout_user(row)

    @pytest.mark.regression
    def test_customer_security_group_crud(self, ui):
        ui.testrail_case_id = 2007

        lp = LoginPage(ui)
        csg = CustomerSecurityGroups(ui)
        security_group_body = csg.security_group_body.copy()
        edit_security_group_body = csg.security_group_body.copy()

        #-------------------
        security_group_body["name"] = Tools.random_string_l(10)
        security_group_body["checked"] = True
        #-------------------
        edit_security_group_body["name"] = Tools.random_string_l(10)
        edit_security_group_body["checked"] = False

        lp.log_in_customer_portal()
        csg.open_security_groups()
        csg.create_security_group(security_group_body)
        row = csg.get_row_of_table_item_by_column(security_group_body["name"], 1)
        csg.check_security_group(security_group_body, row)
        csg.update_security_group(edit_security_group_body, row)
        csg.check_security_group(edit_security_group_body, row)
        csg.delete_security_group(edit_security_group_body, row)

    @pytest.mark.regression
    def test_checkout_group_crud(self, ui):
        ui.testrail_case_id = 1861

        lp = LoginPage(ui)
        cgp = CheckoutGroupsPage(ui)
        checkout_group_body = cgp.checkout_group_body.copy()
        edit_checkout_group_body = cgp.checkout_group_body.copy()

        #-------------------
        checkout_group_body["name"] = f"Name {Tools.random_string_l()}"
        checkout_group_body["email"] = Tools.random_email()
        #-------------------
        edit_checkout_group_body["name"] = f"Edit name {Tools.random_string_l()}"
        #-------------------

        lp.log_in_customer_portal()
        cgp.sidebar_users_and_groups()
        cgp.click_xpath(Locator.xpath_button_tab_by_name("Checkout Groups"))
        cgp.create_checkout_group(checkout_group_body.copy())
        row = cgp.scan_table(checkout_group_body["name"], "Checkout Group Name", pagination=False)
        cgp.check_new_checkout_group(checkout_group_body.copy(), row)
        cgp.update_new_checkout_group(edit_checkout_group_body.copy(), row)
        cgp.sidebar_users_and_groups()
        cgp.click_xpath(Locator.xpath_button_tab_by_name("Checkout Groups"))
        cgp.wait_until_page_loaded()
        row = cgp.scan_table(edit_checkout_group_body["name"], "Checkout Group Name", pagination=False)
        cgp.check_new_checkout_group(edit_checkout_group_body.copy(), row)
        cgp.delete_new_checkout_group(row)

    @pytest.mark.regression
    def test_checkout_group_assign_user(self, ui, delete_customer_user, delete_checkout_group):
        ui.testrail_case_id = 1890

        lp = LoginPage(ui)
        cgp = CheckoutGroupsPage(ui)

        response_checkout_group = setup_checkout_group(ui)
        response_customer_user = setup_customer_user(ui)

        lp.log_in_customer_portal()
        cgp.sidebar_users_and_groups()
        cgp.click_xpath(Locator.xpath_button_tab_by_name("Checkout Groups"))
        cgp.wait_until_page_loaded()
        row = cgp.scan_table(response_checkout_group["name"], "Checkout Group Name", pagination=False)
        cgp.click_xpath(Locator.xpath_by_count(Locator.xpath_associated_users, row))
        cgp.assign_user(response_customer_user["customerUser"]["email"])
        cgp.check_assigned_user(response_customer_user["customerUser"], 1)

        cgp.sidebar_users_and_groups()
        cgp.click_xpath(Locator.xpath_button_tab_by_name("Fobs & Passcodes"))
        cgp.wait_until_page_loaded()
        row = cgp.scan_table(response_customer_user["customerUser"]["email"], "Email", pagination=False)
        cgp.check_table_item_by_header(row, "Checkout Group", response_checkout_group["name"])

        cgp.click_xpath(Locator.xpath_button_tab_by_name("Checkout Groups"))
        cgp.wait_until_page_loaded()
        row = cgp.scan_table(response_checkout_group["name"], "Checkout Group Name", pagination=False)
        cgp.click_xpath(Locator.xpath_by_count(Locator.xpath_associated_users, row))
        cgp.unassign_user(1)
        cgp.get_element_by_xpath(Locator.xpath_no_data_found)

    @pytest.mark.regression
    def test_checkout_group_assign_shipto(self, ui, delete_shipto, delete_checkout_group):
        ui.testrail_case_id = 1863

        lp = LoginPage(ui)
        cgp = CheckoutGroupsPage(ui)

        response_checkout_group = setup_checkout_group(ui)
        response_shipto = SetupShipto(ui).setup()

        lp.log_in_customer_portal()
        cgp.sidebar_users_and_groups()
        cgp.click_xpath(Locator.xpath_button_tab_by_name("Checkout Groups"))
        cgp.wait_until_page_loaded()
        row = cgp.scan_table(response_checkout_group["name"], "Checkout Group Name", pagination=False)
        cgp.click_xpath(Locator.xpath_by_count(Locator.xpath_associated_shiptos, row))
        cgp.assign_shipto(response_shipto["shipto"]["number"])
        cgp.check_assigned_shipto(response_shipto["shipto"], 1)
        cgp.unassign_shipto(1)
        cgp.get_element_by_xpath(Locator.xpath_no_data_found)

    @pytest.mark.smoke
    def test_smoke_create_user(self, smoke_api):
        smoke_api.testrail_case_id = 2002

        ua = UserApi(smoke_api)
        user_body = {
            "email": Tools.random_email(20),
            "firstName": Tools.random_string_l(),
            "lastName": Tools.random_string_l()
        }

        user_id = ua.create_distributor_superuser(user_body)
        response = ua.get_distributor_super_user_by_email(user_body["email"])
        count = len(response)
        assert count == 1, f"Users count is {count}"
        user = response[0]
        email = user["email"]
        name = user["firstName"]
        last_name = user["lastName"]
        assert email == user_body["email"], f"User email is {email}, but should be {user_body['email']}"
        assert name == user_body["firstName"], f"User name is {name}, but should be {user_body['firstName']}"
        assert last_name == user_body["lastName"], f"User last name is {last_name}, but should be {user_body['lastName']}"
        ua.delete_user(user_id)