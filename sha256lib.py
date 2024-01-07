import hashlib

def sha256(data):
    h = hashlib.sha256(bytes.fromhex(data)).digest()
    return h

data = input("需要加密的字符：")
result = sha256(data)
print("sha256 Hash:", result.hex())