from src.pages.sub.login_page import LoginPage
from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.case import Case
from src.resources.activity import Activity


def distributor_login(case):
    case.log_name("Valid log in Distributor portal")
    #case.testrail_config()

    try:
        lp = LoginPage(case.activity)
        dpp = DistributorPortalPage(case.activity)

        lp.follow_auth_portal()
        lp.input_email(case.activity.variables.distributor_email)
        lp.input_password(case.activity.variables.distributor_password)
        lp.click_on_submit_button()
        dpp.click_id(case.activity.locators.id_enter_here)
        dpp.distributor_sidebar_should_contain_email()
        dpp.url_should_contain("distributor")
        token = dpp.get_authorization_token()

        case.finish_case()
    except:
        case.critical_finish_case()
    return token

if __name__ == "__main__":
    distributor_login(Case(Activity()))