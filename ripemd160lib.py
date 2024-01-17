# import hashlib

# def ripemd160(data):
#     h = hashlib.new('ripemd160')
#     h.update(data.encode('utf-8'))
#     return h.hexdigest()

# data = input("需要加密的字符：")
# result = ripemd160(data)
# print("RIPEMD-160 Hash:", result)
byte_array = bytearray(b'91b24bf9f5288532960ac687abb035127b1d28a5')
byte_data = byte_array.decode().encode()
print(byte_data)
hex_data = byte_data.hex()
print(hex_data)

