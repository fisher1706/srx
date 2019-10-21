from src.pages.distributor.distributor_portal_page import DistributorPortalPage
import os

class SettingsPage(DistributorPortalPage):
    def __init__(self, activity):
        super().__init__(activity)

    def import_document(self):
        start_number_of_rows = self.get_element_count(self.locators.xpath_by_count(self.locators.xpath_table, 1) + self.locators.xpath_table_row)
        self.generate_csv("doc.pdf", [[1, 2]])
        folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        folder += "/output/doc.pdf"
        self.activity.driver.find_element_by_id(self.locators.id_file_upload).send_keys(folder)
        self.should_be_present_xpath(self.locators.xpath_successfully_uploaded_document_msg)
        self.elements_count_should_be(self.locators.xpath_by_count(self.locators.xpath_table, 1) + self.locators.xpath_table_row, start_number_of_rows+1)

    def delete_last_document(self):
        start_number_of_rows = self.get_element_count(self.locators.xpath_by_count(self.locators.xpath_table, 1) + self.locators.xpath_table_row)
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_delete_document, start_number_of_rows))
        self.click_xpath(self.locators.xpath_dialog + self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.elements_count_should_be(self.locators.xpath_by_count(self.locators.xpath_table, 1) + self.locators.xpath_table_row, start_number_of_rows-1)

