import pytest
from src.pages.general.login_page import LoginPage
from src.pages.admin.admin_portal_page import AdminPortalPage
from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.pages.customer.customer_portal_page import CustomerPortalPage
from src.pages.checkout.checkout_portal_page import CheckoutPortalPage
from src.resources.locator import Locator
from src.resources.permissions import Permissions

class TestAuthorization():
    @pytest.mark.regression
    def test_success_login_admin_portal(self, ui):
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
    def test_success_login_distributor_portal(self, ui):
        BaseAuthorization.base_success_login_distributor_portal(ui)

    @pytest.mark.regression
    def test_invalid_login_admin_portal(self, ui):
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
    def test_reset_password_admin_portal(self, ui):
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
    def test_success_login_distributor_portal_smoke(self, smoke_ui):
        BaseAuthorization.base_success_login_distributor_portal(smoke_ui)

    @pytest.mark.regression
    def test_success_login_customer_portal(self, ui):
        BaseAuthorization.base_success_login_customer_portal(ui)

    @pytest.mark.smoke
    def test_success_login_customer_portal_smoke(self, smoke_ui):
        BaseAuthorization.base_success_login_customer_portal(smoke_ui)

    @pytest.mark.regression
    def test_success_login_checkout_portal(self, ui):
        BaseAuthorization.base_success_login_checkout_portal(ui)

    @pytest.mark.smoke
    def test_success_login_checkout_portal_smoke(self, smoke_ui):
        BaseAuthorization.base_success_login_checkout_portal(smoke_ui)

    @pytest.mark.skip
    @pytest.mark.smoke
    def test_open_zendesk(self, smoke_ui):
        smoke_ui.testrail_case_id = 2303

        lp = LoginPage(smoke_ui)
        dpp = DistributorPortalPage(smoke_ui)

        lp.log_in_distributor_portal()
        dpp.get_element_by_xpath("//*[@href='https://storeroomlogix.zendesk.com']")
        dpp.follow_url("https://storeroomlogix.zendesk.com")
        lp.input_email(smoke_ui.distributor_email)
        lp.input_password(smoke_ui.distributor_password)
        lp.click_on_submit_button()
        dpp.get_element_by_id("user-name")

    @pytest.mark.smoke
    def test_redirect_distributor(self, smoke_ui):
        smoke_ui.testrail_case_id = 2335

        lp = LoginPage(smoke_ui)
        dpp = DistributorPortalPage(smoke_ui)

        lp.follow_url(smoke_ui.session_context.url.get_url_for_env("storeroomlogix.com", "distributor"))
        lp.url_should_be(smoke_ui.session_context.url.get_url_for_env("storeroomlogix.com/sign-in", "auth"))
        lp.input_email(smoke_ui.distributor_email)
        lp.input_password(smoke_ui.distributor_password)
        lp.follow_url(smoke_ui.session_context.url.get_url_for_env("storeroomlogix.com", "customer"))
        lp.url_should_be(smoke_ui.session_context.url.get_url_for_env("storeroomlogix.com/sign-in", "auth"))
        lp.input_email(smoke_ui.distributor_email)
        lp.input_password(smoke_ui.distributor_password)
        lp.click_on_submit_button()
        lp.url_should_be(smoke_ui.session_context.url.get_url_for_env("storeroomlogix.com/marketing", "distributor"))
        lp.get_element_by_id(Locator.id_enter_here)

        lp.follow_url(smoke_ui.session_context.url.get_url_for_env("storeroomlogix.com", "distributor"))
        lp.url_should_be(smoke_ui.session_context.url.get_url_for_env("storeroomlogix.com/customers", "distributor"))
        dpp.distributor_sidebar_should_contain_email()
        lp.follow_url(smoke_ui.session_context.url.get_url_for_env("storeroomlogix.com", "customer"))
        lp.url_should_be(smoke_ui.session_context.url.get_url_for_env("storeroomlogix.com/customers", "distributor"))
        dpp.distributor_sidebar_should_contain_email()



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