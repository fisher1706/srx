from src.pages.page import Page

class AdminPortalPage(Page):
    def __init__(self, activity):
        super().__init__(activity)
    
    def admin_sidebar_should_contain_email(self):
        self.should_be_present_xpath("//p[text()='"+self.variables.admin_email+"']")

    def sign_out(self):
        self.click_xpath("//a[@href='/sign-out']")