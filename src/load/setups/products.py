from src.api.setups.setup_product import SetupProduct

def test_product_setup(load_api):
    for index in range(2000000):
        setup_product = SetupProduct(load_api)
        if index%5 == 0:
            setup_product.add_option("serialized")
            setup_product.add_option("round_buy", 1)
        setup_product.setup(201)
