from selenium import webdriver

class page_url_is(object):
    def __init__(self, url):
        self.url = url

    def __call__(self, driver):
        if (driver.current_url == self.url):
            return True
        else:
            return False