from hashlib import md5
from Crypto.Cipher import AES
from random import randint, randbytes, seed

def next_coeff(val):
    return int(md5(val.to_bytes(32, byteorder="big")).hexdigest(),16)

def calc_coeffs(coeffs):
    for i in range(1,n+1):
        coeffs.append(next_coeff(coeffs[i-1]))

def calc_y(x, coeffs):
    y = 0
    for i, coeff in enumerate(coeffs):
        y +=coeff *x**i
    return y%p

p =  92434467187580489687
k = 10
n = 18

# from msg.enc
x, y = 21202245407317581090, 11086299714260406068
coeff1 =  93526756371754197321930622219489764824
enc_flag = bytes.fromhex("1aaad05f3f187bcbb3fb5c9e233ea339082062fc10a59604d96bcc38d0af92cd842ad7301b5b72bd5378265dae0bc1c1e9f09a90c97b35cfadbcfe259021ce495e9b91d29f563ae7d49b66296f15e7999c9e547fac6f1a2ee682579143da511475ea791d24b5df6affb33147d57718eaa5b1b578230d97f395c458fc2c9c36525db1ba7b1097ad8f5df079994b383b32695ed9a372ea9a0eb1c6c18b3d3d43bd2db598667ef4f80845424d6c75abc88b59ef7c119d505cd696ed01c65f374a0df3f331d7347052faab63f76f587400b6a6f8b718df1db9cebe46a4ec6529bc226627d39baca7716a4c11be6f884c371b08d87c9e432af58c030382b737b9bb63045268a18455b9f1c4011a984a818a5427231320ee7eca39bdfe175333341b7c")

coeffs = [coeff1]
calc_coeffs(coeffs)
coeffs = coeffs[:k-1]

secret = (y - x*calc_y(x, coeffs))%p

seed(secret)
key = randbytes(16)
cipher = AES.new(key, AES.MODE_ECB)
print(cipher.decrypt(enc_flag).decode())

# HTB{1_d1dnt_kn0w_0n3_sh4r3_w45_3n0u9h!1337}
