num = int(input("请输入一个整数："))

# 将整数转换为长整型
num = num.bit_length() + 1

# 向左移动32位
moved_num = num >> 32

# 输出移动前的二进制数
binary_before = bin(num)[2:]

# 输出移动后的十进制数和二进制数
decimal_after = moved_num
binary_after = bin(moved_num)[2:]

print("移动前的二进制数:", binary_before)
print("移动后的十进制数:", decimal_after)
print("移动后的二进制数:", binary_after)