from datetime import datetime


class Coupon:
    def __init__(
        self,
        numeric_barcode: str,
        expiration_date: datetime,
        min_purchase: float,
        description: str,
    ):
        self.numeric_barcode = numeric_barcode
        self.expiration_date = expiration_date
        self.min_purchase = min_purchase
        self.description = description

    def _is_expired(self):
        return True if datetime.now() > self.expiration_date else False

    def discount_amount(self, subtotal: float):
        pass

    def get_barcode(self) -> str:
        """Return the 12-digit barcode of the coupon."""
        return self.numeric_barcode


class PercentDiscountCoupon(Coupon):

    def __init__(
        self,
        numeric_barcode: str,
        expiration_date: datetime,
        min_purchase: float,
        description: str,
        percent_value: float,
    ):
        super().__init__(
            numeric_barcode, expiration_date, min_purchase, description
        )
        self.percent_value = percent_value

    # def get_barcode(self) -> str:
    #     """Return the 12-digit barcode of the coupon."""
    #     return self.numeric_barcode

    def discount_amount(self, subtotal: float):
        if subtotal >= self.min_purchase and (not self._is_expired()):
            return subtotal * self.percent_value / 100
        else:
            return 0


class FixedDiscountCoupon(Coupon):

    def __init__(
        self,
        numeric_barcode: str,
        expiration_date: datetime,
        min_purchase: float,
        description: str,
        fixed_value: float,
    ):
        super().__init__(
            numeric_barcode, expiration_date, min_purchase, description
        )
        self.fixed_value = fixed_value  # should be float

    # def get_barcode(self) -> str:
    #     """Return the 12-digit barcode of the coupon."""
    #     return self.numeric_barcode

    def discount_amount(self, subtotal: float):
        if subtotal >= self.min_purchase and not self._is_expired():
            return (
                self.fixed_value
                if subtotal - self.fixed_value > 0
                else subtotal
            )
        else:
            return 0


def coupon_doctests():
    """Function to run the doctests for the Coupon class.
    >>> barcode = '012345678925'
    >>> expiration_date_not_expired = datetime(2025, 12, 31, 11, 59, 59)
    >>> expiration_date_expired = datetime(2024, 12, 31, 11, 59, 59)
    >>> min_purchase = 20.0
    >>> description = 'This is our tester!'
    >>> percent_value = 15.5
    >>> fixed_value = 30.0
    >>> test_coupon1 = PercentDiscountCoupon(barcode, \
                                expiration_date_expired, \
                                min_purchase, \
                                description, \
                                percent_value)
    >>> test_coupon1._is_expired()
    True
    >>> test_coupon2 = PercentDiscountCoupon(barcode, \
                                expiration_date_not_expired, \
                                min_purchase, \
                                description, \
                                percent_value)
    >>> test_coupon2._is_expired()
    False
    >>> test_percent = PercentDiscountCoupon(barcode, \
                                                expiration_date_not_expired, \
                                                min_purchase, \
                                                description, \
                                                percent_value)
    >>> test_percent.discount_amount(200.0)
    31.0
    >>> test_percent.discount_amount(15.0)
    0
    >>> test_fixed = FixedDiscountCoupon(barcode, \
                                            expiration_date_not_expired, \
                                            min_purchase, \
                                            description, \
                                            fixed_value)
    >>> test_fixed.discount_amount(200.0)
    30.0
    >>> test_fixed.discount_amount(20.0)
    20.0
    >>> test_fixed.discount_amount(10.0)
    0


    """
