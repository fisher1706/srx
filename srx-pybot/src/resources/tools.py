import string
import random
import os
import json

class Tools():
    @staticmethod
    def random_string_u(length=10):
        letters = string.ascii_uppercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    @staticmethod
    def random_string_l(length=10):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    @staticmethod
    def random_email(length=10):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        random_email = f"email.{random_string}@example.com"
        return random_email

    @staticmethod
    def get_dto(filename):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/api/dto/"
        with open(path+filename, "r") as read_file:
            return json.load(read_file)