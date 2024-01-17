import hashlib
import ecdsa
import base58
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
def check(lst):
    # 初始化
    # h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    h = [2695943694, 1502697358, 3548167586, 2977794860, 3795497621]
    # 算法
    # word = h[0].to_bytes(4, byteorder="little")
    word = h[0]
    # word = int.from_bytes(word, byteorder="big")
    hashed = word
    hashed <<= 32
    # word = h[1].to_bytes(4, byteorder="little")
    word = h[1]
    # word = int.from_bytes(word, byteorder="big")
    hashed |= word
    hashed <<= 32
    # word = h[2].to_bytes(4, byteorder="little")
    word = h[2]
    # word = int.from_bytes(word, byteorder="big")
    hashed |= word
    hashed <<= 32
    # word = h[3].to_bytes(4, byteorder="little")
    word = h[3]
    # word = int.from_bytes(word, byteorder="big")
    hashed |= word
    hashed <<= 32
    # word = h[4].to_bytes(4, byteorder="little")
    word = h[4]
    # word = int.from_bytes(word, byteorder="big")
    hashed |= word
    return hashed

def generate_lists(lst, index):
    # lst = [4436961533, 1826849740, 2274322692, 4436961533, 3152139022]
    if index == len(lst):
        # 递归出口，当遍历到列表的最后一个位置时，执行check操作
        ripemd160_hash_int = check(lst)
        # ripemd160_hash_int = 
        ripemd160_hash = ripemd160_hash_int.to_bytes((ripemd160_hash_int.bit_length() + 7) // 8, 'big')
        print(lst,ripemd160_hash.hex())
        if "a0b0d60e5991578ed37cbda2b17d8b2ce23ab295" == ripemd160_hash.hex():
            with open("results.txt", "w", encoding="utf-8") as file:
                result = f"找到满足的结果： {lst}\n"
                file.write(result)
    else:
        # for i in range(0,20000000000):
        for i in range(1):
            lst[index] = i
            generate_lists(lst, index + 1)

def generate_all_lists():
    lst = [0] * 5
    generate_lists(lst, 0)

generate_all_lists()






