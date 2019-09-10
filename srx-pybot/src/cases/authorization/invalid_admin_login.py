from src.resources.case import Case
from src.resources.activity import Activity
from src.pages.sub.login_page import LoginPage

def invalid_admin_login(case):
    case.log_name("Invalid log in Admin portal")
    case.testrail_config(case.activity.variables.run_number, 7)
    lp = LoginPage(case.activity)

    lp.follow_admin_portal()
    lp.submit_button_should_be_disabled()
    lp.input_email(case.activity.data.nonexistent_email)
    lp.submit_button_should_be_disabled()
    lp.input_password(case.activity.data.nonexistent_password)
    lp.submit_button_should_be_enabled()
    lp.click_on_submit_button()
    lp.error_should_be_present()
    lp.input_email(case.activity.data.incorrect_email)
    lp.invalid_email_message_should_be_present()
    lp.clear_email()
    lp.required_email_message_should_be_present()
    lp.clear_password()
    lp.required_password_message_should_be_present()

    case.finish_case()

if __name__ == "__main__":
    invalid_admin_login(Case(Activity()))
