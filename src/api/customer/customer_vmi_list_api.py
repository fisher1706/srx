from src.api.api import API

class CustomerVmiListApi(API):
    def get_locations(self, distributor_id=None, shipto_id=None):
        if distributor_id is None:
            distributor_id = self.data.distributor_id
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/locations?distributorIds={distributor_id}&shipToIds={shipto_id}")
        token = self.get_customer_token()
        params = {
            "distributorIds": distributor_id,
            "shiptoIds": shipto_id
        }
        response = self.send_get(url, token)

        if (response.status_code == 200):
            self.logger.info("Locations has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]