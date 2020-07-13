from src.api.distributor.product_api import ProductApi
from src.resources.tools import Tools
import random


def setup_product(context, product_dto=None, is_asset=None, sku=None, is_serialized=None, is_lot=None, package_conversion=None, expected_status_code=None):
    pa = ProductApi(context)

    if (product_dto is None):
        product_dto = Tools.get_dto("product_dto.json")
        if (sku is None):
            product_dto["partSku"] = Tools.random_string_u(18)
        else:
            product_dto["partSku"] = sku
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = random.choice(range(2, 100))
        if (is_asset is not None):
            product_dto["assetFlag"] = bool(is_asset)
        if (is_serialized is not None):
            product_dto["serialized"] = bool(is_serialized)
        if (is_lot is not None):
            product_dto["lot"] = bool(is_lot)
        if (package_conversion is not None):
            product_dto["packageConversion"] = package_conversion

    product_id = pa.create_product(product_dto.copy(), expected_status_code=expected_status_code)
    product_dto["id"] = product_id

    return product_dto.copy()