# # מתי נשתמש ב TUPLE ?
# # כשיש לנו רשימות של נתונים שלא הולכים להשתנות והגישה אליהם היא רק בקריאה
# # הם בלתי ניתנים לשינוי אי אפשר גם לגשת לאיבר ספציפי מהרשימה
#
# tup = (255,0,0)
# print(tup[0])
# tup[0] = 244  # אי אפשר לבצע פעולה השמה או שינוי על טאפל רק קריאה
# print(tup)
#
# lst = ["Daniel","Jack","ZMoki","Shoki"]
# lst2 = [1,3,4,2,55,23,12]
# lst.sort()
# lst2.sort() #  מסדר את כל הליסט מהגדול לקטן במספרים או מהאותיות הקטנות בסטרינגים
# print(lst)
# print(lst2)
#
# lst2.reverse() # מסדר את כל הליסט מהגדול לקטן בסדר הפוך
# print(lst)
#
# lst.append("Blinky") #   דוחף במיקום האחרון את הערך המבוקש אפשרי אפילו רשימה בעצמה אבל זה נשאר כגוף אחד
# print(lst)
#
# lst.insert(1,"Dlinky") # דוחף למיקום ספציפי ערך מסויים
# print(lst)
#
# lst.extend(lst2) # מבצע אותה פעולה כמו APPEND רק שכל איבר שאקסטנג דוחפת היא מפרקת אותו לאיבר בודד ואז
#                   # דוחפת אותו לרשימה
# print(lst)
#
# print(lst2.count(2)) # סופרת כמה פעמים הערך מופיע בתוך הרשימה
#
# lst.pop() # מוחק איבר ברשימה לפי אינדקס אם ריק מוחק מהאחרון
# print(lst)
#
# lst.remove("Blinky") # מוחק ערך ספציפי מרשימה אם הוא מופיע בו
# print(lst)
#
# lst3 = lst.copy() # יוצר שיכפול של הרשימה הקודמת אבל כאיבר חדש לגמרי
# print(lst3)
# print(id(lst3),id(lst))
#
# lst.clear() # מאפס את כל הרשימה על ידי מחיקת כל הערכים בתוכה
# print(lst)
import threading


# my_dict = {'name': 'Sara', 'age': 30, 'city': 'Tel Aviv'}
#
# get = my_dict.get('city') # מחזיר את הערך שמשוייך להגדרה שביקשנו
# print(get)
#
# keys = my_dict.keys() # מחזיר את רשימה כל ההגדרות שבמילון
# print(keys)
# keys_list = list(keys) # אפשר להפוך את כל ההגדרות לליסט ממש משל עצמם בפונקציה קלה של LIST
# print(f"{keys_list}")
# print(type(keys_list))
#
# keys = my_dict.values() # מחזיר את רשימה כל ההערכים במילון
# print(keys) # מאפשר שימוש גם כן בפונקציית LIST
#
# keys = my_dict.items() #
# print(keys)
#
# keys = my_dict.update(my_dict.items())
# print(keys)
#
# removed_value = my_dict.pop('age') # מקבל הגדרה מהמילון מוחק אותה ומחזיר את הערך של ההגדרה
# print(f"{removed_value}")
# print(f"{my_dict}")
# result = my_dict.pop('country', 'Not Found') # אפשר לבקש להסיר ערך מסויים מהמילון ואם הוא לא קיים
#                                # במקום שתווצר שגיאה להחליט ברירת מחדל של ערך החזרה למצב שההגדרה לא תופיע במילון
# print(f"{result}")
#
#

# שאלה 9 בדף להבין למה ב SET מספרים לא מתנהגים רנדומלית ומה זה HASH
#
# sey = {12,9,24,6,2,4}
# print(sey.pop())
# print(sey.pop())
# print(sey.pop())
# print(sey.pop())
# print(sey.pop())
# print(sey.pop())


# inp = [1,3,5,6,2,2,3,3]
# inp2 = 'asbdsbwbrasdba'
# def func(string):
#     diction = {}
#     for index in string:
#         if index in diction:
#             diction[index] += 1
#         else:
#             diction[index] = 1
#     return diction
# print(func(inp))
# print(func(inp2))

# hold = [1,"3","2","1",5]
# print(id(hold))
# def removing(lst):
#     for i in lst:
#        if type(i) != str:
#            lst.remove(i)
#     return lst
# print(removing(hold))
# print(id(hold))

# lst = [1, 21, 3, 43, 5, 6, 7, 8, 9, 10]
# lst2 = [1, 2, 32, 4,55, 6, 7, 8, 10]
# def combined(lst1, lst2):
#     new = []
#     for item in lst1:
#         if item in lst2:
#             new.append(item)
#     return new
# print(combined(lst, lst2))

# diction = {"meat":1,"cheese":3,"milk":4,"vegetable":5,"gadi":1,"yakov":3,"daniel":4}
# def unique(dic):
#     new = []
#     for key in dic:
#         if dic[key] not in new:
#             new.append(dic[key])
#     return new
# print(unique(diction))

#
# a = [1,3,4,2,22,3,3,333,3]
# def rotation(a):
#     b = a[0]
#     a = a[1::]
#     a.append(b)
#     return a
# print(rotation(a))





# runs = int(input("enter the number of numbers: "))
# highest = 0
# second = 0
# if runs > 1:
#     for i in range(runs):
#         inp = int(input("Enter number: "))
#         if inp > highest:
#             second = highest
#             highest = inp
#         if second < inp < highest:
#             second = inp
#     print(f"The highest number is {highest} and the second number is {second}")
# else:
#     print(f"Must contains at least 2 numbers")
#
# l = []
# high = 0
# minimum = 0
# average = 0
# for i in range(5):
#     inp = int(input("Enter num"))
#     average += inp
#     l.append(inp)
#     average /= len(l)
#     for i in range(len(l)):
#         if l[i] > high:
#             minimum = high
#             high = l[i]
#         if minimum > l[i] :
#             minimum = l[i]
# print(high,minimum,average)


