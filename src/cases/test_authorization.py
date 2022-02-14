import pytest
from src.pages.general.login_page import LoginPage
from src.pages.admin.admin_portal_page import AdminPortalPage
from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.pages.customer.customer_portal_page import CustomerPortalPage
from src.pages.checkout.checkout_portal_page import CheckoutPortalPage
from src.pages.checkout.new_checkout_portal_page import NewCheckoutPortalPage
from src.resources.locator import Locator
from src.resources.tools import Tools

@pytest.mark.regression
def test_success_login_admin_portal(ui):
    ui.testrail_case_id = 9

    lp = LoginPage(ui)
    app = AdminPortalPage(ui)

    lp.follow_admin_portal()
    lp.input_email(ui.admin_email)
    lp.input_password(ui.admin_password)
    lp.click_on_submit_button()
    app.admin_sidebar_should_contain_email()
    app.sign_out()
    lp.it_should_be_login_page()

@pytest.mark.regression
def test_success_login_distributor_portal(ui):
    BaseAuthorization.base_success_login_distributor_portal(ui)

@pytest.mark.regression
def test_invalid_login_admin_portal(ui):
    ui.testrail_case_id = 7

    lp = LoginPage(ui)

    lp.follow_admin_portal()
    lp.input_email("example@agilevision.io")
    lp.submit_button_should_be_disabled()
    lp.input_password("example")
    lp.submit_button_should_be_enabled()
    lp.click_on_submit_button()
    lp.error_should_be_present()
    lp.input_email("example@example")
    lp.invalid_email_message_should_be_present()
    lp.clear_email()
    lp.clear_password()
    lp.required_email_message_should_be_present()
    lp.required_password_message_should_be_present()

@pytest.mark.regression
def test_invalid_login_new_checkout_portal(ui):
    ui.testrail_case_id = 4555

    lp = LoginPage(ui)
    cpp = NewCheckoutPortalPage(ui)

    lp.follow_new_checkout_portal()
    cpp.input_email_checkout_portal("example@agilevision.io")
    cpp.input_password_checkout_portal("example")
    cpp.sign_in_checkout_portal()
    cpp.wrong_user_error_should_be_present()
    cpp.clear_email()
    cpp.clear_password()
    cpp.input_email_checkout_portal(ui.customer_email)
    cpp.input_password_checkout_portal("example")
    cpp.sign_in_checkout_portal()
    cpp.wrong_password_error_should_be_present()

@pytest.mark.regression
def test_reset_password_admin_portal(ui):
    ui.testrail_case_id = 8

    lp = LoginPage(ui)

    lp.follow_admin_portal()
    lp.open_forgot_password_page()
    lp.input_email("example.test-reset-password-@agilevision.io")
    lp.submit_button_should_be_enabled()
    lp.click_on_submit_button()
    lp.get_element_by_xpath("//h2[text()='Please check your inbox']")
    lp.return_from_forgot_password_page()
    lp.it_should_be_login_page()

@pytest.mark.smoke
@pytest.mark.first
def test_success_login_distributor_portal_smoke(smoke_ui):
    BaseAuthorization.base_success_login_distributor_portal(smoke_ui)

@pytest.mark.regression
def test_success_login_customer_portal(ui):
    BaseAuthorization.base_success_login_customer_portal(ui)

@pytest.mark.smoke
def test_success_login_customer_portal_smoke(smoke_ui):
    BaseAuthorization.base_success_login_customer_portal(smoke_ui)

@pytest.mark.regression
def test_success_login_checkout_portal(ui):
    BaseAuthorization.base_success_login_checkout_portal(ui)

@pytest.mark.smoke
def test_success_login_checkout_portal_smoke(smoke_ui):
    BaseAuthorization.base_success_login_checkout_portal(smoke_ui)

@pytest.mark.regression
def test_success_login_new_checkout_portal(ui):
    BaseAuthorization.base_success_login_new_checkout(ui)

@pytest.mark.skip
@pytest.mark.smoke
def test_success_login_new_checkout_portal_smoke(smoke_ui):
    BaseAuthorization.base_success_login_new_checkout(smoke_ui)

@pytest.mark.skip
@pytest.mark.smoke
def test_open_zendesk_from_distributor(smoke_ui):
    smoke_ui.testrail_case_id = 2303

    lp = LoginPage(smoke_ui)
    dpp = DistributorPortalPage(smoke_ui)

    lp.log_in_distributor_portal(expected_url=smoke_ui.session_context.url.get_url_for_env("storeroomlogix.com/customers", "distributor"))
    dpp.get_element_by_xpath("//*[@href='https://storeroomlogix.zendesk.com']")
    dpp.follow_url("https://storeroomlogix.zendesk.com")
    dpp.get_element_by_id("user-name")

@pytest.mark.skip
@pytest.mark.smoke
def test_open_zendesk_from_customer(smoke_ui):
    smoke_ui.testrail_case_id = 4739

    lp = LoginPage(smoke_ui)
    cpp = CustomerPortalPage(smoke_ui)

    lp.log_in_customer_portal()
    cpp.get_element_by_xpath("//*[@href='https://storeroomlogix.zendesk.com']")
    cpp.follow_url("https://storeroomlogix.zendesk.com")
    cpp.get_element_by_id("user-name")

