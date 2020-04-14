from src.pages.sub.login_page import LoginPage
from src.pages.customer.customer_users_page import CustomerUsersPage
from src.resources.case import Case
from src.resources.activity import Activity
from src.resources.tools import Tools

def customer_user_crud(case):
    case.log_name("Customer user CRUD")
    case.testrail_config(37)

    try:
        lp = LoginPage(case.activity)
        cup = CustomerUsersPage(case.activity)
        customer_user_body = cup.customer_user_body.copy()
        edit_customer_user_body = cup.customer_user_body.copy()

        #-------------------
        customer_user_body["email"] = Tools.random_email()
        customer_user_body["firstName"] = f"User {Tools.random_string_l()}"
        customer_user_body["lastName"] = f"User {Tools.random_string_l()}"
        customer_user_body["role"] = "User"
        customer_user_body["shiptos"] = [case.activity.variables.shipto_number]
        #-------------------
        edit_customer_user_body["firstName"] = f"User {Tools.random_string_l()}"
        edit_customer_user_body["lastName"] = f"User {Tools.random_string_l()}"
        edit_customer_user_body["role"] = "Customer Super User"
        #-------------------

        lp.log_in_customer_portal()
        cup.sidebar_users_and_groups()
        cup.click_xpath(case.activity.locators.xpath_button_tab_by_name("Users"))
        cup.create_customer_user(customer_user_body.copy())
        cup.check_last_customer_user(customer_user_body.copy())
        cup.update_last_customer_user(edit_customer_user_body.copy())
        cup.sidebar_users_and_groups()
        cup.wait_until_page_loaded()
        cup.check_last_customer_user(edit_customer_user_body.copy())
        cup.delete_last_customer_user()

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    customer_user_crud(Case(Activity()))