import math

a = int(input("a = "))
b = int(input("b = "))
print("a + b = " + str(a + b))
print("a - b = " + str(a - b))
print("a * b = " + str(a * b))
print("a / b = " + str(a / b))
print("a % b = " + str(a % b))
print("a // b = " + str(a // b))
sqrt_sum_10th_powers = math.sqrt(a**10 + b**10)
print("Корень квадратный из суммы их 10-х степеней: " + str(sqrt_sum_10th_powers))