@pytest.mark.smoke
def test_redirect_distributor(smoke_ui):
    smoke_ui.testrail_case_id = 2335

    lp = LoginPage(smoke_ui)
    dpp = DistributorPortalPage(smoke_ui)

    url = smoke_ui.session_context.url

    lp.follow_url(url.distributor_portal)
    lp.url_should_be(url.auth_portal+"/sign-in")
    lp.input_email(smoke_ui.distributor_email)
    lp.input_password(smoke_ui.distributor_password)
    lp.follow_url(url.customer_portal)
    lp.url_should_be(url.auth_portal+"/sign-in")
    lp.input_email(smoke_ui.distributor_email)
    lp.input_password(smoke_ui.distributor_password)
    lp.click_on_submit_button()
    lp.url_should_be(url.distributor_portal+"/marketing")
    lp.get_element_by_id(Locator.id_enter_here)

    lp.follow_url(url.distributor_portal, url.distributor_portal+"/customers")
    lp.url_should_be(url.distributor_portal+"/customers")
    dpp.distributor_sidebar_should_contain_email()
    lp.follow_url(url.customer_portal, url.distributor_portal+"/customers")
    lp.url_should_be(url.distributor_portal+"/customers")
    dpp.distributor_sidebar_should_contain_email()

@pytest.mark.regression
def test_log_out_checkout_portal(ui):
    ui.testrail_case_id = 4558

    lp = LoginPage(ui)
    cpp = NewCheckoutPortalPage(ui)

    lp.follow_new_checkout_portal()
    cpp.input_email_checkout_portal(ui.customer_email)
    cpp.input_password_checkout_portal(ui.customer_password)
    cpp.sign_in_checkout_portal()
    cpp.open_hide_menu()
    cpp.log_out_checkout_portal()
    lp.url_should_be(f"{ui.session_context.url.new_checkout_portal}/auth")

@pytest.mark.regression
def test_log_in_checkout_passcode(ui):
    ui.testrail_case_id = 4556

    lp = LoginPage(ui)
    cpp = NewCheckoutPortalPage(ui)

    lp.follow_new_checkout_portal()
    cpp.input_email_checkout_portal(ui.checkout_group_email)
    cpp.input_password_checkout_portal(ui.checkout_group_password)
    cpp.sign_in_checkout_portal()
    cpp.input_passcode(ui.data.passcode)
    cpp.sign_in_checkout_portal()
    lp.url_should_be(f"{ui.session_context.url.new_checkout_portal}/dashboard")

@pytest.mark.regression
def test_log_out_checkout_passcode(ui):
    ui.testrail_case_id = 4559

    lp = LoginPage(ui)
    cpp = NewCheckoutPortalPage(ui)

    lp.follow_new_checkout_portal()
    cpp.input_email_checkout_portal(ui.checkout_group_email)
    cpp.input_password_checkout_portal(ui.checkout_group_password)
    cpp.sign_in_checkout_portal()
    cpp.input_passcode(ui.data.passcode)
    cpp.sign_in_checkout_portal()
    cpp.open_hide_menu()
    cpp.log_out_checkout_portal()
    lp.url_should_be(f"{ui.session_context.url.new_checkout_portal}/auth")
    cpp.log_out_checkout_groupe()

@pytest.mark.regression
def test_invalid_log_in_passcode(ui):
    ui.testrail_case_id = 4557

    lp = LoginPage(ui)
    cpp = NewCheckoutPortalPage(ui)

    lp.follow_new_checkout_portal()
    cpp.input_email_checkout_portal(ui.checkout_group_email)
    cpp.input_password_checkout_portal(ui.checkout_group_password)
    cpp.sign_in_checkout_portal()
    cpp.input_passcode(Tools.random_string_l(3))
    cpp.sign_in_checkout_portal()
    cpp.wrong_passcode_error_should_be_present()

class BaseAuthorization():

    @staticmethod
    def base_success_login_distributor_portal(context):
        context.testrail_case_id = 1971

        lp = LoginPage(context)
        dpp = DistributorPortalPage(context)

        lp.follow_auth_portal()
        lp.input_email(context.distributor_email)
        lp.input_password(context.distributor_password)
        lp.click_on_submit_button()
        dpp.click_id(Locator.id_enter_here, timeout=30)
        dpp.distributor_sidebar_should_contain_email()
        dpp.url_should_contain("distributor")
        context.session_context.smoke_distributor_token = dpp.get_authorization_token()

    @staticmethod
    def base_success_login_customer_portal(context):
        context.testrail_case_id = 1974

        lp = LoginPage(context)
        cpp = CustomerPortalPage(context)

        lp.follow_auth_portal()
        lp.input_email(context.customer_email)
        lp.input_password(context.customer_password)
        lp.click_on_submit_button()
        cpp.click_id(Locator.id_enter_here, timeout=30)
        cpp.customer_sidebar_should_contain_email()
        cpp.url_should_contain("customer")

    @staticmethod
    def base_success_login_checkout_portal(context):
        context.testrail_case_id = 1975

        lp = LoginPage(context)
        cpp = CheckoutPortalPage(context)

        lp.follow_checkout_portal()
        cpp.input_email_checkout_portal(context.customer_email)
        cpp.input_password_checkout_portal(context.customer_password)
        cpp.sign_in_checkout_portal()
        lp.url_should_be(f"{context.session_context.url.checkout_portal}/actions")

    @staticmethod
    def base_success_login_new_checkout(context):
        context.testrail_case_id = 4554

        lp = LoginPage(context)
        cpp = NewCheckoutPortalPage(context)

        lp.follow_new_checkout_portal()
        cpp.input_email_checkout_portal(context.customer_email)
        cpp.input_password_checkout_portal(context.customer_password)
        cpp.sign_in_checkout_portal()
        lp.url_should_be(f"{context.session_context.url.new_checkout_portal}/dashboard")
