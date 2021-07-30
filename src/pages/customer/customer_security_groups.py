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
        self.input_by_name("name", security_group_body["name"])
        for checkbox in range(1, 4):
            self.select_checkbox(Locator.xpath_by_count(Locator.xpath_checkbox, checkbox))
        self.click_xpath(Locator.xpath_submit_button)
        self.wait_until_page_loaded()
        self.get_element_by_xpath(Locator.xpath_table_row)

    def check_security_group(self, security_group_body, row):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_view_button, row))
        text = self.get_element_by_xpath("//input[@name='name']").get_attribute("value")
        assert text == security_group_body["name"], f"Name contains incorrect text: {text}"
        for checkbox in range(1, 4):
            if security_group_body["checked"]:
                self.checkbox_should_be(Locator.xpath_by_count(Locator.xpath_checkbox, checkbox), True)
            else:
                self.checkbox_should_be(Locator.xpath_by_count(Locator.xpath_checkbox, checkbox), False)
        self.click_xpath("//a[@href='/users-and-groups#security-groups']")

    def update_security_group(self, security_group_body, row):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, row-2))
        self.wait_until_page_loaded()
        self.clear_xpath("//input[@name]")
        self.input_by_name("name", security_group_body["name"])
        self.click_xpath(Locator.xpath_submit_button)
        self.wait_until_page_loaded()
        for checkbox in range(1, 4):
            self.unselect_checkbox(Locator.xpath_by_count(Locator.xpath_checkbox, checkbox))
        self.click_xpath(f"({Locator.xpath_submit_button})[last()]")
        self.wait_until_page_loaded()
        self.click_xpath("//a[@href='/users-and-groups#security-groups']")

    def delete_security_group(self, security_group_body, row):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_remove_button, row-2))
        self.delete_dialog_should_be_about(security_group_body["name"])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
