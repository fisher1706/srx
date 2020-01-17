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
        return self.create_hardware(dto)

    def create_locker(self, locker_type_id, iothub_id=None):
        dto = {
            "lockerType":{
                "id": locker_type_id
            },
            "iotHub":{
                "id": iothub_id
            },
            "type": "LOCKER"
        }
        return self.create_hardware(dto)

    def delete_hardware(self, hardware_id):
        url = self.url.get_api_url_for_env("/admin-portal/admin/distributors/keys/"+str(hardware_id)+"/delete")
        token = self.get_admin_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info("Hardware with ID = '"+str(hardware_id)+"' has been successfully deleted")
        else:
            self.logger.error(str(response.content))

    def get_locker_types(self):
        url = self.url.get_api_url_for_env("/admin-portal/admin/locker-types")
        token = self.get_admin_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Locker types have been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]

    def get_first_locker_type(self):
        locker_types = self.get_locker_types()
        return locker_types[0]

    def update_locker_weight_configuration(self, locker_id, number, condition):
        dto = {
            "config":{
                "doors":[{
                    "noWeights": condition,
                    "number": number
                }]
            }
        }
        url = self.url.get_api_url_for_env("/admin-portal/admin/distributors/lockers/"+str(locker_id)+"/configuration")
        token = self.get_admin_token()
        response = self.send_put(url, token, dto)
        if (response.status_code == 200):
            self.logger.info("Configuration of locker with ID = '"+str(locker_id)+"' has been successfully updated")
        else:
            self.logger.error(str(response.content))
