from src.resources.activity import Activity
from src.resources.testrail import APIClient
import random
import traceback

class Case():
    def __init__(self, activity, level='CASE'):
        self.activity = activity
        self.level = level
        self.testrail = False
        self.admin_token = None
        self.distributor_token = None
        self.customer_token = None

    def critical_finish_case(self):
        self.activity.logger.critical(f"Test crashed\n{traceback.format_exc()}")
        self.finish_case()

    def finish_case(self):
        if (self.activity.api_test == False):
            self.activity.driver.delete_all_cookies()
        self.activity.logger.output_case_result()
        self.testrail_publish_result()
        self.activity.logger.case_error_count = 0
        self.activity.logger.case_critical_count = 0
        self.activity.logger.case_result = ""
        if (self.level == 'CASE'):
            self.activity.finish_activity()

    def log_name(self, name):
        self.activity.logger.log_case_name(name)

    def testrail_publish_result(self):
        if (self.testrail == True and self.run_number is not None):
            if (self.activity.logger.case_error_count == 0 and self.activity.logger.case_critical_count == 0):
                self.result = 1
                self.comment = "[pybot]: Test passed"
            else:
                self.result = 5
                self.comment = "[pybot]: Test failed"+self.activity.logger.case_result
            client = APIClient('https://agilevisionio.testrail.io')
            client.user = self.activity.testrail_email
            client.password = self.activity.testrail_password
            for run in self.run_number:
                body = f"add_result_for_case/{run}/{self.case_number}"
                client.send_post(
                    body,
                    { 'status_id': self.result, 'comment': self.comment }
                )
        else:
            self.activity.logger.info("Testrail does not configure")

    def testrail_config(self, case_number, run_number=None):
        self.testrail = True
        if (run_number is None):
            run_number = self.activity.variables.run_number
        elif (run_number is None and self.activity.run_number is not None):
            run_number = self.activity.run_number
        self.run_number = run_number
        self.case_number = case_number

    def print_traceback(self):
        self.activity.logger.info(str(traceback.format_exc()))
