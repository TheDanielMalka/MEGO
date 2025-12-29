def bar(list_of_numbers:list) -> list:
    total_sum = 0
    for number in list_of_numbers:
        total_sum += number
    return total_sum


def __bar__(number:int) -> list:
    returned_list = []
    for i in range(0,number+1):
        returned_list.append(i)
    return returned_list

if __name__ == '__main__':
    print(bar([1,3,4,6,7,8]))
    print(__bar__(10))