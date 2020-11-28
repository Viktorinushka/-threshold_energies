# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 12:57:24 2020

@author: 7996832
"""
from matplotlib import pyplot as plt
from scipy import interpolate
import math
import numpy as np

str = ""
f = open('data.txt')
x_ = []
y_ = []


def threshold(rho_0, E_0, E_rho_list1, eps1, E_rho_list2, eps2):
    for i in range(int(len(E_rho_list1))-1):
        if ((E_rho_list1[i+1]>=(E_0/rho_0)) & (E_rho_list1[i] <= E_0/rho_0)):
            enter = eps1[i+1]
    for i in range(int(len(E_rho_list2))-1):
        if ((E_rho_list2[i+1]>=(E_0/rho_0)) & (E_rho_list2[i] <= E_0/rho_0)):
            end = eps2[i]
    return [enter, end]

# кладем в x и y строчки значений
for j in range(81):
    for i in range(9):
        a = f.read(1)
        str = str + a
        i = i + 1
    x_.append(str)
    str = ""
    f.read(1)
    for i in range(9):
        a = f.read(1)
        str = str + a
        i = i + 1
    y_.append(str)
    str = ""
    f.read(2)
f.close()
x = []
y = []
# превращаем в числа
for j in range(70):
    if x_[j][6] == "+":
        x.append(float(x_[j][0] + x_[j][1] + x_[j][2] + x_[j][3] + x_[j][4]) * 10 ** int(x_[j][8]))
    if x_[j][6] == "-":
        x.append(float(x_[j][0] + x_[j][1] + x_[j][2] + x_[j][3] + x_[j][4]) * 10 ** (-int(x_[j][8])))
    if y_[j][6] == "+":
        y.append(float(y_[j][0] + y_[j][1] + y_[j][2] + y_[j][3] + y_[j][4]) * 10 ** int(y_[j][8]))
    if y_[j][6] == "-":
        y.append(float(y_[j][0] + y_[j][1] + y_[j][2] + y_[j][3] + y_[j][4]) * 10 ** (-int(y_[j][8])))

x_1 = []  # промежуток спада графика
y_1 = []
x_2 = []  # промежуток роста графика
y_2 = []
for i in range(34):
    x_1.append(x[i])
    y_1.append(y[i])
for i in range(33, 70):
    x_2.append(x[i])
    y_2.append(y[i])
x_1 = np.array(x_1)
x_2 = np.array(x_2)
y_1 = np.array(y_1)
y_2 = np.array(y_2)

m = []
y_new = []
rho = []
intersection_points = []
eps1 = []
eps2 = []


def f(y0, x_, y_):  # выдает точку пересечения двух графиков
    xx = np.array(x_)
    yy = np.array(y_)
    tck = interpolate.splrep(yy, xx)
    return interpolate.splev(y0, tck)


E_rho_list2 = []
# k - плотность
# m - напряженность,
for k in range(414, 1227, 2):
    rho.append(k / 1000)
    y_new = 0.001 * k * y_2
    for m in range(100, 302, 2):
        if ((y_new[0] <= m / 100) & (m / 100 <= y_new[33])) | ((y_new[0] >= m / 100) & (m / 100 >= y_new[33])):
            eps2.append(f(m / 100, x_2, y_new))
            E_rho_list2.append(m/(k/1000))  # (кВ/м)/(кг/м^3)

x_1 = x_1[::-1]
y_1 = y_1[::-1]
E_rho_list1 = []
for k in range(414, 1227, 2):
    y_new = 0.001 * k * y_1
    for m in range(100, 302, 2):
        if ((y_new[0] <= m / 100) & (m / 100 <= y_new[33])) | ((y_new[0] >= m / 100) & (m / 100 >= y_new[33])):
            eps1.append(f(m / 100, x_1, y_new))
            E_rho_list1.append(m/(k/1000))  # (кВ/м)/(кг/м^3)

plt.figure(figsize=(15, 7))
plt.subplot(1, 2, 1)
plot1 = plt.scatter(E_rho_list1, eps1, s=1)
plt.xlabel("E/rho, (кВ/м)/(кг/м^3)")
plt.ylabel("enter point of electron (energy), МэВ")
plt.grid()

plt.subplot(1, 2, 2)
plt.xlabel("E/rho, (кВ/м)/(кг/м^3)")
plt.ylabel("end point of electron (energy), МэВ")
plt.grid()
plot2 = plt.scatter(E_rho_list2, eps2, s=1)
plt.show()

print('введите E_0, кВ/м')
E_0 = float(input())
print('введите rho_0, кг/м^3')
rho_0 = float(input())
points = threshold(rho_0, E_0, E_rho_list1, eps1, E_rho_list2, eps2)
print('Энергия_входа, МэВ:', points[0])
print('Энергия_выхода, МэВ:', points[1])


