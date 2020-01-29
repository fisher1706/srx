from src.pages.page import Page
from src.waits.not_first_page_bootstrap import not_first_page_bootstrap
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

class AdminPortalPage(Page):
    def __init__(self, activity):
        super().__init__(activity)
    
    def admin_sidebar_should_contain_email(self):
        self.should_be_present_xpath("//span[text()='"+self.variables.admin_email+"']")

    def sign_out(self):
        self.click_id("sidebar-sign-out")

    def sidebar_hardware(self):
        self.click_id("sidebar-hardware")

    def sidebar_universal_catalog(self):
        self.click_id("sidebar-universal-catalog")

    def get_table_rows_number_bootstrap(self):
        return len(self.activity.driver.find_elements_by_xpath(self.locators.bootstrap_table_row))

    def get_header_column_bootstrap(self, header):
        headers = self.activity.driver.find_elements_by_xpath(self.locators.bootstrap_table_header_column)
        for index, item in enumerate(headers):
            if (item.text == header):
                return index+1
        else:
            return False

    def get_table_item_text_by_indexes_bootstrap(self, row, column):
        xpath = self.locators.xpath_table_item_bootstrap(row, column)
        return self.get_element_text(xpath)

    def get_last_table_item_text_by_header_bootstrap(self, header):
        column = self.get_header_column_bootstrap(header)
        if (column):
            return self.get_table_item_text_by_indexes_bootstrap(self.get_table_rows_number_bootstrap(), column)
        else:
            self.logger.error("There is no header '"+header+"'")

    def check_last_table_item_by_header_bootstrap(self, header, expected_text):
        if (expected_text is not None):
            current_text = self.get_last_table_item_text_by_header_bootstrap(header)
            if isinstance(expected_text, list):
                correctness = True
                for element in expected_text:
                    if (element not in current_text):
                        self.logger.error("Last list element in '"+header+"' column is incorrect")
                        correctness = False
                        break
                if (correctness == True):
                    self.logger.info("Last element in '"+header+"' column is correct")
            else:
                if (current_text == expected_text):
                    self.logger.info("Last element in '"+header+"' column is correct")
                else:
                    self.logger.error("Last element in '"+str(header)+"' column is '"+str(current_text)+"', but should be '"+str(expected_text)+"'")

    def open_last_page_bootstrap(self):
        if (self.get_element_count(self.locators.class_pagination_bar+"/li") > 1): #there are more than 1 pages
            title_of_current_page = self.activity.driver.find_element_by_xpath("//li[@class='active page-item']").get_attribute("title")
            pages = self.activity.driver.find_elements_by_xpath("//li[@class='page-item']")
            for page in pages:
                title = page.get_attribute("title")
                if (title != "next page"):
                    title_of_last_page = title
                else:
                    break
            if (title_of_current_page < title_of_last_page): #not last page is selected now
                pages_count = self.get_element_count(self.locators.class_page_item)
                if (pages_count >= 6):
                    self.click_xpath("//li[@title='last page']/a")
                else:
                    self.click_xpath(self.locators.xpath_by_count(self.locators.class_page_item, pages_count-1)+"/a")
                    try:
                        WebDriverWait(self.driver, 15).until(not_first_page_bootstrap())
                    except TimeoutException:
                        self.logger.error("Last page is not opened")
                    else:
                        self.logger.info("Last page is opened")