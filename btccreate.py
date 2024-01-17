import hashlib
import ecdsa
import base58
"""This Python module is an implementation of the SHA-256 algorithm.
From https://github.com/keanemind/Python-SHA-256"""

K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

def sha256_hash(message: bytearray) -> bytearray:
    """Return a SHA-256 hash from the message passed.
    The argument should be a bytes, bytearray, or
    string object."""

    if isinstance(message, str):
        message = bytearray(message, 'ascii')
    elif isinstance(message, bytes):
        message = bytearray(message)
    elif not isinstance(message, bytearray):
        raise TypeError

    # Padding
    length = len(message) * 8 # len(message) is number of BYTES!!!
    message.append(0x80)
    while (len(message) * 8 + 64) % 512 != 0:
        message.append(0x00)

    message += length.to_bytes(8, 'big') # pad to 8 bytes or 64 bits

    assert (len(message) * 8) % 512 == 0, "Padding did not complete properly!"

    # Parsing
    blocks = [] # contains 512-bit chunks of message
    for i in range(0, len(message), 64): # 64 bytes is 512 bits
        blocks.append(message[i:i+64])

    # Setting Initial Hash Value
    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h5 = 0x9b05688c
    h4 = 0x510e527f
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19
    # SHA-256 Hash Computation
    for message_block in blocks:
        # Prepare message schedule
        message_schedule = []
        for t in range(0, 64):
            if t <= 15:
                # adds the t'th 32 bit word of the block,
                # starting from leftmost word
                # 4 bytes at a time
                message_schedule.append(bytes(message_block[t*4:(t*4)+4]))
            else:
                term1 = _sigma1(int.from_bytes(message_schedule[t-2], 'big'))
                term2 = int.from_bytes(message_schedule[t-7], 'big')
                term3 = _sigma0(int.from_bytes(message_schedule[t-15], 'big'))
                term4 = int.from_bytes(message_schedule[t-16], 'big')

                # append a 4-byte byte object
                schedule = ((term1 + term2 + term3 + term4) % 2**32).to_bytes(4, 'big')
                message_schedule.append(schedule)

        assert len(message_schedule) == 64
        # print("message_schedule=",message_schedule)
        # for mes in message_schedule:
        #     print(mes.hex(),"\n")
        # Initialize working variables
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7

        # Iterate for t=0 to 63
        for t in range(64):
            t1 = ((h + _capsigma1(e) + _ch(e, f, g) + K[t] +
                   int.from_bytes(message_schedule[t], 'big')) % 2**32)

            t2 = (_capsigma0(a) + _maj(a, b, c)) % 2**32

            h = g
            g = f
            f = e
            e = (d + t1) % 2**32
            d = c
            c = b
            b = a
            a = (t1 + t2) % 2**32

        # Compute intermediate hash value
        h0 = (h0 + a) % 2**32
        h1 = (h1 + b) % 2**32
        h2 = (h2 + c) % 2**32
        h3 = (h3 + d) % 2**32
        h4 = (h4 + e) % 2**32
        h5 = (h5 + f) % 2**32
        h6 = (h6 + g) % 2**32
        h7 = (h7 + h) % 2**32

    return ((h0).to_bytes(4, 'big') + (h1).to_bytes(4, 'big') +
            (h2).to_bytes(4, 'big') + (h3).to_bytes(4, 'big') +
            (h4).to_bytes(4, 'big') + (h5).to_bytes(4, 'big') +
            (h6).to_bytes(4, 'big') + (h7).to_bytes(4, 'big'))

def _sigma0(num: int):
    """As defined in the specification."""
    num = (_rotate_right(num, 7) ^
           _rotate_right(num, 18) ^
           (num >> 3))
    return num

def _sigma1(num: int):
    """As defined in the specification."""
    num = (_rotate_right(num, 17) ^
           _rotate_right(num, 19) ^
           (num >> 10))
    return num

def _capsigma0(num: int):
    """As defined in the specification."""
    num = (_rotate_right(num, 2) ^
           _rotate_right(num, 13) ^
           _rotate_right(num, 22))
    return num

def _capsigma1(num: int):
    """As defined in the specification."""
    num = (_rotate_right(num, 6) ^
           _rotate_right(num, 11) ^
           _rotate_right(num, 25))
    return num

def _ch(x: int, y: int, z: int):
    """As defined in the specification."""
    return (x & y) ^ (~x & z)

