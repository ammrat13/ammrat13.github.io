---
title: "DEF CON CTF 2022 Qualifiers Writeup: Same Old"
libs: [mathjax]
---

<div class="mathjaxDeclarations">
    @@\newcommand{\nl}{\\}@@
    @@\newcommand{\FF}{\mathbb{F}}@@
    @@\newcommand{\ZZ}{\mathbb{Z}}@@
    @@\newcommand{\matr}[1]{\mathbf{#1}}@@
    @@\newcommand{\vect}[1]{\mathbf{#1}}@@
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
definition was chosen to make @@\FF_2@@ a *field*, a set where the usual
operations (addition, subtraction, multiplication, division) are defined and
behave the way you'd expect with regular numbers. To represent bitstrings, CRCs
work over @@\FF_2[x]@@: the ring of polynomials with coefficients in @@\FF_2@@,
with polynomial addition and multiplication defined in the usual way. For
example, the string `1010` is represented as @@x^3 + x@@, where @@x@@ is just a
formal symbol not representing any underlying value. Again, this choice was made
to make CRCs easy to reason about mathematically. Polynomials are some of the
nicest objects out there, but they have just enough depth to admit sophisticated
algorithms.

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
message's polynomial and then take the remainder by polynomial long division,
however it's more economical to do the reduction after each operation.
Effectively, you work over @@\FF_2[x] / \langle\pi\rangle@@: the space of
polynomials but you treat those that differ by some multiple of @@\pi@@ as the
same polynomial. Again, long division can take any element to its "canonical"
form.

That's CRCs in a nutshell. Treat your data as a polynomial @@p \in \FF_2[x] /
\langle\pi\rangle@@ and reduce it to its canonical form by polynomial long
division. Implementation is a bit more complicated than that, of course. For
instance, you actually start with @@p \cdot x^{32}@@. That way, you can just
append the checksum to the message when sending it, and the check passes if the
recieved data is congruent to zero modulo @@\pi@@. Additionally, some
implementations perform superficial changes to the data. Some NOT the output.
Some reflect the output's bits (so bit 31 maps to bit 0, 30 to 1, ...). Some
reflect the bits of each input byte individually.

Most importantly, many implementations use a table-driven approach, computing
one byte at a time instead of just one bit. Exploring that is worth an entire
post, but the upshot is that it's only equivalent to this method when the
algorithm is seeded with zero. Some implementations seed it with `0xffff_ffff`
instead, which has the effect of NOTing the first 32 bits of the input.
Equivalently, it prepends
%%\begin{equation\*}
    \frac{1}{x^{32}} \cdot \left( \sum_{i=0}^{31} x^i \right).
\end{equation\*}%%
In general, if the table method is seeded with @@p@@, it XORs that with the
first 32 bits of the input, or it equivalently prepends @@p \cdot x^{-32}@@.


#### The Choice of π

It's worth noting some properties of CRC-32's choice of @@\pi@@. That polynomial
is *irreducible* over @@\FF_2@@, meaning it can't be factored any further
without introducing numbers other than @@\\{0,1\\}@@. A nice result of this
choice is that @@\FF_{2^{32}} = \FF_2[x] / \langle\pi\rangle@@ is itself a
field. Every element has a multiplicative inverse, and it makes sense to talk
about things like @@x^{-32}@@. The polynomial @@\pi@@ is also *primitive*,
meaning the formal symbol @@x@@ generates the multiplicative group. Taking the
powers of @@x@@ will go over every other element (except zero) before cycling
back to @@x@@. Again, these choices were made to make reasoning about this
structure easier.

The notation @@\FF_{2^{32}}@@ is no accident either. It's a field with exactly
that many elements --- a binary choice for each coefficient from @@x^0@@ to
@@x^{31}@@. It's also *the* field with that many elements, since all of them are
isomorphic. Additionally, all finite fields have prime power sizes, and it's
worth exploring why that is, since the same methods are used in the attack
later.

> *Lemma:* A field @@F@@ can be viewed as a vector space over any of its
> subfields @@K@@.

The required axioms can easily be checked. Those for vector addition are almost
trivially satisfied, as are those for identity and distributivity. The only
important thing to check happens with vector multiplication. We require that
%%\begin{equation\*}
    a \cdot b\vect{v} = (ab) \cdot \vect{v}
\end{equation\*}%%
where @@a,b \in K@@ and @@ab \in K@@. That's why we needed @@K@@ to be a
subfield. □

An easy example is @@\FF_{2^{32}}@@ itself. The elements @@1, x, x^2, \cdots@@
can be thought of as basis "vectors," scaled by either zero or one: an element
of @@\FF_2@@. This line of thinking extends quite well.

> *Theorem:* A finite field @@F@@ has order @@\|F\| = p^n@@ for @@p@@ prime.

Consider the additive group generated by @@1@@, so
%%\begin{align\*}
& 0 \nl
& 0 + 1 \nl
& 0 + 1 + 1 \nl
& \cdots.
\end{align\*}%%
It can be checked that these elements form a subfield @@K \subseteq F@@.
Additionally, since @@F@@ is finite, continuting to add ones in this manner will
eventually start to repeat elements, meaning @@K \cong \ZZ/p\ZZ@@. For that to
be a field, @@p@@ must be prime.

By the lemma above @@F@@ is a vector space over @@K@@, and since it's finite,
it's finitely generated. Let @@\\{b\_1, \cdots, b\_n\\}@@ be a
basis, so every linear combination
%%\begin{equation\*}
    \alpha\_1 b\_1 + \cdots + \alpha\_n b\_n
\end{equation\*}%%
gives a unique element of @@F@@. With each @@\alpha@@ in @@K@@, we get @@p@@
possibilities for each coefficient, giving a total of @@p^n@@ different
elements. □

This proof was found on [MathOverflow][2], but it's not the only one. Another,
also from [MathOverflow][3], uses Bézout's identity to show by contradiction that the
field would have zero divisors otherwise.


#### The Approach

With all the introductory material out of the way, we can start tackling the
actual problem. As a reminder, we want to find a string that starts with a
specific substring (say `GreyHatGT`) whose CRC-32 is a particular value. I'll
actually restrict the search space a bit more. I'll look for a string that
starts with `GreyHatGT` then contains exactly @@\ell@@ characters, each either
@@c@@ or @@d@@. Originally I chose `0` and `1` because their ASCII codes differ
by @@1@@, but that's not required. Just let @@\delta = d - c@@. Now compute
@@p@@ the CRC-32 of the original message: `GreyHatGT` followed by the character
@@c@@ repeated @@\ell@@ times. Of course, this will likely differ from the
target polynomial @@t@@, but we can change the message by substituting some
instances of @@c@@ with @@d@@ --- by adding @@\delta@@s shifted by the
appropriate amounts.

Specifically, we wish to solve for @@\alpha_i \in \FF_2@@ in
%%\begin{equation\*}
    x^{32} \cdot \sum\_{i=0}^{\ell-1} \alpha\_i \cdot x^{8i}\delta = t - p.
\end{equation\*}%%
The @@x^{8i}@@ term in the sum shifts the correction into the correct place. For
example, setting @@i=0@@ will shift the correction to the last place in the
string, setting @@i=1@@ will be the second to last, and so on. Choosing
@@\alpha_i=1@@ means to substitute that character, while choosing it zero means
to leave it as @@c@@. The extra shift of @@x^{32}@@ corresponds to the message
being multiplied by that before taking the remainder. Ultimately, changing the
message leads to predictable effects on the output --- if you add something to
the input, you just add the same thing to the output too. So, we take a look at
the difference and try to solve for the required change.

We can rearrange the above equation to read
%%\begin{equation\*}
    \sum\_{i=0}^{\ell-1} \alpha\_i \cdot \left(x^8\right)^i = \frac{t - p}{x^{32}\delta}.
\end{equation\*}%%
On the LHS we have a linear combination of constant elements, and on the RHS we
have a constant. To solve this, we suddenly remember that this field
@@\FF_{2^{32}}@@ can be expressed as a vector space over a subfield. Taking
@@K=\\{0,1\\}=\FF_2@@ allows us to operate under the standard basis
@@\\{1,x,x^2,\cdots,x^{31}\\}@@. The constants can be rewritten in this basis to
get
%%\begin{align\*}
    \sum\_{i=0}^{\ell-1} \alpha\_i \vect{v}\_i &= \vect{y} \nl
    \matr{V}\vect{\alpha} &= \vect{y},
\end{align\*}%%
where @@\matr{V}@@ is the matrix with column vectors @@\vect{v}\_i = x^{8i}@@.
This system can be easily solved, though not necessarily uniquely, as long as
@@\matr{V}@@'s columns span @@\FF_{2^{32}}@@.

So when does that fail? Clearly, when @@\ell@@ is too small, there aren't enough
vectors for a baisis and thus too few for a spanning set. The least you can
possibly get away with is @@\dim\FF_{2^{32}} = 32@@. I assert that @@32@@ is
also sufficient, and you'll never require more.

> *Lemma ([Freshman's Dream][4]):* Over a ring @@R@@ of prime characteristic
> @@p@@, any @@x,y \in R@@ satisfy @@(x+y)^p = x^p+y^p@@.

Simply expand via binomial theorem. All the "impure" terms drop out because
their coefficients are all multiples of @@p@@. Why? Remember that
%%\begin{align\*}
    \binom{p}{k}
        &= \frac{p!}{k! \cdot (p-k)!} \nl
        &= \frac{1}{k!} \cdot p \cdot (p-1) \cdots (p-k+1).
\end{align\*}%%
Since @@p@@ is prime, it's not possible for @@k!@@ to divide @@p@@ with @@k <
p@@. So, the factor remains, and @@\binom{p}{k}@@ is divisible by @@p@@. The
only places this argument breaks are when @@k=p@@ and when @@k=0@@ where
expanding the numerator just results in @@1@@. In those cases,
@@\binom{p}{k}=1@@. Thus, over this ring where multiples of @@p@@ vanish, only
the first and last terms of the binomial expansion remain. □

This result holds over @@\FF_{2^{32}}@@ where @@p=2@@.

> *Lemma ([Lemma 1.6 of this][5]):* The multiplicative group @@F^\times@@ of a
> finite field @@F@@ is cyclic.

Remember that, over fields, polynomials can have at most as many roots as their
degree. If it has a root @@r@@, a factor of @@(X-r)@@ can be divided out. This
can be repeated until the degree of the polynomial is reduced to a constant. We
can use that fact to show the following: if @@F^\times@@ has at least one
element of order @@d@@, then it has exactly @@\phi(d)@@ of them. Let @@g@@ be an
element such that @@g^d@@ is the lowest power of @@g@@ equaling the group
identity @@1@@. Every other element @@X@@ in the group it generates @@\langle
g\rangle@@ will also satisfy @@X^d - 1 = 0@@. There are @@d@@ such other
elements, so we've found all the possible roots of that polynomial. To find
objects in @@F^\times@@ of order exactly @@d@@, it suffices to restrict our
search to @@\langle g\rangle@@. By basic number theory, out of the @@d@@
elements in that cycle with order dividing @@d@@, exactly @@\varphi(d)@@ of them
will have order exactly @@d@@.

Define @@\text{NumElementsOfOrder}(d)@@ to be the number of elements in
@@F^\times@@ such that their @@d@@-th power is the smallest power equaling
@@1@@. As discussed above, that function returns either @@\varphi(d)@@ or @@0@@.
Clearly, summing over all the values @@d@@ can take will give the size of the
group:
%%\begin{align\*}
    \|F^\times\|
        &= \sum\_{d \text{ dividing } \|F^\times\|} \text{NumElementsOfOrder}(d) \nl
        &\leq \sum\_{d \text{ dividing } \|F^\times\|} \varphi(d) \nl
        &\leq \|F^\times\|, \nl
\end{align\*}%%
with the last step deriving from [Gauss's formula][6]. Since the first sum
attains its maximum value, it must agree with the second sum on every term. In
particular, this means
%%\begin{align\*}
    \text{NumElementsOfOrder}(|F^\times|)
        &= \varphi(|F^\times|) \nl
        &\neq 0.
\end{align\*}%%
There is at least one element whose powers generate the whole group. □

This result isn't strictly needed, but it's helpful to get intuition, and the
methods used are cool.


[1]: https://github.com/Nautilus-Institute/quals-2022/tree/main/sameold "sameold challenge solution"
[2]: https://math.stackexchange.com/a/132383 "Number of elements of a finite field"
[3]: https://math.stackexchange.com/a/1230045 "Order of finite fields is $p^n$"
[4]: https://en.wikipedia.org/wiki/Freshman%27s_dream "Freshman's dream"
[5]: https://kconrad.math.uconn.edu/blurbs/galoistheory/finitefields.pdf "Finite fields"
[6]: https://en.wikipedia.org/wiki/Euler%27s_totient_function#Divisor_sum "Totient function: Divisor sum"
