# cart.py

from product import Product
from member import Member, SilverMember, GoldMember, PlatinumMember
from coupon import Coupon, FixedDiscountCoupon, PercentDiscountCoupon


class ShoppingCart:
    def __init__(self):
        self.products: list[Product] = []
        self.membership: Member | None = None
        self.coupons: list[Coupon] = []

    def add_item(self, product: Product):
        self.products.append(product)

    def add_membership(self, membership: Member):
        self.membership = membership

    def add_coupon(self, coupon: Coupon):
        code = coupon.get_barcode()
        if not any(c.get_barcode() == code for c in self.coupons):
            self.coupons.append(coupon)

    def get_items(self):
        return list(self.products)

    def get_membership(self):
        return self.membership

    def get_coupons(self):
        return list(self.coupons)

    def calculate_subtotal(self):
        return sum(p.get_price() for p in self.products)

    def calculate_total(self):
        subtotal = self.calculate_subtotal()

        # total coupon deduction
        coupon_deduction = sum(
            c.discount_amount(subtotal) for c in self.coupons
        )

        # membership deduction
        member_deduction = 0.0
        if self.membership is not None:
            member_deduction = subtotal * self.membership.get_discount_rate()

        total = subtotal - coupon_deduction - member_deduction
        # guard against negative total
        return total if total >= 0 else 0.0


def shopping_cart_doctests():
    """Function to run the doctests for the ShoppingCart class.

    Note that you should run this doctest at the root folder of the project
    (same level as main.py)

    # It's recommended that you add additional doctests

    >>> cart = ShoppingCart()
    >>> cart.add_item(Product('random_barcode', 'Milk', 2, 150))
    >>> cart.add_item(Product('random_barcode2', 'Bread', 3, 80))
    >>> cart.calculate_subtotal() == 5 == cart.calculate_total()
    True
    >>> sm = PlatinumMember('random_barcode3', 'John', 0)
    >>> cart.add_membership(sm)

    >>> cart.calculate_total() == 4.5
    True
    >>> from datetime import datetime
    >>> fc = FixedDiscountCoupon('b4', datetime(2030, 1, 1), 1, 'desc', 1)
    >>> cart.add_coupon(fc)

    >>> cart.calculate_total() == 3.5
    True
    >>> cart.add_coupon(fc)
    >>> len(cart.get_coupons()) == 1
    True
    >>> len(cart.get_items()) == 2
    True

    >>> p1 = Product('012345678905', 'Cheddar Cheese', 4.50, 60)
    >>> p2 = Product('027222235225', 'Apple', 1.20, 200)
    >>> m = GoldMember('222222222222', 'Alice', 100)
    >>> c = FixedDiscountCoupon('111111111111', datetime(2026, 6, 15), 0, '$5 off', 5)

    >>> cart = ShoppingCart()
    >>> cart.add_item(p1)
    >>> cart.add_item(p2)
    >>> cart.add_membership(m)
    >>> cart.add_coupon(c)

    >>> cart.calculate_subtotal()
    5.7
    >>> round(cart.calculate_total(),2)
    0.42
    >>> cart.get_membership().return_membership_type()
    'Gold'
    """
