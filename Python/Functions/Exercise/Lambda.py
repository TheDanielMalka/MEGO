# def f(a, *args, **kwargs):
#     print(a, args, kwargs)
#
# f(1, 2, 3,4,5,6,6,6,6,'asdasd', x=10, y=20)
#
# a = lambda x, y: x + y
# print(a(1,2))
# print((lambda x,y:x*y)(5,2))
#
# names = ['David','Alon','Gal']
# names.sort(key=lambda x:len(x))
# print(names)
#
#
# nums = [200,101,34,24,12,11,23,12]
# def sum1(x):
#     sum = 0
#     while x>0:
#         sum+=x%10
#         x//=10
#     return sum
# nums.sort(key=sum1) # יהיה מיון לפי הפונקציה של חישוב הספרות - על כל מספר יבוצע הפונקציה ואחר כך תכניס אותו
# # בTUPLE לפי הסדר שביקשנו
# print(nums)
#
# #
#
# nums = [200,101,34,24,12,11,23,12]
# def sum1(x):
#     sum = 0
#     count = 0
#     digit=0
#     while x>0:
#         sum+=x%10
#         x//=10
#         count+=1
#     return sum,count
# nums.sort(key=sum1)
# print(nums)


# words = ['work','baby','ddd','aa']
# spec = [word for word in words if word != 'baby' ]
# print(spec)

# numbs = ['10','4','3','7','9']
# numbs.sort(key=lambda numb: int(numb))
# print(numbs)


# numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# even = sum(filter(lambda num: num % 2 == 0, numbers))
# odd = sum(filter(lambda num: num % 2 == 1, numbers))

# diction = {'Milk':10,'Bread':50,'Banana':20}
# def sales(dict):
#     dict = {key: value * 0.9 for key, value in dict.items()}
#     return dict
# print(sales(diction))


# words = ['work','baby','ddd','aa']
# words = list(filter(lambda num: len(num) % 2 == 0, words))
# print(words)

# words = ['work','baby','ddd','aa']
# words.sort(key=lambda word: word[-1])
# print(words)

# numbers = [1, -2, 3, 4, -5, 6, 7, -8, -90, 10]
# s = max(numbers,key=lambda number: abs(number))
# print(s)


# suc = lambda s:s.strip().upper()
# print(suc("        hello world   "))

# def myfunc(n):
#     return lambda a: a * n
# mydoubler = myfunc(2)
# mysecond = myfunc(3)
# print(mysecond(4))
# print(mydoubler(4))

# print(dir(str)) # רשימה של כל המתודות שעובדות עם טייפ מסויים
# print(dir(__builtins__))
# print(dir(int)) # ד

# def double(num):
#     return num * 2
# map(double, [1, 2, 3])

# nums = [4,11,13,5,9,8,10,9]
# d = list(map(lambda x:x*3,filter(lambda x: 5<x<10,nums)))
# print(d)
#
#
# strings = ['kiwi', 'apsple', 'bsssssanana', 'orangaaaaaaaae', 'grapefruit']
# b = sorted(strings,key=len)
# print(b)
#
# list1 = [5 , 7 ,9 ,3 ,4]
# list2 = [5 ,2 ,4]
# d = list(filter(lambda x:x in list1,list2))
# print(d)
#
# str1 = ['a','b','c','d','e','f']
# str2 = ['a','b','c']
# new = list(filter(lambda x:x not in str2,str1))
# print(new)
#
# items = ['apple', 'banana', 'cherry','grapes']
# indexed_items = list(enumerate(filter(lambda x:'e' in x,items)))
# print(indexed_items)

x = 50
y = 20
lis = [1,2,3]
def shoki():
    global x , y , lis
    z = 5
    a = sum(lis)
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age
    class Person2:
        def __init__(self, name, age):
            self.name = name
            self.age = age

    print(locals())
    print(globals())
    print(vars(Person))
shoki()
print(globals())
print(locals())
print(vars())