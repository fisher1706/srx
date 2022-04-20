from curses import ERR
import logging
import pytest


def ERROR(message):
    LOG.error(message)
    pytest.fail()

def CHECK(statement: bool, message_if_true: str, message_if_false: str):
    if statement:
        LOG.info(message_if_true)
    else:
        ERROR(message_if_false)

class LOG():
    text = str()

    def join(message):
        LOG.text = "\n".join([LOG.text, message])

    def clear():
        LOG.text = str()

    #----LOG LEVELS----
    def debug(message):
        LOG.join(f"[DEBUG] {message}")
        logging.debug(message)

    def info(message):
        LOG.join(f"[INFO] {message}")
        logging.info(message)

    def warning(message):
        LOG.join(f"[WARNING] {message}")
        logging.warning(message)

    def error(message):
        LOG.join(f"[ERROR] {message}")
        logging.error(message)

    def critical(message):
        LOG.join(f"[CRITICAL] {message}")
        logging.critical(message)
