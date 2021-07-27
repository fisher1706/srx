import traceback
import time
import os
import logging
from selenium.webdriver.common.by import By
from src.resources.tools import Tools

class Logger():
    'The class ensure all necessary logging'

    def __init__(self, context):
        self.logging = logging
        self.log = ""
        self.context = context

    def info(self, string):
        self.logging.info(string)
        self.log += f"\n[INFO] {string}"

    def error(self, string):
        if self.context.screenshot:
            path = f"{os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))}/screenshots/"
            if not os.path.exists(path):
                try:
                    os.mkdir(path)
                except OSError:
                    self.info("Creation of Screenshots directory is failed")
            self.context.driver.save_screenshot(f"{path}{time.strftime('%Y.%m.%dT%H:%M:%S', time.localtime(time.time()))}.png")
            Tools.generate_log(f"{path}{time.strftime('%Y.%m.%dT%H:%M:%S', time.localtime(time.time()))}.log", self.context.driver.get_log("performance"))
            self.info("EXCEPTION")
            self.info(f"URL: {self.context.driver.current_url}")
            try:
                self.info(f"TEXT: \n{self.context.driver.find_element(By.XPATH, '//body').text}")
            except:
                self.info("TEXT NOT FOUND")
        if self.context.is_teardown:
            self.warning("\n\nError during teardown")
        trace = traceback.format_exc()
        self.logging.error(string)
        if trace != 'NoneType: None\n':
            self.log += f"\n[ERROR] {string}\n\n{traceback.format_exc()}"
        else:
            self.log += f"\n[ERROR] {string}\n"
        raise Exception(string)

    def warning(self, string):
        self.logging.warning(string)
        self.log += f"\n[WARNING] {string}"
        self.context.warnings_counter += 1

    def __str__(self):
        return self.log
