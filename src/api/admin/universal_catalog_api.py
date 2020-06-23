from src.api.api import API

class UniversalCatalogApi(API):
    def get_universal_catalog(self, upc="", gtin="", manufacturer="", manufacturer_part_number="", count=False):
        url = self.url.get_api_url_for_env(f"/admin-portal/admin/upc-gtin-catalog?upc={upc}&gtin={gtin}&manufacturer={manufacturer}&manufacturerPartNumber={manufacturer_part_number}")
        token = self.get_admin_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Universal catalog has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        if (count == True):
            return response_json["data"]["totalElements"]
        else:
            return response_json["data"]["entities"]