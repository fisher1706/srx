
def get_generation(id, status):
    return {
        "generationId": id,
        "billToId": 12625,
        "priceBranch": "12",
        "shipBranch": "10",
        "glBranch": "12",
        "salesSource": "INS",
        "orderDate": "2021-08-25T05:00:00Z",
        "shipToId": 102235,
        "status": status,
        "invoiceNumber": 1,
        "shipDate": "2021-08-26T05:00:00Z",
        "requiredDate": "2021-08-25T05:00:00Z",
        "poNumber": "CRIB 8/25/2021",
    }

def get_line(line_id, quantities):
    generations = []
    for index, item in enumerate(quantities):
        generations.append(get_line_generation(line_id, index + 1, item))
    return {
        "lineId": line_id,
        "productId": 5,
        "orderQty": 100,
        "taxableCode": 1,
        "generations": generations
    }

def get_line_generation(line_id, generation_id, stock_qty):
    return {
        "generationId": generation_id,
        "labelPerQuantity": "",
        "lineId": line_id,
        "productId": 5,
        "stockQty": stock_qty,
        "nonstockQty": 0
    }

def create_generation(name_orders):
    generations = []
    for index, item in enumerate(name_orders):
        generations.append(get_generation(index+1, item))

    return generations


def create_data_order(data_orders, number=1):
    name_orders = [data.get("status") for data in data_orders if data.get("status")]
    qnt_orders = [data.get("qnt") for data in data_orders if data.get("qnt")]

    generations = [create_generation(name_orders)]
    lines = [get_line(number, qnt_orders)]

    return generations, lines



if __name__ == '__main__':


    data = [{"trans": "XX-1"}, {"qnt": 10}, {"status": "Invoice"},
            {"trans": "XX-2"}, {"qnt": 20}, {"status": "PickUpNow"}]

    x, y = create_data_order(data)
    print(x)
    print(y)






