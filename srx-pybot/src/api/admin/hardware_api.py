from src.api.api import API

class HardwareApi(API):
    def __init__(self, case):
        super().__init__(case)

    def create_hardware(self, dto):
        url = self.url.get_api_url_for_env("/admin-portal/admin/distributors/keys/create")
        token = self.get_admin_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 201):
            self.logger.info("New hardware with type '"+dto["type"]+"' has been successfully created")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]

    def create_iothub(self, distributor_id=None):
        if (distributor_id is None):
            distributor_id = self.variables.distributor_id
        dto = {
            "distributorId": distributor_id,
            "type": "IOTHUB"
        }
        return self.create_hardware(dto.copy())

    def delete_hardware(self, hardware_id):
        url = self.url.get_api_url_for_env("/admin-portal/admin/distributors/keys/"+str(hardware_id)+"/delete")
        token = self.get_admin_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info("New hardware with ID = '"+str(hardware_id)+"' has been successfully deleted")
        else:
            self.logger.error(str(response.content))