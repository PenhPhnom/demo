# hex_string = "a0b0d60e5991578ed37cbda2b17d8b2ce23ab295"

# # 将十六进制字符串转换为字节
# byte_data = bytes.fromhex(hex_string)

# # 将字节转换为十进制数
# decimal_value = int.from_bytes(byte_data, byteorder='big')

# print("转换后的字节:", byte_data)
# print("转换后的十进制数:", decimal_value)

# decimal_value = 917382101398954197690965969683202974335429685909

# # 将十进制数转换为二进制字符串
# binary_string = bin(decimal_value)[2:]

# # 将二进制字符串按照每 32 位一组分组
# grouped_binary = [binary_string[i:i+32] for i in range(0, len(binary_string), 32)]

# print("转换后的二进制字符串:", binary_string)
# print("每 32 位一组分组后的二进制数:")
# for i, group in enumerate(grouped_binary, 1):
#     print(f"第{i}组:", group)

# binary_groups = [
#     "10100000101100001101011000001110",
#     "01011001100100010101011110001110",
#     "11010011011111001011110110100010",
#     "10110001011111011000101100101100",
#     "11100010001110101011001010010101"
# ]

# # 将每组二进制字符串转换为十进制数并放入列表
# decimal_values = [int(group, 2) for group in binary_groups]

# print("每组二进制字符串对应的十进制数列表:", decimal_values)

# def modular_inverse(a, m):
#     """
#     计算给定余数在给定模数下的逆元
#     """
#     # 使用扩展欧几里得算法计算
#     m0, x0, x1 = m, 0, 1
#     while a > 1:
#         q = a // m
#         m, a = a % m, m
#         x0, x1 = x1 - q * x0, x0
#     return x1 + m0 if x1 < 0 else x1

# # 给定的余数和模数
# remainder = 2695943694
# modulus = 2**32

# # 计算逆元
# inverse = modular_inverse(remainder, modulus)

# # 输出结果
# print("除数（逆元）:", inverse)

# def find_possible_dividend(remainder, modulus):
#     """
#     寻找给定余数和模数可能的被除数

#     参数:
#     remainder (int): 余数
#     modulus (int): 模数

#     返回:
#     list: 可能的被除数列表
#     """
#     possible_dividends = []
    
#     # 遍历商
#     for quotient in range(2**32):
#         possible_dividend = modulus * quotient + remainder
#         if possible_dividend<20000000000:
#             possible_dividends.append(possible_dividend)
#             print(possible_dividend,"=",modulus, "*", quotient, "+", remainder)
#     return possible_dividends

# # 给定的余数和模数
# remainder = 2695943694
# modulus = 2**32

# # 寻找可能的被除数
# possible_dividends = find_possible_dividend(remainder, modulus)

# # 输出结果
# print("可能的被除数列表:", possible_dividends)

def find_possible_dividends(remainders, modulus, max_possible_dividend):
    """
    寻找给定余数列表和模数可能的被除数列表

    参数:
    remainders (list): 余数列表
    modulus (int): 模数
    max_possible_dividend (int): 被除数的最大范围

    返回:
    list: 可能的被除数列表
    """
    possible_dividends = []

    for remainder in remainders:
        possible_dividend = []
        
        # 遍历商，限制商的范围
        for quotient in range(max_possible_dividend // modulus + 1):
            current_possible_dividend = modulus * quotient + remainder
            if current_possible_dividend <= max_possible_dividend:
                possible_dividend.append(current_possible_dividend)
            else:
                break

            # 输出中间过程
            print(f"Quotient: {quotient}, Remainder: {remainder}, Current Possible Dividend: {current_possible_dividend}")

        possible_dividends.append(possible_dividend)

    return possible_dividends

# 给定的余数列表和模数
remainders = [2695943694, 1502697358, 3548167586, 2977794860, 3795497621]
modulus = 2**32
max_possible_dividend = 200_000_000_000  # 被除数的最大范围

# 寻找可能的被除数列表
possible_dividends = find_possible_dividends(remainders, modulus, max_possible_dividend)

# 输出结果
print("可能的被除数列表:")
for i, possible_dividend in enumerate(possible_dividends, start=1):
    print(f"余数 {i}: {possible_dividend}","\n")













