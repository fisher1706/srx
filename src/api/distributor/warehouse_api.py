from src.api.api import API

class WarehouseApi(API):
    def get_warehouses(self):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/warehouses")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("ShipTo has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json

    def get_first_warehouse_id(self):
        response = self.get_warehouses()
        return response["data"]["entities"][0]["id"]