import os
import json

class ApiMethods():
    @staticmethod
    def get_dto(filename):
        path = os.path.dirname(os.path.abspath(__file__))+"/dto/"
        with open(path+filename, "r") as read_file:
            return json.load(read_file)