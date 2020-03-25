from selenium import webdriver

class wait_until_disabled(object):
    def __init__(self, xpath):
        self.xpath = xpath

    def __call__(self, driver):
        element = driver.find_element_by_xpath(self.xpath)
        if (element.is_enabled()):
            return False
        else:
            return True