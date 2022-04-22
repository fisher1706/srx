import logging
import pytest

class Error():
    @staticmethod
    def error(message):
        if Var.is_teardown:
            Var.teardown_error = True
        Log.error(message)
        pytest.fail()

    @staticmethod
    def check(statement: bool, message_if_true: str, message_if_false: str):
        if statement:
            Log.info(message_if_true)
        else:
            Error.error(message_if_false)

class Log():
    text = str()

    @staticmethod
    def join(message):
        Log.text = "\n".join([Log.text, message])

    @staticmethod
    def clear():
        Log.text = str()

    #----LOG LEVELS----
    @staticmethod
    def debug(message):
        Log.join(f"[DEBUG] {message}")
        logging.debug(message)

    @staticmethod
    def info(message):
        Log.join(f"[INFO] {message}")
        logging.info(message)

    @staticmethod
    def warning(message):
        Log.join(f"[WARNING] {message}")
        logging.warning(message)

    @staticmethod
    def error(message):
        Log.join(f"[ERROR] {message}")
        logging.error(message)

    @staticmethod
    def critical(message):
        Log.join(f"[CRITICAL] {message}")
        logging.critical(message)

class Var():
    is_teardown = None
    teardown_error = None

    @staticmethod
    def clear():
        Var.is_teardown = False
        Var.teardown_error = False

    def __setattr__(self, key, value):
        if hasattr(self, key):
            object.__setattr__(self, key, value)
        else:
            raise TypeError("Cannot create new attribute for class VAR")
