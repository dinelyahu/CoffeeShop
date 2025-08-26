
from CoffeeShop.ItemInOrder import ItemInOrder
from loaders.data_loader import load_products
from pathlib import Path

BASE = Path(__file__).resolve().parent
products = load_products(BASE / "LoadData" / "products.json")
print(f"loaded {len(products)} products")

