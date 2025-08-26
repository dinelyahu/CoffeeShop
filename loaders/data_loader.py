from CoffeeShop.Product import Product
import json
from typing import List


#function for loading json file and create list of Products
def load_products(path) -> List[Product]:
    with open(path, 'r' , encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data , list):
        raise ValueError('The data must contain a list of items')

    products = []

    seen = set()
    for i , item in enumerate(data, start = 1):
        try:
            name = item['name']
            price = item['price']
            category = item['category']
            is_active = item['is_active']
        except KeyError as e:
            raise KeyError(f"Missing value in row {i}")

        if name in seen:
            raise ValueError(f"You can't create duplicates with product: {name}")
        seen.add(name)

        products.append(Product(name, price, category, is_active))

    return products


# Creating a 2 dicts for "id" : Product , "name" : product
def index_products_by_id_and_name(products: List[Product])-> tuple[dict[int , Product] , dict[str , Product]]:
    by_id = {}
    by_name = {}


    for product in products:

        by_id[product.id] = product
        by_name[product.name.strip().casefold()] = product


    return by_id , by_name




