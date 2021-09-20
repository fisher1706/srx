import time
import random
import pytest
from src.resources.tools import Tools
from src.pages.general.login_page import LoginPage
from src.pages.distributor.pricing_page import PricingPage
from src.resources.permissions import Permissions
from src.api.setups.setup_location import SetupLocation
from src.api.distributor.settings_api import SettingsApi
from src.api.distributor.location_api import LocationApi

@pytest.mark.parametrize("permissions", [
    {
        "user": None,
        "testrail_case_id": 35
    },
    {
        "user": Permissions.pricing("EDIT"),
        "testrail_case_id": 2277
    }
    ])
@pytest.mark.acl
@pytest.mark.regression
def test_pricing_import(ui, permission_ui, permissions, delete_distributor_security_group):
    ui.testrail_case_id = permissions["testrail_case_id"]
    context = Permissions.set_configured_user(ui, permissions["user"], permission_context=permission_ui)

    lp = LoginPage(context)
    pp = PricingPage(context)
    pricing_body = pp.pricing_body.copy()
    temporary_price = str(random.choice(range(100)))

    #-------------------
    pricing_body["Distributor SKU"] = "PRICING_SKU"
    pricing_body["Price"] = "$"+temporary_price+".00"
    pricing_body["UOM"] = "M"
    pricing_body["Expiration Date"] = "Fri, Dec 12, 2025"
    #-------------------
    pricing = [
        [pricing_body["Distributor SKU"], temporary_price, pricing_body["UOM"], "12/12/2025 10:15:30"]
    ]
    #-------------------

    lp.log_in_distributor_portal()
    pp.sidebar_pricing()
    pp.select_customer_shipto(customer_name=ui.data.customer_name)
    pp.import_pricing(pricing)
    pp.select_customer_shipto(customer_name=ui.data.customer_name)
    pp.check_price_by_name(pricing_body.copy())

@pytest.mark.regression
def test_price_is_updated_after_disabling_cache(ui, delete_shipto):
    ui.testrail_case_id = 7608
    sta = SettingsApi(ui)
    lp = LoginPage(ui)
    pp = PricingPage(ui)
    la = LocationApi(ui)

    product_dto = Tools.get_dto("product_dto.json")
    product_dto["partSku"] = "PRICING_SKU"
    product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
    product_dto["roundBuy"] = "1"
    product_dto["upc"] = Tools.random_string_u(18)
    product_dto["gtin"] = Tools.random_string_u(18)
    product_dto["manufacturer"] = Tools.random_string_u(18)
    product_dto["manufacturerPartNumber"] = Tools.random_string_u(18)

    setup_location = SetupLocation(ui)
    setup_location.add_option("product", product_dto)
    response_location = setup_location.setup()

    location_responce = la.get_location_by_sku(sku="PRICING_SKU", shipto_id=response_location["shipto_id"])
    price = location_responce[0]["orderingConfig"]["price"]
    pricing_body = pp.pricing_body.copy()
    temporary_price = str(random.choice(range(100)))

    #-------------------
    pricing_body["Distributor SKU"] = "PRICING_SKU"
    pricing_body["Price"] = "$"+temporary_price+".00"
    pricing_body["UOM"] = "M"
    pricing_body["Expiration Date"] = "Fri, Dec 12, 2025"
    #-------------------
    pricing = [
        [pricing_body["Distributor SKU"], temporary_price, pricing_body["UOM"], "12/12/2025 10:15:30"]
    ]
    #-------------------

    lp.log_in_distributor_portal()
    pp.sidebar_pricing()
    pp.select_customer_shipto(customer_name=ui.data.customer_name)
    pp.import_pricing(pricing)

    location_responce_updated = la.get_location_by_sku(sku="PRICING_SKU", shipto_id=response_location["shipto_id"])
    price_after_update = location_responce_updated[0]["orderingConfig"]["price"]

    assert price == price_after_update

    response_cache = sta.get_cache_settings(shipto_id=response_location["shipto_id"])

    response_cache["pricingSource"]["settings"]["useCache"] = False
    response_cache["pricingSource"]["defaultSettings"]["useCache"] = False
    response_cache["pricingSource"]["useDefault"] = False
    response_cache.pop("orderCloseSettings", None)
    response_cache.pop("replenishmentListRules", None)

    sta.update_cache_settings(dto=response_cache, shipto_id=response_location["shipto_id"])

    la.check_updated_price(name="PRICING_SKU", shipto_id=response_location["shipto_id"], expected_price=float(temporary_price))

