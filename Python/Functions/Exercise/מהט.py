# class AIQData:
#     def __init__(self,date:str,city:str,popul:int,aiq:int):
#         self.date = date
#         self.city = city
#         self.popul = popul
#         self.aiq = aiq
#
#     def raiting(self):
#         if self.aiq < 50:
#             return 1
#         elif self.aiq < 100:
#             return 2
#         elif self.aiq < 150:
#             return 3
#         elif self.aiq < 200:
#             return 4
#         else:
#             return 5
#
# ary = [AIQData("01-06","Jerusalem",1000,100),AIQData("01-06","London",1000,200),
# AIQData("01-06","Haifa",1000,140),AIQData("01-06","TelAviv",1000,201),]
# city = ["London","Tzfat","Tlv","Paris","Jerusalem"]
# def print_dangerous(arr,check_date):
#     for city in arr:
#         if city.date == check_date:
#             raiting = city.raiting()
#             if  raiting >= 4:
#                     print(city.city)
# def print_cities(arr,cities):
#     for city in cities:
#         good=bad=0
#         for compare in arr:
#             if city == compare.city:
#                 raiting = compare.raiting()
#                 if raiting == 1:
#                     good+=1
#                 elif raiting == 5:
#                     bad+=1
#         print(f"Good: {good}, Bad:{bad}")
# print_dangerous(ary,"01-06")
# print_cities(ary,city)


#
#
# def ezer(num):
#     lst =[]
#     while num > 0:
#         lst.append(num%10)
#         num //= 10
#     return lst
#
# def is_strangers(num1, num2): # num1 = 1234 / num2 = 5678
#     check = ezer(num2)
#     for digit in check:
#         if num1 % 10 == digit:
#             return False
#         num1 //= 10
#     return True


def why(arr):
    temp = []
    for i in range(len(arr)):
        if arr[i] < 0:
            temp.append(arr[i])

    for i in range(len(arr)):
        if arr[i] >= 0:
            temp.append(arr[i])
    for i in range(len(arr)):
        arr[i] = temp[i]

arr = [12,0,-344,-46,670,0]
new = [-344,-46,0,0,12,670]
# פעולת WHY לוקחת רשימת מספרים ומסדרת אותם קודם כל המספרים השליליים בצד שמאל אחרי זה 0 ואז חיובים לפי סדר המפגש של הרשימה המקורית לא לפי הגודל האמיתי