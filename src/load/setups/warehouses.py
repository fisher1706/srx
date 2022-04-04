from src.api.distributor.warehouse_api import WarehouseApi
from src.resources.tools import Tools

def test_warehouses_setup(load_api):
    wa = WarehouseApi(load_api)

    for index in range(1000):
        body = Tools.get_dto("warehouse_dto.json")
        body["name"] = f"{index}"
        body["number"] = f"{index}"
        body["contactEmail"] = f"load.contact.{index}@agilevision.io"
        body["invoiceEmail"] = f"load.invoice.{index}@agilevision.io"
        wa.create_warehouse(body)
