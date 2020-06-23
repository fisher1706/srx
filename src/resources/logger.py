import logging
import traceback

class Logger():
    def __init__(self, context):
        self.logging = logging
        self.log = ""
        self.context = context

    def info(self, string):
        self.logging.info(string)
        self.log += f"\n[INFO] {string}"

    def error(self, string):
        if (self.context.is_teardown is True):
            self.warning("\n\nError during teardown")
        trace = traceback.format_exc()
        self.logging.error(string)
        if (trace != 'NoneType: None\n'):
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