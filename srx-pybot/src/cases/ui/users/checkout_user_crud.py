from src.pages.sub.login_page import LoginPage
from src.pages.customer.checkout_users_page import CheckoutUsersPage
from src.resources.case import Case
from src.resources.activity import Activity
from src.resources.tools import Tools

def checkout_user_crud(case):
    case.log_name("Checkout user CRUD")
    case.testrail_config(case.activity.variables.run_number, 1848)

    try:
        lp = LoginPage(case.activity)
        cup = CheckoutUsersPage(case.activity)
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
        cup.click_xpath(case.activity.locators.xpath_button_tab_by_name("Fobs & Passcodes"))
        cup.create_checkout_user(checkout_user_body.copy())
        row = cup.scan_table(checkout_user_body["firstName"], "First Name", pagination=False)
        cup.check_new_checkout_user(checkout_user_body.copy(), row)
        cup.update_new_checkout_user(edit_checkout_user_body.copy(), row, first_group=True)
        cup.sidebar_users_and_groups()
        cup.click_xpath(case.activity.locators.xpath_button_tab_by_name("Fobs & Passcodes"))
        cup.wait_until_page_loaded()
        row = cup.scan_table(edit_checkout_user_body["firstName"], "First Name", pagination=False)
        cup.check_new_checkout_user(edit_checkout_user_body.copy(), row)
        cup.delete_new_checkout_user(row)

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    checkout_user_crud(Case(Activity()))