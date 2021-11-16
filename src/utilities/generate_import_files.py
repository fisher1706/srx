import os
import csv
import string
import random

def generate_csv(filename, rows):
        folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder += "/output/"+filename
        headers = []
        for header in range(len(rows[0])):
            headers.append(header)
        table = []
        table.append(headers)
        for row in rows:
            table.append(row)
        with open(folder, "w", newline="", encoding="utf8") as file:
            writer = csv.writer(file)
            writer.writerows(table)

def random_string_u(length=10):
        letters = string.ascii_uppercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

products = []
locations = []
pricing = []
rfids = []
usage_history = []
crib_crawl = []
body = []
for i in range(50000):
    SKU = random_string_u(20)

    product_row = [SKU, SKU, None, SKU, None, SKU, None, None, None, None, None, None, SKU, SKU, 1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
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

generate_csv("products.csv", products)
generate_csv("locations.csv", locations)
generate_csv("pricing.csv", pricing)
generate_csv("rfids.csv", rfids)
generate_csv("usage_history.csv", usage_history)
generate_csv("crib_crawl.csv", crib_crawl)