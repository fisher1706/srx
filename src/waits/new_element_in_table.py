from selenium import webdriver

class new_element_in_table(object):
    def __init__(self, number):
        self.number = number

    def __call__(self, driver):
        if (driver.find_element_by_xpath(f"(//div[@role='rowgroup'])[{self.number}]")):
            return True
        else:
            return False