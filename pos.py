# pos.py

from store_backend import StoreBackend
from barcode import BarcodeProcessor
from cart import ShoppingCart


class POSSystem:
    """
    Orchestrates a complete checkout:
      - scans binary barcodes from a file
      - builds a ShoppingCart with products, coupons, membership
      - computes total, updates inventory and member points, and saves
    """

    def __init__(
        self, inventory_path: str, membership_path: str, coupon_path: str
    ):
        # back‐end databases
        self.store = StoreBackend(inventory_path, membership_path, coupon_path)
        # low‐level barcode validation & conversion
        self.barcode_processor = BarcodeProcessor()
        # the cart for the current transaction
        self.cart = ShoppingCart()

    def process_barcodes(self, barcode_path: str) -> None:
        """
        Read each line of the given file as a binary barcode (95 bits).
        For each:
          1) try validate+convert; if ValueError, flip and retry;
          2) if still invalid, skip;
          3) do a modulo check (raises ValueError on failure), skip if invalid;
          4) identify type and add to cart if matches & in stock.
        """
        with open(barcode_path, "r") as f:
            for raw in f:
                b = raw.strip()
                # 1) validate & convert (original or flipped)
                try:
                    num = self.barcode_processor.convert_to_12_digits(b)
                except ValueError:
                    try:
                        flipped = self.barcode_processor.invert_barcode(b)
                        num = self.barcode_processor.convert_to_12_digits(
                            flipped
                        )
                    except ValueError:
                        # both original and flipped failed
                        continue

                # 2) modulo check
                try:
                    self.barcode_processor.modulo_check(num)
                except ValueError:
                    continue

                # 3) identify and add to cart
                kind = self._identify_barcode_type(num)
                if kind == "product":
                    prod = self.store.get_product(num)
                    if (
                        prod
                        and prod.is_in_stock()
                        and self.cart.products.count(prod)
                        < prod.get_quantity()
                    ):
                        self.cart.add_item(prod)

                elif kind == "coupon":
                    coup = self.store.get_coupon(num)
                    if coup:
                        self.cart.add_coupon(coup)

                elif kind == "membership":
                    mem = self.store.get_member(num)
                    if mem:
                        self.cart.add_membership(mem)

    def _identify_barcode_type(self, numeric_barcode: str) -> str:
        """
        First digit determines type:
          '0' -> product, '1' -> coupon, '2' -> membership
        """
        if numeric_barcode.startswith("0"):
            return "product"
        if numeric_barcode.startswith("1"):
            return "coupon"
        if numeric_barcode.startswith("2"):
            return "membership"
        # unexpected first digit: treat as product by default
        return "product"

    def checkout(self) -> float:
        """
        Finalize the sale:
          - compute total
          - decrement inventory by 1 per product
          - award points to membership based on total paid
          - save inventory & memberships
        Returns:
          final total charge (float)
        """
        total = self.cart.calculate_total()

        # update inventory
        for p in self.cart.get_items():
            self.store.decrease_product_quantity(p, 1)

        # update membership points
        member = self.cart.get_membership()
        if member:
            # points multiplier is per-dollar; round down to integer points
            pts = total * member.get_points_multiplier()
            self.store.add_member_points(member, pts)

        # persist changes
        self.store.save_inventory()
        self.store.save_memberships()

        return total

    def get_current_cart(self) -> ShoppingCart:
        """Return the ShoppingCart for the current transaction."""
        return self.cart


def pos_doctests(self):
    """Function to run the doctests for the POSSystem class.

    Note that you should run this doctest at the root folder of the project
    (same level as main.py)

    It's recommended that you add additional doctests
    or test using by creating scripts like main.py

    >>> pos = POSSystem(
    ...     'db-data/inventory.csv',
    ...     'db-data/memberships.csv',
    ...     'db-data/coupons.csv'
    ... )
    >>> pos.process_barcodes('cart-data/scan_1_binary.txt')
    >>> cart = pos.get_current_cart()
    >>> items = cart.get_items()
    >>> len(items) == 2
    True
    >>> item_names = [item.get_name() for item in items]
    >>> 'Apple' in item_names and 'Cheddar Cheese' in item_names
    True
    >>> cart.get_membership().get_name() == 'John Smith'
    True
    >>> cart.get_membership().return_membership_type() == "Gold"
    True
    >>> import math
    >>> math.isclose(pos.checkout(), 0.415, abs_tol=0.001)
    True
    >>> updated_memerships_exists = False
    >>> try:
    ...     f = open('db-data/updated_memberships.csv')
    ...     f.close()
    ...     updated_memerships_exists = True
    ... except FileNotFoundError:
    ...     updated_memerships_exists = False
    >>> updated_memerships_exists
    True
    >>> updated_inventory_exists = False
    >>> updated_inventory_exists = False
    >>> try:
    ...     f = open('db-data/updated_inventory.csv')
    ...     f.close()
    ...     updated_inventory_exists = True
    ... except FileNotFoundError:
    ...     updated_inventory_exists = False
    >>> updated_inventory_exists
    True
    >>> expected_types = ['coupon', 'membership', 'product', 'product']
    >>> calculated_types = []
    >>> with open('cart-data/scan_1.txt', 'r') as f:
    ...     for line in f:
    ...         numeric_barcode = line.strip()
    ...         barcode_type = pos._identify_barcode_type(numeric_barcode)
    ...         calculated_types.append(barcode_type)
    >>> expected_types == calculated_types
    True

    >>> pos = POSSystem(
    ...     'db-data/inventory.csv',
    ...     'db-data/memberships.csv',
    ...     'db-data/coupons.csv'
    ... )
    >>> pos.process_barcodes('cart-data/test_scan_binary.txt')
    >>> cart = pos.get_current_cart()
    >>> items = cart.get_items()
    >>> len(items)
    260
    >>> item_names = [item.get_name() for item in items]
    >>> 'Apple' in item_names and 'Cheddar Cheese' in item_names
    True
    >>> item_names.count("Apple")
    200
    >>> item_names.count('Cheddar Cheese')
    60
    >>> updated_memerships_exists = False
    >>> try:
    ...     f = open('db-data/updated_memberships.csv')
    ...     f.close()
    ...     updated_memerships_exists = True
    ... except FileNotFoundError:
    ...     updated_memerships_exists = False
    >>> updated_memerships_exists
    True
    >>> updated_inventory_exists = False
    >>> updated_inventory_exists = False
    >>> try:
    ...     f = open('db-data/updated_inventory.csv')
    ...     f.close()
    ...     updated_inventory_exists = True
    ... except FileNotFoundError:
    ...     updated_inventory_exists = False
    >>> updated_inventory_exists
    True
    >>> expected_types = ['coupon', 'membership', 'product', 'product']
    >>> calculated_types = []
    >>> with open('cart-data/scan_1.txt', 'r') as f:
    ...     for line in f:
    ...         numeric_barcode = line.strip()
    ...         barcode_type = pos._identify_barcode_type(numeric_barcode)
    ...         calculated_types.append(barcode_type)
    >>> expected_types == calculated_types
    True


    """
