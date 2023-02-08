import numpy as np


def find_intersection(a, b):
    if a == 0:
        return float('inf')
    return -b/a


def sign(a):
    if a < 0:
        return -1
    return 1


with open("p102_triangles.txt") as f:
    summa = 0
    while 1:
        counter = negcounter = 0
        x1, y1, x2, y2, x3, y3 = map(int, input().split())     # считываем координаты точек треугольника
        if [y1, y2, y3].count(0) >= 2:                      # если 2 точки имеют y=0, то (0,0) принадлежит треугольнику
            summa += 1
            continue
        a = np.array([[x1, 1], [x2, 1]])                    # находим три уравнения прямых, которыми задан треугольник
        b = np.array([y1, y2])

        if x1 != x2:
            a1, b1 = np.linalg.solve(a, b)
            i1 = find_intersection(a1, b1)
        else:                                               # если прямая вида y = b, проверяем, пересекает ли она y=0
            i1 = float("inf")
            if sign(y1) != sign(y2):                        # и смотрим, с какой стороны пересекает
                if x1 < 0:
                    negcounter += 1
                else:
                    counter += 1


        a = np.array([[x2, 1], [x3, 1]])
        b = np.array([y2, y3])
        if x2 != x3:
            a2, b2 = np.linalg.solve(a, b)
            i2 = find_intersection(a2, b2)
        else:
            i2 = float("inf")
            if sign(y2) != sign(y3):  # и смотрим, с какой стороны пересекает
                if x2 < 0:
                    negcounter += 1
                else:
                    counter += 1

        a = np.array([[x1, 1], [x3, 1]])
        b = np.array([y1, y3])
        if x1 != x3:
            a3, b3 = np.linalg.solve(a, b)
            i3 = find_intersection(a3, b3)
        else:
            i3 = float("inf")
            if sign(y1) != sign(y3):  # и смотрим, с какой стороны пересекает
                if x1 < 0:
                    negcounter += 1
                else:
                    counter += 1

        if min(x1, x2) <= i1 and i1 <= max(x1, x2):
            if i1 < 0:
                negcounter += 1
                print(1)
            else:
                counter += 1
        if min(x2, x3) <= i2 and i2 <= max(x2, x3):
            if i2 < 0:
                negcounter += 1
                print(2)
            else:
                counter += 1

        if min(x1, x3) <= i3 and i3 <= max(x1, x3):
            if i3 < 0:
                negcounter += 1
                print(3)
            else:
                counter += 1

        if negcounter % 2 == 1 or counter % 2 == 1:
            summa += 1
            print(negcounter, counter)
            print("Belongs")
            print(i1, i2, i3)
        else:
            print("Doesn't belong")
print(summa)


