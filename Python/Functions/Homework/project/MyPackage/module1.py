def foo(num:int) -> int:
    return num + 1

def __foo__(string:str) -> str:
    return string[::-1]



if __name__ == '__main__':
    print(foo(5))
    print(__foo__("Daniel"))