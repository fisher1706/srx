from src.api.distributor.product_api import ProductApi
from src.resources.tools import Tools
import random


def setup_product(context, product_dto=None, is_asset=False, sku=None):
    pa = ProductApi(context)

    if (product_dto is None):
        product_dto = Tools.get_dto("product_dto.json")
        if (sku is None):
            product_dto["partSku"] = Tools.random_string_u(18)
        else:
            product_dto["partSku"] = sku
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = random.choice(range(2, 100))
        if (is_asset is True):
            product_dto["assetFlag"] = True

    pa.create_product(product_dto.copy())

    return product_dto.copy()