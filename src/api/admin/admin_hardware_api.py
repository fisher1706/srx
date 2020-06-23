from src.api.api import API
from src.resources.tools import Tools

class AdminHardwareApi(API):
    def create_hardware(self, dto):
        url = self.url.get_api_url_for_env("/admin-portal/admin/distributors/hardware")
        token = self.get_admin_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 201):
            self.logger.info(f"New hardware with type '{dto['type']}' has been successfully created")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]

    def create_iothub(self, distributor_id=None):
        if (distributor_id is None):
            distributor_id = self.data.distributor_id
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
            "hardwareVersion": "v1",
            "type": "LOCKER"
        }
        return self.create_hardware(dto)

    def create_storage(self, doorsQuantity, columnsQuantity, iothub_id=None):
        dto = {
            "value": "",
            "type": "STORAGE",
            "iotHub": {
                "id": iothub_id
            },
            "distributorId": 4,
            "lockerType": {
                "id":"",
                "doorsQuantity": doorsQuantity,
                "columnsQuantity": columnsQuantity,
                "cellsWithoutWeightQuantity": 4
                }
        }
        return self.create_hardware(dto)
    
    def update_locker(self, locker_id, locker_type_id, iothub_id=None):
        dto = {
            "id": locker_id,
            "lockerType":{
                "id": locker_type_id
            },
            "iotHub":{
                "id": iothub_id
            },
            "type": "LOCKER"
        }
        return self.update_hardware(dto)

    def create_rfid(self, distributor_id=None):
        if (distributor_id is None):
            distributor_id = self.data.distributor_id
        dto = {
            "distributorId": distributor_id,
            "type": "RFID"
        }
        return self.create_hardware(dto)

    def delete_hardware(self, hardware_id):
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/hardware/{hardware_id}")
        token = self.get_admin_token()
        for count in range (1, 5):
            response = self.send_delete(url, token)
            if (response.status_code == 200):
                self.logger.info(f"Hardware with ID = '{hardware_id}' has been successfully deleted")
                break
            elif (response.status_code == 400):
                self.logger.info(f"Hardware with ID = '{hardware_id}' cannot be deleted now")
                self.logger.info(str(response.content))
            else:
                self.logger.error(str(response.content))
                break
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

    def update_locker_configuration(self, locker_id, condition, number=None):
        locker_configuration = self.get_locker_configuration(locker_id)
        if (number is None):
            number = Tools.random_string_l(15)
        for door in locker_configuration:
            if (door["number"] == 1):
                first_door_id = door["id"]
                break
        else:
            self.logger.error("Something went wrong: there is no lockerdoor with number 1")
        dto = [{
            "id": first_door_id,
            "number": 1,
            "noWeight": condition,
            "doorSerialNumber": number,
            "smartShelfHardware": {
                "id": None
            }
        }]
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/lockers/{locker_id}/configuration")
        token = self.get_admin_token()
        response = self.send_put(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(f"Configuration of locker with ID = '{locker_id}' has been successfully updated")
        else:
            self.logger.error(str(response.content))

    def get_locker_configuration(self, locker_id):
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/lockers/{locker_id}/configuration")
        token = self.get_admin_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info(f"Configuration of locker with ID = '{locker_id}' has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]

    def update_hardware(self, dto):
        url = self.url.get_api_url_for_env("/admin-portal/admin/distributors/hardware/")
        token = self.get_admin_token()
        response = self.send_put(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(f"Hardware with ID = '{dto['id']}' has been successfully updated")
        else:
            self.logger.error(str(response.content))