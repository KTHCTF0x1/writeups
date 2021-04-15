import binascii
from Crypto.Cipher import AES
from Crypto.Util import Counter
import sys, datetime, getopt, getpass, time, random, secrets, struct, aes_keywrap
HEADER_FMT = '>5sB8s40si'
FILE_MAGIC = b'EFC82'
DATA_MAGIC = FILE_MAGIC
HEADER_SIZE = struct.calcsize(HEADER_FMT)

THE_TIME_STAMP = None
random.seed('0427cb12119c11aff423b6333c4189175b22b3c377718053f71d5f37fd2a8f22')
RDATA = str(random.getrandbits(256))

def get_rng(seed=None):
    rnd = random.Random()
    if not seed:
        user = "erism"
        ts_ms = THE_TIME_STAMP.isoformat(sep='!', timespec='milliseconds')
        seed = f"{user}_{ts_ms}_{RDATA}"
    rnd.seed(seed)
    return rnd

def generate_ephemeral_key() -> bytes:
    rnd = get_rng()
    return bytes((rnd.getrandbits(8) for _ in range(32)))

file_enc = open("message.txt.enc", "rb")
enc_data = file_enc.read()
header = enc_data[:HEADER_SIZE]
magic, version, iv_part, wrapped_ek, filelen = struct.unpack(HEADER_FMT, header)
if magic != FILE_MAGIC or version != 1 or filelen != len(enc_data) - HEADER_SIZE:
    raise Exception('File is corrupt, or not an encrypted file')

# Tue, 9 Feb 2021 10:27:56 -0600
base = datetime.datetime(2021, 2, 10).timestamp()

old_enc_data = enc_data

n = 1000*60*60*24
print("N", n)
for i in range(n):
    if i % 10000 == 0:
        print(i, "/", n, THE_TIME_STAMP, i/n*100.0)
    THE_TIME_STAMP = datetime.datetime.fromtimestamp(base - float(i)/1000.0)
    
    ephemeral_key = generate_ephemeral_key()

    decryptor = AES.new(ephemeral_key, mode=(AES.MODE_CTR), counter=Counter.new(64, prefix=iv_part))
    data = decryptor.decrypt(enc_data[HEADER_SIZE:])
    if data.startswith(DATA_MAGIC):
        print('Decrypted data:', repr(data))
        break

print("DONE")
