from src.pages.base_page import BasePage

class CheckoutPortalPage(BasePage):
    def input_email_checkout_portal(self, email):
        self.input_by_name("login", email)

    def input_password_checkout_portal(self, password):
        self.input_by_name("password", password, hide_log=True)

    def sign_in_checkout_portal(self):
        self.click_xpath("//span[text()='SIGN IN']/..")