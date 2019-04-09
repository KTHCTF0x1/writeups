
## Title: Pgp-com
**Points:** 451  
**Solves:** 24

### Descriptions: 
You know how PGP works, right?

### Solution:

We are given a file called `pgp-communication.txt` which contains one private pgp key, one public key, 3 messages and the password `changemeNOW`.
We put them in separate files called `key.priv`, `key.pub`, `msg1.asc`, `msg2.asc` and `msg3.asc`. We notice that `msg2.asc` is noticeably smaller than the other messages.

We use the commands `gpg --import key.pub` and `gpg --import key.priv` to import the keys so we can use them. We then try to decrypt the messages using: `gpg msg1.asc`. Message 1 and 3 works, but 2 fails saying something like `gpg: decryption failed: No secret key`.

Message 1 talks about how they have created their own pgp implementation and message 3 says that they have found a bug and that their randomness is bad but that it shouldn't affect the keypairs.

Using the tool `pgpdump`, https://www.mew.org/~kazu/proj/pgpdump/en/, we found that `msg1` and `msg3` had 3 public keys associated with them and that `msg2` only had 2. It was missing the one we had. Apparently pgp works by encrypting the message with a symmetric key, encrypting that symmetric key using assymetric keypairs and then storing that encrypted "session" key along with the message. It made sense now why we couldn't decrypt `msg2`. There was no encryption of the session key using our keypair stored with `msg2`.

So if the keypairs don't have bad randomness, then maybe the session keys have bad randomness? 

Since we have imported `key.priv` we can decrypt and extract the session keys of `msg1` and `msg3` using:

`gpg --show-session-key msg1.asc`

We find that the session keys are:

`msg1: 9:0000000000000000000000000000000000000000000000000000000000001336`  
`msg3: 9:0000000000000000000000000000000000000000000000000000000000001338`

So we make the guess that `msg2`'s session key ends in `1337`. We decrypt `msg2` with a custom session key with

`gpg --override-session-key 9:0000000000000000000000000000000000000000000000000000000000001337 -d msg2.asc`

and we get the flag.

**Flag:** midnight{sequential_session_is_bad_session}
