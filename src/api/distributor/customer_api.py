from src.api.api import API
from src.resources.messages import Message
from src.fixtures.decorators import default_expected_code

class CustomerApi(API):
    @default_expected_code(201)
    def create_customer(self, dto, warehouse_id=None, expected_status_code=None):
        if warehouse_id is None:
            warehouse_id = self.data.warehouse_id
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/warehouses/{warehouse_id}/customers/create")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 201:
            self.logger.info(f"New customer '{dto['name']}' has been successfully created")
            response_json = response.json()
            new_customer = (response_json["data"].split("/"))[-1]
            return new_customer
        self.logger.info(Message.info_operation_with_expected_code.format(entity="Customer", operation="creation", status_code=response.status_code, content=response.content))

    @default_expected_code(200)
    def delete_customer(self, customer_id, warehouse_id=None, expected_status_code=None):
        if warehouse_id is None:
            warehouse_id = self.data.warehouse_id
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/warehouses/{warehouse_id}/customers/{customer_id}/delete")
        token = self.get_distributor_token()
        response = self.send_post(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="Customer", id=customer_id, operation="deleted"))
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Customer", operation="deletion", status_code=response.status_code, content=response.content))

    @default_expected_code(201)
    def update_customer(self, dto, customer_id, expected_status_code=None):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/warehouses/{self.data.warehouse_id}/customers/{customer_id}/update")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 201:
            self.logger.info(Message.entity_with_id_operation_done.format(entity="Customer", id=customer_id, operation="updated"))
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Customer", operation="updating", status_code=response.status_code, content=response.content))

    def get_customers(self, name=None, number=None, full=None):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/customers")
        token = self.get_distributor_token()
        params = {
            "name": name,
            "number": number
        }
        response = self.send_get(url, token, params=params)
        if response.status_code == 200:
            self.logger.info(Message.entity_operation_done.format(entity="Customers", operation="got"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        if full:
            return response_json["data"]
        return response_json["data"]["entities"]
