class is_page_loading(object):
    def __call__(self, driver):
        if (driver.find_element_by_xpath("//div[@class='-loading-inner']/..").get_attribute("class") == "-loading -active"):
            return True
        else:
            return False