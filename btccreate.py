import hashlib
import ecdsa
import base58

# 指定私钥字符串
private_key_str = input("需要加密的私钥：")

# 将私钥字符串转换为字节类型
private_key_bytes = bytes.fromhex(private_key_str)

# 构建私钥对象
private_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
private_key_hex = private_key.to_string().hex()
print("私钥:", private_key_hex)

# 计算压缩公钥
public_key = private_key.get_verifying_key()
public_key_compressed = public_key.to_string().hex()
print("压缩公钥:", public_key_compressed)

# 计算非压缩公钥
public_key_uncompressed = "04" + public_key.to_string().hex()
print("非压缩公钥:", public_key_uncompressed)

# 计算hash160公钥
public_key_sha256 = hashlib.sha256(bytes.fromhex(public_key_uncompressed)).digest()
public_key_hash160 = hashlib.new('ripemd160', public_key_sha256).digest()
print("Hash160公钥:", public_key_hash160.hex())

# 计算地址（与前面的代码保持一致）

# 计算地址
# 1. 对公钥进行SHA-256哈希
public_key_hash = hashlib.sha256(bytes.fromhex(public_key_uncompressed)).digest()
# 2. 对哈希结果进行RIPEMD-160哈希
ripemd160_hash = hashlib.new('ripemd160', public_key_hash).digest()
# 3. 添加版本字节到哈希结果前面
version_byte = b'\x00'  # 主网地址的版本字节为0x00
hashed_string = version_byte + ripemd160_hash
a = public_key_hash.hex()
# 4. 对结果进行两次SHA-256哈希
hashed_twice = hashlib.sha256(hashlib.sha256(hashed_string).digest()).digest()
# 5. 取前4个字节为校验和
checksum = hashed_twice[:4]
# 6. 将校验和添加到版本字节和哈希结果后面
binary_address = hashed_string + checksum
# 7. 对二进制地址进行Base58编码
address = base58.b58encode(binary_address)
print("地址:", address.decode())