
## Title: Labyrevnt
**Points:** 107  
**Solves:** 60

### Descriptions: 
aarch64 is the future, crackme


### Solution:

Find that there is not much that actually happens other then some simple operations that are ran on every input byte. We solver simply by extracting the compare values and brute forcing the flag one character at a time.

Solve script:
```C
unsigned long long calc(char c) {
    unsigned long long big = -0x395b586ca42e166bull;
    unsigned long long res = 0x1337ull ^ 1ull * big;
    res = (res ^ (unsigned long long)c) * big;
    res = (res ^ res >> 0x2full) * big;
    res = res ^ res >> 0x2full;
    unsigned long long want = 0x34514c558ba5e73bull;

    printf("%llx\n", res);
    return res
}
int main(){
    unsigned long long arr[] = {0x188cf31a079d66fc, 0xa12c8af2572dfa48, 0x1ff01ebc0c7408cb,0xd58e3ba2fbef9d8c, 0x5674b7653639cb87, 0x3eb8b6a6f0753e49,0x1ff01ebc0c7408cb, 0xf9dfa617052dfd5e, 0x34514c558ba5e73b,0xf9dfa617052dfd5e, 0x3a9c8840cebaea9e, 0xb13e0ecbeba2478f,0x827aee59df4bcce8, 0x3a9c8840cebaea9e, 0xb13e0ecbeba2478f,0x827aee59df4bcce8, 0x7641dbd6cd9d79af, 0x7641dbd6cd9d79af,0x7641dbd6cd9d79af, 0x0000000000000000};
    for(auto val: arr)for(char c = 1; c != 0; c++){
        if(calc(c) == val){
            printf("%c", c);
            break;
        }
    }
}
```


**Flag:** w1thOut_A_mUrmUr...
