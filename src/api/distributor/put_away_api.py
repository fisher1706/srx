from src.api.api import API
from src.fixtures.decorators import Decorator
import requests
import os
import time

class PutAwayApi(API):
    @Decorator.default_expected_code(200)
    def put_away(self, dto, expected_status_code):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/putaway")
        token = self.get_mobile_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, f"Incorrect status_code! Expected: '{expected_status_code}'; Actual: {response.status_code}; Repsonse content:\n{str(response.content)}"
        if (response.status_code == 200):
            self.logger.info(f"Put Away was performed successfuly")
            response_json = response.json()
        else:
            self.logger.info(f"Put Away completed with status_code = '{response.status_code}', as expected: {response.content}")