from src.api.distributor.product_api import ProductApi
from src.api.api_methods import ApiMethods as apim
import random


def product_basis(case, product_dto=None):
    pa = ProductApi(case)

    if (product_dto is None):
        product_dto = apim.get_dto("product_dto.json")
        product_dto["partSku"] = case.random_string_u(18)
        product_dto["shortDescription"] = product_dto["partSku"] + " - short description"
        product_dto["roundBuy"] = random.choice(range(1, 100))

    pa.create_product(product_dto.copy())

    return product_dto.copy()