from src.api.api import API
from src.resources.messages import Message
from src.fixtures.decorators import Decorator

class CustomerApi(API):
    @Decorator.default_expected_code(201)
    def create_customer(self, dto, expected_status_code):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/warehouses/{self.data.warehouse_id}/customers/create")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 201):
            self.logger.info(f"New customer '{dto['name']}' has been successfully created")
            response_json = response.json()
            new_customer = (response_json["data"].split("/"))[-1]
            return new_customer
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Customer", operation="creation", status_code=response.status_code, content=response.content))

    @Decorator.default_expected_code(200)
    def delete_customer(self, customer_id, expected_status_code):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/warehouses/{self.data.warehouse_id}/customers/{customer_id}/delete")
        token = self.get_distributor_token()
        response = self.send_post(url, token)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info(f"Customer with ID = '{customer_id}' has been successfully deleted")
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Customer", operation="deletion", status_code=response.status_code, content=response.content))

    @Decorator.default_expected_code(201)
    def update_customer(self, dto, customer_id, expected_status_code):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/warehouses/{self.data.warehouse_id}/customers/{customer_id}/update")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 201):
            self.logger.info(f"Customer with ID = '{customer_id}' has been successfully updated")
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Customer", operation="updating", status_code=response.status_code, content=response.content))

    def get_customers(self, name=None, number=None):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/customers")
        token = self.get_distributor_token()
        params = {
            "name": name,
            "number": number
        }
        response = self.send_get(url, token, params=params)

        if (response.status_code == 200):
            self.logger.info("Customers has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]