from src.api.api import API

class CustomerApi(API):
    def __init__(self, case):
        super().__init__(case)

    def create_customer(self, dto, warehouse_id):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/warehouses/"+str(warehouse_id)+"/customers/create")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 201):
            self.logger.info("New customer '"+dto["name"]+"' has been successfully created")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        new_customer = (response_json["data"].split("/"))[-1]
        return new_customer

    def delete_customer(self, warehouse_id, customer_id):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/warehouses/"+str(warehouse_id)+"/customers/"+str(customer_id)+"/delete")
        token = self.get_distributor_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info("Customer with ID = '"+str(customer_id)+"' has been successfully deleted")
        else:
            self.logger.error(str(response.content))
