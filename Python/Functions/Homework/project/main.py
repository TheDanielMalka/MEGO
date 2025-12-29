import MyPackage

print(MyPackage.foo(5))
print(MyPackage.bar([1,3,4,6,7,8]))

from MyPackage import foo
from MyPackage import bar

print(foo(5))
print(bar([1,3,4,6,7,8]))

from MyPackage import *

print(foo(5))
print(bar([1,3,4,6,7,8]))

try:
    __foo__(5)
except Exception as e:
    print(e)
