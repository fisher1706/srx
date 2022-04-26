class is_page_loading(): #pylint: disable=C0103
    def __call__(self, driver):
        if driver.find_element_by_xpath("//div[@class='-loading-inner']/..").get_attribute("class") == "-loading -active":
            return True
        return False
