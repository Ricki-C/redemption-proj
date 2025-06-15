from product import Product
from member import Member, SilverMember, GoldMember, PlatinumMember
from coupon import Coupon, PercentDiscountCoupon, FixedDiscountCoupon
from datetime import datetime


class ProductDatabase:
    SAVE_PATH = "db-data/updated_inventory.csv"

    def __init__(self, inventory_path: str):
        self.inventory_path = inventory_path
        self.products = {}
        with open(self.inventory_path, "r") as file:
            lines = file.readlines()
            for i in range(1, len(lines)):
                product_info = lines[i].strip().split(",")
                self.products[product_info[0]] = Product(
                    product_info[0],
                    product_info[1],
                    float(product_info[2]),
                    int(float(product_info[3])),
                )

    def get_product(self, numeric_barcode: str):
        if numeric_barcode in self.products:
            return self.products[numeric_barcode]
        else:
            return None

    def decrement_inventory(self, numeric_barcode: str, quantity: int):
        product = self.get_product(numeric_barcode)
        if product is not None:
            product.decrease_quantity(quantity)

    def save_inventory(self):
        with open(self.inventory_path, "r") as file1:
            with open(ProductDatabase.SAVE_PATH, "w") as file2:
                lines = file1.readlines()
                file2.write("numeric_barcode,name,price,quantity\n")
                for i in range(1, len(lines)):
                    barcode = lines[i].strip().split(",")[0]
                    product = self.get_product(barcode)
                    if product != None:
                        file2.write(
                            str(product.get_barcode())
                            + ","
                            + str(product.get_name())
                            + ","
                            + str(product.get_price())
                            + ","
                            + str(product.get_quantity())
                            + "\n"
                        )


class MemberDatabase:
    SAVE_PATH = "db-data/updated_memberships.csv"

    def __init__(self, membership_path: str):
        self.membership_path = membership_path
        self.members = {}
        with open(self.membership_path, "r") as file:
            lines = file.readlines()
            for i in range(1, len(lines)):
                member_info = lines[i].strip().split(",")
                member_type = member_info[2]
                if member_type == "Silver":
                    self.members[member_info[0]] = SilverMember(
                        member_info[0],
                        member_info[1],
                        int(float(member_info[3]))
,
                    )
                elif member_type == "Gold":
                    self.members[member_info[0]] = GoldMember(
                        member_info[0],
                        member_info[1],
                        int(float(member_info[3]))
,
                    )
                else:
                    self.members[member_info[0]] = PlatinumMember(
                        member_info[0],
                        member_info[1],
                        int(float(member_info[3]))
,
                    )

    def get_member(self, numeric_barcode: str) -> Member:
        if numeric_barcode in self.members:
            return self.members[numeric_barcode]
        else:
            return None

    def add_points(self, numeric_barcode: str, points: int):
        member = self.get_member(numeric_barcode)
        if member is not None:
            member.add_points(points)

    def save_memberships(self):
        with open(self.membership_path, "r") as file1:
            with open(MemberDatabase.SAVE_PATH, "w") as file2:
                lines = file1.readlines()
                file2.write("numeric_barcode,name,tier,points\n")
                for i in range(1, len(lines)):
                    barcode = lines[i].strip().split(",")[0]
                    member = self.get_member(barcode)
                    if member != None:
                        file2.write(
                            str(member.get_barcode())
                            + ","
                            + str(member.get_name())
                            + ","
                            + str(member.return_membership_type())
                            + ","
                            + str(member.get_points())
                            + "\n"
                        )


class CouponDatabase:
    def __init__(self, coupon_path: str):
        self.coupon_path = coupon_path
        self.coupons = {}
        with open(self.coupon_path, "r") as file:
            lines = file.readlines()
            for i in range(1, len(lines)):
                coupon_info = lines[i].strip().split(",")
                date = coupon_info[1].split("-")
                if coupon_info[2] == "percent":
                    self.coupons[coupon_info[0]] = PercentDiscountCoupon(
                        str(coupon_info[0]),
                        datetime(int(date[0]), int(date[1]), int(date[2])),
                        float(coupon_info[4]),
                        str(coupon_info[5]),
                        float(coupon_info[3]),
                    )
                else:
                    self.coupons[coupon_info[0]] = FixedDiscountCoupon(
                        str(coupon_info[0]),
                        datetime(int(date[0]), int(date[1]), int(date[2])),
                        float(coupon_info[4]),
                        str(coupon_info[5]),
                        float(coupon_info[3]),
                    )

    def get_coupon(self, numeric_barcode: str) -> Coupon:
        if numeric_barcode in self.coupons:
            return self.coupons[numeric_barcode]
        else:
            return None


