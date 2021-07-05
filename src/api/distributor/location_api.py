from src.api.api import API
from src.fixtures.decorators import Decorator
from src.resources.messages import Message

class LocationApi(API):
    @Decorator.default_expected_code(200)
    def create_location(self, dto, shipto_id, expected_status_code, customer_id=None):
        if customer_id is None:
            customer_id = self.data.customer_id
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{customer_id}/shiptos/{shipto_id}/locations/create")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info(f"New location '{dto[0]['orderingConfig']['product']['partSku']}' has been successfully created")
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Location", operation="creation", status_code=response.status_code, content=response.content))

    @Decorator.default_expected_code(200)
    def update_location(self, dto, shipto_id, expected_status_code, mobile=False):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.data.customer_id}/shiptos/{shipto_id}/locations/update")
        token = self.get_mobile_or_base_token(mobile)
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info(f"Location with SKU = '{dto[0]['orderingConfig']['product']['partSku']}' has been successfully updated")
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Location", operation="updating", status_code=response.status_code, content=response.content))

    @Decorator.default_expected_code(200)
    def get_location_by_sku(self, shipto_id, sku, expected_status_code, mobile=False, customer_id=None):
        if customer_id is None:
            customer_id = self.data.customer_id
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{customer_id}/shiptos/{shipto_id}/locations?orderingConfig.product.partSku={sku}")
        token = self.get_mobile_or_base_token(mobile)
        response = self.send_get(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info("Location has been successfully got")
            response_json = response.json()
            return response_json["data"]["entities"]
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Location", operation="reading", status_code=response.status_code, content=response.content))

    def get_ordering_config_by_sku(self, shipto_id, sku):
        response = self.get_location_by_sku(shipto_id, sku)
        return response[0]["orderingConfig"]["id"]

    @Decorator.default_expected_code(200)
    def get_locations(self, shipto_id, expected_status_code, mobile=False):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.data.customer_id}/shiptos/{shipto_id}/locations")
        token = self.get_mobile_or_base_token(mobile)
        response = self.send_get(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info("Locations was successfully got")
            response_json = response.json()
            return response_json["data"]["entities"]
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Location", operation="reading", status_code=response.status_code, content=response.content))

    @Decorator.default_expected_code(200)
    def delete_location(self, location_id, shipto_id, expected_status_code):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.data.customer_id}/shiptos/{shipto_id}/locations/delete")
        token = self.get_distributor_token()
        location_dto = [{"id": location_id}]
        response = self.send_post(url, token, location_dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info(f"Location with ID = '{location_id}' has been successfully deleted")
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Location", operation="deletion", status_code=response.status_code, content=response.content))

    @Decorator.default_expected_code(200)
    def location_bulk_update(self, action, shipto_id, expected_status_code, all=False, customer_id=None, ids=None):
        if (customer_id is None):
            customer_id = self.data.customer_id
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{customer_id}/shiptos/{shipto_id}/locations/bulkUpdate?action={action}&all={all}")
        token = self.get_distributor_token()
        response = self.send_post(url, token, ids)
        assert expected_status_code == response.status_code, f"Incorrect status_code! Expected: '{expected_status_code}'; Actual: {response.status_code}; Repsonse content:\n{str(response.content)}"
        self.logger.info(f"Location bulk update completed with status_code = '{response.status_code}', as expected: {response.content}")

    @Decorator.default_expected_code(200)
    def get_vmi_analysis(self, shipto_id, expected_status_code, mobile=False):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.data.customer_id}/shiptos/{shipto_id}/vmi-analysis")
        token = self.get_mobile_or_base_token(mobile)
        response = self.send_get(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info("VMI Analysis has been successfully got")
            response_json = response.json()
            return response_json["data"]["entities"]
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="VMI Analysis", operation="reading", status_code=response.status_code, content=response.content))
