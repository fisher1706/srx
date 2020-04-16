from src.api.cognito import Cognito
import requests
import json

class API():
    def __init__(self, case):
        self.logger = case.activity.logger
        self.url = case.activity.url
        self.locators = case.activity.locators
        self.variables = case.activity.variables
        self.activity = case.activity
        self.case = case

    def get_token(self, username, password, user_pool_id, client_id, client_secret=None):
        return Cognito(username, password, user_pool_id, client_id, client_secret).id_token

    def get_distributor_token(self, username=None, password=None):
        if (self.case.distributor_token is None):
            if (username is None):
                username = self.variables.distributor_email
            if (password is None):
                password = self.variables.distributor_password
            self.case.distributor_token = self.get_token(username, password, self.activity.USER_POOL_ID, self.activity.CLIENT_ID, self.activity.CLIENT_SECRET)
        return self.case.distributor_token

    def get_customer_token(self, username=None, password=None):
        if (self.case.customer_token is None):
            if (username is None):
                username = self.variables.customer_email
            if (password is None):
                password = self.variables.customer_password
            self.case.customer_token = self.get_token(username, password, self.activity.USER_POOL_ID, self.activity.CLIENT_ID, self.activity.CLIENT_SECRET)
        return self.case.customer_token

    def get_admin_token(self):
        if (self.case.admin_token is None):
            self.case.admin_token = self.get_token(self.variables.admin_email, self.variables.admin_password, self.activity.USER_POOL_ID, self.activity.CLIENT_ID, self.activity.CLIENT_SECRET)
        return self.case.admin_token

    def get_checkout_token(self, username=None, password=None):
        if (self.case.checkout_token is None):
            if (username is None):
                username = self.variables.customer_email
            if (password is None):
                password = self.variables.customer_password
            self.case.checkout_token = self.get_token(username, password, self.activity.USER_POOL_ID, self.activity.CHECKOUT_CLIENT_ID)
        return self.case.checkout_token

    def send_post(self, url, token, data=None, additional_headers=None, line_data=None):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "Accept":"application/json"
        }
        if (additional_headers is not None):
            headers.update(additional_headers)
        if (line_data is not None):
            return requests.post(url, headers=headers, data=line_data)
        else:
            return requests.post(url, headers=headers, data=json.dumps(data))

    def send_get(self, url, token):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "Accept":"application/json"
        }
        return requests.get(url, headers=headers)

    def send_delete(self, url, token):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "Accept":"application/json"
        }
        return requests.delete(url, headers=headers)

    def send_put(self, url, token, data=None):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "Accept":"application/json"
        }
        return requests.put(url, headers=headers, data=json.dumps(data))
