from src.api.api import API

class CustomerUserApi(API):
    def __init__(self, case):
        super().__init__(case)

    def create_customer_user(self, dto, warehouse_id):
        url = self.url.get_api_url_for_env("/customer-portal/customer/users")
        token = self.get_customer_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info("New customer user '"+dto["email"]+"' has been successfully created")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        new_customer_user = (response_json["data"]["id"])
        return new_customer_user

    def delete_customer_user(self, warehouse_id, customer_id):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/warehouses/"+str(warehouse_id)+"/customers/"+str(customer_id)+"/delete")
        token = self.get_customer_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info("Customer with ID = '"+str(customer_id)+"' has been successfully deleted")
        else:
            self.logger.error(str(response.content))