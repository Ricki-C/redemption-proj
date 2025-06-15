import os


def run_all_doctests():
    """Run all the doctests in the project."""
    # List of files to run doctests on
    files_to_test = [
        "barcode.py",
        "product.py",
        "member.py",
        "coupon.py",
        "database.py",
        "store_backend.py",
        "cart.py",
        "pos.py",
    ]

    # Run doctests for each file
    for file in files_to_test:
        print(f"\nRunning doctests for {file}...")
        os.system(f"python -m doctest {file}")


if __name__ == "__main__":
    run_all_doctests()
