from src.api.api import API
from src.fixtures.decorators import Decorator
from src.resources.messages import Message
import requests
import os
import time

class ProductApi(API):
    @Decorator.default_expected_code(201)
    def create_product(self, dto, expected_status_code):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/products/create")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 201):
            self.logger.info(f"New product '{dto['partSku']}' has been successfully created")
            response_json = response.json()
            product_id = (response_json["data"].split("/"))[-1]
            return product_id
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Product", operation="creation", status_code=response.status_code, content=response.content))

    def get_upload_url(self):
        url = self.url.get_api_url_for_env("/distributor-portal/distributor/products/upload-url")
        token = self.get_distributor_token()
        response = self.send_get(url, token)
        if (response.status_code == 200):
            self.logger.info(Message.entity_operation_done.format(entity="Upload URL", operation="created"))
        else:
            self.logger.error(str(response.content))
        response_json = response.json()
        return_response = {
            "url": response_json["data"]["url"],
            "filename": response_json["data"]["fileName"]
        }
        return return_response

    def file_upload(self, url, retries=3):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/dto/smoke-product-template.csv"
        files = {"file": (path, open(path, "rb"))}
        timeout = 0.2
        for i in range(retries+1):
            try:
                response = requests.put(url, files=files)
            except:
                self.logger.info(f"Usuccessful attempt to put a file. Retry in {timeout} sec")
                time.sleep(timeout)
                timeout *= 2
                continue
            else:
                break
        else:
            self.logger.error("Max retries exceeded")
        if (response.status_code == 200):
            self.logger.info(Message.entity_operation_done.format(entity="File", operation="upload"))
        else:
            self.logger.error(str(response.content))

    def get_import_status(self, filename, type="PARSE_AND_VALIDATE"):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/import-status/Products/{filename}")
        params = {
            "type": type
        }
        token = self.get_distributor_token()
        for i in range(30):
            response = self.send_get(url, token, params=params)
            if (response.status_code == 404):
                self.logger.info(f"File not found. Next attempt after 5 seconds")
                time.sleep(5)
                continue
            elif (response.status_code == 200):
                self.logger.info(Message.entity_operation_done.format(entity="File status", operation="got"))
                break
            else:
                self.logger.error(str(response.content))
        else:
            self.logger.error("File not found after 30 seconds waiting")
        response_json = response.json()
        return response_json["data"]

    @Decorator.default_expected_code(200)
    def update_product(self, dto, product_id, expected_status_code):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/products/{product_id}/update")
        token = self.get_distributor_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info(f"Product with SKU = '{dto['partSku']}' has been successfully updated")
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Product", operation="updating", status_code=response.status_code, content=response.content))

    def get_product(self, product_sku=None):
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/products")
        params = {
            "partSku": product_sku
        }
        token = self.get_distributor_token()
        response = self.send_get(url, token, params=params)
        if (response.status_code == 200):
            self.logger.info(Message.entity_operation_done.format(entity="Product", operation="got"))
            response_json = response.json()
            return response_json["data"]["entities"]
        else:
            self.logger.error(str(response.content))

    def get_customer_product(self, customer_id=None, product_sku=None):
        if customer_id is None:
            customer_id = self.data.customer_id
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{customer_id}/products")
        params = {
            "partSku": product_sku
        }
        token = self.get_distributor_token()
        response = self.send_get(url, token, params=params)
        if (response.status_code == 200):
            self.logger.info(Message.entity_operation_done.format(entity="Customer product", operation="got"))
            response_json = response.json()
            return response_json["data"]["entities"]
        else:
            self.logger.error(str(response.content))

    @Decorator.default_expected_code(200)
    def update_customer_product(self, dto, product_id, expected_status_code, customer_id=None):
        if customer_id is None:
            customer_id = self.data.customer_id
        url = self.url.get_api_url_for_env(f"/distributor-portal/distributor/customers/{customer_id}/products/{product_id}")
        token = self.get_distributor_token()
        response = self.send_put(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected_status_code=expected_status_code, actual_status_code=response.status_code, content=response.content)
        if (response.status_code == 200):
            self.logger.info(f"Customer product with SKU = '{dto['partSku']}' has been successfully updated")
        else:
            self.logger.info(Message.info_operation_with_expected_code.format(entity="Customer product", operation="updating", status_code=response.status_code, content=response.content))