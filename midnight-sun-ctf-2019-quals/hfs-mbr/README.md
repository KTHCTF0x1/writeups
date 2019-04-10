# hfs-mbr

**Category**: rev
**Authors**: @viktoredstrom, @n00byedge

---

After taking a look at the bootloader as loaded from the MBR, we can see that all there is is just a bit of video setup code and a BIOS call to load the rest of the bootloaders data into memory.
![bootloader](img/bootloader.png?raw=true)

Let's let the MBR load the rest of the code and take a look what happens if we dump the memory after that:
![entry](img/entry.png?raw=true)

The next piece of code seems to take some input (according to IDAs very helpful comments), do a range check on the input character and if it passes, it will jump to a function using a jump table, indexed by this character.

Each of these functions seem to do a different thing, jumping to one of two labels under different circumstances, let's take a look at them:
![gbp](img/gbp.png?raw=true)

We can see here that if we reach 9 on any of these two variables, the program does one of two things:
  * If the first counter reaches `9` first, we win;
  * If the second counter reached `9` first, we lose
We can also see that incrementing the first counter also increments the second counter. Let's call the first counter `goodBoyPoints` and the second counter `badBoyPoints`.

So we need to hit a good boy point every time, let's see which functions can yield that and analyze them. We see that these functions depend on the value `badBoyPoints`. For example:
![e](img/e.png?raw=true)

This is the code which gets executed if we enter the character `e`. This will run `addGoodBoyPoint` iff `ds:0x81BA` (`badBoyPoints`) is equal to `0x7`. This means `e` is the `0x7`th character, 0 indexed. Repeating this analysis for each of the functions capable of giving us a good boy point, we finally get the password:
`sojupwner`

Logging in to the remote server with this password yields the following flag: `midnight{w0ah_Sh!t_jU5t_g0t_REALmode}`
