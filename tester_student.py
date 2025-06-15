import random
import string

random.seed(10)
LEFT_SIDE_MODULES = {
    "0001101": "0",
    "0011001": "1",
    "0010011": "2",
    "0111101": "3",
    "0100011": "4",
    "0110001": "5",
    "0101111": "6",
    "0111011": "7",
    "0110111": "8",
    "0001011": "9",
}

RIGHT_SIDE_MODULES = {
    "1110010": "0",
    "1100110": "1",
    "1101100": "2",
    "1000010": "3",
    "1011100": "4",
    "1001110": "5",
    "1010000": "6",
    "1000100": "7",
    "1001000": "8",
    "1110100": "9",
}

GUARDS = {"LEFT": "101", "CENTER": "01010", "RIGHT": "101"}


LEFT_DIGITS2MODULES = {digit: module for module, digit in LEFT_SIDE_MODULES.items()}
RIGHT_DIGITS2MODULES = {digit: module for module, digit in RIGHT_SIDE_MODULES.items()}

MODULE_WIDTH = 7


def barcode_digits2binary(barcode_12: str) -> str:
    """Given a barcode (length 12 string), convert it to a binary string.

    Args:
        barcode_12 (str): The barcode to convert.
    """
    # Each module is 7 bits long

    modules = []

    # Initialize the binary string with the left guard (3 bits)
    modules.append(GUARDS["LEFT"])

    # Add the left modules (6 digits × 7 bits)
    for digit in barcode_12[:6]:
        module = LEFT_DIGITS2MODULES[digit]
        modules.append(module)

    # Add the center guard (5 bits)
    modules.append(GUARDS["CENTER"])

    # Add the right modules (6 digits × 7 bits)
    for digit in barcode_12[6:]:
        module = RIGHT_DIGITS2MODULES[digit]
        # Ensure the module is 7 bits long
        modules.append(module)

    # Add the right guard (3 bits)
    modules.append(GUARDS["RIGHT"])

    binary_barcode = "".join(modules)
    # Verify the total length is 95 bits
    if len(binary_barcode) != 95:
        raise ValueError(
            f"Invalid barcode length: {len(binary_barcode)} bits (expected 95)"
        )

    return binary_barcode


def generate_barcode_12(item_type: str):
    """Given a item type (product, coupon, or membership), generate a barcode\
        12. It's currently generatina a numeric barcode that is not valid.\
        Update it to generate a valid numeric barcode.

    Args:
        item_type (str): The type of item to generate a barcode for.

    Raises:
        ValueError: If the item type is not valid.

    Returns:
        str: The barcode (12 digits in string format)

    """

    first_digit = None
    if item_type == "product":
        first_digit = "0"
    elif item_type == "coupon":
        first_digit = "1"
    elif item_type == "membership":
        first_digit = "2"
    else:
        raise ValueError(
            f"Invalid item type: {item_type}, must be product, coupon, or membership"
        )

    # Generate the rest of 10 digits
    rest_of_digits = "".join(random.choices(string.digits, k=10))

    first_11_digits = first_digit + rest_of_digits
    # NOTE: last digit should be based modulo check if you want to generate a
    # valid numeric barcode
    last_digit = 3
    # last_digit = generate_last_digit(first_11_digits)

    return first_11_digits + str(last_digit)


def generate_last_digit(barcode_11: str) -> int:
    """Given the first 11 digits of a numeric barcode, generate the last digit.

    Args:
        barcode_11 (str): The first 11 digits of a numeric barcode.

    Returns:
        int: The last digit of the barcode.
    """
    # OPTIONAL TODO
    check_digit = 0
    return check_digit


def generate_cart_data(numeric_cart_path, binary_cart_path):
    """Given a path of a numeric cart, generate the binary cart  at the\
    specified path

    Args:
        numeric_cart_path (str): path of numeric cart (file with\
            numeric_barcodes), each on a new line
        binary_cart_path (str): path of binary cart (file with \
            binary_barcodes), each on a new line
    """
    with open(numeric_cart_path, "r") as file:
        lines = file.readlines()
        binary_lines = [barcode_digits2binary(line.strip()) for line in lines]
    to_write = "\n".join(binary_lines)
    with open(binary_cart_path, "w") as new_file:
        new_file.write(to_write)
