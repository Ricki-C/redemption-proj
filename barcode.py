class BarcodeProcessor:
    L_CODE = {
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
    R_CODE = {
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

    L_DECODE = {bits: digit for bits, digit in L_CODE.items()}
    R_DECODE = {bits: digit for bits, digit in R_CODE.items()}

    def __init__(self):
        pass

    def _validate_length(self, binary_barcode: str):
        if len(binary_barcode) != 95:
            raise ValueError("Wrong length")
        return True

    def _validate_left_guard(self, binary_barcode: str):
        if not binary_barcode.startswith("101"):
            raise ValueError("Wrong LEFT guard")
        return True

    def _validate_right_guard(self, binary_barcode: str):
        if not binary_barcode.endswith("101"):
            raise ValueError("Wrong RIGHT guard")
        return True

    def _validate_center_guard(self, binary_barcode: str):
        if binary_barcode[45:50] != "01010":
            raise ValueError("Wrong CENTER guard")
        return True

    def _get_left_modules(self, binary_barcode: str):
        return [binary_barcode[3 + i * 7 : 3 + (i + 1) * 7] for i in range(6)]

    def _get_right_modules(self, binary_barcode: str):
        return [
            binary_barcode[50 + i * 7 : 50 + (i + 1) * 7] for i in range(6)
        ]

    def _validate_modules(self, binary_barcode: str, module: str = "LEFT"):
        if module == "LEFT":
            mods = self._get_left_modules(binary_barcode)
        else:
            mods = self._get_right_modules(binary_barcode)

        if len(mods) != 6:
            raise ValueError(f"Wrong number of {module} modules")

        if any(len(m) != 7 for m in mods):
            raise ValueError(f"Wrong length within {module} module")

        if module == "LEFT":

            if any(m.count("1") % 2 == 0 for m in mods):
                raise ValueError(f"Wrong number of ones in {module} module")
            if any(not (m.startswith("0") and m.endswith("1")) for m in mods):
                raise ValueError(f"Wrong start or end in {module} module")
        else:

            if any(m.count("1") % 2 != 0 for m in mods):
                raise ValueError(f"Wrong number of ones in {module} module")
            if any(not (m.startswith("1") and m.endswith("0")) for m in mods):
                raise ValueError(f"Wrong start or end in {module} module")

        return True

    def validate_barcode(self, binary_barcode: str):
        self._validate_length(binary_barcode)
        self._validate_left_guard(binary_barcode)
        self._validate_center_guard(binary_barcode)
        self._validate_right_guard(binary_barcode)
        self._validate_modules(binary_barcode, module="LEFT")
        self._validate_modules(binary_barcode, module="RIGHT")
        return True

    def convert_to_12_digits(self, binary_barcode: str):
        self.validate_barcode(binary_barcode)
        left = self._get_left_modules(binary_barcode)
        right = self._get_right_modules(binary_barcode)

        digits = []
        for m in left:
            if m not in self.L_DECODE:
                raise ValueError("Wrong binary combination")
            digits.append(self.L_DECODE[m])
        for m in right:
            if m not in self.R_DECODE:
                raise ValueError("Wrong binary combination")
            digits.append(self.R_DECODE[m])

        return "".join(digits)

    def modulo_check(self, numeric_barcode: str):
        if len(numeric_barcode) != 12 or not numeric_barcode.isdigit():
            raise ValueError("Security check failed")

        odd_sum = sum(int(numeric_barcode[i]) for i in range(0, 11, 2))
        even_sum = sum(int(numeric_barcode[i]) for i in range(1, 11, 2))
        total = odd_sum * 3 + even_sum

        check_digit = (10 - (total % 10)) % 10
        if check_digit != int(numeric_barcode[-1]):
            raise ValueError("Security check failed")

        return True

    def invert_barcode(self, binary_barcode: str):
        return binary_barcode[::-1]


def barcode_doctests():
    """
    >>> from tester_student import generate_barcode_12, barcode_digits2binary
    >>> scanner = BarcodeProcessor()
    >>> valid_numeric = '252109613999'
    >>> valid_binary = barcode_digits2binary(valid_numeric)
    >>> invalid_numeric = '036000291439'
    >>> invalid_binary = barcode_digits2binary(invalid_numeric)
    >>> scanner._validate_length('')
    Traceback (most recent call last):
    ...
    ValueError: Wrong length
    >>> scanner._validate_length(valid_binary)
    True
    >>> scanner._validate_left_guard('101' + '0'*92)
    True
    >>> scanner._validate_right_guard('0'*92 + '101')
    True
    >>> scanner._validate_center_guard(valid_binary)
    True
    >>> scanner._validate_modules(valid_binary, module='LEFT')
    True
    >>> scanner._validate_modules(valid_binary, module='RIGHT')
    True
    >>> scanner.validate_barcode(valid_binary)
    True
    >>> scanner.modulo_check(valid_numeric)
    True
    >>> scanner.convert_to_12_digits(valid_binary) == valid_numeric
    True
    >>> scanner.modulo_check(invalid_numeric)
    Traceback (most recent call last):
    ...
    ValueError: Security check failed
    >>>
    >>> checks = []
    >>> with open('cart-data/scan_1_binary.txt', 'r') as f:
    ...     for binary_barcode in f:
    ...         binary_barcode = binary_barcode.strip()
    ...         is_valid = scanner.validate_barcode(binary_barcode)
    ...         checks.append(is_valid)
    >>> all(checks)
    True

    >>> checks = []
    >>> with open('cart-data/scan_1.txt', 'r') as f:
    ...     for line in f:
    ...         numeric_barcode = line.strip()
    ...         is_valid = scanner.modulo_check(numeric_barcode)
    ...         checks.append(is_valid)
    >>> all(checks)
    True

    >>> bp = BarcodeProcessor()
    >>> bp.invert_barcode("10110")
    '01101'

    >>> bp._validate_length("1" * 95)
    True

    >>> bp._validate_left_guard("101" + "0" * 42 + "01010" + "1" * 42 + "101")
    True

    >>> bp._validate_center_guard("101" + "0" * 42 + "01010" + "1" * 42 + "101")
    True

    >>> bp._validate_right_guard("101" + "0" * 42 + "01010" + "1" * 42 + "101")
    True
    """
