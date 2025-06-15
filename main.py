from pos import POSSystem


if __name__ == "__main__":
    barcode_path = "cart-data/scan_1_binary.txt"
    inventory_path = "db-data/inventory.csv"
    membership_path = "db-data/memberships.csv"
    coupon_path = "db-data/coupons.csv"

    pos = POSSystem(inventory_path, membership_path, coupon_path)

    # 1. Scan the barcodes
    pos.process_barcodes(
        barcode_path
    )  # this basically populates the cart with the items, coupons, and membership

    print(pos.get_current_cart())
    # 2. Checkout
    pos.checkout()

    ### Improvements
    # 1. make barcode class static or singleton or something
    # 2. Create the disccount logic for coupons and membership
    # 3. Create the inhertence for different membership types
    # 4. Dictionary should be used somewhere, could instead ask students to have a writeup asking how we can replace a product class with a dictionary (name maps to price, quantity)
    # 5. make sure how POS interacts with db is consitent (eg. shouuld POS shouldn't directly modify product or membership objects but should do so through store_back_end, which calls the db, which calls the object method) Naming for methods also needs to be consistent
