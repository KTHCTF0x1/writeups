
## Title: Blueberry Pop
**Points:** 155  
**Solves:** 33

### Descriptions: 
Eric from the organization 'Our future' seems to be in distress. What seems to be the issue? 

We are given a `blueberrypop.tar.gz`

### Solution:

The tar.gz contains a file called `HILFE.eml`, an email. The email has two other
files attached to it. One elf-file encryption program and one encrypted message.
Our goal is to decrypt the message.

Someone else please fill in the beginning ...

...


We manage to extract the following .pyc-files from the elf:

```
main.pyc
pyiboot01_bootstrap.pyc
pyimod01_os_path.pyc
pyimod02_archive.pyc
pyimod03_importers.pyc
pyi_rth_multiprocessing.pyc
```

We try to use [uncompyle6](https://pypi.org/project/uncompyle6/) to decompile 
the .pyc-files back to python code. Only some of them work, but don't contain 
anything interesting. Especially `main.pyc` doesn't want to decompile. When 
trying, uncompyle6 spits out `Unknown type 0` and an assertion error.

If you look at the first couple of bytes in each pyc-file you can see that some
start with 33 and some with 55.

```
main.pyc
00000000: 330d 0d0a 0000 0000 0000 0000 0000 0000  3...............
pyiboot01_bootstrap.pyc
00000000: 330d 0d0a 0000 0000 0000 0000 0000 0000  3...............
pyimod01_os_path.pyc
00000000: 550d 0d0a 0000 0000 7079 6930 590c 0000  U.......pyi0Y...
pyimod02_archive.pyc
00000000: 550d 0d0a 0000 0000 7079 6930 512b 0000  U.......pyi0Q+..
pyimod03_importers.pyc
00000000: 550d 0d0a 0000 0000 7079 6930 9862 0000  U.......pyi0.b..
pyi_rth_multiprocessing.pyc
00000000: 330d 0d0a 0000 0000 0000 0000 0000 0000  3...............
```

The ones starting with 33 don't want to decompile and the ones that start with
55 do. After looking at some [notes](https://github.com/mattiasgrenfeldt/writeups/tree/master/2020/defconquals/bytecoooding)
from a previous CTF about the pyc file format we can see that the first bytes
contain the version of the pyc. Since having 55 first worked we just tried that
and then uncompyle6 was happy. We now have the source code for main.py.

After looking through the source code we realize that the private key held by
Eric, the person who encrypted the message, is irrelevant. The message is
actually encrypted by an 'ephemeral key' which is generated from the username of
the person encrypting the message, the current timestamp when encrypting (in
milliseconds) and a 256 random value.

The username can be guessed to be erism from the email file. The timestamp
should be within 24 hours of sending the email probably. The 256 bit random
value is not actually random since the random generator is seeded with a static 
value.

So we know all the info except the timestamp. Time to bruteforce! See `solve.py`
for the full brute force script.

After running it for a while, starting several scripts at different starting
times to make it go faster, getting nervous that you picked the wrong username,
starting a couple more with "Eric", "eric", "Eric Smith" and
"erism@ourfuture.org" as the username, the first script launched finally spits
out the flag:

**Flag:** midnight{YABSRG_y3t_4n0th3r_b4d_s33d3d_r4nd0m_g3n}
