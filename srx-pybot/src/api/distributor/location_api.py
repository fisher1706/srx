from src.api.api import API

class LocationApi(API):
    def __init__(self, case):
        super().__init__(case)

    def create_location(self, dto, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.variables.customer_id}/shiptos/{shipto_id}/locations/create")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(f"New location '{dto[0]['orderingConfig']['product']['partSku']}' has been successfully created")
        else:
            self.logger.error(str(response.content))

    def update_location(self, dto, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.variables.customer_id}/shiptos/{shipto_id}/locations/update")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(f"Location '{dto[0]['orderingConfig']['product']['partSku']}' has been successfully updated")
        else:
            self.logger.error(str(response.content))

    def get_location_by_sku(self, shipto_id, sku):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.variables.customer_id}/shiptos/{shipto_id}/locations?orderingConfig.product.partSku={sku}")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Location was successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]

    def get_ordering_config_by_sku(self, shipto_id, sku):
        response = self.get_location_by_sku(shipto_id, sku)
        return response[0]["orderingConfig"]["id"]

    def get_locations(self, shipto_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{self.variables.customer_id}/shiptos/{shipto_id}/locations")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Locations was successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]