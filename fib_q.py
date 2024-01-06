#计算1²+...+n²的和
n = int(input("请输入要计算的项数："))
a1 = 1
an = 750**2

sum_of_square = n * (a1 + an) // 2
print("等差数列的和为：", sum_of_square)