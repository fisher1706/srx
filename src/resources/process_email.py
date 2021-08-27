import os
import mailparser
from bs4 import BeautifulSoup
from lxml.html import fromstring

class ProcessEmail():
    @staticmethod
    def parse_email_to_list(filename):
        folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder += "/output/"+filename
        mail = mailparser.parse_from_file(folder)
        text_body = ' '.join(BeautifulSoup(mail.text_html[0], "html.parser").stripped_strings)
        body_list = text_body.split(" ")

        return body_list

    @staticmethod
    def get_password_from_email(filename):
        body_list = ProcessEmail.parse_email_to_list(filename)
        next_substring = False
        for substring in body_list:
            if next_substring:
                return substring
            if substring == "Password":
                next_substring = True

    @staticmethod
    def get_acception_link_from_email(filename):
        folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder += "/output/"+filename
        mail = mailparser.parse_from_file(folder)
        root = fromstring(mail.body)
        return root.xpath("//b[text()='Accept Invite']/../@href")

    @staticmethod
    def get_reset_password_link_from_email(filename):
        folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder += "/output/"+filename
        mail = mailparser.parse_from_file(folder)
        root = fromstring(mail.body)
        return root.xpath("//b[text()='Reset password']/../@href")

    @staticmethod
    def get_email_subject(filename):
        folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder += "/output/"+filename
        mail = mailparser.parse_from_file(folder)
        return mail.subject

    @staticmethod
    def get_email_to(filename):
        folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder += "/output/"+filename
        mail = mailparser.parse_from_file(folder)
        return mail.to