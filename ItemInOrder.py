from Product import Product


class ItemInOrder:

    #Product attributes:
    def __init__(self ,product:Product, quantity:int=1):
        self.product = product
        self.quantity = quantity



    # getter and setter
    @property
    def product(self):
        return self._product


    @product.setter
    def product(self , product: Product):
        if not isinstance(product , Product):
            raise TypeError("This is not a product")

        self._product = product


    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):

        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer")
        if quantity <= 0:
            raise ValueError(f"{quantity} has to be greater than zero")

        self._quantity = quantity

    def calculate_total_price(self):
        return self.product.price*self.quantity

    def __repr__(self):
        return f"{type(self).__name__} ({self.product}, {self.quantity})"
    def __str__(self):
        return f"{self._product} X {self.quantity}"





