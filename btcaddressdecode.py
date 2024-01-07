import hashlib
import base58

def get_public_key_from_address(address):
    # Base58解码比特币地址
    decoded_address = base58.b58decode(address)
    # 提取公钥哈希和校验和
    public_key_hash = decoded_address[1:-4]
    checksum = decoded_address[-4:]
    # 验证校验和
    calculated_checksum = hashlib.sha256(hashlib.sha256(decoded_address[:-4]).digest()).digest()[:4]
    if checksum != calculated_checksum:
        raise ValueError("Invalid address or checksum")

    # 返回公钥哈希
    return public_key_hash

def get_public_key_uncompressed_from_address(address):

    # 返回公钥哈希
    return public_key_uncompressed

def get_public_key_compressed_from_address(address):

    # 返回公钥哈希
    return public_key_compressed

def get_private_key_from_address(address):

    # 返回公钥哈希
    return private_key

# 比特币地址
btc_address = input("需要解码的地址:")

# 通过地址获取公钥哈希
public_key_hash = get_public_key_from_address(btc_address)
public_key = public_key_hash.hex()

public_key_uncompressed = ''
public_key_compressed = ''
private_key = ''
#输出哈希160的公钥
print("Public Key Hash160:", public_key)
#输出非压缩的公钥
print("Public Key Uncompressed:", public_key_uncompressed)
#输出压缩的公钥
print("public key compressed:", public_key_compressed)
#输出私钥
print("Private Key:", private_key)

