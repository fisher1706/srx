from src.resources.case import Case
from src.resources.activity import Activity
from src.api.distributor.product_api import ProductApi

def import_product(case):
    case.log_name("Import product")
    case.testrail_config(2004)

    try:
        pa = ProductApi(case)

        response = pa.get_upload_url()
        url = response["url"]
        filename = response["filename"]
        pa.file_upload(url)
        import_status = pa.get_import_status(filename)

        case.finish_case()
    except:
        case.critical_finish_case()
    
if __name__ == "__main__":
    case = Case(Activity(api_test=True, smoke=True))
    ProductApi(case).get_distributor_token()
    import_product(case)