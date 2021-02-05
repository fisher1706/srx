from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.locator import Locator
import time

class DistributorSecurityGroups(DistributorPortalPage):
    distributor_security_group_body = {
        "name": None,
        "checked": None,
    }

    def open_security_groups(self):
        self.sidebar_users()
        self.click_tab_by_name("Security Groups")

    def create_security_group(self, distributor_security_group_body):
        self.click_id(Locator.id_add_button)
        self.input_by_name("name", distributor_security_group_body["name"])
        for x in range(1, 4):
            self.select_checkbox(Locator.xpath_by_count(Locator.xpath_checkbox, x))
        self.click_xpath(Locator.xpath_submit_button)
        self.wait_until_page_loaded()
        self.get_element_by_xpath(Locator.xpath_table_row)

    def check_security_group(self, distributor_security_group_body, row):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_view_button, row))
        text = self.get_element_by_xpath("//input[@name='name']").get_attribute("value")
        assert text == distributor_security_group_body["name"], f"Name contains incorrect text: {text}"
        for x in range(1, 4):
            if (distributor_security_group_body["checked"]):
                self.checkbox_should_be(Locator.xpath_by_count(Locator.xpath_checkbox, x), True)
            else:
                self.checkbox_should_be(Locator.xpath_by_count(Locator.xpath_checkbox, x), False)
        self.wait_until_page_loaded()
        self.click_xpath("//a[@href='/users-groups#security-groups']")

    def update_security_group(self, distributor_security_group_body, row):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, row-1))
        self.input_by_name("name", distributor_security_group_body["name"])
        self.click_xpath(Locator.xpath_submit_button)
        for x in range(1, 4):
            if (distributor_security_group_body["checked"]):
                self.select_checkbox(Locator.xpath_by_count(Locator.xpath_checkbox, x))
            else:
                self.unselect_checkbox(Locator.xpath_by_count(Locator.xpath_checkbox, x))
        self.click_xpath(f"({Locator.xpath_save_button})[last()]")
        self.wait_until_page_loaded()
        self.click_xpath("//a[@href='/users-groups#security-groups']")
        self.wait_until_page_loaded()

    def delete_security_group(self, distributor_security_group_body, row):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_remove_button, row-1))
        self.delete_dialog_should_be_about(distributor_security_group_body["name"])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()