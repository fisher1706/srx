from src.api.cognito import Cognito
import requests
import json
from src.api.api_methods import ApiMethods as apim

class API():
    def __init__(self, case):
        self.driver = case.activity.driver
        self.logger = case.activity.logger
        self.url = case.activity.url
        self.locators = case.activity.locators
        self.variables = case.activity.variables
        self.activity = case.activity
        self.case = case

    def get_token(self, username, password):
        return Cognito(self.activity, username, password).id_token

    def get_distributor_token(self):
        if (self.case.distributor_token is None):
            self.case.distributor_token = self.get_token(self.variables.distributor_email, self.variables.distributor_password)
        return self.case.distributor_token

    def get_customer_token(self):
        if (self.case.customer_token is None):
            self.case.customer_token = self.get_token(self.variables.customer_email, self.variables.customer_password)
        return self.case.customer_token

    def send_post(self, url, token, data=None):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "Accept":"application/json"
        }
        return requests.post(url, headers=headers, data=json.dumps(data))

    def send_get(self, url, token):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "Accept":"application/json"
        }
        return requests.get(url, headers=headers)
