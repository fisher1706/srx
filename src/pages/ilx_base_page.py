from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class IlxBase:
    def __init__(self, ilx_context):
        self.ilx_context = ilx_context
        self.ilx_driver = ilx_context.ilx_driver
        self.url = self.ilx_context.ilx_session_context.ilx_url
        self.__wait = WebDriverWait(self.ilx_driver, 5, 0.5)

    @staticmethod
    def __get_element_by(find_by):
        find_by = find_by.lower()

        locating = {
            'css': By.CSS_SELECTOR,
            'xpath': By.XPATH,
            'class_name': By.CLASS_NAME,
            'id': By.ID,
            'link_text': By.LINK_TEXT,
            'name': By.NAME,
            'partial_link_text': By.PARTIAL_LINK_TEXT,
            'tag_name': By.TAG_NAME
        }

        return locating[find_by]

    @staticmethod
    def get_elements_data(elements):
        data =  [{'name': element.text, 'id': element.get_attribute('id')}
        for element in elements if element.text and element.get_attribute('id')]
        return data

    @staticmethod
    def get_element_text_by_text(elements, name):
        data = [element.text for element in elements if str(element.text) == str(name)]
        if data:
            return data[0]
        return None

    def open_browser(self):
        self.ilx_driver.get(self.url)

    def refresh_browser(self):
        self.ilx_driver.refresh()

    def is_visible(self, find_by, locator):
        return self.__wait.until(ec.visibility_of_element_located((self.__get_element_by(find_by), locator)))

    def is_present(self, find_by, locator):
        return self.__wait.until(ec.presence_of_element_located((self.__get_element_by(find_by), locator)))

    def is_not_present(self, find_by, locator):
        return self.__wait.until(ec.invisibility_of_element_located((self.__get_element_by(find_by), locator)))

    def are_visible(self, find_by, locator):
        return self.__wait.until(ec.visibility_of_all_elements_located((self.__get_element_by(find_by), locator)))

    def are_present(self, find_by, locator):
        return self.__wait.until(ec.presence_of_all_elements_located((self.__get_element_by(find_by), locator)))

    def move_to_element(self, find_by, locator):
        element = self.is_visible(find_by, locator)
        actions = ActionChains(self.ilx_driver)
        actions.move_to_element(element).perform()
        return element
