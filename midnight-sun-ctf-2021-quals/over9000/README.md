
## Title: Labyrevnt
**Points:** 244  
**Solves:** 16

### Descriptions: 
One of our operatives managed to extract an important file and the encryption key from a spy. Sadly it is encrypted using some weird spanish encryption tool and all we could find is this shareware encryptor which is slow and has no decryption function. Can you recover the key? 

We also get `oVER9000.tar.gz`

### Solution:

The tar contains three files: `encrypt`, `crypt.bin` and `key.txt`.

```
encrypt:   ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, stripped
crypt.bin: data
key.txt:   UTF-8 Unicode text, with very long lines
```

Worth noting is that `crypt.bin` is 36 KB and that `key.txt` is 17 KB, so pretty large. So the goal is to decrypt `crypt.bin` using `key.txt`.

We can try to encrypt using `echo "hello" | ./encrypt key`, but as the
description says it is veeeery slow. The cipher seems to be a stream cipher. The
same number of bytes in the plaintext as in the ciphertext.

When looking into `encrypt` we can see this general structure:

1. Allocate 0x20006 byte buffer. This is the internal state.
2. Read the key from command line argument.
3. Do large precomputation using the key, this modifies the internal state.
4. Then comes the encryption loop. For each iteration: read 1 input byte, modify
the internal state, mixing in the input byte, take some part of the internal 
state as the encrypted output byte.

Instead of trying to understand the cipher in detail and write a decryption function our attack plan is to bruteforce each byte of the plaintext one at a time:

1. Recovered_plaintext = ""
2. Encrypt (Recovered_plaintext + b) for each b = [0,255], see which output matches a prefix of the 
ciphertext.
3. Recovered_plaintext += the byte that made the ciphertexts match
4. Repeat step 2,3 as long as there is ciphertext left to decrypt.

Now this works fine, but the code is sooo slow. We need to speed it up for this
to become feasible.

When looking at the code we notice that there are a bunch of dummy busy-loops
spread out in the code. Like this:

```c
i = 0x100;
do {
    DAT_00104030 = DAT_00104030 * DAT_00104030;
    i = i + -1;
} while (i != 0);
```

We simply patch out those loops with NOPS. This improves the running speed 
somewhat. But it is not fast enough.

Since we are using the same key each time we can do the key-precomputation just
once and save the result. We run the program in gdb, stop just before the
encryption loop starts and extract the internal state buffer. We then rewrite
encryption loop in C and plug in the hardcoded internal state.

(Here I made some stupid python script which called the C-program, this was not
fast, don't do that.)

Since we now can encrypt quickly, we implement the rest of the attack in the
same C-program. The full code can be seen in `solve.c`. After a short bruteforce
we get the flag:

**Flag:** midnight{H0w_10ng_wi11_73H_d4mn3d_7hing_1457}