def _maj(x: int, y: int, z: int):
    """As defined in the specification."""
    return (x & y) ^ (x & z) ^ (y & z)

def _rotate_right(num: int, shift: int, size: int = 32):
    """Rotate an integer right."""
    return (num >> shift) | (num << size - shift)
def cycle_shift(v, pos):
    bin_str = []
    for i in range(32):
        bin_str.append(v % 2)
        v >>= 1
    bin_str.reverse()
    for i in range(pos):
        bit = bin_str[0]
        for j in range(1, 32):
            bin_str[j-1] = bin_str[j]
        bin_str[31] = bit
    number = 0
    for i in range(32):
        number += bin_str[i] * (2 ** (31 - i))
    
    return number


def function_choose(j):
    functions = [lambda x, y, z: (x ^ y ^ z),
                 lambda x, y, z: ((x & y) | ((~x) & z)),
                 lambda x, y, z: ((x | (~y)) ^ z),
                 lambda x, y, z: ((x & z) | (y & (~z))),
                 lambda x, y, z: (x ^ (y | (~z)))]
    if j < 16:
        return functions[0]
    if 16 <= j < 32:
        return functions[1]
    if 32 <= j < 48:
        return functions[2]
    if 48 <= j < 64:
        return functions[3]
    if 64 <= j:
        return functions[4]


