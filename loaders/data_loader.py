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



def save_inventory(
    path,
    stock_by_id: dict[int, int],
    by_id: dict[int, Product],
    *,
    drop_zeros: bool = True,
    sort_by_name: bool = True
) -> None:

    if not isinstance(stock_by_id, dict):
        raise TypeError("stock_by_id must be dict[int, int]")
    if not isinstance(by_id, dict):
        raise TypeError("by_id must be dict[int, Product]")

    rows = []
    for pid, qty in stock_by_id.items():
        if type(pid) is not int:
            raise TypeError(f"product_id {pid!r} must be int")
        if type(qty) is not int:
            raise TypeError(f"quantity for product_id {pid} must be int")
        if qty < 0:
            raise ValueError(f"quantity for product_id {pid} must be >= 0")
        if drop_zeros and qty == 0:
            continue
        try:
            name = by_id[pid].name
        except KeyError:
            raise KeyError(f"unknown product_id {pid} (not in by_id)")
        rows.append({"name": name, "quantity": qty})

    if sort_by_name:
        rows.sort(key=lambda r: r["name"].strip().casefold())

    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
