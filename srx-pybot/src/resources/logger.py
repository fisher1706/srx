import logging
import logging.handlers
import os
root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
full_log_path = os.path.join(root_directory,'output/full.log')
suite_log_path = os.path.join(root_directory,'output/suite.log')

class Logger():
    def __init__(self):
        self.my_logger = logging.getLogger()
        self.my_logger.setLevel(logging.INFO)

        self.full_handler = logging.handlers.RotatingFileHandler(full_log_path)
        self.full_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s][%(levelname)s]: %(message)s',datefmt='%d.%m.%Y %H:%M:%S')
        self.full_handler.setFormatter(formatter)

        self.suite_handler = logging.handlers.RotatingFileHandler(suite_log_path, mode='w')
        self.suite_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s][%(levelname)s]: %(message)s',datefmt='%d.%m.%Y %H:%M:%S')
        self.suite_handler.setFormatter(formatter)

        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s][%(levelname)s]: %(message)s',datefmt='%d.%m.%Y %H:%M:%S')
        self.console_handler.setFormatter(formatter)

        self.my_logger.addHandler(self.full_handler)
        self.my_logger.addHandler(self.suite_handler)
        self.my_logger.addHandler(self.console_handler)

        self.suite_error_count = 0
        self.suite_critical_count = 0
        self.case_error_count = 0
        self.case_critical_count = 0
        self.case_result = ""
        self.expected_error_series = 0
        self.current_error_series = 0

    def info(self, msg):
        self.current_error_series = 0
        self.my_logger.info(msg)
        self.case_result = self.case_result + '\n[INFO] ' + msg

    def error(self, msg):
        self.my_logger.error(msg)
        self.suite_error_count = self.suite_error_count + 1
        self.case_error_count = self.case_error_count + 1
        self.current_error_series = self.current_error_series +1
        self.case_result = self.case_result + '\n[ERROR] ' + msg
        if (self.current_error_series >= self.expected_error_series and self.expected_error_series > 0):
            raise IOError("Series of errors. Test finished")

    def critical(self, msg):
        self.my_logger.critical(msg)
        self.suite_critical_count = self.suite_critical_count + 1
        self.case_critical_count = self.case_critical_count + 1
        self.case_result = self.case_result + '\n[CRITICAL] ' + msg

    def output_case_result(self):
        self.info("----------------------------")
        self.info("CASE ERRORS: "+str(self.case_error_count))
        self.info("CASE CRITICALS: "+str(self.case_critical_count))
        self.info("============================")

    def output_suite_result(self):
        self.info("SUITE ERRORS: "+str(self.suite_error_count))
        self.info("SUITE CRITICALS: "+str(self.suite_critical_count))
        self.info("============================")

    def log_case_name(self, name):
        self.info("START CASE: "+name)
        self.info("----------------------------")