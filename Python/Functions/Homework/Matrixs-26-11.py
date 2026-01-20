# # 1
# matrix = [[3,9,-4,2],[9,2,5,0],[-4,5,-1,3],[2,0,3,0]]
# def is_symmetric(mat):
#     for i in range(len(mat)):
#         for j in range(len(mat)):
#             if mat[i][j] != mat[j][i]:
#                 return False
#     return True
# print(is_symmetric(matrix))

#2
# def is_anti_symmetric(mat):
#     for i in range(len(mat)):
#         for j in range(len(mat)):
#             if mat[i][j] != (mat[j][i] * -1):
#                 return False
#     return True
# print(is_anti_symmetric([[0,9,-4,-2],[-9,0,5,0],[4,-5,0,-3],[-2,0,3,0]]))


#3
# matrix = [
#     [11, 0, 0, 0],
#     [-9, 2, 0, 0],
#     [7, -5, 0, 0],
#     [23, 0, 3, -5]]
# def is_lower_triangular(matr):
#     for i in range(len(matr)):
#         for j in range(len(matr)):
#             if j > i and matr[i][j] != 0:
#                 return False
#     return True
#
# print(is_lower_triangular(matrix))

#4

# matrix = [
#     [4, 27,0 ,19],
#     [0, 0, 6, -4],
#     [0, 0, 5,  3],
#     [0, 0, 0, -7]]
# def is_upper_triangular(matr):
#     for i in range(len(matr)):
#         for j in range(len(matr)):
#             if j < i and matr[i][j] != 0:
#                 return False
#     return True
#
# print(is_upper_triangular(matrix))


#5
# matrix = [
#     [2, 0, 0, 0],
#     [0, 9, 0, 0],
#     [0, 0, 0, 0],
#     [0, 0, 0, 6]]
# def is_diag(matr):
#     for i in range(len(matr)):
#         for j in range(len(matr)):
#             if (j < i or j > i) and matr[i][j] != 0:
#                 return False
#     return True
# print(is_diag(matrix))

#6
# matrix = [
#     [9, 0, 0, 0],
#     [0, 9, 0, 0],
#     [0, 0, 9, 0],
#     [0, 0, 0, 9]]
# def is_diag(matr):
#     for i in range(len(matr)):
#         for j in range(len(matr)):
#             if ((j < i or j > i) and matr[i][j] != 0) or matr[i][i] != matr[i-1][i-1]:
#                 return False
#     return True
# print(is_diag(matrix))

#7

# matrix = [
#     [0, 0, 0, 0],
#     [0, 0, 0, 0],
#     [0, 0, 0, 0],
#     [0, 0, 0, 0]]
# def is_zero(matr):
#     for i in range(len(matr)):
#         for j in range(len(matr)):
#             if matr[i][j] != 0:
#                 return False
#     return True
# print(is_zero(matrix))

#8
# matrix = [
#     [1, 0, 0, 0],
#     [0, 1, 0, 0],
#     [0, 0, 1, 0],
#     [0, 0, 0, 1]]
# def is_iden(matr):
#     for i in range(len(matr)):
#         for j in range(len(matr)):
#             if ( (j < i or j > i) and matr[i][j] !=0 ) or matr[i][i] != 1:
#                 return False
#     return True
# print(is_iden(matrix))

#9

# pictures=[
# [1,1,1,1,1,1,1],
# [1,1,0,1,0,1,1],
# [1,1,0,1,0,1,1],
# [1,1,1,1,1,1,1],
# [1,1,1,1,1,1,1],
# [1,0,1,1,1,0,1],
# [1,1,0,0,0,1,1],
# [1,1,1,1,1,1,1] ]
# def count_rectangle(pic):
#     rectangle_count = 0
#     rows = len(pic)
#     cols = len(pic[0])
#     for r in range(rows):
#         for c in range(cols):
#             if pic[r][c] == 0:
#                 if pic[r+1][c] == 1:
#                     if pic[r][c+1] == 1:
#                         rectangle_count += 1
#     return rectangle_count
# print(count_rectangle(pictures))

#10

matrix = [
[1, 2, 3],
[4, 5, 6],
[7, 8, 9]]
def neighbor_sum_matrix(matr):
    row = len(matr)
    col = len(matr[0])
    new_matrix = []
    for i in range(row):
        new_row = []
        for j in range(col):
            summ = 0
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    if di == 0 and dj == 0:
                        continue
                    neib_i = i + di
                    neib_j = j + dj
                    if 0 <= neib_i < row and 0 <= neib_j < col:
                        summ += matr[neib_i][neib_j]
            new_row.append(summ)
        new_matrix.append(new_row)
    return new_matrix
matrix_show = neighbor_sum_matrix(matrix)
for line in range(len(matrix_show)):
    print(matrix_show[line])

