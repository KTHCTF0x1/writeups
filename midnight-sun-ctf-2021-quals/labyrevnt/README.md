
## Title: Labyrevnt
**Points:** 102  
**Solves:** 65

### Descriptions: 
You find yourself at a labyrinth. Can you find the way through it?

### Solution:

Objdump the given binary and extract all function calls in for every function. Then run dfs to find the path from walk_start to walk_end. Then manually save the letter that will result in that jump by dissasembling in Ghidra.

Script to find path from objdump:
```python
s = ''
edges = {}


def parse(s):
    p = s.split('><')[0]
    edges[p] = s.split('><')[1:]


with open('dmp', 'r') as o:
    for l in o.readlines():
        if '0000000000' in l:
            s += 'f' + l.split(' ')[-1][:-2]+'\n'
            continue
        if 'callq' in l and 'walk_' in l:
            s += l.split(' ')[-1]+'\n'
            continue
    for l in s.split('f<')[1:]:
        parse(l.replace('\n', '')[:-1])
seen = []


def dfs(n):
    if n in seen:
        return None
    seen.append(n)
    if n == 'walk_end':
        return [n]
    for i in edges[n]:
        r = dfs(i)
        if r != None:
            return [n]+r


print(dfs('walk_start'))
```
**Password:** aBIksNPZlfMnluFMRqtNOAkdWfuMuTIICGGWvhbWYwMlbdlCGznVNVzAsHjynOjHuuuvMkOmLMhYVeEWKjGLhmhLxyvtvxpzGCWuibxDhGzEmAfkepZDINxdHTQkKrirkJNnmyVRweEjBoEAwgTVEEkEVdRjzAFcxZrdSYbPQstuILsIjOSWgLLLXvkCAQVyYqJxa


**Flag:** midnight{y0u_w3r3_l05t_f0r_4_wh1l3_bu7_y0u_f1n411y_g0t_0ut}
