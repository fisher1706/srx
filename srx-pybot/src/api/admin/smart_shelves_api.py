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
