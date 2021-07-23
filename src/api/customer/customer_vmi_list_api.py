from src.api.api import API
from src.fixtures.decorators import Decorator
from src.resources.messages import Message

class CustomerVmiListApi(API):
    def get_locations(self, distributor_id=None, shipto_id=None):
        if distributor_id is None:
            distributor_id = self.data.distributor_id
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/locations")
        token = self.get_customer_token()
        params = {
            "distributorIds": distributor_id,
            "shipToIds": shipto_id
        }
        response = self.send_get(url, token, params=params)

        if (response.status_code == 200):
            self.logger.info(Message.entity_operation_done.format(entity="Location", operation="got"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]

    @Decorator.default_expected_code(200)
    def update_location(self, dto, expected_status_code):
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/locations/update")
        token = self.get_customer_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info(f"Location with SKU = '{dto[0]['orderingConfig']['product']['partSku']}' has been successfully updated")
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Location", operation="updating", status_code=response.status_code, content=response.content))
