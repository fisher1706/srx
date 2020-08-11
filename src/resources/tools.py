import string
import random
import os
import json
import csv

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
        random_email = f"email.{random_string}@agilevision.io"
        return random_email

    @staticmethod
    def get_dto(filename, path="/api/dto/"):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+path
        with open(path+filename, "r") as read_file:
            return json.load(read_file)

    @staticmethod
    def generate_csv(filename, rows):
        folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder += "/output/"+filename
        headers = []
        for n in range(len(rows[0])):
            headers.append(n)
        table = []
        table.append(headers)
        for row in rows:
            table.append(row)
        with open(folder, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(table)