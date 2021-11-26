#!/usr/bin/env python3
from pwn import *

flag_len = 25
with open("flag.txt", "w") as f:
    f.write("A"*flag_len)

flag = bytearray()
r = gdb.debug("./vault", api=True)
r.gdb.execute("b*$rebase(0x0c3a1)")
for i in range(flag_len):
    print(flag)
    r.gdb.continue_and_wait()
    x = r.gdb.execute("i r rcx", to_string=True)
    flag.append(int(x.split(" ")[-1]))
    r.gdb.execute("set $rax = %d" % flag[-1])

print("done:", flag)
