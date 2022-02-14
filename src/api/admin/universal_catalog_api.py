from src.api.api import API
from src.resources.messages import Message

class UniversalCatalogApi(API):
    def get_universal_catalog(self, upc="", gtin="", manufacturer="", manufacturer_part_number="", count=False):
        url = self.url.get_api_url_for_env("/admin-portal/admin/upc-gtin-catalog")
        params = {
            "upc": upc,
            "gtin": gtin,
            "manufacturer": manufacturer,
            "manufacturerPartNumber": manufacturer_part_number
        }
        token = self.get_admin_token()
        response = self.send_get(url, token, params=params)
        if response.status_code == 200:
            self.logger.info(Message.entity_operation_done.format(entity="Universal Catalog", operation="got"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        if count:
            return response_json["data"]["totalElements"]
        return response_json["data"]["entities"]
