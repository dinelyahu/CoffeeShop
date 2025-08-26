from types import MappingProxyType


class Inventory:

    def __init__(self , stock: dict[int , int]):
        self.stock = stock


    #methods:

    @property
    def stock(self):
        return MappingProxyType(self._stock)

    @stock.setter
    def stock(self, stock_dict):
        if not isinstance(stock_dict, dict):
            raise TypeError("Error! The type must be : dict[int, int]")
        validated = {}
        for key , value  in stock_dict.items():
            if not isinstance(key, int) or not isinstance(value , int) or isinstance(value , bool) or isinstance(key, bool):
                raise TypeError("Error ! must be an integer")
            if value < 0:
                raise ValueError("Quantity must be >= 0")
            validated[key] = value

        self._stock = validated

    def available(self, product_id: int):
        if type(product_id) is not  int:
            raise TypeError(f"product id must be int")
        try:
            return self._stock[product_id]
        except KeyError:
            raise KeyError(f"unknown product_id {product_id}")

    def exists(self, product_id: int) -> bool:
        if not (isinstance(product_id, int) and not isinstance(product_id, bool)):
            raise TypeError("product_id must be int")
        return product_id in self._stock

    def set_stock(self, product_id: int, qty: int) -> None:
        if type(product_id) is not int:
            raise TypeError("product_id must be int")
        if type(qty) is not int:
            raise TypeError("qty must be int")
        if qty < 0:
            raise ValueError("qty must be >= 0")
        self._stock[product_id] = qty

    def add_stock(self, product_id: int, delta: int) -> None:
        if type(product_id) is not int:
            raise TypeError("product_id must be int")
        if type(delta) is not int:
            raise TypeError("delta must be int")

        current = self._stock.get(product_id, 0)
        new_qty = current + delta

        if product_id not in self._stock and delta <= 0:
            raise KeyError(f"unknown product_id {product_id} (delta <= 0)")

        if new_qty < 0:
            raise ValueError(f"cannot reduce stock of {product_id} below 0 (current={current}, delta={delta})")

        self._stock[product_id] = new_qty

    def has(self, product_id: int, qty: int = 1) -> bool:
        if type(product_id) is not int:
            raise TypeError("product_id must be int")
        if type(qty) is not int:
            raise TypeError("qty must be int")
        if qty <= 0:
            raise ValueError("qty must be > 0")
        available = self._stock.get(product_id)
        return (available is not None) and (available >= qty)

    def to_dict(self) -> dict[int, int]:
        """צילום מצב מלאי בפורמט {product_id: quantity} לשמירה/דיבוג"""
        return dict(self._stock)  # העתק, לא את המילון הפנימי
