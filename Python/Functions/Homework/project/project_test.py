from MyPackage import module1
from MyPackage import module2


def run_tests():
    print("Starting tests...")
    assert module1 not in globals(), "Test Failed: module1 in globals()"
    assert module2 not in globals(), "Test Failed: module2 in globals()"


if __name__ == "__main__":
    run_tests()