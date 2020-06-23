from src.api.api import API
from src.resources.tools import Tools

class StoragesApi(API):
    def get_storage_door_configuration(self, storage_id):
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/storage/{storage_id}/configuration")
        token = self.get_admin_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Storage door configuration has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]
