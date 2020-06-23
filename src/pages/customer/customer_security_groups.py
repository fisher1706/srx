from src.pages.customer.customer_portal_page import CustomerPortalPage
from src.resources.locator import Locator

class CustomerSecurityGroups(CustomerPortalPage):
    security_group_body = {
        "name": None,
        "checked": None,
    }

    def open_security_groups(self):
        self.sidebar_users_and_groups()
        self.click_tab_by_name("Security Groups")

    def create_security_group(self, security_group_body):
        self.click_id(Locator.id_add_button)
        self.wait_until_progress_bar_loaded()
        self.input_by_name("name", security_group_body["name"])
        self.click_xpath(Locator.xpath_submit_button)
        self.wait_until_progress_bar_loaded(7)

    def check_security_group(self, security_group_body, row):
        self.click_xpath(Locator.xpath_table_item(row, 1))
        self.wait_until_progress_bar_loaded()
        text = self.get_element_by_xpath("//input[@name='name']").get_attribute("value")
        assert text == security_group_body["name"], f"Name contains incorrect text: {text}"
        for x in range(1, 4):
            if (security_group_body["checked"] is True):
                self.checkbox_should_be(Locator.xpath_by_count(Locator.xpath_checkbox, x), True)
            elif (security_group_body["checked"] is False):
                self.checkbox_should_be(Locator.xpath_by_count(Locator.xpath_checkbox, x), False)
        self.click_xpath("//a[@href='/users-and-groups#security-groups']")
    
    def update_security_group(self, security_group_body, row):
        self.click_xpath(Locator.xpath_table_item(row, 1))
        self.wait_until_progress_bar_loaded()
        self.input_by_name("name", security_group_body["name"])
        self.click_xpath(Locator.xpath_submit_button)
        self.wait_until_progress_bar_loaded()
        for x in range(1, 4):
            if (security_group_body["checked"] is True):
                self.select_checkbox(Locator.xpath_by_count(Locator.xpath_checkbox, x))
            if (security_group_body["checked"] is False):
                self.unselect_checkbox(Locator.xpath_by_count(Locator.xpath_checkbox, x))
        self.click_xpath(f"({Locator.xpath_submit_button})[last()]")
        self.wait_until_progress_bar_loaded()
        self.click_xpath("//a[@href='/users-and-groups#security-groups']")
        self.wait_until_progress_bar_loaded(7)

    def delete_security_group(self, security_group_body, row):
        self.click_table_title(Locator.title_delete_security_group, row)
        self.delete_dialog_should_be_about(security_group_body["name"])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
