class Product:
    def __init__(
        self, numeric_barcode: str, name: str, price: float, quantity: int
    ):
        self.numeric_barcode = numeric_barcode
        self.name = name
        self.price = price
        self.quantity = quantity

    def decrease_quantity(self, quantity: int):
        self.quantity -= quantity

    def is_in_stock(self):
        return True if self.quantity > 0 else False

    def get_barcode(self):
        return self.numeric_barcode

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_quantity(self):
        return self.quantity


def product_doctests():
    """Function to run the doctests for the Product class.
    >>> numeric_barcode = '012345678905'
    >>> p = Product(numeric_barcode, 'Test', 10.0, 5)
    >>> p.get_barcode() == numeric_barcode
    True
    >>> p.get_name() == 'Test'
    True
    >>> p.get_price() == 10.0
    True
    >>> p.get_quantity() == 5
    True
    >>> p.is_in_stock()
    True
    >>> p.decrease_quantity(5)
    >>> p.get_quantity() == 0
    True
    >>> p.is_in_stock()
    False


    >>> p = Product('012345678905', 'Cheddar Cheese', 4.50, 60)
    >>> p.get_barcode()
    '012345678905'
    >>> p.get_name()
    'Cheddar Cheese'
    >>> p.get_price()
    4.5
    >>> p.get_quantity()
    60
    >>> p.is_in_stock()
    True
    >>> p.decrease_quantity(10)
    >>> p.get_quantity()
    50
    >>> Product('012345678900', 'Empty Item', 0.00, 0).is_in_stock()
    False
    """
