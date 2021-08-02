class dialog_is_not_present(): #pylint: disable=C0103
    def __call__(self, driver):
        if driver.find_element_by_xpath("/html/body").get_attribute("style") == "overflow: hidden;":
            return False
        return True
