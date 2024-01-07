import hashlib
import random
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0x0000000000000000000000000000000000000000000000000000000000000000
b = 0x0000000000000000000000000000000000000000000000000000000000000007
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# 定义椭圆曲线点类
class ECPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if self.x == other.x and self.y == other.y:
            return self.double()
        else:
            return self.add(other)

    def double(self):
        s = (3 * self.x ** 2) * pow(2 * self.y, p - 2, p) % p
        x3 = (s ** 2 - 2 * self.x) % p
        y3 = (s * (self.x - x3) - self.y) % p
        return ECPoint(x3, y3)

    def add(self, other):
        s = (other.y - self.y) * pow(other.x - self.x, p - 2, p) % p
        x3 = (s ** 2 - self.x - other.x) % p
        y3 = (s * (self.x - x3) - self.y) % p
        return ECPoint(x3, y3)

    def __mul__(self, k):
        k %= n
        result = ECPoint(0, 0)
        for i in range(256):
            if k & (1 << i):
                result += self
            self += self
        return result

# 生成密钥对
def generate_key_pair():
    private_key = random.randint(1, n - 1)
    public_key = ECPoint(Gx, Gy) * private_key
    return private_key, public_key

# 签名和验证
def sign(private_key, message):
    hash_message = hashlib.sha256(message.encode()).digest()
    k = random.randint(1, n - 1)
    r = (ECPoint(Gx, Gy) * k).x % n
    s = (pow(k, n - 2, n) * (int.from_bytes(hash_message, 'big') + private_key * r)) % n
    return r, s

def verify(public_key, message, signature):
    hash_message = hashlib.sha256(message.encode()).digest()
    print("hash_message=",hash_message)
    r, s = signature
    print("r,s=",r, s)
    w = pow(s, n - 2, n)
    print("w",w)
    u1 = (int.from_bytes(hash_message, 'big') * w) % n
    u2 = (r * w) % n
    P = ECPoint(Gx, Gy) * u1 + public_key * u2
    print("u1,u2,p=",u1,u2,p)
    print("r == P.x % n=",r == P.x % n,"r=",r ,"P.x=", P.x ,"n=",n,"P.x % n=",P.x % n)
    return r == P.x % n

if __name__ == '__main__':
    # 生成密钥对
    private_key, public_key = generate_key_pair()

    # 打印私钥和公钥
    print(f'Private Key: {private_key}')
    print(f'Public Key: {public_key.x}, {public_key.y}')

    # 签名和验证示例
    message = 'Hello, world!'
    signature = sign(private_key, message)
    print(f'Signature: {signature}')
    print(f'Verify: {verify(public_key, message, signature)}')