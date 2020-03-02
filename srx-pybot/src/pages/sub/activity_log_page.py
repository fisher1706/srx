from src.pages.page import Page

class ActivityLogPage(Page):
    def __init__(self, activity):
        super().__init__(activity)

    def get_full_activity_log_row(self, row_number):
        self.expand_activity_log_row(row_number)
        expanded_row_xpath = f"({self.locators.xpath_by_count(self.locators.xpath_table, 1)}{self.locators.xpath_table_row})[{row_number}]{self.locators.xpath_table_row}"
        expanded_rows_number = len(self.activity.driver.find_elements_by_xpath(expanded_row_xpath))
        expanded_rows_text = dict()
        for index in range(1, expanded_rows_number+1):
            expanded_colum_xpath = self.locators.xpath_by_count(expanded_row_xpath, index)+self.locators.xpath_table_column
            expanded_rows_text[self.get_element_text(self.locators.xpath_by_count(expanded_colum_xpath, 1))]=self.get_element_text(self.locators.xpath_by_count(expanded_colum_xpath, 2))
        return self.get_main_activity_log_row(row_number), expanded_rows_text

    def get_main_activity_log_row(self, row_number):
        header_objects = self.activity.driver.find_elements_by_xpath(self.locators.xpath_table_header_column)
        del header_objects[0]
        headers_text = list()
        for header in header_objects:
            headers_text.append(header.text)
        row_objects = self.activity.driver.find_elements_by_xpath(f"(({self.locators.xpath_by_count(self.locators.xpath_table, 1)}{self.locators.xpath_table_row})[{row_number}]{self.locators.xpath_role_row})[1]{self.locators.xpath_table_column}")
        del row_objects[0]
        rows_text = list()
        for row in row_objects:
            rows_text.append(row.text)
        return dict(zip(headers_text, rows_text))

    def expand_activity_log_row(self, row_number):
        expanding_xpath = self.locators.xpath_table_item(row_number, 1, sub_xpath=self.locators.xpath_by_count(self.locators.xpath_table, 1))
        expanding_element = self.get_element_xpath(f"{expanding_xpath}/div/div")
        if (expanding_element.get_attribute('class') == "rt-expander -open"):
            self.logger.info("Row '"+str(row_number)+"' already expanded")
        elif (expanding_element.get_attribute('class') == "rt-expander"):
            self.click_xpath(expanding_xpath)
        else:
            self.logger.error("Incorrect attribute of expanding element")

    def get_full_last_activity_log(self):
        return self.get_full_activity_log_row(1)

    def check_activity_log_row(self, row_number, expected_main_body, expected_expanded_body=None):
        if (expected_expanded_body is not None):
            actual_main_body, actual_expanded_body = self.get_full_activity_log_row(row_number)
            for key in expected_expanded_body.keys():
                assert expected_expanded_body[key] == actual_expanded_body[key], f"{key} value in Activity Log is '{actual_expanded_body[key]}', but should be '{expected_expanded_body[key]}'"
        else:
            actual_main_body = self.get_main_activity_log_row(row_number)
            for key in expected_main_body.keys():
                assert expected_main_body[key] == actual_main_body[key], f"{key} value in Activity Log is '{actual_main_body[key]}', but should be '{expected_main_body[key]}'"

    def check_last_activity_log(self, expected_main_body, expected_expanded_body=None):
        self.check_activity_log_row(1, expected_main_body, expected_expanded_body)
