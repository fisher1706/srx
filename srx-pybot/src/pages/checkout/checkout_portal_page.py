from src.pages.page import Page

class CheckoutPortalPage(Page):
    def __init__(self, activity):
        super().__init__(activity)
        self.sign_in_checkout = "//span[text()='SIGN IN']/.."

    def input_email_checkout_portal(self, email):
        self.input_by_name("login", email)

    def input_password_checkout_portal(self, password):
        self.input_by_name("password", password)

    def sign_in_checkout_portal(self):
        self.click_xpath(self.sign_in_checkout)