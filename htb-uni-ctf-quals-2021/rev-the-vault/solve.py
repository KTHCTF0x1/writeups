#!/usr/bin/env python3
from pwn import *

flag = b"HTB{" + bytes([0x76])
with open("flag.txt", "wb") as f:
    f.write(flag)
print(flag)

r = gdb.debug("./vault", """b*$rebase(0x0c3a1)
c\n""" + "c\n"*len(flag))

r.interactive()
