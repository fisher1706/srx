from selenium import webdriver

class not_first_page_bootstrap(object):
    def __call__(self, driver):
        if (driver.find_element_by_xpath("//li[@class='active page-item']").get_attribute("title") == "1"):
            return False
        else:
            return True