# hfs-vm

**Category**: RE
**Authors**: @viktoredstrom

---

## Description
```bash
[*] '/home/vagrant/midnight/hfs-vm/hfs-vm'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```
We're given this program which interprets some custom set of instructions. Our task is to write some program which will give us a flag.

## Specs

There are 10 instructions, 16 registers (counting SP and PC) and 4 syscalls. Syscalls works by having a parent/child process (one responsible for our VM and the other for syscalls) and the two sharing data by using read/write on filedescriptors setup via `socketpair()`.

Instructions:

| opcode | action               |
| ------ | -------------------- |
| 0x0    | mov reg, reg/imm     |
| 0x1    | add reg, reg/imm     |
| 0x2    | sub reg, reg/imm     |
| 0x3    | xchg reg, reg/imm    |
| 0x4    | xor reg, reg/imm     |
| 0x5    | push reg, reg/imm    |
| 0x6    | pop reg, reg/imm     |
| 0x7    | mem[reg] = reg/imm   |
| 0x8    | reg = mem[reg]       |
| 0x9    | syscall              |
| 0xa    | print regs + stack   |

Syscalls:

| opcode | action      |
| ------ | ----------- |
| 0x0    | ls          |
| 0x1    | print       |
| 0x2    | getuid      |
| 0x3    | read flag   |
| 0x3    | read urandom |  

## <span style="color:red">B</span>hidra gang
```c
ulong do_syscall(char *reg_buf)

{
  ushort *puVar1;
  ushort uVar2;
  undefined8 uVar3;
  ulong uVar4;
  ulong uVar5;
  long in_FS_OFFSET;
  char local_25;
  undefined2 local_24;
  undefined2 local_22;
  long stack_cookie;
  ushort value_of_sp;

  stack_cookie = *(long *)(in_FS_OFFSET + 0x28);
  local_25 = (char)*(undefined2 *)(reg_buf + 0x12);
  local_24 = *(undefined2 *)(reg_buf + 0x14);
  local_22 = *(undefined2 *)(reg_buf + 0x16);
  puVar1 = *(ushort **)(reg_buf + 8);
  value_of_sp = *(ushort *)(reg_buf + 0x2c);
  uVar2 = (0x20 - value_of_sp) * 2;
  *puVar1 = uVar2;
  memcpy(puVar1 + 1,reg_buf + (ulong)value_of_sp * 2 + 0x30,(ulong)uVar2);
  uVar3 = FUN_001012d0(*(int *)reg_buf,&local_25,5);
  if ((int)uVar3 == 0) {
    uVar4 = read_into_buf(*(int *)reg_buf,reg_buf + 0x10,2);
    uVar5 = uVar4 & 0xffffffff;
    if ((int)uVar4 == 0) {
      memcpy(reg_buf + (ulong)*(ushort *)(reg_buf + 0x2c) * 2 + 0x30,*(ushort **)(reg_buf + 8) + 1,
             (ulong)**(ushort **)(reg_buf + 8));
      goto LAB_0010174d;
    }
  }
  uVar5 = 0xffffffff;
LAB_0010174d:
  if (stack_cookie == *(long *)(in_FS_OFFSET + 0x28)) {
    return uVar5;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

So which syscall will be performed is determined by the value in reg_1 and we copy 2*(0x20 - $sp) worth of data onto our stack, so we need to align our stack pointer accordingly.

## Solution
```python
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
```

Which gives us the flag: `midnight{m3_h4bl0_vm}`
