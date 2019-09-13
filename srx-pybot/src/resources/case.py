from src.resources.activity import Activity
from src.resources.testrail import APIClient
import random
import string

class Case():
    def __init__(self, activity, level='CASE'):
        self.activity = activity
        self.level = level
        self.testrail = False

    def finish_case(self):
        self.activity.driver.delete_all_cookies()
        self.activity.logger.output_case_result()
        self.testrail_publish_result()
        self.activity.logger.case_error_count = 0
        self.activity.logger.case_crytical_count = 0
        self.activity.logger.case_result = ""
        if (self.level == 'CASE'):
            self.activity.finish_activity()

    def log_name(self, name):
        self.activity.logger.log_case_name(name)

    def testrail_publish_result(self):
        if (self.testrail == True):
            if (self.activity.logger.case_error_count == 0 and self.activity.logger.case_crytical_count == 0):
                self.result = 1
                self.comment = "[pybot]: Test passed"
            else:
                self.result = 5
                self.comment = "[pybot]: Test failed"+self.activity.logger.case_result
            client = APIClient('https://agilevisionio.testrail.io')
            client.user = 'dprovorov@agilevision.io'
            client.password = 'ZDqF6V3SxJT6tKVBGJiN-4Q/5mlBKf6qPcmdod8tB'
            for run in self.run_number:
                body = 'add_result_for_case/' + str(run) + '/' + str(self.case_number)
                client.send_post(
                    body,
                    { 'status_id': self.result, 'comment': self.comment }
                )
        else:
            pass

    def testrail_config(self, run_number, case_number):
        self.testrail = True
        self.run_number = run_number
        self.case_number = case_number

    def random_string_u(self, length=10):
        letters = string.ascii_uppercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        self.activity.logger.info("New random string generated: '"+random_string+"'")
        return random_string

    def random_string_l(self, length=10):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        self.activity.logger.info("New random string generated: '"+random_string+"'")
        return random_string

    def random_email(self, length=10):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        random_email = "email."+random_string+"@example.com"
        self.activity.logger.info("New random email generated: '"+random_email+"'")
        return random_email