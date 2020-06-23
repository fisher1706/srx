from src.api.api import API

class CustomerApi(API):
    def create_customer(self, dto, warehouse_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/warehouses/{warehouse_id}/customers/create")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 201):
            self.logger.info(f"New customer '{dto['name']}' has been successfully created")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        new_customer = (response_json["data"].split("/"))[-1]
        return new_customer

    def delete_customer(self, warehouse_id, customer_id):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/warehouses/{warehouse_id}/customers/{customer_id}/delete")
        token = self.get_distributor_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info(f"Customer with ID = '{customer_id}' has been successfully deleted")
        else:
            self.logger.error(str(response.content))
