from src.api.api import API
from src.resources.messages import Message
from glbl import Log, Error

class StoragesApi(API):
    def get_storage_door_configuration(self, storage_id):
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/storage/{storage_id}/configuration")
        token = self.get_admin_token()
        response = self.send_get(url, token)
        if response.status_code == 200:
            Log.info(Message.entity_operation_done.format(entity="Storage Door configuration", operation="got"))
        else:
            Error.error(str(response.content))
        response_json = response.json()
        return response_json["data"]
