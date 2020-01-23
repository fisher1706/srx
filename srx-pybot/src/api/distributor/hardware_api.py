from src.api.api import API

class HardwareApi(API):
    def __init__(self, case):
        super().__init__(case)
    
    def update_hardware(self, dto):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/hardware")
        token = self.get_distributor_token()
        response = self.send_put(url, token, dto)
        if (response.status_code == 200):
            self.logger.info("Hardware with ID = '"+str(dto["id"])+"' has been successfully updated")
        else:
            self.logger.error(str(response.content))