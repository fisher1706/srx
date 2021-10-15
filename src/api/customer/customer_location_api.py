from src.api.api import API
from src.fixtures.decorators import default_expected_code
from src.resources.messages import Message

class CustomerLocationApi(API):
    @default_expected_code(201)
    def create_location(self, dto, expected_status_code=None):
        url = self.url.get_api_url_for_env("/customer-portal/customer/locations")
        token = self.get_customer_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 201:
            self.logger.info(f"New location '{dto['orderingConfig']['product']['partSku']}' has been successfully created")
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Location", operation="creation", status_code=response.status_code, content=response.content))

    @default_expected_code(200)
    def update_location(self, dto, expected_status_code=None):
        url = self.url.get_api_url_for_env("/customer-portal/customer/locations/update")
        token = self.get_customer_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            self.logger.info(f"Location with SKU = '{dto[0]['orderingConfig']['product']['partSku']}' has been successfully updated")
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Location", operation="updating", status_code=response.status_code, content=response.content))

    @default_expected_code(200)
    def get_locations(self, shipto_ids, product_sku=None, expected_status_code=None):
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/locations")
        params = {
            "shipToIds": shipto_ids,
            "orderingConfig.product.partSku": product_sku
        }
        token = self.get_customer_token()
        response = self.send_get(url, token, params=params)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            self.logger.info(Message.entity_operation_done.format(entity="Location", operation="got"))
            response_json = response.json()
            return response_json["data"]["entities"]
        self.logger.info(Message.info_operation_with_expected_code.format(entity="Location", operation="reading", status_code=response.status_code, content=response.content))
