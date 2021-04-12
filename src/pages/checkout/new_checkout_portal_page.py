from src.pages.base_page import BasePage

class NewCheckoutPortalPage(BasePage):
    def input_email_checkout_portal(self, email):
        self.input_by_name("email", email)

    def input_password_checkout_portal(self, password):
        self.input_by_name("password", password, hide_log=True)

    def sign_in_checkout_portal(self):
        self.click_xpath("//div[@class='submit-container']")

    def clear_email(self):
        self.clear_xpath("//input[@name='email']")

    def clear_password(self):
        self.clear_xpath("//input[@name='password']")

    def wrong_user_error_should_be_present(self):
       assert self.get_element_text("//div[@class='error-container']") == "PreAuthentication failed with error User does not exist.."

    def wrong_password_error_should_be_present(self):
       assert self.get_element_text("//div[@class='error-container']") == "Incorrect username or password."

    def signin_button_should_be_disabled(self):
        self.should_be_disabled_xpath("//div[@class='submit-container']")
