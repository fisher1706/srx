from src.api.api import API
from src.resources.tools import Tools
from src.resources.messages import Message
from glbl import Log, Error

class AdminHardwareApi(API):
    def create_hardware(self, dto):
        url = self.url.get_api_url_for_env("/admin-portal/admin/distributors/hardware")
        token = self.get_admin_token()
        response = self.send_post(url, token, dto)
        if response.status_code == 201:
            Log.info(f"New hardware with type '{dto['type']}' has been successfully created")
        else:
            Error.error(str(response.content))
        response_json = response.json()
        return response_json["data"]

    def create_iothub(self, distributor_id=None):
        if distributor_id is None:
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

    def create_storage(self, doors_quantity, columns_quantity, iothub_id=None):
        dto = {
            "value": "",
            "type": "STORAGE",
            "iotHub": {
                "id": iothub_id
            },
            "distributorId": 4,
            "hardwareVersion": "v1",
            "lockerType": {
                "id":"",
                "doorsQuantity": doors_quantity,
                "columnsQuantity": columns_quantity,
                "cellsWithoutWeightQuantity": 4
                }
        }
        return self.create_hardware(dto)

    def update_locker(self, locker_id, locker_type_id, iothub_id=None, version="v1"):
        dto = {
            "id": locker_id,
            "lockerType":{
                "id": locker_type_id
            },
            "iotHub":{
                "id": iothub_id
            },
            "type": "LOCKER",
            "hardwareVersion": version
        }
        return self.update_hardware(dto)

    def create_rfid(self, distributor_id=None):
        if distributor_id is None:
            distributor_id = self.data.distributor_id
        dto = {
            "distributorId": distributor_id,
            "type": "RFID"
        }
        return self.create_hardware(dto)

    def delete_hardware(self, hardware_id):
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/hardware/{hardware_id}")
        token = self.get_admin_token()
        for _ in range(1, 5):
            response = self.send_delete(url, token)
            if response.status_code == 200:
                Log.info(Message.entity_with_id_operation_done.format(entity="Hardware", id=hardware_id, operation="deleted"))
                break
            elif response.status_code == 400:
                Log.info(f"Hardware with ID = '{hardware_id}' cannot be deleted now")
                Log.info(str(response.content))
            else:
                Error.error(str(response.content))
                break
        else:
            Error.error(str(response.content))

    def get_locker_types(self):
        url = self.url.get_api_url_for_env("/admin-portal/admin/locker-types")
        token = self.get_admin_token()
        response = self.send_get(url, token)
        if response.status_code == 200:
            Log.info(Message.entity_operation_done.format(entity="Locker Type", operation="got"))
        else:
            Error.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]

    def get_first_locker_type(self):
        locker_types = self.get_locker_types()
        return locker_types[0]

    def update_locker_configuration(self, locker_id, condition, number=None):
        locker_configuration = self.get_locker_configuration(locker_id)
        if number is None:
            number = Tools.random_string_l(15)
        for door in locker_configuration:
            if door["number"] == 1:
                first_door_id = door["id"]
                break
        else:
            Error.error("Something went wrong: there is no lockerdoor with number 1")
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
        if response.status_code == 200:
            Log.info(Message.entity_with_id_operation_done.format(entity="Configuration of locker", id=locker_id, operation="updated"))
        else:
            Error.error(str(response.content))

    def get_locker_configuration(self, locker_id):
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/lockers/{locker_id}/configuration")
        token = self.get_admin_token()
        response = self.send_get(url, token)
        if response.status_code == 200:
            Log.info(Message.entity_with_id_operation_done.format(entity="Configuration of locker", id=locker_id, operation="got"))
        else:
            Error.error(str(response.content))
        response_json = response.json()
        return response_json["data"]

    def update_hardware(self, dto):
        url = self.url.get_api_url_for_env("/admin-portal/admin/distributors/hardware")
        token = self.get_admin_token()
        response = self.send_put(url, token, dto)
        if response.status_code == 200:
            Log.info(Message.entity_with_id_operation_done.format(entity="Hardware", id=dto['id'], operation="updated"))
        else:
            Error.error(str(response.content))
