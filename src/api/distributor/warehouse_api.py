from src.api.api import API
from src.resources.messages import Message
from src.fixtures.decorators import Decorator

class WarehouseApi(API):

    warehouse_body = {
        "name": None,
        "number": None,
        "address":{
        "line1": None,
        "line2": None,
        "city": None,
        "zipCode": None,
        "state": None
        },
        "zoneId": None,
        "contactEmail": None,
        "invoiceEmail": None
    }

    @Decorator.default_expected_code(200)
    def create_warehouse(self,dto,expected_status_code):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/warehouses/create")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info("Warehouse has been successfully created")
            response_json = response.json()
            return response_json
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Warehouses", operation="creation", status_code=response.status_code, content=response.content))

    @Decorator.default_expected_code(200)
    def update__warehouse(self, dto, warehouese_id, expected_status_code):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/warehouses/{warehouese_id}/update")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info(f"Warehouse with ID = '{warehouese_id}' has been successfully updated")
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Warehouse", operation="updating", status_code=response.status_code, content=response.content))
  
    @Decorator.default_expected_code(200)
    def delete_warehouse(self, warehouese_id, expected_status_code):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/warehouses/{warehouese_id}/delete")
        token = self.get_distributor_token()
        response = self.send_post(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info(f"Waregouse with ID = '{warehouese_id}' has been successfully deleted")
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Warehouse", operation="deletion", status_code=response.status_code, content=response.content))

    def get_warehouses(self):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/warehouses")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Warehouses has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json

    def get_first_warehouse_id(self):
        response = self.get_warehouses()
        return response["data"]["entities"][0]["id"]
