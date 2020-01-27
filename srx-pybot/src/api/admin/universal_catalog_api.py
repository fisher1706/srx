from src.api.api import API

class UniversalCatalogApi(API):
    def __init__(self, case):
        super().__init__(case)

    def get_universal_catalog(self, upc="", gtin="", manufacturer="", manufacturer_part_number=""):
        url = self.url.get_api_url_for_env("/admin-portal/admin/upc-gtin-catalog?upc="+str(upc)+"&gtin="+str(gtin)+"&manufacturer="+str(manufacturer)+"&manufacturerPartNumber="+str(manufacturer_part_number))
        token = self.get_admin_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info("Universal catalog has been successfully got")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return response_json["data"]["entities"]