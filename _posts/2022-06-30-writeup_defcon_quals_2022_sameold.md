---
title: "DEF CON CTF 2022 Qualifiers Writeup: Same Old"
libs: [mathjax]
---

<div class="mathjaxDeclarations">
</div>

My family came over for my sister's graduation, so I chose to spend time with
them instead of competing in the 2022 DEF CON CTF Qualifiers. Still, I briefly
looked over the challenges, and I later solved this "mic test" challenge.

> **sameold**
>
> Hack ___ planet!
>
> Submit a string that complies with the following rules:
>
> - The string should start with the punycode of your team name. This is a good
>   time for you to figure out with which team you are playing.
> - After your team name, you may add any number of alphanumeric characters.
> - `CRC32(the_intended_answer) == CRC32(your_string)`

Most teams solved this challenge by brute-force, which is surprisingly the
[intended solution][1]. One can guess that this method "randomly" samples the
possible checksums, taking @@2^{32}@@ tries to find a solution on average. This
hunch is confirmed by all the example answers having six extra characters, where
@@n=6@@ is the smallest integer satisfying @@62^n \geq 2^{32}@@. Finding a
solution using fewer letters is possible but unlikely --- @@21.7\%@@ probability
at most.

However, there is another approach that takes advantage of the Cyclic Redundancy
Check's properties. It is guaranteed to find a solution, and it does so much
faster than the straightforward but exponential method.


[1]: https://github.com/Nautilus-Institute/quals-2022/tree/main/sameold "sameold Challenge Solution"
