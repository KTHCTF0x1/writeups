
## Title: Ezdsa
**Points:** 223  
**Solves:** 57

### Descriptions: 
Someone told me not to use DSA, so I came up with this.

### Solution:

We are given the ip and port of a service and it's source code. This is the relevant part:

```python
h = bytes_to_long(sha1(m).digest())
u = bytes_to_long(Random.new().read(20))
assert(bytes_to_long(m) % (self.q - 1) != 0)

k = pow(self.gen, u * bytes_to_long(m), self.q)
r = pow(self.gen, k, self.p) % self.q
s = pow(k, self.q - 2, self.q) * (h + self.key * r) % self.q
assert(s != 0)

return r, s
```

We interact with the service by supplying `m` and it prints `r` and `s` to us. Through the source code `gen`, `q`, and `p` are given and we see that `self.key = int(FLAG.encode("hex"), 16)`. Except for `key`, only `u` is unknown here. Using factordb.com we guess that p and q are prime.

The line `assert(bytes_to_long(m) % (self.q - 1) != 0)` is to stop us from using Fermat's little theorem which states that

`a^(p-1) = 1 mod p`

where `p` is a prime. If the assert wouldn't have been there we would have set `m` such that `bytes_to_long(m)=q-1` which would have given:

`k = gen^(u*m) = (gen^u)^m = 1 mod q`

So, instead of submitting `m` as `q-1` we submit it as `(q-1)/2`. Since `u` is random it is very likely that it will have a factor of `2` and in that case `u*m` will have a factor of `q-1` which implies that `gen^(u*m) = 1 mod q` anyways.

We now don't have any unknowns left since we eliminated `u`. Now we only have to solve for the flag:

`r = (gen^1 mod p) mod q = (gen mod p) mod q`
`s = (1^(q-2) mod q)*(h + key*r) mod q = h + key*r mod q`
`=> key = (s-h)*r^(-1) mod q`

**Flag:** midnight{th4t_w4s_e4sy_eh?}
