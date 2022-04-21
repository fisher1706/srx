from src.api.api import API
from src.fixtures.decorators import default_expected_code
from src.resources.messages import Message
from glbl import LOG, ERROR

class CustomerProductApi(API):
    @default_expected_code(201)
    def create_product(self, dto, supplier_id, expected_status_code=None):
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/distributors/{supplier_id}/products")
        token = self.get_customer_token()
        response = self.send_post(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 201:
            LOG.info(f"New product '{dto['partSku']}' has been successfully created")
            response_json = response.json()
            product_id = response_json["data"]["id"]
            return product_id
        LOG.info(Message.info_operation_with_expected_code.format(entity="Product", operation="creation", status_code=response.status_code, content=response.content))

    @default_expected_code(200)
    def update_product(self, dto, product_id, expected_status_code=None):
        url = self.url.get_api_url_for_env(f"/customer-portal/customer/products/{product_id}")
        token = self.get_customer_token()
        response = self.send_put(url, token, dto)
        assert expected_status_code == response.status_code, Message.assert_status_code.format(expected=expected_status_code, actual=response.status_code, content=response.content)
        if response.status_code == 200:
            LOG.info(f"Product with SKU = '{dto['partSku']}' has been successfully updated")
        else:
            LOG.info(Message.info_operation_with_expected_code.format(entity="Product", operation="updating", status_code=response.status_code, content=response.content))

    def get_product(self, distributor_ids, product_sku=None):
        url = self.url.get_api_url_for_env("/customer-portal/customer/products")
        params = {
            "distributorIds": distributor_ids,
            "orderingConfig.product.partSku": product_sku
        }
        token = self.get_customer_token()
        response = self.send_get(url, token, params=params)
        if response.status_code == 200:
            LOG.info(Message.entity_operation_done.format(entity="Product", operation="got"))
            response_json = response.json()
            return response_json["data"]["entities"]
        ERROR(str(response.content))
