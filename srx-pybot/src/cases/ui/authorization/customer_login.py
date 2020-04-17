from src.pages.sub.login_page import LoginPage
from src.pages.customer.customer_portal_page import CustomerPortalPage
from src.resources.case import Case
from src.resources.activity import Activity

def customer_login(case):
    case.log_name("Valid log in Customer portal")
    #case.testrail_config()

    try:
        lp = LoginPage(case.activity)
        cpp = CustomerPortalPage(case.activity)

        lp.follow_auth_portal()
        lp.input_email(case.activity.variables.customer_email)
        lp.input_password(case.activity.variables.customer_password)
        lp.click_on_submit_button()
        cpp.click_id(case.activity.locators.id_enter_here)
        cpp.customer_sidebar_should_contain_email()
        cpp.url_should_contain("customer")
        token = lp.get_authorization_token()

        case.finish_case()
    except:
        case.critical_finish_case()
    return token

if __name__ == "__main__":
    customer_login(Case(Activity()))