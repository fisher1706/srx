class wait_until_dropdown_is_not_empty(object):
    def __init__(self, xpath):
        self.xpath = xpath

    def __call__(self, driver):
        text = self.get_element_text(self.xpath)
        if (text is ""):
            return False
        else:
            return True