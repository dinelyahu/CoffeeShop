import math


class Product:

    _id_counter = 0

    #Product attributes:
    def __init__(self , name: str , price: float , category: str = 'General' ,is_active: bool = True):
        self._id = self.next_id()
        self.name = name
        self.price = price
        self.category = category
        self.is_active = is_active


    # getter and setter
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self , name: str):
        if not isinstance(name , str):
            raise TypeError("Name must be a string")
        if not name.strip():
            raise ValueError(f"Name '{name}' can't be empty")
        self._name = name.strip()


    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        try:
            price = float(price)
        except (TypeError , ValueError):
            raise TypeError("price must be a number")

        if price < 0:
            raise ValueError(f"{price} has to be equal or greater than zero")
        if not math.isfinite(price):
            raise ValueError("Price must be a finite number")
        self._price = round(price , 2)

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self , value: str):
        if not isinstance(value , str):
            raise TypeError("Category must be a string")
        if not value.strip():
            raise ValueError("Category can't be empty")
        self._category = value.strip()


    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self ,value: bool ):
        if not isinstance(value, bool):
            raise TypeError("is_active must be True or False")
        self._is_active = value


    #Methods:
    @classmethod
    def next_id(cls):
        cls._id_counter+=1
        return cls._id_counter

    def __repr__(self):
        return f"{type(self).__name__} ({self.id}, '{self.name}', {self.price}, '{self.category}', {self.is_active})"

    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)