def product_database_doctests():
    """Function to run the doctests for the ProductDatabase class.

    Note that you should run this doctest at the root folder of the project
    (same level as main.py)

    It's recommended that you add additional doctests

    >>> pdb = ProductDatabase('db-data/inventory.csv')
    ...
    >>> milk_barcode = '012345678905'
    >>> milk = pdb.get_product(milk_barcode)
    >>> milk.get_quantity() == 150
    True
    >>> pdb.decrement_inventory(milk_barcode, 10)
    >>> milk.get_quantity()
    140
    >>> milk.get_quantity() == 140
    True
    >>> pdb.save_inventory()
    >>> pdb2 = ProductDatabase('db-data/inventory.csv')
    >>> milk2 = pdb2.get_product(milk_barcode)
    >>> milk2.get_quantity() == 150
    True
    >>> pdb3 = ProductDatabase('db-data/updated_inventory.csv')
    >>> milk3 = pdb3.get_product(milk_barcode)
    >>> milk3.get_quantity() == 140
    True

    >>> pdb = ProductDatabase('db-data/test_inventory.csv')
    >>> milk = pdb.get_product('012345678905')
    >>> milk.get_name()
    'Milk'
    >>> milk.get_price()
    2.99
    >>> milk.get_quantity()
    150

    >>> wagyu = pdb.get_product('014643206491')
    >>> wagyu.get_name()
    'Wagyu Beef'
    >>> wagyu.get_price()
    60.0
    >>> wagyu.get_quantity()
    1

    >>> pdb.get_product('000000000000') is None
    True

    >>> pdb = ProductDatabase("db-data/inventory.csv")
    >>> milk = pdb.get_product("012345678905")
    >>> milk.decrease_quantity(10)
    >>> pdb.save_inventory()

    >>> # Read back the saved file to confirm update
    >>> with open(ProductDatabase.SAVE_PATH, "r") as f:
    ...     lines = f.readlines()
    >>> "012345678905,Milk,2.99,140" in [line.strip() for line in lines]
    True
    """


def member_database_doctests():
    """Function to run the doctests for the MemberDatabase class.

    Note that you should run this doctest at the root folder of the project
    (same level as main.py)

    It's recommended that you add additional doctests

    >>> mdb = MemberDatabase('db-data/memberships.csv')
    >>> jane_barcode = '257274767454'
    >>> jane = mdb.get_member(jane_barcode)
    >>> jane.get_points() == 1200
    True
    >>> mdb.add_points(jane_barcode, 100)
    >>> jane.get_points() == 1300
    True
    >>> mdb.save_memberships()
    >>> file_exists = None
    >>> try:
    ...     f = open('db-data/updated_memberships.csv')
    ...     f.close()
    ...     file_exists = True
    ... except FileNotFoundError:
    ...     file_exists = False
    >>> file_exists
    True

    >>> mdb = MemberDatabase('db-data/test_memberships.csv')
    >>> jane = mdb.get_member('257274767454')
    >>> jane.get_name()
    'Jane Doe'
    >>> jane.get_points()
    1200
    >>> jane.return_membership_type()
    'Silver'

    >>> bob = mdb.get_member('223052518921')
    >>> bob.return_membership_type()
    'Platinum'

    >>> mdb.get_member('000000000000') is None
    True

    >>> mdb = MemberDatabase("db-data/memberships.csv")
    >>> member = mdb.get_member("297458184493")  # John Smith
    >>> member.add_points(100)
    >>> mdb.save_memberships()

    >>> with open(MemberDatabase.SAVE_PATH, "r") as f:
    ...     lines = f.readlines()
    >>> "297458184493,John Smith,Gold,5500" in [line.strip() for line in lines]
    True
    """


def coupon_database_doctests():
    """Function to run the doctests for the CouponDatabase class.

    Note that you should run this doctest at the root folder of the project
    (same level as main.py)

    It's recommended that you add additional doctests

    >>> cdb = CouponDatabase('db-data/coupons.csv')
    >>> sample_coupon_barcode = '149234073227'
    >>> coupon = cdb.get_coupon(sample_coupon_barcode)
    >>> isinstance(coupon, PercentDiscountCoupon)
    True

    >>> from datetime import datetime
    >>> cdb = CouponDatabase('db-data/test_coupons.csv')
    >>> coupon1 = cdb.get_coupon('149234073227')
    >>> isinstance(coupon1, PercentDiscountCoupon)
    True
    >>> coupon1.percent_value
    15.0
    >>> coupon1.min_purchase
    30.0

    >>> coupon2 = cdb.get_coupon('167586463312')
    >>> isinstance(coupon2, FixedDiscountCoupon)
    True
    >>> coupon2.fixed_value
    5.0

    >>> coupon_expired = cdb.get_coupon('120726178637')
    >>> coupon_expired.expiration_date < datetime(2025, 1, 1)
    True

    >>> cdb.get_coupon('000000000000') is None
    True
    """
