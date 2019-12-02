from src.api.api import API

class ShiptoApi(API):
    def __init__(self, case):
        super().__init__(case)

    def create_shipto(self, dto):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/customers/"+self.variables.customer_id+"/shipto/create")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 201):
            self.logger.info("New shipto '"+dto["number"]+"' has been successfully created")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        new_shipto = (response_json["data"].split("/"))[-1]
        return new_shipto

    def delete_shipto(self, id):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/customers/"+self.variables.customer_id+"/shipto/"+str(id)+"/delete")
        token = self.get_distributor_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info("ShipTo with ID = '"+str(id)+"' has been successfully deleted")
        else:
            self.logger.error(str(response.content))

    def get_shipto_by_number(self, number):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/customers/"+self.variables.customer_id+"/shiptos/pageable?number="+str(number))
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("ShipTo has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json

    def get_po_number_by_number(self, number):
        response = self.get_shipto_by_number(number)
        return response["data"]["entities"][0]["poNumber"]

    def check_po_number_by_number(self, number, expected_po_number):
        actual_po_number = self.get_po_number_by_number(number)
        if (actual_po_number == expected_po_number):
            self.logger.info("PO number is correct")
        else:
            self.logger.error("PO number should be '"+str(expected_po_number)+"', but now it is '"+str(actual_po_number)+"'")