@pytest.mark.regression
def test_price_is_not_updated(ui, delete_shipto):
    ui.testrail_case_id = 7606
    sta = SettingsApi(ui)
    lp = LoginPage(ui)
    pp = PricingPage(ui)
    la = LocationApi(ui)

    product_dto = Tools.get_dto("product_dto.json")
    product_dto["partSku"] = "PRICING_SKU"
    product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
    product_dto["roundBuy"] = "1"
    product_dto["upc"] = Tools.random_string_u(18)
    product_dto["gtin"] = Tools.random_string_u(18)
    product_dto["manufacturer"] = Tools.random_string_u(18)
    product_dto["manufacturerPartNumber"] = Tools.random_string_u(18)


    setup_location = SetupLocation(ui)
    setup_location.add_option("product", product_dto)
    response_location = setup_location.setup()

    location_responce = la.get_location_by_sku(sku="PRICING_SKU", shipto_id=response_location["shipto_id"])
    price = location_responce[0]["orderingConfig"]["price"]
    pricing_body = pp.pricing_body.copy()
    temporary_price = str(random.choice(range(100)))

    #-------------------
    pricing_body["Distributor SKU"] = "PRICING_SKU"
    pricing_body["Price"] = "$"+temporary_price+".00"
    pricing_body["UOM"] = "M"
    pricing_body["Expiration Date"] = "Fri, Dec 12, 2025"
    #-------------------
    pricing = [
        [pricing_body["Distributor SKU"], temporary_price, pricing_body["UOM"], "12/12/2025 10:15:30"]
    ]
    #-------------------
    response_cache = sta.get_cache_settings(shipto_id=response_location["shipto_id"])

    response_cache["pricingSource"]["settings"]["useCache"] = False
    response_cache["pricingSource"]["defaultSettings"]["useCache"] = True
    response_cache["pricingSource"]["useDefault"] = False
    response_cache.pop("orderCloseSettings", None)
    response_cache.pop("replenishmentListRules", None)

    sta.update_cache_settings(dto=response_cache, shipto_id=response_location["shipto_id"])

    lp.log_in_distributor_portal()
    pp.sidebar_pricing()
    pp.select_customer_shipto(customer_name=ui.data.customer_name)
    pp.import_pricing(pricing)

    location_responce_updated = la.get_location_by_sku(sku="PRICING_SKU", shipto_id=response_location["shipto_id"])
    price_after_update = location_responce_updated[0]["orderingConfig"]["price"]

    for _ in range(6):
        assert price == price_after_update
        time.sleep(5)

@pytest.mark.regression
def test_price_is_updated(ui, delete_shipto):
    ui.testrail_case_id = 7607
    sta = SettingsApi(ui)
    lp = LoginPage(ui)
    pp = PricingPage(ui)
    la = LocationApi(ui)

    product_dto = Tools.get_dto("product_dto.json")
    product_dto["partSku"] = "PRICING_SKU"
    product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
    product_dto["roundBuy"] = "1"
    product_dto["upc"] = Tools.random_string_u(18)
    product_dto["gtin"] = Tools.random_string_u(18)
    product_dto["manufacturer"] = Tools.random_string_u(18)
    product_dto["manufacturerPartNumber"] = Tools.random_string_u(18)


    setup_location = SetupLocation(ui)
    setup_location.add_option("product", product_dto)
    response_location = setup_location.setup()

    pricing_body = pp.pricing_body.copy()
    temporary_price = str(random.choice(range(100)))

    #-------------------
    pricing_body["Distributor SKU"] = "PRICING_SKU"
    pricing_body["Price"] = "$"+temporary_price+".00"
    pricing_body["UOM"] = "M"
    pricing_body["Expiration Date"] = "Fri, Dec 12, 2025"
    #-------------------
    pricing = [
        [pricing_body["Distributor SKU"], temporary_price, pricing_body["UOM"], "12/12/2025 10:15:30"]
    ]
    #-------------------
    response_cache = sta.get_cache_settings(shipto_id=response_location["shipto_id"])

    response_cache["pricingSource"]["settings"]["useCache"] = False
    response_cache["pricingSource"]["defaultSettings"]["useCache"] = False
    response_cache["pricingSource"]["useDefault"] = False
    response_cache.pop("orderCloseSettings", None)
    response_cache.pop("replenishmentListRules", None)

    sta.update_cache_settings(dto=response_cache, shipto_id=response_location["shipto_id"])

    lp.log_in_distributor_portal()
    pp.sidebar_pricing()
    pp.select_customer_shipto(customer_name=ui.data.customer_name)
    pp.import_pricing(pricing)

    la.check_updated_price(name="PRICING_SKU", shipto_id=response_location["shipto_id"], expected_price=float(temporary_price))
   