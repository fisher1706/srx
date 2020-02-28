from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.product_basis import product_basis
from src.api.admin.universal_catalog_api import UniversalCatalogApi

def no_empty_products_in_universal_catalog(case):
    case.log_name("There are no empty products in the universal catalog")
    case.testrail_config(case.activity.variables.run_number, 1860)

    try:
        uca = UniversalCatalogApi(case)

        start_count = uca.get_universal_catalog(count=True)
        product_basis(case)
        end_count = uca.get_universal_catalog(count=True)
        assert start_count == end_count, f"Empty products should not be added to the universal catalog ({start_count} != {end_count})"

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    no_empty_products_in_universal_catalog(Case(Activity(api_test=True)))