#斐波那契数列展示前多少项
def fibonacci(n):
    fib_list = [0, 1]  # 初始斐波那契数列列表，包含前两个数0和1
    for i in range(2, n + 1):
        fib_list.append(fib_list[i - 1] + fib_list[i - 2]+c)  # 计算当前位置的斐波那契数，并添加到列表中

    return fib_list
# 测试代码
n = int(input("请输入要计算的斐波那契数列位置："))
m = int(input("请输入要计算的斐波那契数列取模数："))
cs =input("请输入要计算的斐波那契数列平移数(默认不平移，为0)：")
if cs != '' :
    c = int(cs)
else:
    c = 0
result = fibonacci(n)
count = 0
hang = 0
print(f"一共有{len(result)}个数字"+'\n')
# 打印结果
for num in result:
    count += 1
    print(format(num), end='\t')
    if count % 8 == 0:
        hang += 1
        print(f"第{hang}行"+'\n')
print('\n'+"输出余数列数组 Mod",m,'\n')
count = 0
hang = 0
for num in result:
    count += 1
    s =  num % m
    print("{:.0f}".format(s), end='\t')
    if count % 8 == 0:
        hang += 1
        print(f"第{hang}行"+'\n')
print()
