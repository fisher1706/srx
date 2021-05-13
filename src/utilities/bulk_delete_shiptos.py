import pytest
from src.api.distributor.shipto_api import ShiptoApi

def test_create_shipto_with_deleted_number(api):
    sa = ShiptoApi(api)

    shiptos = sa.get_shipto_by_number(None)["data"]["entities"]

    for shipto in shiptos:
        if shipto["id"] > 22668:
            try:
                sa.delete_shipto(shipto["id"])
            except:
                print("FAIL")