# lst = []
# dictionary = {"Milk":5,"Bread":3,"Sugar":2}
# def convert(dictionary):
#     for key, value in dictionary.items():
#         lst.append((key, value))
# convert(dictionary)
# print(lst)

# dictionary = {"Milk":5,"Bread":3,"Sugar":2,"Gadi":11,"Shoki":-1}
# def max_min_values(dictionary):
#     minimum = 0
#     maximum = 0
#     max_key = 0
#     min_key = 0
#     for key,value in dictionary.items():
#         if value < minimum or minimum == 0:
#             minimum = value
#             min_key = key
#         if value > maximum:
#             maximum = value
#             max_key = key
#
#     return min_key, max_key
# print(max_min_values(dictionary))


# star = "AsabdArs"
# dict = {}
# def create(string):
#     for item in string:
#         if item in dict:
#             dict[item] += 1
#         else:
#             dict[item] = 1
#     return dict
# print(create(star))



# lst1 =[1,2,3,4,5,8,8,8,8,8,8]
# lst2 = [2,4,6,8,6,6,6,6,13]
# result = []
# def combine(list1, list2):
#     count = 0
#     for item in list1:
#         if item not in list2:
#             result.append(item)
#             count += 1
#     count = 0
#     for item in list2:
#         if item not in list1:
#             result.append(item)
#             count += 1
#     return set(result)
# print(combine(lst1, lst2))


#
# def simple_sort(lst):
#     result = []
#     while len(lst) > 0:
#         smallest = min(lst)
#         result.append(smallest)
#         lst.remove(smallest)
#     return result
# print(simple_sort([3,6,8,2,9,5,1,13,-14,-22,3]))

#
# grades = {"Daniel": 110,
#           "gadi": 56,
#           "Yakov": 90,
#           "Noam":111,
#           "Aharon":92,
#           "Shiko":103}
# def highest_grade(students):
#     maxGrade = max(students.values())
#     for student in students:
#         if maxGrade == students[student]:
#             return student
#     return maxGrade
# print(highest_grade(grades))

# 15

# diction = {"Daniel":33,
#           "Shimon":35,
#            "Shahar":26,
#            "Yael":22,
#            "David":5,
#            "Ori":4}
# def ages(dictionary):
#     lst = []
#     for key in dictionary:
#         if dictionary[key] >= 18:
#             lst.append(key)
#     return lst
# print(ages(diction))

# 16

# def unique_elements(lst):
#     seen = set(lst)
#     result = []
#     for element in lst:
#         if element in seen and element not in result:
#             result.append(element)
#     return result
# print(unique_elements([1,22,4,2,3,33,4,5,22,5,33,2]))

# 17

# word = "abhello2 4world"
#
# def next_alpha(string):
#     new = ''
#     for index in string:
#         if "a" <= index <= "z":
#             new += chr(ord('a') + (ord(index) - ord('a')+1)) # new += chr(97 + (97 - (97+1)) = 98...
#         else:
#             new += index # if not lower
#     return new
# print(next_alpha(word))
#



# 18
# lst = ["asdasdasdasd",'asds321321312312312321adasdasdsa',
# 'asdad','as12222222222222222222222222222222dsassd',
# '123213123123213213123123']
# def longest(string):
#     previous = len(string[0])
#     new = ''
#     for item in string:
#         if len(item) > previous:
#             new = item
#             previous = len(item)
#     return new
# print(longest(lst))



# lst = []
# maximum = 0
# index = 0
# for i in range(1,6):
#     lst.append(int(input("Enter num")))
#     lst[i-1] *= i
#     if maximum < lst[i-1]:
#         maximum = lst[i-1]
#         index = i
# print(f"the list is : {lst} max num is : {maximum} his index is {index}")

# lst2 = []
# lst = []
# for i in range(int(input("Enter list size"))):
#     inp = int(input("Enter a num to append to the list"))
#     lst.append(inp)
#     lst2.append(inp)
# counter = 1
# for num in lst:
#     num *= counter
#     lst[counter-1] = num
#     counter += 1
# maximum = 0
# maximum_num_index = 0
# for i in range(len(lst)):
#     if lst[i] > maximum:
#         maximum = lst[i]
#         maximum_num_index = i+1
# print(f"Original list is: {lst2} \n"
#       f"Doubled list: {lst} \n"
#       f"Maximum number is: {maximum} \n"
#       f"Maximum index is: {maximum_num_index}")
#


# def find_index(arr:list, var:int):
#     for index in range(len(arr)):
#         if arr[index] == var:
#             return index
#     return None
# print(f"your var index is: {find_index([1,3,5,7,9],3)}")
# print(f"your var index is: {find_index([1,3,5,7,9],10)}")

#
# lst = [11,33,5,6,2,4,6,8,9,55]
# item=4
# def shoki(lst,item):
#     high=len(lst)-1
#     low=0
#     lst = sorted(lst)
#     while low<=high:
#         mid = (low+high)//2
#         if lst[mid]==item:
#             return mid
#         elif lst[mid]<item:
#             low=mid+1
#             lst = lst[mid:]
#         elif lst[mid]>item:
#             high=mid-1
#             lst = lst[:mid]
#     else:
#         return -1
# print(shoki(lst,item))
