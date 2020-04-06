from selenium import webdriver

class is_progress_bar_loading(object):
    def __call__(self, driver):
        element = driver.find_element_by_xpath("//div[@role='progressbar']")
        count = len(element.get_attribute("class"))
        if count == 23:
            return True
        if count == 29:
            return False
        