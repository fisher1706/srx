from src.resources.tools import Tools
products = []
locations = []
for i in range(100):
    SKU = Tools.random_string_u(20)
    product_row = [SKU, None, None, SKU, None, None, None, None, None, None, None, None, None, 10, None, None, None, None, None, None, None, None, None, None, None, None, None]
    location_row = [SKU,SKU,SKU,SKU,None,None,None,None,SKU,10,20,"LABEL",SKU+"_cust",None,"Customer","off",1]
    products.append(product_row)
    locations.append(location_row)
    
Tools.generate_csv("products.csv", products)
Tools.generate_csv("locations.csv", locations)