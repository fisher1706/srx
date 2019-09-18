from src.pages.sub.login_page import LoginPage
from src.resources.case import Case
from src.resources.activity import Activity

def reset_admin_password(case):
    case.log_name("Check the Reset Password form on Admin portal")
    case.testrail_config(case.activity.variables.run_number, 8)

    try:
        lp = LoginPage(case.activity)

        lp.follow_admin_portal()
        lp.open_forgot_password_page()
        lp.submit_button_should_be_disabled()
        lp.input_email(case.activity.data.nonexistent_email)
        lp.submit_button_should_be_enabled()
        lp.click_on_submit_button()
        lp.incorrect_email_message_should_be_present()
        lp.input_email(case.activity.data.incorrect_email)
        lp.invalid_email_message_should_be_present()
        lp.submit_button_should_be_disabled()
        lp.return_from_forgot_password_page()
        lp.it_should_be_login_page()

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    reset_admin_password(Case(Activity()))