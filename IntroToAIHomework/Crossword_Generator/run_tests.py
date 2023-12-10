import matplotlib.pyplot as plt

arr = [1.6, 1.8, 2, 1.2, 0, 0.5, 2, 2, 1.5, 1, 1, 0]
arr.sort(reverse=True)
arr = arr[:9]
print(arr)
points = (sum(arr)) * 15 / 18
print(points)