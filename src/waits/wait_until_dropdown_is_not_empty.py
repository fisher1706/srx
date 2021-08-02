class wait_until_dropdown_is_not_empty(): #pylint: disable=C0103
    def __init__(self, xpath):
        self.xpath = xpath

    def __call__(self, driver):
        text = self.get_element_text(self.xpath) #pylint: disable=E1101
        if text == "":
            return False
        return True
