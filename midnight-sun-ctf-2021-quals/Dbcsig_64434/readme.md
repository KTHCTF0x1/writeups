## Title: Dbcsig_64434
**Points:** 228  
**Solves:** 18

### Descriptions: 
Signatures, signatures, signatures...

Download: dbcsig_64434.tar.gz

### Solution:
p is 512 bit. From 
`x = int.from_bytes(h*2, "big")`
we get that `x=x1*(2^256+1)` and from 

```python
k = next_prime(int.from_bytes(
    sha256(message + priv.to_bytes(128, "big")).digest() + \
    sha256(message).digest(),
    "big"
))
```

we get that `k = k1*2^256+k2` for known number `k2` and 256 bit numbers `k1` and `x1`.
In practice we need to bruteforce the small constant added by `next_prime` to properly find the value of `k2`, but as primes are logarithmically spaced it shouldn't be more than a couple of hundred. 

Now with `s = int(Zmod((p-1)/2)(-r*priv+h)/k)` we get the following equation, where `k1` and `x1` are the only unknowns:

`(k1*2^256+k2)*s+r*(x1*(2^256+1))==h) (mod (p-1)/2)`

This can easily be rewritten into 

`(k1+t*x1+u)=0 (mod (p-1)/2)`

Because `k1` and `x1` are small compared to the modulus, we can solve this equation with lattice reduction, as described in the paper https://eprint.iacr.org/2020/1506.pdf on page 29.

```python
g =  3
h = 31402050724530798506681514245176314739367147232981131812111980907582143500008
p = 403564885370838178925695432427367491470237155186244212153913898686763710896400971013343861778118177227348808022449550091155336980246939657874541422921996385839128510463
pub = 246412225456431779180824199385732957003440696667152337864522703662113001727131541828819072458270449510317065822513378769528087093456569455854781212817817126406744124198
r = 195569213557534062135883086442918136431967939088647809625293990874404630325238896363416607124844217333997865971186768485716700133773423095190740751263071126576205643521
s = 156909661984338007650026461825579179936003525790982707621071330974873615448305401425316804780001319386278769029432437834130771981383408535426433066382954348912235133967

from hashlib import sha256
k2 = int.from_bytes(sha256(b"blockchain-ready deterministic signatures").digest(),"big")
for i in range(500):
    k2+=1
    
    z = Zmod((p-1)//2)
    
    a = z(r)/s/2^256
    b = z(h)/s/2^256-z(k2)/2^256

    a,b,c = z(1)/a,(2^256+1), -b/a
    t = int(z(b)/a)
    u = int(z(c)/a)
    n = (p-1)/2
    K = 2^256

    M = matrix([[n, 0,0],
    [t ,  1, 0],
    [u ,  0, K]])

    k1_,x1_,_ = M.LLL()[0]
    k1_ = -k1_

    print(x1_*(2^256+1))
```

This script prints one solution for each `i`. One number stands out as smaller than the others, so we guess that that is it.

Flag: midnight{13332632188792525073310635276710580378130784424834265094905078640561661762622074406657091318849731839042773641535670695955904806248363952689290204619121447}
