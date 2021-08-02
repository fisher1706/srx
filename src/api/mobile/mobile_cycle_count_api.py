from src.api.api import API
from src.fixtures.decorators import default_expected_code

class MobileCycleCountApi(API):
    @default_expected_code(200)
    def update_ohi(self, dto, shipto_id, location_id, expected_status_code=None, customer_id=None):
        if customer_id is None:
            customer_id = self.data.customer_id
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{customer_id}/shiptos/{shipto_id}/locations/{location_id}/updateOhi")
        token = self.get_mobile_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, f"Incorrect status_code! Expected: '{expected_status_code}'; Actual: {response.status_code}; Repsonse content:\n{str(response.content)}"
        if response.status_code == 200:
            self.logger.info("OHI updated successfully")
        else:
            self.logger.info(f"Update OHI completed with status_code = '{response.status_code}', as expected: {response.content}")
