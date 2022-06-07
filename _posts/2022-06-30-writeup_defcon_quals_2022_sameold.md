---
title: "DEF CON CTF 2022 Qualifiers Writeup: Same Old"
libs: [mathjax]
---

<div class="mathjaxDeclarations">
    @@\newcommand{\nl}{\\}@@
    @@\newcommand{\FF}{\mathbb{F}}@@
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
[intended solution][1]. I can guess that this method "randomly" samples the
possible checksums, taking @@2^{32}@@ tries to find a solution on average. This
hunch is confirmed by all the example answers having six extra characters, where
@@n=6@@ is the smallest integer satisfying @@62^n \geq 2^{32}@@. Finding a
solution using fewer letters is possible but unlikely --- @@21.7\%@@ probability
at most.

However, there is another approach that leverages the properties of a Cyclic
Redundancy Check (CRC). It is guaranteed to find a solution, and it does so much
faster than the straightforward but exponential method.


#### How CRCs Work

First, it's necessary to understand some of the math underlying CRCs.
Ultimately, the goal of any checksum is to take in some data and derive from it
a "check value" of a fixed length --- 32-bit in our case. It just has to
withstand random mutations, not adversarial changes to the input. As such, these
algorithms can (and should) be simpler than hashes. They should be
mathematically nice to ease reasoning about how they respond to different
classes of errors and how those responses may be used to recover the original
data from the corrupted copy.

In the specific case of CRCs, they treat each bit as an element of @@\FF_2@@: an
element of @@\\{0,1\\}@@ where addition is XOR and multiplication is AND. This
definition was chosen to make @@\FF_2@@ a *field*, a set of numbers where the
usual operations (addition, subtraction, multiplication, division) are defined
and behave the way you'd expect with regular numbers. To represent bitstrings,
CRCs work over @@\FF_2[x]@@: the ring of polynomials with coefficients in
@@\FF_2@@, with polynomial addition and multiplication defined in the usual way.
For example, the string `1010` is represented as @@x^3 + x@@, where @@x@@ is
just a formal symbol not representing any underlying value.

To calculate the checksum, CRCs reduce the bitstream modulo some polynomial. For
the case of CRC-32, it's
%%\begin{align\*}
    \pi =&\,
        x^{32} + x^{26} + x^{23} + x^{22} \nl
        &+ x^{16} + x^{12} + x^{11} + x^{10} \nl
        &+ x^8 + x^7 + x^5 + x^4 \nl
        &+ x^2 + x + 1,
\end{align\*}%%
the symbol @@\pi@@ of course standing for πolynomial. You can construct the
polynomial and then reduce it by polynomial long division, however it's more
economical to do the reduction after each operation. Effectively, you work over
@@\FF_2[x] / \langle\pi\rangle@@: the space of polynomials but you treat those
that differ by some multiple of @@\pi@@ as the same polynomial. Again, long
division can take any element to its "canonical" form.

That's CRCs in a nutshell. Treat your data as a polynomial @@p \in \FF_2[x] /
\langle\pi\rangle@@ and reduce it to its canonical form by polynomial long
division. Implementation is a bit more complicated than that, of course. For
instance, you actually reduce @@p \cdot x^{32}@@. When sending the message, you
can just append the checksum to it, and the check passes if the recieved message
is congruent to zero modulo @@\pi@@. Some implementations NOT the output.
Some reflect the bits of the output (so bit 31 maps to bit 0, 30 to 1, ...).
Some reflect the bits of each input byte individually. Most importantly, many
implementations use a table-driven approach, computing one word at a time
instead of just one bit. Exploring that is worth an entire post, but the upshot
is that it's only equivalent to this method when the algorithm is seeded with
zero. Some implementations seed it with `0xffff_ffff` instead, which has the
effect of NOTing the first 32 bits of the input. Equivalently, it prepends
%%\begin{equation\*}
    \frac{1}{x^{32}} \cdot \left( \sum_{i=0}^{31} x^i \right)
\end{equation\*}%%
to the input. In general, if the table method is seeded with @@p@@, it XORs that
with the first 32 bits of the input, or it equivalently prepends @@p \cdot
x^{-32}@@.


#### The Choice of π


[1]: https://github.com/Nautilus-Institute/quals-2022/tree/main/sameold "sameold Challenge Solution"
