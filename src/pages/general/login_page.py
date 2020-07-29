from src.pages.base_page import BasePage
from src.resources.locator import Locator

class LoginPage(BasePage):
    def follow_admin_portal(self):
        self.follow_url(self.url.admin_portal)

    def follow_auth_portal(self):
        self.follow_url(self.url.auth_portal)

    def follow_checkout_portal(self):
        self.follow_url(self.url.checkout_portal)

    def input_email(self, email):
        self.input_data_id(email, Locator.id_email)

    def input_password(self, password):
        self.input_data_id(password, Locator.id_password)

    def submit_button_should_be_disabled(self):
        self.should_be_disabled_xpath(Locator.xpath_submit_button)

    def submit_button_should_be_enabled(self):
        self.should_be_enabled_xpath(Locator.xpath_submit_button)

    def click_on_submit_button(self):
        self.click_xpath(Locator.xpath_submit_button)

    def error_should_be_present(self):
        self.get_element_by_xpath("//span[text()='Incorrect email address or password.']")

    def invalid_email_message_should_be_present(self):
        self.get_element_by_xpath("//p[text()='Email must be a valid email']")

    def required_email_message_should_be_present(self):
        self.get_element_by_xpath("//p[text()='Email is a required field']")

    def required_password_message_should_be_present(self):
        self.get_element_by_xpath("//p[text()='Please enter password']")

    def clear_email(self):
        self.clear_id(Locator.id_email)

    def clear_password(self):
        self.clear_id(Locator.id_password)

    def it_should_be_login_page(self):
        self.get_element_by_xpath(Locator.xpath_forgot_password)
        self.get_element_by_id(Locator.id_email)
        self.get_element_by_id(Locator.id_password)

    def open_forgot_password_page(self):
        self.click_xpath(Locator.xpath_forgot_password)

    def incorrect_email_message_should_be_present(self):
        self.get_element_by_xpath("//span[text()='Please check if the entered email address is correct and try again.']")

    def return_from_forgot_password_page(self):
        self.click_xpath("//a[@href='/sign-in']")

    def log_in_admin_portal(self):
        self.follow_admin_portal()
        self.input_email(self.context.admin_email)
        self.input_password(self.context.admin_password)
        self.click_on_submit_button()

    def log_in_distributor_portal(self, email=None, password=None):
        self.follow_auth_portal()
        if (email is None):
            email = self.context.distributor_email
        if (password is None):
            password = self.context.distributor_password
        self.input_email(email)
        self.input_password(password)
        self.click_on_submit_button()
        self.title_should_be("SRX Distributor Portal")
        self.follow_url(self.url.distributor_portal)

    def log_in_customer_portal(self, email=None, password=None):
        self.follow_auth_portal()
        if (email is None):
            email = self.context.customer_email
        if (password is None):
            password = self.context.customer_password
        self.input_email(email)
        self.input_password(password)
        self.click_on_submit_button()
        self.title_should_be("SRX User Dashboard")
        self.follow_url(self.url.customer_portal)
        self.click_xpath(Locator.xpath_button)