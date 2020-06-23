from selenium import webdriver

class last_page(object):
    def __call__(self, driver):
        pagination_buttons = driver.find_elements_by_xpath("//div[@class='pagination-bottom']//button")
        if (pagination_buttons[-2].get_attribute("disabled") == "true"):
            return True
        else:
            return False