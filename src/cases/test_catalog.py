import pytest
from src.resources.tools import Tools
from src.resources.locator import Locator
from src.pages.distributor.catalog_page import CatalogPage
from src.pages.admin.universal_catalog_page import UniversalCatalogPage
from src.pages.general.login_page import LoginPage
from src.api.admin.universal_catalog_api import UniversalCatalogApi
from src.api.distributor.product_api import ProductApi
from src.api.setups.setup_product import setup_product

class TestCatalog():
    @pytest.mark.regression
    def test_product_crud(self, ui):
        ui.testrail_case_id = 33

        lp = LoginPage(ui)
        cp = CatalogPage(ui)
        product_body = cp.product_body.copy()
        edit_product_body = cp.product_body.copy()

        #-------------------
        product_body["partSku"] = Tools.random_string_u(18)
        product_body["shortDescription"] = f"{product_body['partSku']} - short description"
        product_body["roundBuy"] = "15"
        #-------------------
        edit_product_body["partSku"] = Tools.random_string_u(18)
        edit_product_body["shortDescription"] = f"{product_body['partSku']} - edit short description"
        edit_product_body["roundBuy"] = "27"
        edit_product_body["lifecycleStatus"] = "OBSOLETE"
        edit_product_body["image"] = "agilevision.io"
        edit_product_body["longDescription"] = "long description"
        edit_product_body["weight"] = "100"
        edit_product_body["height"] = "200"
        edit_product_body["width"] = "300"
        edit_product_body["depth"] = "400"
        edit_product_body["issueQuantity"] = "500"
        edit_product_body["packageConversion"] = "600"
        edit_product_body["manufacturerPartNumber"] = "700"
        edit_product_body["manufacturer"] = "800"
        edit_product_body["alternative"] = "900"
        edit_product_body["productLvl1"] = "1000"
        edit_product_body["productLvl2"] = "1100"
        edit_product_body["productLvl3"] = "1200"
        edit_product_body["attribute1"] = "1300"
        edit_product_body["attribute2"] = "1400"
        edit_product_body["attribute3"] = "1500"
        edit_product_body["gtin"] = "1600"
        edit_product_body["upc"] = "1700"
        edit_product_body["keyword"] = "1800"
        edit_product_body["unitName"] = "1900"
        #-------------------

        lp.log_in_distributor_portal()
        cp.sidebar_catalog()
        cp.create_product(product_body.copy())
        cp.check_last_product(product_body.copy())
        cp.update_last_product(edit_product_body.copy())
        cp.check_last_product(edit_product_body.copy())

    @pytest.mark.regression
    def test_product_import(self, ui):
        ui.testrail_case_id = 34

        lp = LoginPage(ui)
        cp = CatalogPage(ui)
        product_body = cp.product_body.copy()

        #-------------------
        product_body["partSku"] = Tools.random_string_u(18)
        product_body["shortDescription"] = f"{product_body['partSku']} - short description"
        product_body["roundBuy"] = "39"
        #-------------------
        products = [
            [product_body["partSku"], None, None, product_body["shortDescription"], None, None, None, None, None, None, None, None, None, product_body["roundBuy"], None, None, None, None, None, None, None, None, None, None, None, None, None]
        ]
        #-------------------

        lp.log_in_distributor_portal()
        cp.sidebar_catalog()
        cp.import_product(products)
        cp.check_last_product(product_body.copy())

    @pytest.mark.regression
    def test_universal_catalog_crud(self, ui):
        ui.testrail_case_id = 1857
        
        lp = LoginPage(ui)
        ucp = UniversalCatalogPage(ui)
        universal_product_body = ucp.universal_product_body.copy()
        edit_universal_product_body = ucp.universal_product_body.copy()

        #-------------------
        universal_product_body["upc"] = Tools.random_string_u(18)
        universal_product_body["manufacturerPartNumber"] = Tools.random_string_u(18)
        #-------------------
        edit_universal_product_body["manufacturerPartNumber"] = Tools.random_string_u(18)
        edit_universal_product_body["manufacturer"] = Tools.random_string_u(18)
        edit_universal_product_body["gtin"] = Tools.random_string_u(18)
        edit_universal_product_body["upc"] = Tools.random_string_u(18)
        #-------------------
        table_body = ucp.remapping_to_table_keys(universal_product_body.copy())
        edit_table_body = ucp.remapping_to_table_keys(edit_universal_product_body.copy())

        lp.log_in_admin_portal()
        ucp.sidebar_universal_catalog()
        ucp.create_universal_product(universal_product_body.copy())
        ucp.open_last_page()
        new_product_row = ucp.scan_table(universal_product_body["upc"], "UPC", table_body.copy())
        ucp.update_universal_product(edit_universal_product_body.copy(), new_product_row)
        new_product_row = ucp.scan_table(edit_universal_product_body["upc"], "UPC", edit_table_body.copy())
        ucp.delete_universal_product(new_product_row)

    @pytest.mark.regression
    def test_universal_catalog_import(self, ui):
        ui.testrail_case_id = 1858

        lp = LoginPage(ui)
        ucp = UniversalCatalogPage(ui)
        universal_product_body = ucp.universal_product_body.copy()

        #-------------------
        universal_product_body["manufacturerPartNumber"] = Tools.random_string_u(18)
        universal_product_body["manufacturer"] = Tools.random_string_u(18)
        universal_product_body["gtin"] = Tools.random_string_u(18)
        universal_product_body["upc"] = Tools.random_string_u(18)
        #-------------------
        table_body = ucp.remapping_to_table_keys(universal_product_body.copy())

        universal_catalog_import = [
            [universal_product_body["upc"], universal_product_body["gtin"], universal_product_body["manufacturer"], universal_product_body["manufacturerPartNumber"]]
        ]

        lp.log_in_admin_portal()
        ucp.sidebar_universal_catalog()
        ucp.import_universal_catalog(universal_catalog_import)
        ucp.open_last_page()
        new_product_row = ucp.scan_table(universal_product_body["upc"], "UPC", table_body.copy())
        ucp.delete_universal_product(new_product_row)

    @pytest.mark.regression
    def test_no_empty_products_in_universal_catalog(self, api):
        api.testrail_case_id = 1860

        uca = UniversalCatalogApi(api)

        start_count = uca.get_universal_catalog(count=True)
        setup_product(api)
        end_count = uca.get_universal_catalog(count=True)
        assert start_count == end_count, f"Empty products should not be added to the universal catalog ({start_count} != {end_count})"

    @pytest.mark.regression
    def test_universal_catalog_by_distributor_catalog(self, api):
        api.testrail_case_id = 1859

        uca = UniversalCatalogApi(api)

        product_dto = Tools.get_dto("product_dto.json")
        product_dto["partSku"] = Tools.random_string_u(18)
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = "1"
        product_dto["upc"] = Tools.random_string_u(18)
        product_dto["gtin"] = Tools.random_string_u(18)
        product_dto["manufacturer"] = Tools.random_string_u(18)
        product_dto["manufacturerPartNumber"] = Tools.random_string_u(18)

        setup_product(api, product_dto=product_dto)
        universal_catalog = uca.get_universal_catalog(upc=product_dto["upc"], gtin=product_dto["gtin"], manufacturer=product_dto["manufacturer"], manufacturer_part_number=product_dto["manufacturerPartNumber"])
        assert len(universal_catalog) == 1, "Only 1 element in universal catalog should match to the filter"
        assert universal_catalog[0]["distributorName"] == api.data.distributor_name
        assert universal_catalog[0]["upc"] == product_dto["upc"]


    @pytest.mark.smoke
    def test_smoke_import_prodcut(self, smoke_api):
        smoke_api.testrail_case_id = 2004
        pa = ProductApi(smoke_api)

        response = pa.get_upload_url()
        url = response["url"]
        filename = response["filename"]
        pa.file_upload(url)
        import_status = pa.get_import_status(filename)
