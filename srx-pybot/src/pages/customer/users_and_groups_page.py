from src.pages.customer.customer_portal_page import CustomerPortalPage

class UsersGroups(CustomerPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.security_group_body = {
            "name": None,
            "checked": None,
        }

    def open_security_groups(self):
        self.sidebar_users_and_groups()
        self.click_tab_by_name("Security Groups")

    def create_security_group(self, security_group_body):
        self.click_id(self.locators.id_add_button)
        self.wait_until_progress_bar_loaded()
        self.input_by_name("name", security_group_body["name"])
        self.click_xpath(self.locators.xpath_submit_button)
        self.wait_until_progress_bar_loaded(7)
        self.wait_until_page_loaded()

    def check_security_group(self, security_group_body, row):
        self.click_xpath(self.locators.xpath_table_item(row, 1))
        self.wait_until_progress_bar_loaded()
        text = self.get_element_xpath("//input[@name='name']").get_attribute("value")
        assert text == security_group_body["name"], f"Name contains incorrect text: {text}"
        for x in range(1, 4):
            if (security_group_body["checked"] is True):
                self.checkbox_should_be(self.locators.xpath_by_count(self.locators.xpath_checkbox, x), True)
            elif (security_group_body["checked"] is False):
                self.checkbox_should_be(self.locators.xpath_by_count(self.locators.xpath_checkbox, x), False)
        self.click_xpath("//a[@href='/users-and-groups#security-groups']")
        self.wait_until_progress_bar_loaded()
    
    def update_security_group(self, security_group_body, row):
        self.click_xpath(self.locators.xpath_table_item(row, 1))
        self.wait_until_progress_bar_loaded()
        self.input_by_name("name", security_group_body["name"])
        for x in range(1, 4):
            if (security_group_body["checked"] is True):
                self.select_checkbox(self.locators.xpath_by_count(self.locators.xpath_checkbox, x))
            if (security_group_body["checked"] is False):
                self.unselect_checkbox(self.locators.xpath_by_count(self.locators.xpath_checkbox, x))
        self.click_xpath(self.locators.xpath_submit_button)
        self.click_xpath(self.locators.xpath_by_count(self.locators.xpath_submit_button, 2))
        self.wait_until_progress_bar_loaded(7)
        self.click_xpath("//a[@href='/users-and-groups#security-groups']")
        self.wait_until_progress_bar_loaded(7)

    def delete_security_group(self, security_group_body, row):
        self.click_table_title(self.locators.title_delete_security_group, row)
        self.delete_dialog_should_be_about(security_group_body["name"])
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
