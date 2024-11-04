# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 19:24:30 2024

@author: huong
"""
import numpy as np
print("Xin chào, thế giới!")

# Tính tổng của hai số
so_1 = 5
so_2 = 10
tong = so_1 + so_2

# In kết quả
print("Tổng của", so_1, "và", so_2, "là:", tong)
print('='*15)
print('\n Hello world! \n')
print('='*15)
print('Hello')
c=[[1,2,3,4],[2,3,6,4],[5,3,7,8]]
b=10.0
d=np.array(c)
A = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

B = [
    [9, 8, 7],
    [6, 5, 4],
    [3, 2, 1]
]

# Khởi tạo ma trận kết quả 3x3 với các phần tử ban đầu là 0
ket_qua = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

# Thực hiện phép nhân hai ma trận
for i in range(3):          # Duyệt qua các hàng của ma trận A
    for j in range(3):      # Duyệt qua các cột của ma trận B
        for k in range(3):  # Thực hiện tích tương ứng
            ket_qua[i][j] += A[i][k] * B[k][j]

# In kết quả
print("Ma trận kết quả sau khi nhân là:")
for hang in ket_qua:
    print(hang)
A = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

B = [
    [9, 8, 7],
    [6, 5, 4],
    [3, 2, 1]
]

# Khởi tạo ma trận kết quả 3x3 với các phần tử ban đầu là 0
ket_qua = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

# Thực hiện phép nhân hai ma trận
for i in range(3):          # Duyệt qua các hàng của ma trận A
    for j in range(3):      # Duyệt qua các cột của ma trận B
        for k in range(3):  # Thực hiện tích tương ứng
            ket_qua[i][j] += A[i][k] * B[k][j]

# In kết quả
print("Ma trận kết quả sau khi nhân là:")
for hang in ket_qua:
    print(hang)
for x in range(1,12):
    print(x,end=" ")
i=1
while i <10:
    print(i)
    i+=1
def myfunction(fname):
    print('Give me a name please!',fname)
myfunction(6)
def sum(a,b):
    tong=abs(a) + abs(b)
    return tong
print(sum(1,4), sum(2,6))
arr=np.array([1,2,3,4,5], dtype=int)
print(arr)
zero=np.zeros((3,4),dtype=int)
one=np.ones((2,3,4),dtype=int)
print(one)