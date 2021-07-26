from src.api.api import API
from src.resources.tools import Tools
from src.resources.messages import Message

class SmartShelvesApi(API):
    def create_smart_shelf(self, dto):
        url = self.url.get_api_url_for_env("/admin-portal/admin/distributors/smart-shelves")
        token = self.get_admin_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(Message.entity_operation_done.format(entity="Smart Shelf", operation="created"))
        else:
            self.logger.error(str(response.content))
    
    def get_door_configuration(self, locker_id):
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/lockers/{locker_id}/configuration")
        token = self.get_admin_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info(Message.entity_operation_done.format(entity="Locker Door configuration", operation="got"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]

    def get_storage_door_configuration(self, storage_id):
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/storage/{storage_id}/configuration")
        token = self.get_admin_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info(Message.entity_operation_done.format(entity="Storage Door configuration", operation="got"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]

    def get_smart_shelves_id(self, locker_name):
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/smart-shelves")
        params = {
            "lockerSerial": locker_name
        }
        token = self.get_admin_token()
        response = self.send_get(url, token, params=params)
        if (response.status_code == 200):
            self.logger.info(Message.entity_operation_done.format(entity="Smart Shelf ID", operation="got"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"][0]["id"]

    def get_smart_shelves_id_assigned_to_hardware(self, hardware_name):
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/smart-shelves")
        params = {
            "lockerSerial": hardware_name
        }
        token = self.get_admin_token()
        response = self.send_get(url, token, params=params)
        if (response.status_code == 200):
            self.logger.info(Message.entity_operation_done.format(entity="Smart Shelf ID", operation="got"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        smart_shelves_id_list = []
        for item in response_json["data"]["entities"]:
            smart_shelves_id_list.append(item["id"])
        return smart_shelves_id_list

    def delete_smart_shelves(self, smart_shelves_id):
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/smart-shelves/{smart_shelves_id}")
        token = self.get_admin_token()
        for count in range (1, 5):
            response = self.send_delete(url, token)
            if (response.status_code == 200):
                self.logger.info(Message.entity_with_id_operation_done.format(entity="Smart Shelf", id=smart_shelves_id, operation="deleted"))
                break
            elif (response.status_code == 400):
                self.logger.info(f"Smart shelf with ID = '{smart_shelves_id}' cannot be deleted now")
                self.logger.info(str(response.content))
            else:
                self.logger.error(str(response.content))
                break
        else:
            self.logger.error(str(response.content))
    
    def update_smart_shelf(self, locker_body, serial_number=None, distributor_id=None, locker_body_second=None):
        smart_shelf = self.get_smart_shelf(locker_body["value"])
        smart_shelf_dto = Tools.get_dto("smart_shelves_dto.json")
        smart_shelf_dto["id"] = smart_shelf["id"]
        smart_shelf_dto["serialNumber"] = smart_shelf["serialNumber"]
        smart_shelf_dto["distributor"]["id"] = smart_shelf["distributor"]["id"]
        smart_shelf_dto["doorConfiguration"]["hardware"]["id"] = smart_shelf["doorConfiguration"]["hardware"]["id"]
        smart_shelf_dto["doorConfiguration"]["id"] = smart_shelf["doorConfiguration"]["id"]
        if (serial_number is not None):
            smart_shelf_dto["serialNumber"] = serial_number
        if (distributor_id is not None):
            if (not distributor_id):
                smart_shelf_dto["distributor"]["id"] = None
                smart_shelf_dto["doorConfiguration"]["hardware"]["id"] = None
                smart_shelf_dto["doorConfiguration"]["id"] = None
            else:
                smart_shelf_dto["distributor"]["id"] = distributor_id
            if (locker_body_second is None):
                self.logger.error("You need specify new locker")
        if (locker_body_second is not None):
            if (not locker_body_second):
                smart_shelf_dto["doorConfiguration"]["hardware"]["id"] = None
                smart_shelf_dto["doorConfiguration"]["id"] = None
            else:
                smart_shelf_dto["doorConfiguration"]["hardware"]["id"] = locker_body_second["id"]
                first_door_configuration = self.get_door_configuration(locker_body_second["id"])[0]
                smart_shelf_dto["doorConfiguration"]["id"] = first_door_configuration["id"]
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/smart-shelves")
        token = self.get_admin_token()
        response = self.send_put(url, token, smart_shelf_dto)
        if (response.status_code == 200):
            self.logger.info(Message.entity_with_id_operation_done.format(entity="Smart Shelf", id=smart_shelf_dto['id'], operation="updated"))
        else:
            self.logger.error(str(response.content))

    def get_smart_shelf(self, locker_name):
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/smart-shelves")
        params = {
            "lockerSerial": locker_name
        }
        token = self.get_admin_token()
        response = self.send_get(url, token, params=params)
        if (response.status_code == 200):
            self.logger.info(Message.entity_operation_done.format(entity="Smart Shelf", operation="got"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"][0]
