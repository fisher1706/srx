from src.pages.sub.login_page import LoginPage
from src.pages.checkout.checkout_portal_page import CheckoutPortalPage
from src.resources.case import Case
from src.resources.activity import Activity

def checkout_login(case):
    case.log_name("Valid log in Checkout portal")
    #case.testrail_config()

    try:
        lp = LoginPage(case.activity)
        cpp = CheckoutPortalPage(case.activity)

        lp.follow_checkout_portal()
        cpp.input_email_checkout_portal(case.activity.variables.customer_email)
        cpp.input_password_checkout_portal(case.activity.variables.customer_password)
        cpp.sign_in_checkout_portal()
        cpp.should_be_present_xpath("//*[text()=' Issue ']")
        lp.url_should_contain("checkout")

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    checkout_login(Case(Activity()))