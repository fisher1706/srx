from src.pages.sub.login_page import LoginPage
from src.pages.customer.checkout_users_page import CheckoutUsersPage
from src.resources.case import Case
from src.resources.activity import Activity
from src.resources.tools import Tools

def checkout_user_import_without_group(case):
    case.log_name("Checkout user import without checkout group")
    case.testrail_config(1849)

    try:
        lp = LoginPage(case.activity)
        cup = CheckoutUsersPage(case.activity)
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
        cup.click_xpath(case.activity.locators.xpath_button_tab_by_name("Fobs & Passcodes"))
        cup.import_checkout_user(checkout_users)
        row = cup.scan_table(checkout_user_body["firstName"], "First Name", pagination=False)
        cup.check_new_checkout_user(checkout_user_body.copy(), row)
        cup.delete_new_checkout_user(row)

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    checkout_user_import_without_group(Case(Activity()))