import hashlib

def ripemd160(data):
    h = hashlib.new('ripemd160')
    h.update(data.encode('utf-8'))
    return h.hexdigest()

data = input("需要加密的字符：")
result = ripemd160(data)
print("RIPEMD-160 Hash:", result)