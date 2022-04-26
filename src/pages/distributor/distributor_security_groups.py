from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.locator import Locator
from src.api.distributor.user_api import UserApi

class DistributorSecurityGroups(DistributorPortalPage):
    distributor_security_group_body = {
        "name": None,
        "checked": None,
    }

    def open_security_groups(self):
        self.sidebar_users()
        self.click_tab_by_name("Security Groups")

    def create_security_group(self, distributor_security_group_body):
        ua = UserApi(self.context)
        start_number_of_rows = ua.get_security_groups()['totalElements']
        self.click_id(Locator.id_add_button)
        self.input_by_name("name", distributor_security_group_body["name"])
        for checkbox in range(1, 4):
            self.select_checkbox(Locator.xpath_by_count(Locator.xpath_checkbox, checkbox))
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.last_page(10)
        self.element_should_have_text(Locator.xpath_get_table_item_by_index(start_number_of_rows%10, 1), distributor_security_group_body["name"])

    def check_security_group(self, distributor_security_group_body):
        self.click_xpath(Locator.xpath_last_role_row + Locator.xpath_view_button)
        text = self.get_element_by_xpath("//input[@name='name']").get_attribute("value")
        assert text == distributor_security_group_body["name"], f"Name contains incorrect text: {text}"
        for checkbox in range(1, 4):
            if distributor_security_group_body["checked"]:
                self.checkbox_should_be(Locator.xpath_by_count(Locator.xpath_checkbox, checkbox), True)
            else:
                self.checkbox_should_be(Locator.xpath_by_count(Locator.xpath_checkbox, checkbox), False)
        self.click_xpath("//a[@href='/distributor/users-groups#security-groups']")
        self.last_page()
        self.element_should_have_text(Locator.xpath_get_last_table_item(1), distributor_security_group_body["name"])

    def update_security_group(self, distributor_security_group_body):
        self.click_xpath(Locator.xpath_last_role_row + Locator.xpath_edit_button)
        self.input_by_name("name", distributor_security_group_body["name"])
        self.click_xpath(Locator.xpath_submit_button)
        for checkbox in range(1, 4):
            if distributor_security_group_body["checked"]:
                self.select_checkbox(Locator.xpath_by_count(Locator.xpath_checkbox, checkbox))
            else:
                self.unselect_checkbox(Locator.xpath_by_count(Locator.xpath_checkbox, checkbox))
        self.click_xpath(f"({Locator.xpath_save_button})[last()]")
        self.check_reset_permissions()
        self.click_xpath("//a[@href='/distributor/users-groups#security-groups']")
        self.click_xpath(Locator.xpath_reload_button)
        self.last_page()
        self.element_should_have_text(Locator.xpath_get_last_table_item(1), distributor_security_group_body["name"])

    def delete_security_group(self, distributor_security_group_body):
        self.click_xpath(Locator.xpath_last_role_row + Locator.xpath_remove_button)
        self.delete_dialog_should_be_about(distributor_security_group_body["name"])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def check_reset_permissions(self):
        for checkbox in range(5, 36):
            self.select_checkbox(Locator.xpath_by_count(Locator.xpath_checkbox, checkbox))
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_button_reset, 2))
        for checkbox in range(5, 36):
            self.checkbox_should_be(Locator.xpath_by_count(Locator.xpath_checkbox, checkbox), False)
