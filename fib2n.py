# #计算数字位数的语法糖
n = int(input("请输入2的整数次幂："))
power_dec = 2 ** n
power_hex = hex(power_dec)

num_digits_dec = len(str(power_dec))
num_digits_hex = len(power_hex) - 2  # 减去 "0x" 的长度

print("2的512次方的十进制表示为：", power_dec)
print("2的512次方的十六进制表示为：", power_hex)
print("十进制表示有", num_digits_dec, "位")
print("十六进制表示有", num_digits_hex, "位")

