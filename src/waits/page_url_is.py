class page_url_is(): #pylint: disable=C0103
    def __init__(self, url):
        self.url = url

    def __call__(self, driver):
        if driver.current_url == self.url:
            return True
        return False
