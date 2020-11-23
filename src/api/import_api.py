from src.api.api import API
from src.resources.tools import Tools
import os
import time
import requests

class ImportApi(API):
    def full_import_usage_history(self, body, customer_id=None):
        if customer_id is None:
            customer_id = self.data.customer_id
        upload_url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{customer_id}/usage/history/upload-url")
    
        Tools.generate_csv("usage_history.csv", body)
        upload_url_response = self.get_upload_url(upload_url)

        url = upload_url_response["url"]
        filename = upload_url_response["filename"]
        import_status_url_validate = self.url.get_api_url_for_env(f"/distributor-portal/distributor/import-status/UsageHistory/{filename}?type=PARSE_AND_VALIDATE")
        import_status_url_save = self.url.get_api_url_for_env(f"/distributor-portal/distributor/import-status/UsageHistory/{filename}?type=PARSE_AND_SAVE")
        parse_url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/parse/UsageHistory/{filename}")

        self.file_upload(url, "usage_history.csv")
        self.get_import_status(import_status_url_validate)
        self.parse(parse_url)
        self.get_import_status(import_status_url_save)

    def get_upload_url(self, url):
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

    def file_upload(self, url, filename, retries=3):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path += "/output/"+filename
        files = {"file": (path, open(path, "rb"))}
        timeout = 0.2
        response = None
        for i in range(retries+1):
            try:
                response = requests.put(url, files=files)
            except:
                time.sleep(timeout)
                timeout *= 2
                continue
            else:
                break
        else:
            self.logger.error("Max retries exceeded: "+str(response.content))
        if (response.status_code == 200):
            self.logger.info(f"File has been successfuly upload")
        else:
            self.logger.error(str(response.content))

    def get_import_status(self, url):
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

    def parse(self, url):
        token = self.get_distributor_token()
        response = self.send_post(url, token)
        if (response.status_code == 200):
            self.logger.info(f"File has been succesfully parsed")
        else:
            self.logger.error(str(response.content))