# member.py


class Member:
    points_multiplier: float = 1.0
    discount_rate: float = 0.0

    def __init__(self, numeric_barcode: str, name: str, points: int):
        self.numeric_barcode = numeric_barcode
        self.name = name
        self.points = points

    def add_points(self, points: int):
        self.points += points

    def get_name(self):
        return self.name

    def get_points(self):
        return self.points

    def get_barcode(self):
        return self.numeric_barcode

    def get_points_multiplier(self):
        return self.points_multiplier

    def get_discount_rate(self):
        return self.discount_rate

    def return_membership_type(self) -> str:
        pass


class SilverMember(Member):
    points_multiplier = 1.1  # 1.1 points per dollar
    discount_rate = 0.01  # 1% discount

    def return_membership_type(self) -> str:
        return "Silver"


class GoldMember(Member):
    points_multiplier = 1.5 
    discount_rate = 0.05 

    def return_membership_type(self) -> str:
        return "Gold"


class PlatinumMember(Member):
    points_multiplier = 2.0  # 2 points per dollar
    discount_rate = 0.10  # 10% discount

    def return_membership_type(self) -> str:
        return "Platinum"


def member_doctests():
    """Function to run the doctests for the Member class.
    >>> numeric_barcode = '012345678912'
    >>> name = 'David'
    >>> points = 10

    >>> test_member = PlatinumMember(numeric_barcode, name, points)
    >>> test_member.get_barcode() == numeric_barcode
    True
    >>> test_member.get_name() == name
    True
    >>> test_member.get_points() == points
    True
    >>> test_member.get_points_multiplier() == 2
    True
    >>> test_member.get_discount_rate() == 0.1
    True
    >>> test_member.add_points(5)
    >>> test_member.get_points()
    15

    >>> test_silver = SilverMember(numeric_barcode, name, points)
    >>> test_silver.return_membership_type() == 'Silver'
    True
    >>> test_silver.get_points_multiplier() == 1.1
    True
    >>> test_silver.get_discount_rate() == 0.01
    True

    >>> test_gold = GoldMember(numeric_barcode, name, points)
    >>> test_gold.return_membership_type() == 'Gold'
    True
    >>> test_gold.get_points_multiplier() == 1.5
    True
    >>> test_gold.get_discount_rate() == 0.05
    True

    >>> test_plat = PlatinumMember(numeric_barcode, name, points)
    >>> test_plat.return_membership_type() == 'Platinum'
    True
    >>> test_plat.get_points_multiplier() == 2
    True
    >>> test_plat.get_discount_rate() == 0.1
    True


    >>> m = GoldMember('222222222222', 'Alice', 50)
    >>> m.get_name()
    'Alice'
    >>> m.get_points()
    50
    >>> m.get_barcode()
    '222222222222'
    >>> m.get_points_multiplier()
    1.5
    >>> m.get_discount_rate()
    0.05
    >>> m.return_membership_type()
    'Gold'
    >>> m.add_points(25)
    >>> m.get_points()
    75
    """
