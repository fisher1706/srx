from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from src.waits.dialog_is_not_present import dialog_is_not_present
from src.waits.new_element_in_table import new_element_in_table
from src.waits.last_page import last_page
from src.waits.is_page_loading import is_page_loading
from src.waits.elements_count_should_be import elements_count_should_be
import csv
import os

class Page():
    def __init__(self, activity):
        self.driver = activity.driver
        self.logger = activity.logger
        self.url = activity.url
        self.locators = activity.locators
        self.variables = activity.variables
        self.activity = activity
    
    def click_id(self, id):
        try:
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, id))).click()
        except NoSuchElementException:
            self.logger.error("Element with ID = '"+id+"' not found")
        except:
            self.logger.error("Element with ID = '"+id+"' is not clickable")
        else:
            self.logger.info("Element with ID = '"+id+"' is clicked")

    def click_xpath(self, xpath):
        try:
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        except NoSuchElementException:
            self.logger.error("Element with XPATH = '"+xpath+"' not found")
        except:
            self.logger.error("Element with XPATH = '"+xpath+"' is not clickable")
        else:
            self.logger.info("Element with XPATH = '"+xpath+"' is clicked")

    def input_data_id(self, data, id):
        try:
            element = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.ID, id))
            )
        except NoSuchElementException:
            self.logger.error("Element with ID = '"+id+"' not found")
        except:
            self.logger.error("Data '"+data+"' was not inputed into element with ID = '"+id+"'")
        else:
            element.clear()
            element.send_keys(data)
            self.logger.info("Data '"+data+"' inputed into element with ID = '"+id+"'")

    def input_data_xpath(self, data, xpath):
            element = self.get_element_xpath(xpath)
            element.clear()
            element.send_keys(data)
            self.logger.info("Data '"+data+"' inputed into element with XPATH = '"+xpath+"'")

    def get_element_xpath(self, xpath):
        try:
            element = self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            self.logger.error("Element with XPATH = '"+xpath+"' not found")
        except:
            self.logger.error("It's not possible to get element with XPATH = '"+xpath+"'")
        else:
            return element

    def input_by_name(self, name, data):
        if (data is not None):
            self.input_data_xpath(data, "//input[@name='"+name+"']")

    def should_be_disabled_id(self, id):
        try:
            element = self.driver.find_element_by_id(id)
        except NoSuchElementException:
            self.logger.error("Element with ID = '"+id+"' not found")
        else:
            if(element.is_enabled()==True):
                self.logger.error("Element with ID = '"+id+"' is enabled, but should be disabled")
            else:
                self.logger.info("Element with ID = '"+id+"' is disabled, as should")

    def should_be_disabled_xpath(self, xpath):
        try:
            element = self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            self.logger.error("Element with XPATH = '"+xpath+"' not found")
        else:
            if(element.is_enabled()==True):
                self.logger.error("Element with XPATH = '"+xpath+"' is enabled, but should be disabled")
            else:
                self.logger.info("Element with XPATH = '"+xpath+"' is disabled, as should")

    def should_be_enabled_id(self, id):
        try:
            element = self.driver.find_element_by_id(id)
        except NoSuchElementException:
            self.logger.error("Element with ID = '"+id+"' not found")
        else:
            if(element.is_enabled()==False):
                self.logger.error("Element with ID = '"+id+"' is disabled, but should be enabled")
            else:
                self.logger.info("Element with ID = '"+id+"' is enabled, as should")

    def should_be_enabled_xpath(self, xpath):
        try:
            element = self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            self.logger.error("Element with XPATH = '"+xpath+"' not found")
        else:
            if(element.is_enabled()==False):
                self.logger.error("Element with XPATH = '"+xpath+"' is disabled, but should be enabled")
            else:
                self.logger.info("Element with XPATH = '"+xpath+"' is enabled, as should")

    def should_be_present_id(self, id):
        try:
            self.activity.driver.find_element_by_id(id)
        except NoSuchElementException:
            self.logger.error("Element with ID = '"+id+"' not found")
        else:
            self.logger.info("Element with ID = '"+id+"' is present")

    def should_be_present_xpath(self, xpath):
        try:
            self.activity.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            self.logger.error("Element with XPATH = '"+xpath+"' not found")
        else:
            self.logger.info("Element with XPATH = '"+xpath+"' is present")

    def clear_id(self, id):
        try:
            self.activity.driver.find_element_by_id(id).clear()
        except NoSuchElementException:
            self.logger.error("Element with ID = '"+id+"' not found")
        else:
            self.logger.info("Element with ID = '"+id+"' is cleared")

    def clear_xpath(self, xpath):
        try:
            self.activity.driver.find_element_by_xpath(xpath).clear()
        except NoSuchElementException:
            self.logger.error("Element with XPATH = '"+xpath+"' not found")
        else:
            self.logger.info("Element with XPATH = '"+xpath+"' is cleared")

    def follow_url(self, url):
        try:
            self.driver.get(url)
        except:
            self.logger.error("Error during try to follow URL = '"+url+"'")
        else:
            self.logger.info("URL = '"+url+"' is followed")

    def title_should_be(self, title):
        try:
            element = WebDriverWait(self.driver, 15).until(
                EC.title_is(title)
            )
        except:
            self.logger.error("Title should be '"+title+"', but now it is '"+self.driver.title+"'")
        else:
            self.logger.info("Title is '"+title+"'")

    def select_checkbox(self, xpath):
        try:
            element = self.activity.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            self.logger.error("Checkbox with XPATH = '"+xpath+"' not found")
        else:
            checked = element.get_attribute("checked")
            if (checked == 'true'):
                self.logger.info("Checkbox with XPATH = '"+xpath+"' has been already checked")
            elif (checked is None):
                element.click()
                self.logger.info("Checkbox with XPATH = '"+xpath+"' is checked")

    def unselect_checkbox(self, xpath):
        try:
            element = self.activity.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            self.logger.error("Checkbox with XPATH = '"+xpath+"' not found")
        else:
            checked = element.get_attribute("checked")
            if (checked == 'true'):
                element.click()
                self.logger.info("Checkbox with XPATH = '"+xpath+"' is unchecked")
            elif (checked is None):
                self.logger.info("Checkbox with XPATH = '"+xpath+"' has been already unchecked")

    def select_checkbox_in_dialog_by_name(self, name):
        self.select_checkbox(self.locators.xpath_checkbox_in_dialog_by_name(name))

    def clear_all_selectboxes_in_dialog(self):
        try:
            checkboxes = self.activity.driver.find_elements_by_xpath(self.locators.xpath_dialog+self.locators.xpath_checkbox)
        except:
            self.logger.error("Checkboxes in dialog not found")
        else:
            for element in checkboxes:
                checked = element.get_attribute("checked")
                if (checked == 'true'):
                    element.click()

    def select_in_dropdown(self, xpath, name):
        if (name is not None):
            try:
                element = self.activity.driver.find_element_by_xpath(xpath)
            except NoSuchElementException:
                self.logger.error("Dropdown list with XPATH = '"+xpath+"' not found")
            else:
                element.click()
                self.logger.info("Dropdown list with XPATH = '"+xpath+"' is opened")
                self.click_xpath(xpath+"/..//div[text()='"+name+"']")

    def dialog_should_not_be_visible(self):
        try:
            WebDriverWait(self.driver, 15).until(dialog_is_not_present())
        except TimeoutException:
            self.logger.error("Dialog is not closed")
        else:
            self.logger.info("Dialog is closed")

    def dialog_should_be_visible(self):
        try:
            WebDriverWait(self.driver, 15).until_not(dialog_is_not_present())
        except TimeoutException:
            self.logger.error("Dialog is not opened")
        else:
            self.logger.info("Dialog is opened")

    def new_element_appears_in_table(self, number):
        try:
            WebDriverWait(self.driver, 15).until(new_element_in_table(number))
        except TimeoutException:
            self.logger.error("New element doesn't appear in the table")
        else:
            self.logger.info("New element appears in the table")

    def get_element_count(self, xpath):
        try:
            elements = self.activity.driver.find_elements_by_xpath(xpath)
        except:
            self.logger.error("Elements with XPATH = '"+xpath+"' do not found")
        else:
            count = len(elements)
            self.logger.info("There are '"+str(count)+"' elements with XPATH = '"+xpath+"'")
            return count

    def elements_count_should_be(self, xpath, number):
        try:
            WebDriverWait(self.driver, 15).until(elements_count_should_be(xpath, number))
        except TimeoutException:
            self.logger.error("Count of elements is incorrect")
        else:
            self.logger.info("Count of elements is correct")

    def get_table_rows_number(self):
        return self.get_element_count(self.locators.xpath_table_row)

    def get_header_column(self, header):
        headers = self.activity.driver.find_elements_by_xpath(self.locators.xpath_table_header_column)
        for index, item in enumerate(headers):
            if (item.text == header):
                return index+1
        else:
            return False

    def get_table_item_text_by_indexes(self, row, column):
        xpath = self.locators.xpath_table_item(row, column)
        return self.get_element_text(xpath)

    def get_element_text(self, xpath):
        try:
            element = self.activity.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            self.logger.error("Element with XPATH = '"+xpath+"' not found")
        else:
            return element.text

    def check_last_table_item_by_header(self, header, expected_text):
        self.check_table_item_by_header(self.get_table_rows_number(), header, expected_text)

    def get_last_table_item_text_by_header(self, header):
        return self.get_table_item_text_by_header(header, self.get_table_rows_number())

    def get_table_item_text_by_header(self, header, row):
        column = self.get_header_column(header)
        if (column):
            return self.get_table_item_text_by_indexes(row, column)
        else:
            self.logger.error("There is no header '"+header+"'")

    def check_table_item_by_header(self, row, header, expected_text):
        if (expected_text is not None):
            column = self.get_header_column(header)
            current_text = None
            if (column):
                current_text = self.get_table_item_text_by_indexes(row, column)
            else:
                self.logger.error("There is no header '"+header+"'")
            if isinstance(expected_text, list):
                correctness = True
                for element in expected_text:
                    if (element not in current_text):
                        self.logger.error(str(row)+" element in '"+header+"' column is incorrect")
                        correctness = False
                        break
                if (correctness == True):
                    self.logger.info(str(row)+" elements in '"+header+"' column is correct")
            else:
                if (current_text == expected_text):
                    self.logger.info(str(row)+" element in '"+header+"' column is correct")
                else:
                    self.logger.error(str(row)+" element in '"+header+"' column is '"+str(current_text)+"', but should be '"+expected_text+"'")

    def delete_dialog_about(self):
        xpath = self.locators.xpath_dialog+"//b"
        try:
            element = self.activity.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            self.logger.error("Element with XPATH = '"+xpath+"' not found")
        else:
            return element.text

    def delete_dialog_should_be_about(self, expected_text):
        current_text = self.delete_dialog_about()
        if (current_text == expected_text):
            self.logger.info("Delete dialog about '"+current_text+"'")
        else:
            self.logger.info("Delete dialog about '"+current_text+"', but should be about '"+expected_text+"'")

    def set_slider(self, xpath, condition):
        if (condition is not None):
            try:
                element = self.activity.driver.find_element_by_xpath(xpath)
            except NoSuchElementException:
                self.logger.error("Slider with XPATH = '"+xpath+"' not found")
            else:
                if (element.get_attribute("value") != condition):
                    element.click()
                    self.logger.info("Value of slider with XPATH = '"+xpath+"' is changed")
                else:
                    self.logger.info("Slider with XPATH = '"+xpath+"' already has necessary value")

    def wait_until_page_loaded(self):
        try:
            WebDriverWait(self.driver, 3).until(is_page_loading())
        except TimeoutException:
            pass
        WebDriverWait(self.driver, 15).until_not(is_page_loading())

    def should_be_last_page(self):
        try:
            WebDriverWait(self.driver, 15).until(last_page())
        except TimeoutException:
            self.logger.error("Last page is not opened")
        else:
            self.logger.info("Last page is opened")

    def open_last_page(self):
        pagination_buttons = self.activity.driver.find_elements_by_xpath(self.locators.xpath_pagination_bottom+"//button")
        if (len(pagination_buttons) > 3):
            if(pagination_buttons[-2].is_enabled() == True):
                self.wait_until_page_loaded()
                pagination_buttons[-2].click()
                self.should_be_last_page()
                self.wait_until_page_loaded()

    def remove_focus(self):
        root = self.driver.find_element_by_xpath("/html")
        root.click()

    def generate_csv(self, filename, rows):
        folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder += "/output/"+filename
        headers = []
        for n in range(len(rows[0])):
            headers.append(n)
        table = []
        table.append(headers)
        for row in rows:
            table.append(row)
        with open(folder, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(table)

    def import_csv(self, id, filename):
        folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder += "/output/"+filename
        self.activity.driver.find_element_by_id(id).send_keys(folder)
        self.dialog_should_be_visible()
        self.click_xpath(self.locators.xpath_continue_import)
        self.dialog_should_not_be_visible()

    def select_customer_shipto(self, customer_xpath=None, customer_name=None, shipto_xpath=None, shipto_name=None):
        if (customer_xpath is None):
            customer_xpath=self.locators.xpath_by_count(self.locators.xpath_select_box, 1)
        if (shipto_xpath is None):
            shipto_xpath=self.locators.xpath_by_count(self.locators.xpath_select_box, 2)
        self.wait_until_page_loaded()
        self.select_in_dropdown(customer_xpath, customer_name)
        self.wait_until_page_loaded()
        self.select_in_dropdown(shipto_xpath, shipto_name)
        self.wait_until_page_loaded()

    def scan_table(self, scan_by, column_header, body):
        column = self.get_header_column(column_header)
        pagination_buttons = self.activity.driver.find_elements_by_xpath(self.locators.xpath_pagination_bottom+"//button")
        if (column):
            is_break = False
            while True:
                for row in range(1, self.get_table_rows_number()+1):
                    cell_value = self.get_table_item_text_by_indexes(row, column)
                    if (cell_value == scan_by):
                        self.logger.info("Text '"+scan_by+"' is found in the table")
                        for cell in body.keys():
                            self.check_table_item_by_header(row, cell, body[cell])
                        is_break = True
                        break
                if(is_break):
                    break
                if (len(pagination_buttons) > 3 and pagination_buttons[-2].is_enabled() == True):
                        pagination_buttons[-1].click()
                        self.wait_until_page_loaded()
                else:
                    self.logger.error("There is no value '"+scan_by+"' in the '"+str(column)+"' column")
                    break
        else:
            self.logger.error("There is no header '"+header+"'")

    def manage_shipto(self, shiptos, prefix_path=""):
        if (shiptos is not None):
            self.click_xpath(self.locators.xpath_button_by_name("Manage"))
            for shipto in shiptos:
                for row in range(1, self.get_element_count(prefix_path+self.locators.xpath_table_row)+1):
                    if (shipto == self.activity.driver.find_element_by_xpath(self.locators.xpath_table_item_in_dialog(row, 1)).text):
                        self.click_xpath(self.locators.xpath_table_item_in_dialog(row, 5)+"//button")
                        break
                else:
                    self.logger.error("There is no ShipTo '"+shipto+"'")
            self.click_xpath(self.locators.xpath_button_by_name("Apply"))

    def get_row_of_table_item_by_header(self, scan_by, column_header, prefix_path=""):
        column = self.get_header_column(column_header)
        for index, row in enumerate(range(1, self.get_element_count(prefix_path+self.locators.xpath_table_row)+1)):
            if (scan_by == self.activity.driver.find_element_by_xpath(prefix_path+self.locators.xpath_table_item(row, column)).text):
                return index+1