# CoffeeShop/main.py
from __future__ import annotations
from pathlib import Path
import sys
import json

# --- לוודא שהייבוא החבילתי יעבוד גם בהרצה ישירה של הקובץ ---
BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# --- imports מסודרים מהחבילה ---
from CoffeeShop.Product import Product
from CoffeeShop.ItemInOrder import ItemInOrder
from CoffeeShop.Order import Order, OrderStatus
from CoffeeShop.Inventory import Inventory
from CoffeeShop.loaders.data_loader import (
    load_products,
    save_inventory,
    index_products_by_id_and_name,
)

DATA_DIR = BASE / "LoadData"
PRODUCTS_PATH = DATA_DIR / "products.json"
INVENTORY_PATH = DATA_DIR / "inventory.json"


# -------- fallback קטן לטעינת המלאי לפי שם -> מזהה --------
def load_inventory_from_json(path: Path, by_name: dict[str, Product]) -> dict[int, int]:
    """
    inventory.json יכול להיות:
    1) [{"name": "...", "quantity": 123}, ...]
    2) {"Espresso": 200, ...}
    מחזיר dict[product_id -> quantity]
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    stock: dict[int, int] = {}
    if isinstance(data, list):
        rows = data
        for i, row in enumerate(rows, start=1):
            try:
                name = str(row["name"])
                qty = int(row["quantity"])
            except Exception as e:
                raise ValueError(f"inventory.json: bad row #{i}: {row!r}") from e
            key = name.strip().casefold()
            if key not in by_name:
                raise KeyError(f"inventory.json: unknown product name: {name!r}")
            pid = by_name[key].id
            if qty < 0:
                raise ValueError(f"inventory.json: quantity must be >= 0 (got {qty})")
            stock[pid] = qty
    elif isinstance(data, dict):
        for name, qty in data.items():
            key = str(name).strip().casefold()
            if key not in by_name:
                raise KeyError(f"inventory.json: unknown product name: {name!r}")
            pid = by_name[key].id
            qty = int(qty)
            if qty < 0:
                raise ValueError(f"inventory.json: quantity must be >= 0 (got {qty})")
            stock[pid] = qty
    else:
        raise TypeError("inventory.json must be a list or an object")

    return stock


# -------- עזרי תצוגה --------
def print_menu(products: list[Product]) -> None:
    print("\n--- תפריט ---")
    for p in products:
        active = "" if p.is_active else " (לא פעיל)"
        print(f"{p.id:>2}. {p.name:20}  {p.category:12}  {p.price:.2f}₪{active}")
    print("-" * 40)

def print_order(order: Order) -> None:
    print("\n--- הזמנה נוכחית ---")
    if not order.items:
        print("(ריקה)")
        return
    for line in order.items:
        total = line.calculate_total_price()
        print(f"{line.product.id:>2}. {line.product.name:20} x {line.quantity:<3} = {total:.2f}₪")
    print(f"סה\"כ: {order.calculate_total_price():.2f}₪")
    # התאמה לשמות שדה שונים אם יש
    status = getattr(order, "status", getattr(order, "_status", None))
    status_name = getattr(status, "name", str(status)) if status else "OPEN"
    print(f"סטטוס: {status_name}")
    print("-" * 40)

def ask_int(prompt: str) -> int:
    while True:
        s = input(prompt).strip()
        try:
            return int(s)
        except ValueError:
            print("בבקשה הזן מספר תקין.")


# -------- Checkout: בדיקה → הורדה → סימון כשולם --------
def checkout(order: Order, inventory: Inventory, by_id: dict[int, Product]) -> bool:
    if not order.items:
        print("אין פריטים בהזמנה.")
        return False

    shortages: list[str] = []
    for line in order.items:
        pid, qty = line.product.id, line.quantity
        try:
            available = inventory.available(pid)
        except KeyError:
            available = 0
        if available < qty:
            shortages.append(f"- {by_id[pid].name}: ביקשת {qty}, יש {available}")

    if shortages:
        print("\nאין מספיק מלאי לפריטים הבאים:\n" + "\n".join(shortages))
        return False

    # מפחיתים בפועל (delta שלילי) ואז מסמנים כשולם
    for line in order.items:
        inventory.add_stock(line.product.id, -line.quantity)
    order.mark_paid()
    print(f"\nשולם בהצלחה! סה\"כ לתשלום: {order.calculate_total_price():.2f}₪")
    return True


def main() -> None:
    print("ברוך הבא לבית הקפה ☕")
    customer = input("שם לקוח: ").strip() or "לקוח"

    # 1) מוצרים + אינדקסים
    products = load_products(PRODUCTS_PATH)
    by_id, by_name = index_products_by_id_and_name(products)

    # 2) מלאי
    stock = load_inventory_from_json(INVENTORY_PATH, by_name)
    inventory = Inventory(stock)

    order = Order(customer)

    actions = {
        "1": "הצג תפריט",
        "2": "הוסף פריט להזמנה",
        "3": "הסר פריט מהזמנה",
        "4": "הצג הזמנה",
        "5": "תשלום ושמירת מלאי",
        "6": "יציאה",
    }

    while True:
        print("\nבחר פעולה:")
        for k, v in actions.items():
            print(f"{k}. {v}")
        choice = input("> ").strip()

        if choice == "1":
            print_menu(products)

        elif choice == "2":
            print_menu(products)
            pid = ask_int("מזהה פריט (id): ")
            if pid not in by_id:
                print("מזהה פריט לא קיים.")
                continue
            qty = ask_int("כמות: ")
            if qty <= 0:
                print("כמות חייבת להיות גדולה מאפס.")
                continue
            try:
                order.add_item(by_id[pid], qty)
                print(f"התווסף: {by_id[pid].name} x {qty}")
            except Exception as e:
                print(f"שגיאה בהוספה: {e}")

        elif choice == "3":
            if not order.items:
                print("אין מה להסיר—ההזמנה ריקה.")
                continue
            print_order(order)
            pid = ask_int("מזהה פריט להסרה: ")
            qty = ask_int("כמות להסרה: ")
            try:
                order.remove_item(pid, qty)
                print("עודכן.")
            except Exception as e:
                print(f"שגיאה בהסרה: {e}")

        elif choice == "4":
            print_order(order)

        elif choice == "5":
            ok = checkout(order, inventory, by_id)
            if ok:
                try:
                    save_inventory(INVENTORY_PATH, dict(inventory.stock), by_id, drop_zeros=True, sort_by_name=True)
                    print(f"המלאי נשמר ל־{INVENTORY_PATH.name}.")
                except Exception as e:
                    print(f"שגיאה בשמירת המלאי: {e}")
                # פותחים הזמנה חדשה לאחר תשלום
                order = Order(customer)

        elif choice == "6":
            print("ביי! 👋")
            break

        else:
            print("בחירה לא מוכרת.")


if __name__ == "__main__":
    main()
