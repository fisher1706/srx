from src.api.api import API
from src.fixtures.decorators import Decorator

class LocationApi(API):
    @Decorator.default_expected_code(200)
    def create_location(self, dto, shipto_id, expected_status_code):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.data.customer_id}/shiptos/{shipto_id}/locations/create")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, f"Incorrect status_code! Expected: '{expected_status_code}'; Actual: {response.status_code}; Repsonse content:\n{str(response.content)}"
        if (response.status_code == 200):
            self.logger.info(f"New location '{dto[0]['orderingConfig']['product']['partSku']}' has been successfully created")
        else:
            self.logger.info(f"Location creation completed with status_code = '{response.status_code}', as expected: {response.content}")

    @Decorator.default_expected_code(200)
    def update_location(self, dto, shipto_id, expected_status_code):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.data.customer_id}/shiptos/{shipto_id}/locations/update")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, f"Incorrect status_code! Expected: '{expected_status_code}'; Actual: {response.status_code}; Repsonse content:\n{str(response.content)}"
        if (response.status_code == 200):
            self.logger.info(f"Location with SKU = '{dto[0]['orderingConfig']['product']['partSku']}' has been successfully updated")
        else:
            self.logger.info(f"Location updating completed with status_code = '{response.status_code}', as expected: {response.content}")

    def get_location_by_sku(self, shipto_id, sku):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.data.customer_id}/shiptos/{shipto_id}/locations?orderingConfig.product.partSku={sku}")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Location has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]

    def get_ordering_config_by_sku(self, shipto_id, sku):
        response = self.get_location_by_sku(shipto_id, sku)
        return response[0]["orderingConfig"]["id"]

    def get_locations(self, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.data.customer_id}/shiptos/{shipto_id}/locations")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Locations was successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]

    def delete_location(self, location_id, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.data.customer_id}/shiptos/{shipto_id}/locations/delete")
        token = self.get_distributor_token()
        location_dto = [{"id": location_id}]
        response = self.send_post(url, token, location_dto)
        if (response.status_code == 200):
            self.logger.info("Location was successfully deleted")
        else:
            self.logger.error(str(response.content))

    @Decorator.default_expected_code(200)
    def location_bulk_update(self, action, shipto_id, expected_status_code, all=False, customer_id=None, ids=None):
        if (customer_id is None):
            customer_id = self.data.customer_id
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{customer_id}/shiptos/{shipto_id}/locations/bulkUpdate?action={action}&all={all}")
        token = self.get_distributor_token()
        response = self.send_post(url, token, ids)
        assert expected_status_code == response.status_code, f"Incorrect status_code! Expected: '{expected_status_code}'; Actual: {response.status_code}; Repsonse content:\n{str(response.content)}"
        self.logger.info(f"Location bulk update completed with status_code = '{response.status_code}', as expected: {response.content}")