def RIPEMD160(byte):
    # 添加
    byte_message = byte
    len_message = len(byte_message) * 8
    byte_message.append(0x80)
    while (len(byte_message) * 8) % 512 != 448:
        byte_message.append(0x00)
    if len_message >= 2**64:
        len_message &= 0xFFFFFFFFFFFFFFFF
    first_part = len_message & 0xFFFFFFFF
    first_part = first_part.to_bytes(4, byteorder="little")
    second_part = len_message >> 32
    second_part = second_part.to_bytes(4, byteorder="little")
    byte_message += first_part
    byte_message += second_part
    # 初始化
    
    constant_adding = [0x00000000, 0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xA953FD4E]
    constant_adding_hatch = [0x50A28BE6, 0x5C4DD124, 0x6D703EF3, 0x7A6D76E9, 0x00000000]
    r = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
         7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8,
         3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12,
         1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2,
         4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13]
    r_hatch = [5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12,
               6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2,
               15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13,
               8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14,
               12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11]
    s = [11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8,
         7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12,
         11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5,
         11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12,
         9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6]
    s_hatch = [8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6,
               9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11,
               9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5,
               15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8,
               8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11]
    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    # 将消息拆分为单词
    length = len(byte_message) * 8
    separated_message = []
    for i in range((length//512)):
        part = byte_message[64 * i:64*(i + 1)]
        separated_message.append([])
        for j in range(16):
            word = part[4 * j:4*(j + 1)]
            separated_message[i].append(int.from_bytes(word, byteorder="little", signed=False))
    # print(separated_message)
    # separated_message = [[4294967296, 4294967296, 4294967296, 4294967296, 4294967296, 4294967296, 4294967296, 4294967296, 128, 0, 0, 0, 0, 0, 256, 0]]
    # 算法
    for i in range(len(separated_message)):
        part = separated_message[i]
        A = h[0]
        B = h[1]
        C = h[2]
        D = h[3]
        E = h[4]
        A_hatch = h[0]
        B_hatch = h[1]
        C_hatch = h[2]
        D_hatch = h[3]
        E_hatch = h[4]
        print(h)
        for j in range(80):
            f = function_choose(j)
            f_hatch = function_choose(79 - j)
            if j < 16:
                k = constant_adding[0]
                k_hatch = constant_adding_hatch[0]
            if 16 <= j < 32:
                k = constant_adding[1]
                k_hatch = constant_adding_hatch[1]
            if 32 <= j < 48:
                k = constant_adding[2]
                k_hatch = constant_adding_hatch[2]
            if 48 <= j < 64:
                k = constant_adding[3]
                k_hatch = constant_adding_hatch[3]
            if 64 <= j < 80:
                k = constant_adding[4]
                k_hatch = constant_adding_hatch[4]
            x = part[r[j]]
            x_hatch = part[r_hatch[j]]

            T = (A + f(B, C, D) + x + k) % (2**32)
            T = cycle_shift(T, s[j])
            T = (T + E) % (2**32)
            A = E
            E = D
            D = cycle_shift(C, 10)
            C = B
            B = T
            T = (A_hatch + f_hatch(B_hatch, C_hatch, D_hatch) + x_hatch + k_hatch) % (2 ** 32)
            T = cycle_shift(T, s_hatch[j])
            T = (T + E_hatch) % (2 ** 32)
            A_hatch= E_hatch
            E_hatch = D_hatch
            D_hatch = cycle_shift(C_hatch, 10)
            C_hatch = B_hatch
            B_hatch = T
        T = (h[1] + C + D_hatch) % (2 ** 32)
        h[1] = (h[2] + D + E_hatch) % (2 ** 32)
        h[2] = (h[3] + E + A_hatch) % (2 ** 32)
        h[3] = (h[4] + A + B_hatch) % (2 ** 32)
        h[4] = (h[0] + B + C_hatch) % (2 ** 32)
        h[0] = T
        print("h=",h)
    else:
        print("h=s=",h)
        word = h[0].to_bytes(4, byteorder="little")
        word = int.from_bytes(word, byteorder="big")
        hashed = word
        hashed <<= 32
        word = h[1].to_bytes(4, byteorder="little")
        word = int.from_bytes(word, byteorder="big")
        hashed |= word
        hashed <<= 32
        word = h[2].to_bytes(4, byteorder="little")
        word = int.from_bytes(word, byteorder="big")
        hashed |= word
        hashed <<= 32
        word = h[3].to_bytes(4, byteorder="little")
        word = int.from_bytes(word, byteorder="big")
        hashed |= word
        hashed <<= 32
        word = h[4].to_bytes(4, byteorder="little")
        word = int.from_bytes(word, byteorder="big")
        hashed |= word
    print(hashed)
    return hashed

# 指定私钥字符串
private_key_str = input("需要加密的私钥：")

# 将私钥字符串转换为字节类型
private_key_bytes = bytes.fromhex(private_key_str)

# 构建私钥对象
private_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
private_key_hex = private_key.to_string().hex()

# 计算标准公钥
public_key = private_key.get_verifying_key()
public_key_compressed = public_key.to_string().hex()
public_key_uncompressed = "04" + public_key.to_string().hex()

# 计算hash160公钥
# 1. 对公钥进行SHA-256哈希
# public_key_hash = hashlib.sha256(bytes.fromhex(public_key_uncompressed)).digest()
public_key_hash = sha256_hash(bytes.fromhex(public_key_uncompressed))
# 2. 对哈希结果进行RIPEMD-160哈希
# ripemd160_hash = hashlib.new('ripemd160', public_key_hash).digest()
ripemd160_hash_int = RIPEMD160(bytearray(public_key_hash))
ripemd160_hash = ripemd160_hash_int.to_bytes((ripemd160_hash_int.bit_length() + 7) // 8, 'big')
print("ripemd160_hash,ripemd160_hash_int=",ripemd160_hash.hex(),ripemd160_hash_int)
# 3. 添加版本字节到哈希结果前面
version_byte = b'\x00'  # 主网地址的版本字节为0x00
hashed_string = version_byte + ripemd160_hash
a = public_key_hash.hex()
# 4. 对结果进行两次SHA-256哈希
# hashed_twice = hashlib.sha256(hashlib.sha256(hashed_string).digest()).digest()
hashed_twice = sha256_hash(sha256_hash(hashed_string))
# 5. 取前4个字节为校验和
checksum = hashed_twice[:4]
# 6. 将校验和添加到版本字节和哈希结果后面
binary_address = hashed_string + checksum
# 7. 对二进制地址进行Base58编码
address = base58.b58encode(binary_address)
print("\n")
print("version_byte",version_byte.hex(),"主网版本号")
print("ripemd160_hash",ripemd160_hash.hex(),"ripemd160哈希值")
print("\n")
print("hashed_string = version_byte + ripemd160_hash")
print("hashed_string",hashed_string.hex(),"版本号+哈希160的值")
print("\n")
print("hashed_twice = hashlib.sha256(hashlib.sha256(hashed_string).digest()).digest()")
print("hashed_twice",hashed_twice.hex(),"两次hash256")
print("checksum",checksum.hex(),"校验值")
print("\n")
print("binary_address = hashed_string + checksum")
print("binary_address",binary_address.hex(),"校验和添加到版本字节和哈希结果后面")
print("\n")
print("address = base58.b58encode(binary_address)")
print("地址:", address.decode())