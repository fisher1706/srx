import logging
import pytest

def ERROR(message):
    if VAR.is_teardown:
        VAR.teardown_error = True
    LOG.error(message)
    pytest.fail()

def CHECK(statement: bool, message_if_true: str, message_if_false: str):
    if statement:
        LOG.info(message_if_true)
    else:
        ERROR(message_if_false)

class LOG():
    text = str()

    @staticmethod
    def join(message):
        LOG.text = "\n".join([LOG.text, message])

    @staticmethod
    def clear():
        LOG.text = str()

    #----LOG LEVELS----
    @staticmethod
    def debug(message):
        LOG.join(f"[DEBUG] {message}")
        logging.debug(message)


    @staticmethod
    def info(message):
        LOG.join(f"[INFO] {message}")
        logging.info(message)

    @staticmethod
    def warning(message):
        LOG.join(f"[WARNING] {message}")
        logging.warning(message)

    @staticmethod
    def error(message):
        LOG.join(f"[ERROR] {message}")
        logging.error(message)

    @staticmethod
    def critical(message):
        LOG.join(f"[CRITICAL] {message}")
        logging.critical(message)

class VAR():
    is_teardown = None
    teardown_error = None

    @staticmethod
    def clear():
        VAR.is_teardown = False
        VAR.teardown_error = False

    def __setattr__(self, key, value):
        if hasattr(self, key):
            object.__setattr__(self, key, value)
        else:
            raise TypeError("Cannot create new attribute for class VAR")
