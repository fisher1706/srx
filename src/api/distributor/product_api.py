from src.api.api import API
import requests
import os
import time

class ProductApi(API):
    def create_product(self, dto):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/products/create")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        if (response.status_code == 201):
            self.logger.info(f"New product '{dto['partSku']}' has been successfully created")
        else:
            self.logger.error(str(response.content))

    def get_upload_url(self):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/products/upload-url")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info(f"Upload URL has been successfully created")
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return_response = {
            "url": response_json["data"]["url"],
            "filename": response_json["data"]["fileName"]
        }
        return return_response

    def file_upload(self, url):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/dto/smoke-product-template.csv"
        files = {"file": (path, open(path, "rb"))}
        response = requests.put(url, files=files)
        if (response.status_code == 200):
            self.logger.info(f"File has been successfuly upload")
        else:
            self.logger.error(str(response.content))

    def get_import_status(self, filename):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/import-status/Products/{filename}?type=PARSE_AND_VALIDATE")
        token = self.get_distributor_token()
        for i in range(6):
            response = self.send_get(url, token)
            if (response.status_code == 404):
                self.logger.info(f"File not found. Next attempt after 5 seconds")
                time.sleep(5)
                continue
            elif (response.status_code == 200):
                self.logger.info(f"File status successfuly got")
                break
            else:
                self.logger.error(str(response.content))
        else:
            self.logger.error("File not found after 30 seconds waiting")
        response_json = response.json()
        return response_json["data"]