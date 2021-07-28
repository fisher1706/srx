class elements_count_should_be(): #pylint: disable=C0103
    def __init__(self, xpath, number):
        self.number = number
        self.xpath = xpath

    def __call__(self, driver):
        elements = driver.find_elements_by_xpath(self.xpath)
        count = len(elements)
        if count == self.number:
            return True
        return False
