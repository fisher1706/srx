from src.api.api import API
from src.resources.tools import Tools

class DistributorSettingsApi(API):
    def update_freeze_settings(self, dto, distributor_id=None):
        if distributor_id is None:
            distributor_id = self.data.distributor_id
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/distributors/{distributor_id}/freeze-variables")
        token = self.get_admin_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 200):
            self.logger.info(f"Freeze settings of distributor with ID = '{distributor_id}' has been successfully updated")
        else:
            self.logger.error(str(response.content))

    def set_freeze_settings(self, slow, frozen, distributor_id=None):
        dto = Tools.get_dto("freeze_settings_dto.json")
        dto["monthsUntilSlow"] = slow
        dto["monthsUntilFrozen"] = frozen
        self.update_freeze_settings(dto, distributor_id)