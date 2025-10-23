import hmac
import random
import string
import os
import hashlib

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from pypbc import Element, Zr

# 生成512位密钥（64字节）
def get_key_from_string(key_string, key_length=512):
    # 使用SHA-512生成64字节密钥
    key = hashlib.sha512(key_string.encode()).digest()
    return key[:key_length // 8]  # 转换成字节数


# 加密函数（仍使用AES-256）
def encrypt(data, key_string):
    key = get_key_from_string(key_string, key_length=256)  # AES最大支持256位密钥
    iv = os.urandom(16)

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return iv + encrypted_data


# 解密函数
def decrypt(encrypted_data, key_string):
    key = get_key_from_string(key_string, key_length=256)

    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    return data.decode()

def lagrange_basis_poly(pairing, points, i):
    """计算第 i 个拉格朗日基多项式的系数"""
    n = len(points)
    x_i = points[i]  # 当前插值点 x_i

    # 1. 计算分子多项式: product_{j≠i} (x - x_j)
    numerator_coeffs = [Element.one(pairing, Zr)]  # 初始化为 1 (x^0)

    for j in range(n):
        if j == i:
            continue  # 跳过 x_i
        x_j = points[j]

        # 多项式乘法: (当前多项式) * (x - x_j)
        new_coeffs = [Element.zero(pairing, Zr)] * (len(numerator_coeffs) + 1)

        for power in range(len(numerator_coeffs)):
            a = numerator_coeffs[power]
            if a != Element.zero(pairing, Zr):
                new_coeffs[power + 1] += a  # a * x
                new_coeffs[power] -= a * x_j  # -a * x_j

        numerator_coeffs = new_coeffs

    # 2. 计算分母: product_{j≠i} (x_i - x_j)
    denominator = Element.one(pairing, Zr)
    for j in range(n):
        if j == i:
            continue
        denominator *= (x_i - points[j])

    # 3. 归一化: 分子多项式 / 分母
    final_coeffs = []
    for coeff in numerator_coeffs:
        final_coeffs.append(coeff*(denominator.__invert__()))

    return final_coeffs

def get_lagrange_value(pairing,points,coeffs,j):

    x_j = points[j]
    # 计算 ℓ_i(x_j)
    value = Element.zero(pairing, Zr)
    for power in range(len(coeffs)):
        value += coeffs[power] * (x_j ** power)
    print(f"F({x_j}) = {value}")
    return value

def get_multi_receivers_coefficients(pairing, points,t):
    # 初始化系数列表：[1] 表示 1 (即 x⁰ = 1)
    coeffs = [Element.one(pairing, Zr)]  # coeffs[0] = 1

    n = len(points)

    # 逐步乘以 (x - points[i])
    for i in range(n):
        c = points[i]
        new_coeffs = [Element.zero(pairing, Zr)] * (len(coeffs)+1)
        # 多项式乘法：(当前多项式) * (x - c)
        for power in range(len(coeffs)):
            a = coeffs[power]
            if a != Element.zero(pairing, Zr):
                new_coeffs[power + 1] += a  # a·x^{k+1}
            new_coeffs[power] -= a * c  # -a·c·x^k

        coeffs = new_coeffs

    # 最后 +1（即 x⁰ 的系数加 1）
    coeffs[0] += t

    return coeffs


def get_multi_receivers_value_by_coefficient(pairing, coefficients,x_i):
    p_x = Element.zero(pairing, Zr)
    for power in range(len(coefficients)):
        p_x += coefficients[power] * (x_i ** power)
    return p_x


def generate_random_string(length):
    letters = string.ascii_letters + string.digits  # 包含字母和数字
    return ''.join(random.choice(letters) for _ in range(length))

def sxor(s1,s2):
    l1=len(s1)
    l2=len(s2)
    if l1<l2:
        s1+=(l2-l1)*'0'
    else:
        s2 += (l1 - l2) * '0'

    return ''.join(chr(ord(a)^ord(b)) for a,b in zip(s1,s2))


def generate_mac(key,message):
    key_bytes = key.encode('utf-8')
    message_bytes = message.encode('utf-8')
    result=hmac.new(key_bytes, message_bytes, hashlib.sha256).digest()




