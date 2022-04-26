import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from src.waits import wait_until_disabled, page_url_is, dialog_is_not_present, elements_count_should_be, is_page_loading, last_page, wait_until_dropdown_list_loaded, wait_until_dropdown_is_not_empty #pylint: disable=C0301
from src.resources.locator import Locator
from glbl import Log, Error

class BasePage():
    def __init__(self, context):
        self.context = context
        self.driver = context.driver
        self.url = self.context.session_context.url
        self.data = context.data

    def follow_url(self, url, expected_url=None):
        try:
            self.driver.get(url)
        except:
            expected_url = url if expected_url is None else expected_url
            current_url = self.driver.current_url
            if current_url != expected_url:
                Error.error(f"Error during try to follow URL = '{url}'. Current: {current_url}; Expected: {expected_url}")
            else:
                Log.info(f"URL = '{url}' is followed")
        else:
            Log.info(f"URL = '{url}' is followed")
            self.wait_for_complete_ready_state()

    def get_element_by_xpath(self, xpath, clickable=False):
        try:
            element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
            if clickable:
                element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except:
            Error.error(f"Element with XPATH = '{xpath}' not found")
        else:
            return element

    def get_element_by_id(self, element_id, clickable=False):
        try:
            element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, element_id)))
            if clickable:
                element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, element_id)))
        except:
            Error.error(f"Element with ID = '{element_id}' not found")
        else:
            return element

    def get_element_count(self, xpath):
        try:
            elements = self.driver.find_elements_by_xpath(xpath)
        except:
            Error.error(f"Elements with XPATH = '{xpath}' do not found")
        else:
            count = len(elements)
            Log.info(f"There are '{count}' elements with XPATH = '{xpath}'")
            return count

    def get_element_text(self, xpath):
        element = self.get_element_by_xpath(xpath)
        return element.text

    def click_id(self, element_id, timeout=20):
        element = self.get_element_by_id(element_id)
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.ID, element_id)))
            element.click()
        except TimeoutException:
            Error.error(f"Element with ID = '{element_id}' is not clickable")
        except:
            Error.error(f"Element with ID = '{element_id}' cannot be clicked")
        else:
            Log.info(f"Element with ID = '{element_id}' is clicked")

    def click_xpath(self, xpath, timeout=20, retries=5):
        element = self.get_element_by_xpath(xpath)
        for retry in range(retries):
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
                WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                element.click()
            except TimeoutException:
                if retry == retries - 1:
                    Error.error(f"Element with XPATH = '{xpath}' is not clickable")
                else:
                    Log.info(f"Element with XPATH = '{xpath}' is not clickable")
                time.sleep(1)
                continue
            except:
                if retry == retries - 1:
                    Error.error(f"Element with XPATH = '{xpath}' cannot be clicked")
                else:
                    Log.info(f"Element with XPATH = '{xpath}' cannot be clicked")
                time.sleep(1)
                continue
            else:
                Log.info(f"Element with XPATH = '{xpath}' is clicked")
                break

    def input_data_id(self, data, element_id, hide_log=False):
        self.clear_id(element_id)
        element = self.get_element_by_id(element_id, clickable=True)
        try:
            element.send_keys(data)
        except:
            Error.error(f"Cannot input '{data}' into element with ID = '{element_id}'")
        else:
            if hide_log:
                data = "***"
            Log.info(f"Data '{data}' inputed into element with ID = '{element_id}'")

    def input_data_xpath(self, data, xpath, hide_log=False):
        self.clear_xpath(xpath)
        element = self.get_element_by_xpath(xpath, clickable=True)
        try:
            element.send_keys(data)
        except:
            Error.error(f"Cannot input '{data}' into element with XPATH = '{xpath}'")
        else:
            if hide_log:
                data = "***"
            Log.info(f"Data '{data}' inputed into element with XPATH = '{xpath}'")

    def should_be_disabled_id(self, element_id):
        element = self.get_element_by_id(element_id)
        assert not element.is_enabled(), f"Element with ID = '{element_id}' is enabled, but should be disabled"

    def should_be_disabled_xpath(self, xpath, wait=False):
        element = self.get_element_by_xpath(xpath)
        if not wait:
            assert not element.is_enabled(), f"Element with XPATH = '{xpath}' is enabled, but should be disabled"
        else:
            WebDriverWait(self.driver, 7).until(wait_until_disabled(xpath)) #pylint: disable=E1102
            assert not element.is_enabled(), f"Element with XPATH = '{xpath}' is enabled, but should be disabled"

    def should_be_enabled_id(self, element_id):
        element = self.get_element_by_id(element_id)
        assert element.is_enabled(), f"Element with ID = '{element_id}' is disabled, but should be enabled"

    def should_be_enabled_xpath(self, xpath, wait=False):
        element = self.get_element_by_xpath(xpath)
        if not wait:
            assert element.is_enabled(), f"Element with XPATH = '{xpath}' is disabled, but should be enabled"
        else:
            WebDriverWait(self.driver, 7).until_not(wait_until_disabled(xpath)) #pylint: disable=E1102
            assert element.is_enabled(), f"Element with XPATH = '{xpath}' is disabled, but should be enabled"

    def get_authorization_token(self):
        cookies = self.driver.get_cookies()
        token = None
        for cookies_dict in cookies:
            name = cookies_dict["name"].split(".")[-1]
            if name == "idToken":
                token = cookies_dict["value"]
                break
        return token

    def url_should_be(self, url):
        try:
            WebDriverWait(self.driver, 20).until(page_url_is(url)) #pylint: disable=E1102
        except:
            Error.error("Incorrect page url")
        else:
            Log.info("Page url is correct")

    def url_should_contain(self, text):
        current_url = self.driver.current_url
        if f"{text}" in current_url:
            Log.info(f"URL contains text '{text}'")
        else:
            Error.error(f"URL does not contain '{text}'")

    def input_by_name(self, name, data, hide_log=None):
        if data is not None:
            self.input_data_xpath(data, f"//input[@name='{name}']", hide_log=hide_log)

    def clear_id(self, element_id):
        element = self.get_element_by_id(element_id, clickable=True)
        length = len(element.get_attribute("value"))
        for _ in range(length):
            element.send_keys(Keys.BACKSPACE)

    def clear_xpath(self, xpath):
        element = self.get_element_by_xpath(xpath, clickable=True)
        length = len(element.get_attribute("value"))
        for _ in range(length):
            try:
                element.send_keys(Keys.BACKSPACE)
            except:
                Error.error(f"Cannot complete BACKSPACE for element {xpath}")

    def select_in_dropdown(self, xpath, name):
        if name is not None:
            self.click_xpath(xpath)
            Log.info(f"Dropdown list with XPATH = '{xpath}' is opened")
            self.click_xpath(f"{xpath}/..//div[text()='{name}' and @tabindex='-1']")

    def manage_shipto(self, shiptos, prefix_path=""):
        if shiptos is not None:
            self.click_xpath(Locator.xpath_button_by_name("Manage"))
            self.get_element_by_xpath(Locator.xpath_select_button)
            for shipto_name in shiptos:
                self.get_element_by_xpath(f"{Locator.xpath_dialog}//span[text()='{shipto_name}']")
            for shipto in shiptos:
                for row in range(1, self.get_element_count(prefix_path+Locator.xpath_table_row)+1):
                    if shipto == self.driver.find_element_by_xpath(Locator.xpath_table_item_in_dialog(row, 1)).text:
                        self.click_xpath(f"{Locator.xpath_table_item_in_dialog(row, 5)}//button")
                        break
                else:
                    Error.error(f"There is no ShipTo '{shipto}'")
            self.click_xpath(f"{Locator.xpath_dialog}{Locator.xpath_submit_button}//span[text()='Save']")

    def dialog_should_not_be_visible(self):
        try:
            WebDriverWait(self.driver, 15).until(dialog_is_not_present()) #pylint: disable=E1102
        except:
            Error.error("Dialog is not closed")
        else:
            Log.info("Dialog is closed")

    def dialog_should_be_visible(self):
        try:
            WebDriverWait(self.driver, 15).until_not(dialog_is_not_present()) #pylint: disable=E1102
        except:
            Error.error("Dialog is not opened")
        else:
            Log.info("Dialog is opened")

    def elements_count_should_be(self, xpath, number, time=15):
        try:
            WebDriverWait(self.driver, time).until(elements_count_should_be(xpath, number)) #pylint: disable=E1102
        except:
            Error.error(f"Count of elements is incorrect: should be '{number}', now '{self.get_element_count(xpath)}'")
        else:
            Log.info("Count of elements is correct")

    def wait_until_page_loaded(self, time=3):
        try:
            WebDriverWait(self.driver, time).until(is_page_loading()) #pylint: disable=E1102
        except:
            pass
        WebDriverWait(self.driver, 15).until_not(is_page_loading()) #pylint: disable=E1102

    def wait_for_complete_ready_state(self, incomplete_before=False):
        if incomplete_before:
            WebDriverWait(self.driver, 15).until_not(lambda x: x.execute_script("return document.readyState === 'complete'"))
        WebDriverWait(self.driver, 15).until(lambda x: x.execute_script("return document.readyState === 'complete'"))

    def open_last_page(self):
        pagination_buttons = self.driver.find_elements_by_xpath(f"{Locator.xpath_pagination_bottom}//button")
        if len(pagination_buttons) > 3:
            if pagination_buttons[-2].is_enabled():
                self.wait_until_page_loaded()
                pagination_buttons[-2].click()
                self.should_be_last_page()
                self.wait_until_page_loaded()

    def last_page(self, pagination=None, wait=True):
        self.select_pagination(pagination)
        self.wait_for_the_first_element_in_table()
        if wait:
            try:
                WebDriverWait(self.driver, 7).until_not(wait_until_disabled(Locator.xapth_button_last_page)) #pylint: disable=E1102
            except:
                pass
        if self.get_element_by_xpath(Locator.xapth_button_last_page).is_enabled():
            self.click_xpath(Locator.xapth_button_last_page)
            self.wait_for_the_first_element_in_table()

    def wait_for_the_first_element_in_table(self):
        self.get_element_by_xpath(Locator.xpath_get_table_item(2, 1))

    def select_pagination(self, number_of_elements):
        if number_of_elements is not None:
            self.click_xpath(Locator.xpath_listbox)
            self.click_xpath(Locator.xpath_select_pagination(number_of_elements))

    def should_be_last_page(self):
        try:
            WebDriverWait(self.driver, 15).until(last_page()) #pylint: disable=E1102
        except:
            Error.error("Last page is not opened")
        else:
            Log.info("Last page is opened")

    def get_table_rows_number(self):
        return self.get_element_count(Locator.xpath_table_row)

    def get_header_column(self, header):
        self.get_element_by_xpath(Locator.xpath_table_header_column) #wait for the headers appear
        headers = self.driver.find_elements_by_xpath(Locator.xpath_table_header_column)
        for index, item in enumerate(headers):
            if item.text == header:
                return index+1
        return False

    def get_table_item_text_by_indexes(self, row, column):
        xpath = Locator.xpath_table_item(row, column)
        return self.get_element_text(xpath)

    def check_last_table_item_by_header(self, header, expected_text):
        self.check_table_item_by_header(self.get_table_rows_number(), header, expected_text)

    def get_last_table_item_text_by_header(self, header):
        return self.get_table_item_text_by_header(header, self.get_table_rows_number())

    def get_table_item_text_by_header(self, header, row):
        column = self.get_header_column(header)
        if column:
            return self.get_table_item_text_by_indexes(row, column)
        Error.error(f"There is no header '{header}'")

    def check_table_item_by_header(self, row, header, expected_text):
        if expected_text is not None:
            column = self.get_header_column(header)
            current_text = None
            if column:
                current_text = self.get_table_item_text_by_indexes(row, column)
            else:
                Error.error(f"There is no header '{header}'")
            if isinstance(expected_text, list):
                correctness = True
                for element in expected_text:
                    if element is not None:
                        if element not in current_text:
                            Error.error(f"{row} element in '{header}' column is incorrect")
                            correctness = False
                            break
                if correctness:
                    Log.info(f"{row} element in '{header}' column is correct")
            else:
                self.element_should_have_text(Locator.xpath_table_item(row, column), expected_text)

    def check_table_item(self, expected_text, cell=None, header=None, row=None, last=None):
        if expected_text is not None:
            if (cell is None and header is None) or (cell is not None and header is not None):
                Error.error("Either 'cell' or 'header' parameter should be defined")
            column = cell if header is None else self.get_header_column(header)

            if isinstance(expected_text, list):
                if last is not None:
                    current_text = self.get_element_text(Locator.xpath_get_last_table_item(column))
                elif row is not None:
                    current_text = self.get_element_text(Locator.xpath_get_table_item(row, column))
                else:
                    Error.error("Either 'row' or 'last' parameter should be defined")
                correctness = True
                for element in expected_text:
                    if element is not None:
                        if element not in current_text:
                            Error.error(f"{row} element in '{header}' column is incorrect")
                            correctness = False
                            break
                if correctness:
                    Log.info(f"{row} element in '{header}' column is correct")
            else:
                if last is not None:
                    self.element_should_have_text(Locator.xpath_get_last_table_item(column), expected_text)
                elif row is not None:
                    self.element_should_have_text(Locator.xpath_get_table_item(row, column), expected_text)
                else:
                    Error.error("Either 'row' or 'last' parameter should be defined")

    def delete_dialog_should_be_about(self, expected_text):
        self.wait_until_page_loaded(1)
        current_text = str(self.delete_dialog_about())
        if current_text == expected_text:
            Log.info(f"Delete dialog about '{current_text}'")
        else:
            Error.error(f"Delete dialog about '{current_text}', but should be about '{expected_text}'")

    def delete_dialog_about(self):
        xpath = Locator.xpath_dialog+"//b"
        try:
            element = self.get_element_by_xpath(xpath)
        except:
            Error.error(f"Element with XPATH = '{xpath}' not found")
        else:
            return element.text

    def title_should_be(self, title):
        try:
            WebDriverWait(self.driver, 20).until(EC.title_is(title))
        except:
            Error.error(f"Title should be '{title}', but now it is '{self.driver.title}'")
        else:
            Log.info(f"Title is '{title}'")

    def select_checkbox(self, xpath):
        element = self.get_element_by_xpath(xpath)
        checked = element.get_attribute("checked")
        if checked == 'true':
            Log.info(f"Checkbox with XPATH = '{xpath}' has been already checked")
        elif checked is None:
            element.click()
            Log.info(f"Checkbox with XPATH = '{xpath}' is checked")

    def unselect_checkbox(self, xpath):
        element = self.get_element_by_xpath(xpath)
        checked = element.get_attribute("checked")
        if checked == 'true':
            element.click()
            Log.info(f"Checkbox with XPATH = '{xpath}' is unchecked")
        elif checked is None:
            Log.info(f"Checkbox with XPATH = '{xpath}' has been already unchecked")

    def select_checkbox_in_dialog_by_name(self, name):
        self.select_checkbox(Locator.xpath_checkbox_in_dialog_by_name(name))

    def unselect_checkbox_in_dialog_by_name(self, name):
        self.unselect_checkbox(Locator.xpath_checkbox_in_dialog_by_name(name))

    def set_checkbox_value_in_dialog_by_name(self, name, value):
        if value:
            self.select_checkbox(Locator.xpath_checkbox_in_dialog_by_name(name))
        else:
            self.unselect_checkbox(Locator.xpath_checkbox_in_dialog_by_name(name))

    def clear_all_checkboxes_in_dialog(self):
        try:
            checkboxes = self.driver.find_elements_by_xpath(Locator.xpath_dialog+Locator.xpath_checkbox)
        except:
            Error.error("Checkboxes in dialog not found")
        else:
            for element in checkboxes:
                checked = element.get_attribute("checked")
                if checked == 'true':
                    element.click()

    def checkbox_should_be(self, xpath, condition):
        element = self.get_element_by_xpath(xpath)
        checked = element.get_attribute("checked")
        if condition:
            if checked == 'true':
                Log.info(f"Checkbox with XPATH = '{xpath}' is checked")
            elif checked is None:
                Error.error(f"Checkbox with XPATH = '{xpath}' should be checked")
        elif not condition:
            if checked is None:
                Log.info(f"Checkbox with XPATH = '{xpath}' is unchecked")
            elif checked == 'true':
                Error.error(f"Checkbox with XPATH = '{xpath}' should be unchecked")
        else:
            Error.error("Incorrect checkbox condition")

    def scan_table(self, scan_by, column_header, body=None, pagination=True):
        column = self.get_header_column(column_header)
        if pagination:
            pagination_buttons = self.driver.find_elements_by_xpath(Locator.xpath_pagination_bottom+"//button")
        if column:
            is_break = False
            while True:
                for row in range(1, self.get_table_rows_number()+1):
                    cell_value = self.get_table_item_text_by_indexes(row, column)
                    if cell_value == scan_by:
                        Log.info(f"Text '{scan_by}' is found in the table")
                        if body is None:
                            return row
                        for cell in body.keys():
                            self.check_table_item_by_header(row, cell, body[cell])
                        return row
                if is_break:
                    break
                if pagination:
                    if (len(pagination_buttons) > 3 and pagination_buttons[-2].is_enabled()):
                        pagination_buttons[-1].click()
                        self.wait_until_page_loaded()
                    else:
                        Error.error(f"There is no value '{scan_by}' in the '{column}' column")
                        break
                else:
                    Error.error(f"There is no value '{scan_by}' in the '{column}' column")
                    break
        else:
            Error.error(f"There is no header '{column_header}'")

    def import_csv(self, element_id, filename):
        folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder += "/output/"+filename
        self.get_element_by_id(element_id).send_keys(folder)
        self.dialog_should_be_visible()
        self.click_xpath(Locator.xpath_continue_import)
        self.dialog_should_not_be_visible()

    def click_tab_by_name(self, tab_name):
        self.click_xpath(Locator.xpath_button_tab_by_name(tab_name))
        self.wait_until_progress_bar_loaded()

    def wait_until_progress_bar_loaded(self, time=4):
        try:
            WebDriverWait(self.driver, time).until(EC.presence_of_element_located((By.XPATH, Locator.xpath_progress_bar)))
        except:
            pass
        WebDriverWait(self.driver, 15).until_not(EC.presence_of_element_located((By.XPATH, Locator.xpath_progress_bar)))

    def get_row_of_table_item_by_column(self, scan_by, column, prefix_path=""):
        for index, row in enumerate(range(1, self.get_element_count(prefix_path+Locator.xpath_table_row)+1)):
            if scan_by == self.driver.find_element_by_xpath(prefix_path+Locator.xpath_table_item(row, column)).text:
                return index+1

    def set_slider(self, xpath, condition):
        if condition is not None:
            element = self.get_element_by_xpath(xpath)
            if element.get_attribute("value") != condition:
                element.click()
                Log.info(f"Value of slider with XPATH = '{xpath}' is changed")
            else:
                Log.info(f"Slider with XPATH = '{xpath}' already has necessary value")

    def page_refresh(self):
        self.driver.refresh()

    def get_row_of_table_item_by_header(self, scan_by, column_header, prefix_path=""):
        column = self.get_header_column(column_header)
        for index, row in enumerate(range(1, self.get_element_count(prefix_path+Locator.xpath_table_row)+1)):
            if scan_by == self.get_element_by_xpath(prefix_path+Locator.xpath_table_item(row, column)).text:
                return index+1

    def wait_until_dropdown_list_loaded(self, count):
        try:
            WebDriverWait(self.driver, 15).until(wait_until_dropdown_list_loaded(count)) #pylint: disable=E1102
        except:
            Error.error("Dropdown list is not loaded")
        else:
            Log.info("Dropdown list is loaded")

    def check_found_dropdown_list_item(self, item_xpath, expected_text):
        item_text = self.get_element_text(item_xpath)
        number = self.get_element_count(item_xpath)
        if number == 1:
            if item_text == expected_text:
                Log.info("Dropdown list element has been found")
            else:
                Error.error(f"The text of dropdown list element is '{item_text}'")
        else:
            Error.error(f"The number of dropdown list elements = '{number}'")

    def select_in_dropdown_via_input(self, xpath, name, span=None):
        if name is not None:
            self.click_xpath(xpath)
            Log.info(f"Dropdown list with XPATH = '{xpath}' is opened")
            self.input_data_xpath(name, f"{xpath}//input")
            #self.get_element_by_xpath(f"{xpath}//input").send_keys(Keys.ENTER)
            if span:
                self.click_xpath(f"{xpath}/..//div[@tabindex='-1']//span[text()='{name}']")
            else:
                self.click_xpath(f"{xpath}/..//div[text()='{name}' and @tabindex='-1']")

    def input_inline_xpath(self, data, xpath):
        if data is not None:
            self.click_xpath(xpath)
            self.click_xpath(xpath)
            element = self.get_element_by_xpath(f"{xpath}//input")
            self.driver.execute_script("arguments[0].value = arguments[1]", element, "")
            self.input_data_xpath(data, f"{xpath}//input")
            element.send_keys(Keys.ENTER)

    def select_customer_shipto(self, customer_xpath=None, customer_name=None, shipto_xpath=None, shipto_name=None):
        if customer_xpath is None:
            customer_xpath = Locator.xpath_by_count(Locator.xpath_select_box, 1)
        if shipto_xpath is None:
            shipto_xpath = Locator.xpath_by_count(Locator.xpath_select_box, 2)
        self.wait_until_page_loaded()
        self.select_in_dropdown(customer_xpath, customer_name)
        self.wait_until_page_loaded()
        self.select_in_dropdown(shipto_xpath, shipto_name)
        self.wait_until_page_loaded()

    def element_should_have_text(self, xpath, text):
        self.get_element_by_xpath(xpath)
        try:
            WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element((By.XPATH, xpath), text))
        except:
            Error.error(f"Element with XPATH = '{xpath}' was found but text is different: '{self.get_element_text(xpath)}' != '{text}'")
        else:
            Log.info(f"Element with XPATH = '{xpath}' contains correct text")

    def element_should_have_text_id(self, element_id, text):
        self.get_element_by_id(element_id)
        try:
            WebDriverWait(self.driver, 15).until(EC.text_to_be_present_in_element((By.ID, element_id), text))
        except:
            Error.error(f"Element with XPATH = '{element_id}' was found but text is different")
        else:
            Log.info(f"Element with XPATH = '{element_id}' contains correct text")

    def element_text_should_be_empty(self, xpath):
        text = self.get_element_text(xpath)
        assert text is None or text == "", f"Element {xpath} contains text: {text}"

    def wait_untill_dropdown_not_empty(self, xpath):
        try:
            WebDriverWait(self.driver, 15).until(wait_until_dropdown_is_not_empty(By.XPATH, xpath)) #pylint: disable=E1102
        except:
            pass

    def select_shipto_sku(self, shipto=None, sku=None):
        if shipto is not None:
            self.select_in_dropdown_via_input(Locator.xpath_dropdown_in_dialog(1), shipto)
            self.wait_until_page_loaded()
        if sku is not None:
            self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(2), sku)
            self.wait_until_page_loaded()
