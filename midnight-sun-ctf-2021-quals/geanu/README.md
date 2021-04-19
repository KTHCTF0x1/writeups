
## Title: Geanu
**Points:** 95  
**Solves:** 75

### Descriptions: 
I found this interesting binary from my temp files, I wonder what it does. 

We get a `geanu.tar.gz`

### Solution:
In the tar there is an ELF. One of our teammates figured out that it is a Golang
binary. Probably by looking at the output from `strings` and googling some of
them.

When looking at the ELF in ghidra it is very confusing since it is Go and not C.
It is hard to find the main function.

I found a [blog post](https://cujo.com/reverse-engineering-go-binaries-with-ghidra/)
describing how to reverse golang binaries in ghidra. They had created a [script](https://github.com/getCUJO/ThreatIntel/blob/master/Scripts/Ghidra/go_func.py)
which could be used to recover all the symbols in the binary.

After running the script I could find the main function as `main.main`.

The main function seems to first print the Keanu Reeves banner, read some input,
check some value in an `if`-statement and if the value matches `0x539` (1337) it
will run some function, otherwise not.

After some fiddling with gdb to see exactly which value was compared in the `if`
we come up with the following solve script:

```python
from pwn import *
p = process("./geanu")
p.send(b"AAAABBBBCCCCDDDDEEEEFF\x39\x05")
p.interactive()
```

Apparently you only had to pass this one check and then the binary would print
the flag.

**Flag:** midnight{r3v3rs1n9g0L4ng5uck5}
