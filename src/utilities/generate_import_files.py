from src.resources.tools import Tools
products = []
locations = []
pricing = []
rfids = []
usage_history = []
crib_crawl = []
body = []
for i in range(500):
    SKU = Tools.random_string_u(20)

    product_row = [SKU, None, None, SKU, None, None, None, None, None, None, None, None, None, 10, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    location_row = [SKU,SKU,SKU,SKU,None,None,None,None,SKU,10,20,"LABEL",SKU+"_cust",None,"Customer","off",1]
    pricing_row = [SKU, 10, 1, "2030-12-12T10:15:30"]
    rfid_row = [SKU, SKU, SKU]
    usage_history_row = [SKU, SKU, SKU, SKU, SKU, 10, "12/30/18 10:15:30"]
    crib_crawl_row = [SKU,None,None,None,10,20,SKU,SKU,SKU,SKU,None,None,None,None,"LABEL",None,None]

    products.append(product_row)
    locations.append(location_row)
    pricing.append(pricing_row)
    rfids.append(rfid_row)
    usage_history.append(usage_history_row)
    crib_crawl.append(crib_crawl_row)
    body.append({"partSku": SKU, "quantity": 100})

print(body)

Tools.generate_csv("products.csv", products)
Tools.generate_csv("locations.csv", locations)
Tools.generate_csv("pricing.csv", pricing)
Tools.generate_csv("rfids.csv", rfids)
Tools.generate_csv("usage_history.csv", usage_history)
Tools.generate_csv("crib_crawl.csv", crib_crawl)