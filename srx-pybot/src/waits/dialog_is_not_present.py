from selenium import webdriver

class dialog_is_not_present(object):
  def __call__(self, driver):
    if (driver.find_element_by_xpath("/html/body").get_attribute("style") == "overflow: hidden;"):
        return False
    else:
        return True