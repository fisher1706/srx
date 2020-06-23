class wait_until_dropdown_list_loaded(object):
    def __init__(self, count):
        self.count = count

    def __call__(self, driver):
        xpath = f"//div[@test-id='select-box'][{self.count}]/div/div[2]/div/div"
        if (driver.find_element_by_xpath(xpath).text == "Loading..."):
            return False
        else:
            return True