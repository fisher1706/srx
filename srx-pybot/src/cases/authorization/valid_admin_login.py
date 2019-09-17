from src.pages.sub.login_page import LoginPage
from src.pages.admin.admin_portal_page import AdminPortalPage
from src.resources.case import Case
from src.resources.activity import Activity

def valid_admin_login(case):
    case.log_name("Valid log in Admin portal")
    case.testrail_config(case.activity.variables.run_number, 9)

    try:
        lp = LoginPage(case.activity)
        app = AdminPortalPage(case.activity)

        lp.follow_admin_portal()
        lp.input_email(case.activity.variables.admin_email)
        lp.input_password(case.activity.variables.admin_password)
        lp.click_on_submit_button()
        app.admin_sidebar_should_contain_email()
        app.sign_out()
        lp.it_should_be_login_page()

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    valid_admin_login(Case(Activity()))