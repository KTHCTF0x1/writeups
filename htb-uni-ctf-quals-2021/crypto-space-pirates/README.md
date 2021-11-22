# Space Pirates

**Solves:** 123  
**Score:** 325

## Solution

In this challenge we are given a python program called `chall.py`:

```python
from sympy import *
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from random import randint, randbytes,seed
from Crypto.Util.number import bytes_to_long

FLAG = b'HTB{dummyflag}'
class Shamir:
    def __init__(self, prime, k, n):
        self.p = prime
        self.secret = randint(1,self.p-1)
        self.k = k
        self.n = n
        self.coeffs = [self.secret]
        self.x_vals = []
        self.y_vals = []

    def next_coeff(self, val):
        return int(md5(val.to_bytes(32, byteorder="big")).hexdigest(),16)

    def calc_coeffs(self):
        for i in range(1,self.n+1):
            self.coeffs.append(self.next_coeff(self.coeffs[i-1]))

    def calc_y(self, x):
        y = 0
        for i, coeff in enumerate(self.coeffs):        
            y +=coeff *x**i
        return y%self.p


    def create_pol(self):
        self.calc_coeffs()
        self.coeffs = self.coeffs[:self.k]
        for i in range(self.n):
            x = randint(1,self.p-1)
            self.x_vals.append(x)
            self.y_vals.append(self.calc_y(x))

    def get_share(self):
        return self.x_vals[0], self.y_vals[0]


def main():
    sss = Shamir(92434467187580489687, 10, 18)
    sss.create_pol()
    share = sss.get_share()
    seed(sss.secret)
    key = randbytes(16)
    cipher = AES.new(key, AES.MODE_ECB)
    enc_FLAG = cipher.encrypt(pad(FLAG,16)).hex()
    
    f = open('msg.enc', 'w')
    f.write('share: ' + str(share) + '\n')
    f.write('coefficient: ' + str(sss.coeffs[1]) + '\n')
    f.write('secret message: ' + str(enc_FLAG) + '\n')
    f.close()

if __name__ == "__main__":
    main()
```

And some data in a file called msg.enc:

```
share: (21202245407317581090, 11086299714260406068)
coefficient: 93526756371754197321930622219489764824
secret message: 1aaad05f3f187bcbb3fb5c9e233ea339082062fc10a59604d96bcc38d0af92cd842ad7301b5b72bd5378265dae0bc1c1e9f09a90c97b35cfadbcfe259021ce495e9b91d29f563ae7d49b66296f15e7999c9e547fac6f1a2ee682579143da511475ea791d24b5df6affb33147d57718eaa5b1b578230d97f395c458fc2c9c36525db1ba7b1097ad8f5df079994b383b32695ed9a372ea9a0eb1c6c18b3d3d43bd2db598667ef4f80845424d6c75abc88b59ef7c119d505cd696ed01c65f374a0df3f331d7347052faab63f76f587400b6a6f8b718df1db9cebe46a4ec6529bc226627d39baca7716a4c11be6f884c371b08d87c9e432af58c030382b737b9bb63045268a18455b9f1c4011a984a818a5427231320ee7eca39bdfe175333341b7c
```

By looking at the code and msg.enc we can conclude that msg.enc was generated when chall.py was run and we guess that it was run with the real flag instead of `HTB{dummyflag}`.

The class in the code is called `Shamir` and when instantiating it, the variable is called `sss`. By googling `shamir sss` we find that there is something called [Shamir's Secret Sharing](https://en.wikipedia.org/wiki/Shamir's_Secret_Sharing). That is probably what the class implements, or some modification of it. But this knowledge was not needed to solve it.

The code starts by generating a number `secret` at random. It uses this `secret` value to seed python’s PRNG. It then generates 16 random bytes and encrypts the flag using the random bytes as the key. The encrypted flag is then given to us as `secret message` in msg.enc. So our goal is to figure out `secret`, because with it, we can get the flag back.

The code also generates the coefficients of a polynomial modulo a given prime p:

y = secret + c<sub>1</sub>x + c<sub>2</sub>x<sup>2</sup> + ... + c<sub>n</sub>x<sup>n</sup>

The `secret` value is used as the first coefficient. But how are c<sub>i</sub> calculated? By looking at `calc_coeffs` and `next_coeff` we see that c<sub>i</sub> is generated based only on c<sub>i-1</sub>:

```python
def next_coeff(self, val):
        return int(md5(val.to_bytes(32, byteorder="big")).hexdigest(),16)

def calc_coeffs(self):
        for i in range(1,self.n+1):
            self.coeffs.append(self.next_coeff(self.coeffs[i-1]))
```

The code then evaluates the polynomial for some random inputs and gives us a pair of x and y. This is given as `share` in msg.enc. The final piece of information given to us is `coefficient` in msg.enc. This corresponds to c<sub>1</sub>. Now, using all this information, how do we find `secret`?

secret = y - (c<sub>1</sub>x + c<sub>2</sub>x<sup>2</sup> + ... + c<sub>n</sub>x<sup>n</sup>)

The insight is that since  we are given c<sub>1</sub> we can calculate all following c<sub>i</sub> using `next_coeff`, since c<sub>i</sub> only depends on c<sub>i-1</sub>. We were also given an x and y pair which we can plug in. Thus, we have all the information on the right hand side and can calculate `secret`. Using `secret` we can again seed python’s PRNG, generate the same random 16 bytes and use them as the key to decrypt the flag. The full solve script can be seen in `solve.py` and here after:

```python
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
```
