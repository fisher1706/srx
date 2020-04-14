from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.product_basis import product_basis
from src.api.admin.universal_catalog_api import UniversalCatalogApi
from src.resources.tools import Tools

def universal_catalog_by_distributor_catalog(case):
    case.log_name("Add new element to the universal catalog by adding it to the distributor catalog")
    case.testrail_config(1859)

    try:
        uca = UniversalCatalogApi(case)

        product_dto = Tools.get_dto("product_dto.json")
        product_dto["partSku"] = Tools.random_string_u(18)
        product_dto["shortDescription"] = f"{product_dto['partSku']} - short description"
        product_dto["roundBuy"] = "1"
        product_dto["upc"] = Tools.random_string_u(18)
        product_dto["gtin"] = Tools.random_string_u(18)
        product_dto["manufacturer"] = Tools.random_string_u(18)
        product_dto["manufacturerPartNumber"] = Tools.random_string_u(18)

        product_body = product_basis(case, product_dto=product_dto)
        universal_catalog = uca.get_universal_catalog(upc=product_dto["upc"], gtin=product_dto["gtin"], manufacturer=product_dto["manufacturer"], manufacturer_part_number=product_dto["manufacturerPartNumber"])
        assert len(universal_catalog) == 1, "Only 1 element in universal catalog should match to the filter"
        assert universal_catalog[0]["distributorName"] == case.activity.variables.distributor_name
        assert universal_catalog[0]["upc"] == product_dto["upc"]

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    universal_catalog_by_distributor_catalog(Case(Activity(api_test=True)))