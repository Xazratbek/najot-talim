from uuid import uuid4

class Product:
    def __init__(self, name: str):
        self._id = uuid4()
        self.name = name
        self._price = 0

    def __str__(self):
        return f"Product: {self.name} | ID: {self._id}"

    def __repr__(self):
        return f"Product(id={self.id},name={self.name},price={self._price})"

    def get_product_name(self):
        return self.name

    @property
    def id(self):
        return self._id

    def change_name(self,new_name):
        if new_name != self.name:
            self.name = new_name
            return self.name
        else:
            raise ValueError("Ismni o'zgartirish uchun iltimos yangi ism kiriting")

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self,new_price: float) -> float:
        if new_price <= 0:
            raise ValueError("Manfiy va 0 soni kiritish mumkin emas!")
        self._price = new_price

product_1 = Product("Kurtka")
print(product_1.get_product_name())
product_1.price = 10000
print(product_1.price)
print(product_1.change_name("Kurtka qishki"))
print(product_1.get_product_name())


class OrderLine:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    def line_total(self):
        return self.product.price * self.quantity


class Order:
    def __init__(self):
        self._order_id = uuid4()
        self.lines = []

    def add_line(self,product,quantity):
        line  =  OrderLine(product,quantity)
        self.lines.append(line)

    def remove_line(self,product_id):
        for id in self.lines:
            if id.product.id == product_id:
                self.lines.pop(id)

    def total(self):
        count = 0
        for line in self.lines:
            count += line.line_total()

        return count

order_line_1 = OrderLine(product_1,10)
order = Order()

print(order.add_line(product_1,10))
print(order.total())