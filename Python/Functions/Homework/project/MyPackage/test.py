from module1 import foo
from module2 import bar
from module1 import __foo__


def check_foo():
    assert foo(0) == 1, "Test Failed: foo(0) should be 1"
def check_bar():
    assert bar([1, 2, 3]) == 6, "Test Failed: bar sum should be 6"
def check_foo__():
    assert __foo__ not in globals(), "Test Failed: __foo__ in globals()"
def try_foo_type_error():
    try:
        foo('a')
    except TypeError:
        print("Expected Int got str instead")
def try_bar_type_error():
    try:
        bar(['a', 'b', 'c'])
    except TypeError:
        print("Expected List of numbers got str instead")
    try:
        bar([1 , "2" , 3])
    except TypeError:
        print("Expected List of numbers got str(number) instead")

def run_tests():
    print("Starting tests...")
    check_foo()
    check_bar()
    check_foo__()
    try_foo_type_error()
    try_bar_type_error()

if __name__ == "__main__":
    run_tests()