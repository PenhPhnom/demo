# #计算某一项的位数语法糖
def fibonacci(n):
    fib_list = [0, 1]  # 初始斐波那契数列列表，包含前两个数0和1

    for i in range(2, n + 1):
        fib_list.append(fib_list[i - 1] + fib_list[i - 2])  # 计算当前位置的斐波那契数，并添加到列表中

    return fib_list

# 测试代码
n = int(input("请输入要计算的斐波那契数列位置："))
fib = fibonacci(n)

# 提取指定位置的斐波那契数
fib_num = fib[n]

# 转换为十进制和十六进制，并计算位数
decimal = str(fib_num)
hexadecimal = hex(fib_num)[2:].upper()
num_digits = len(decimal)

# 打印结果
print("斐波那契数列第", n, "项：")
print("十进制：", decimal)
print("十六进制：", hexadecimal)
print("一共有", num_digits, "位数字。")

