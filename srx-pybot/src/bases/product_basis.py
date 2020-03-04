from src.api.distributor.product_api import ProductApi
from src.resources.tools import Tools
import random


def product_basis(case, product_dto=None):
    pa = ProductApi(case)

    if (product_dto is None):
        product_dto = Tools.get_dto("product_dto.json")
        product_dto["partSku"] = Tools.random_string_u(18)
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = random.choice(range(2, 100))

    pa.create_product(product_dto.copy())

    return product_dto.copy()