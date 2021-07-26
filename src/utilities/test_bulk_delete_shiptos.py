from src.api.distributor.shipto_api import ShiptoApi

def test_bulk_delete_shiptos(api):
    sa = ShiptoApi(api)

    shiptos = sa.get_shipto_by_number(None)["data"]["entities"]

    for shipto in shiptos:
        if shipto["id"] > 55774:
            try:
                sa.delete_shipto(shipto["id"])
            except:
                print("FAIL")