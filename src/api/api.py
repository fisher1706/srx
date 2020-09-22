from warrant.aws_srp import AWSSRP
import requests
import json

class API():
    def __init__(self, context):
        self.context = context
        self.logger = context.logger
        self.url = context.session_context.url
        self.data = context.data

    def get_token(self, username, password, pool_id, client_id):
        aws = AWSSRP(username=username, password=password, pool_id=pool_id, client_id=client_id)
        tokens = aws.authenticate_user()
        return tokens['AuthenticationResult']['IdToken']

    def get_distributor_token(self, username=None, password=None):
        if ((self.context.session_context.cognito_user_pool_id is None or
            self.context.session_context.cognito_client_id is None) and
            self.context.session_context.smoke_distributor_token is not None):
            self.context.distributor_token = self.context.session_context.smoke_distributor_token
        if (self.context.distributor_token is None):
            if (username is None):
                username = self.context.distributor_email
            if (password is None):
                password = self.context.distributor_password
            self.context.distributor_token = self.get_token(username, password, self.context.session_context.cognito_user_pool_id, self.context.session_context.cognito_client_id)
        return self.context.distributor_token

    def get_mobile_distributor_token(self, username=None, password=None):
        if (self.context.mobile_distributor_token is None):
            if (username is None):
                username = self.context.distributor_email
            if (password is None):
                password = self.context.distributor_password
            self.context.mobile_distributor_token = self.get_token(username, password, self.context.session_context.cognito_user_pool_id, self.context.session_context.cognito_mobile_client_id)
        return self.context.mobile_distributor_token

    def get_customer_token(self, username=None, password=None):
        if (self.context.customer_token is None):
            if (username is None):
                username = self.context.customer_email
            if (password is None):
                password = self.context.customer_password
            self.context.customer_token = self.get_token(username, password, self.context.session_context.cognito_user_pool_id, self.context.session_context.cognito_client_id)
        return self.context.customer_token

    def get_admin_token(self):
        if (self.context.admin_token is None):
            self.context.admin_token = self.get_token(self.context.admin_email, self.context.admin_password, self.context.session_context.cognito_user_pool_id, self.context.session_context.cognito_client_id)
        return self.context.admin_token

    def get_checkout_token(self, username=None, password=None):
        if (self.context.checkout_token is None):
            if (username is None):
                username = self.context.customer_email
            if (password is None):
                password = self.context.customer_password
            self.context.checkout_token = self.get_token(username, password, self.context.session_context.cognito_user_pool_id, self.context.session_context.cognito_checkout_client_id)
        return self.context.checkout_token

    def get_checkout_group_token(self, username=None, password=None):
        if (self.context.checkout_group_token is None):
            if (username is None):
                username = self.context.checkout_group_email
            if (password is None):
                password = self.context.checkout_group_password
            self.context.checkout_group_token = self.get_token(username, password, self.context.session_context.cognito_user_pool_id, self.context.session_context.cognito_checkout_client_id)
        return self.context.checkout_group_token

    def get_mobile_or_base_token(self, mobile):
        if mobile:
            return self.get_mobile_distributor_token()
        else:
            return self.get_distributor_token()

    def send_post(self, url, token, data=None, additional_headers=None, line_data=None, params=None):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "Accept":"application/json"
        }
        if (additional_headers is not None):
            headers.update(additional_headers)
        if (line_data is not None and params is None):
            return requests.post(url, headers=headers, data=line_data)
        elif (line_data is None and data is not None and params is None):
            return requests.post(url, headers=headers, data=json.dumps(data))
        elif (line_data is None and data is None and params is None):
            return requests.post(url, headers=headers)
        elif (data is not None and params is not None):
            return requests.post(url, headers=headers, params=params, data=json.dumps(data))
        elif (data is None and params is not None):
            return requests.post(url, headers=headers, params=params)

    def send_get(self, url, token, additional_headers=None):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "Accept":"application/json"
        }
        if (additional_headers is not None):
            headers.update(additional_headers)
        return requests.get(url, headers=headers)

    def send_delete(self, url, token, additional_headers=None):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "Accept":"application/json"
        }
        if (additional_headers is not None):
            headers.update(additional_headers)
        return requests.delete(url, headers=headers)

    def send_put(self, url, token, data=None, additional_headers=None):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "Accept":"application/json"
        }
        if (additional_headers is not None):
            headers.update(additional_headers)
        return requests.put(url, headers=headers, data=json.dumps(data))
