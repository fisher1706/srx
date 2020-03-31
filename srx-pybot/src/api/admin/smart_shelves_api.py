from src.api.api import API
from src.resources.tools import Tools

class SmartShelvesApi(API):
    def __init__(self, case):
        super().__init__(case)

    def create_smart_shelf(self, dto):
        url = self.url.get_api_url_for_env("/admin-portal/admin/distributors/smart-shelves/")
        token = self.get_admin_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(f"New smart shelf has been created successfully ")
        else:
            self.logger.error(str(response.content))
    
    def get_door_configuration(self, locker_id):
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/lockers/{locker_id}/configuration")
        token = self.get_admin_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Locker door configuration has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]

    def get_smart_shelves_id(self, locker_name):
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/smart-shelves?&lockerSerial={locker_name}")
        token = self.get_admin_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Smart Shelf id has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"][0]["id"]

    def delete_smart_shelves(self, smart_shelves_id):
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/smart-shelves/{smart_shelves_id}")
        token = self.get_admin_token()
        for count in range (1, 5):
            response = self.send_delete(url, token)
            if (response.status_code == 200):
                self.logger.info(f"Smart shelf with ID = '{smart_shelves_id}' has been successfully deleted")
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
            if (distributor_id is False):
                smart_shelf_dto["distributor"]["id"] = None
                smart_shelf_dto["doorConfiguration"]["hardware"]["id"] = None
                smart_shelf_dto["doorConfiguration"]["id"] = None
            else:
                smart_shelf_dto["distributor"]["id"] = distributor_id
            if (locker_body_second is None):
                self.logger.error("You need specify new locker")
        if (locker_body_second is not None):
            if (locker_body_second is False):
                smart_shelf_dto["doorConfiguration"]["hardware"]["id"] = None
                smart_shelf_dto["doorConfiguration"]["id"] = None
            else:
                smart_shelf_dto["doorConfiguration"]["hardware"]["id"] = locker_body_second["id"]
                first_door_configuration = self.get_door_configuration(locker_body_second["id"])[0]
                smart_shelf_dto["doorConfiguration"]["id"] = first_door_configuration["id"]
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/smart-shelves/")
        token = self.get_admin_token()
        response = self.send_put(url, token, smart_shelf_dto)
        if (response.status_code == 200):
            self.logger.info(f"Smart Shelf with ID = '{smart_shelf_dto['id']}' has been successfully updated")
        else:
            self.logger.error(str(response.content))

    def get_smart_shelf(self, locker_name):
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/smart-shelves?&lockerSerial={locker_name}")
        token = self.get_admin_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Smart Shelf has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"][0]
