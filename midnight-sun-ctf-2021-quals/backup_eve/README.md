## Title: Backup - eve
**Points:** 113  
**Solves:** 55

### Descriptions: 
The backup of the home directories might contain too much information

Service: ssh -p2222 backup-01.play.midnightsunctf.se
Download: backup.tar.gz

### Solution:
The backup tar contains a folder named eve. In that folder the file ```flag.enc``` can be found. From that file we get the string:
```
eunfutsq{up_qsup_wmoerk 0o bjjcD0wf}
```

The first thing that pops into your head when seeing this string is that it's some kind of substitution cipher. Where the first part of the string, eunfutsq{, clearly decodes to midnight{. 

By adding this as a clue in quipquip we get that the first part of the flag is ```midnight{is_this_```. Guessing that 0o corresponds to 0r gets us ```midnight{is_this_warmup 0r bjjcD0wn}```. Since D0wn is a word, we can assume that capital letters and numbers do not change. 

From this you might be thinking that the flag must be ```midnight{is_this_warmup 0r coolD0wn}``` But no.... Unfortunately that isn't the correct flag. For some weird reason the correct flag is ```midnight{is_this_warmup 0r koolD0wn}```. Cooldown with a k and spaces? That's a really nasty flag! 

**Flag:** midnight{is_this_warmup 0r koolD0wn}
