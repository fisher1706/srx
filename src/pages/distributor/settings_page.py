import os
from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.locator import Locator
from src.resources.tools import Tools

class SettingsPage(DistributorPortalPage):
    def import_document(self):
        self.wait_until_page_loaded()
        start_number_of_rows = self.get_element_count(Locator.xpath_by_count(Locator.xpath_table, 1) + Locator.xpath_table_row)
        Tools.generate_csv("doc.pdf", [[1, 2]])
        folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        folder += "/output/doc.pdf"
        self.get_element_by_id(Locator.id_file_upload).send_keys(folder)
        self.get_element_by_xpath(Locator.xpath_successfully_uploaded_document_msg)
        self.elements_count_should_be(Locator.xpath_by_count(Locator.xpath_table, 1) + Locator.xpath_table_row, start_number_of_rows+1)

    def delete_last_document(self):
        start_number_of_rows = self.get_element_count(Locator.xpath_by_count(Locator.xpath_table, 1) + Locator.xpath_table_row)
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_remove_button, start_number_of_rows))
        self.click_xpath(Locator.xpath_dialog + Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.elements_count_should_be(Locator.xpath_by_count(Locator.xpath_table, 1) + Locator.xpath_table_row, start_number_of_rows-1)
