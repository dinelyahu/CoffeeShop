from Product import Product
from ItemInOrder import ItemInOrder
from Order import Order

product1 = Product('glass' , 50 ,)
product2 = Product('chocolate' , 50 ,)
product3 = Product('coffee' , 60 ,)

itemInOrder1 = ItemInOrder(product1, 3)
itemInOrder2 = ItemInOrder(product2, 2)
itemInOrder3 = ItemInOrder(product3, 4)

order1 = Order('Din' )
order1.add_item(product3, 3)
order1.add_item(product3, 3)
order1.add_item(product3, 3)
order1.add_item(product2, 3)


print(order1)
print(order1.calculate_total_price())

order1.remove_item(product3.id)

print("\n",order1)