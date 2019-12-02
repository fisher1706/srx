from src.resources.url import URL as url
from src.api.api_methods import ApiMethods as api_method
from src.api.api import API

class CustomerUsersApi(API):
    def __init__(self, activity):
        super().__init__(activity)

    def create_customer_user(self, id_token, customer_user_body):
        pass