from src.pages.base_page import BasePage

class NewCheckoutPortalPage(BasePage):
    def input_email_checkout_portal(self, email):
        self.input_by_name("email", email)

    def input_password_checkout_portal(self, password):
        self.input_by_name("password", password, hide_log=True)
    
    def input_passcode(self,passcode):
        self.input_by_name("passcode",passcode, hide_log=True)

    def sign_in_checkout_portal(self):
        self.click_xpath("//div[@class='submit-container']")
        self.wait_until_page_loaded()

    def log_out_checkout_portal(self):
        self.click_xpath("//*[@class='item md item-lines-none in-list ion-activatable ion-focusable hydrated']")

    def log_out_checkout_groupe(self):
        self.click_xpath("//*[@class='sc-ion-buttons-md-h sc-ion-buttons-md-s md hydrated']")
        self.click_xpath("//*[@id='ion-overlay-1']/div[2]/div[2]/srx-checkout-group-popover/ion-list/ion-item")
        self.click_xpath("//*[@class ='alert-button ion-focusable ion-activatable alert-button-role-ok sc-ion-alert-md']")

    def select_issue(self):
        self.wait_until_page_loaded()
        self.click_xpath("//*[@class='md ion-activatable hydrated'][1]")
    
    def select_return(self):
        self.wait_until_page_loaded()
        self.click_xpath("//*[@class='md ion-activatable hydrated'][2]")

    def open_hide_menu(self):
        self.wait_until_page_loaded()
        self.click_xpath("//*[@class='md button in-toolbar ion-activatable ion-focusable hydrated']")

    def clear_email(self):
        self.clear_xpath("//input[@name='email']")

    def clear_password(self):
        self.clear_xpath("//input[@name='password']")

    def wrong_user_error_should_be_present(self):
       assert self.get_element_text("//div[@class='error-container']") == "PreAuthentication failed with error User does not exist.."

    def wrong_password_error_should_be_present(self):
       assert self.get_element_text("//div[@class='error-container']") == "Incorrect username or password."

    def wrong_passcode_error_should_be_present(self):
       assert self.get_element_text("//div[@class='error-container']") == "User doesnˈt have permissions to complete this action."

    def signin_button_should_be_disabled(self):
        self.should_be_disabled_xpath("//div[@class='submit-container']")
