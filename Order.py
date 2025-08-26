from datetime import datetime
from Product import Product
from ItemInOrder import ItemInOrder


class Order:

    _id_counter = 0
    def __init__(self , customer_name ):
        self._id = self.next_id()
        self.customer_name = customer_name
        self._items = []
        self._time_stamp = datetime.now()


    #methods:
    @property
    def id(self):
        return self._id

    @classmethod
    def next_id(cls):
        cls._id_counter+=1
        return cls._id_counter

    @property
    def customer_name(self):
        return self._customer_name

    @customer_name.setter
    def customer_name(self, name):
        if not isinstance(name , str):
            raise TypeError("Name must be a string")
        if  not name.strip():
            raise ValueError("Name can't be empty")
        self._customer_name=name.strip()



    @property
    def items(self):
        return self._items

    def add_item(self, product: Product , quantity: int = 1):
        if not isinstance(product, Product):
            raise TypeError("This is not a product")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer")
        if quantity <=0:
            raise ValueError("Quantity must be greater than zero")

        for item in self._items:
            if item.product.id == product.id:
                item.quantity += quantity
                return

        self._items.append(ItemInOrder(product, quantity))

    def remove_item(self, item_id: int, quantity: int = 1):
        if not isinstance(quantity, int):
            raise TypeError("Not an integer")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        for item in self._items:
            if item.product.id == item_id:
                if item.quantity < quantity:
                    raise ValueError(f"You can remove only {item.quantity} items")
                if item.quantity - quantity == 0:
                    self._items.remove(item)
                    return
                else:
                    item.quantity = item.quantity - quantity
                    return
        raise KeyError("Not found an item")

    def calculate_total_price(self):
        total = 0
        for item in self.items:
            total += item.calculate_total_price()
        return total

    def __repr__(self):
        return f"{type(self).__name__}"
    def __str__(self):

        lines = [str(item) for item in self._items]
        all_items = "\n".join(lines) if lines else "(empty)"

        return f"""{type(self).__name__} ID: {self._id}
Customer Name: {self.customer_name}
Items:
{all_items}"""