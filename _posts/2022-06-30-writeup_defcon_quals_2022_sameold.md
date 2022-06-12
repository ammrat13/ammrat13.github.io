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


#### Introduction

##### How CRCs Work

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
        1 + x + x^2 + x^4  + x^5 \nl
        &+ x^7 + x^8 + x^{10} + x^{11} \nl
        &+ x^{12} + x^{16} + x^{22} + x^{23} \nl
        &+ x^{26} + x^{32},
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

##### The Choice of π

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

> *Theorem (from [MathOverflow][2]):* A finite field @@F@@ has order @@\|F\| =
> p^n@@ for @@p@@ prime.

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

This is not the only proof of this theorem. Another, also from
[MathOverflow][3], uses Bézout's identity to show by contradiction that the
field would have zero divisors otherwise.


#### Approach

With all the introductory material out of the way, we can start tackling the
actual problem. As a reminder, we want to find a string that starts with a
specific substring (say `DC`) whose CRC-32 is a particular value. I'll actually
restrict the search space a bit more. I'll look for a string that starts with
`DC` then contains exactly @@\ell@@ characters, each either @@c@@ or @@d@@.
Originally I chose `0` and `1` because their ASCII codes differ by @@1@@, but
that's not required. Just let @@\delta = d - c@@. Now compute @@p@@ the CRC-32
of the original message: `DC` followed by the character @@c@@ repeated @@\ell@@
times. Of course, this will likely differ from the target polynomial @@t@@, but
we can change the message by substituting some instances of @@c@@ with @@d@@ ---
by adding instances of @@\delta@@ shifted by the appropriate amount.

Specifically, we wish to solve for @@\alpha_i \in \FF_2@@ in
%%\begin{equation\*}
    x^{32} \cdot \sum\_{i=0}^{\ell-1} \alpha\_i \cdot x^{8i}\delta = t - p.
\end{equation\*}%%
The @@x^{8i}@@ term in the sum shifts the correction into the correct place. For
example, setting @@i=0@@ will shift the correction to the last character in the
string, setting @@i=1@@ will be the second to last, and so on. Choosing
@@\alpha_i=1@@ means to substitute that character into @@d@@, while choosing it
zero means to leave it as @@c@@. The extra shift of @@x^{32}@@ corresponds to
the message being multiplied by that before taking the remainder. Ultimately,
changing the message leads to predictable effects on the output --- if you add
something to the input, you just add the same thing to the output too. So, we
take a look at the difference and try to solve for the required change.

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


#### Failure Resistance

So when does that fail? Clearly, when @@\ell@@ is too small, there aren't enough
vectors for a baisis and thus too few for a spanning set. The least you can
possibly get away with is @@\ell = \dim\FF_{2^{32}} = 32@@. In some cases,
that's also sufficient.

##### On "2<sup>*w*</sup>-Periodic" Bases

Specifically, when the attacker can choose to substitute individual words
independently of each other, assuming a word's length is a power of two @@2^w@@,
@@\ell=32@@ is sufficient. This is because going through the above process
results in the vectors @@\vect{v}\_i@@ being @@x^{2^w i}@@. I'll prove that this
set is a basis iff the set of @@x^i@@ is a basis, which it obviously is for @@i
= 0, \cdots, 31@@.

> *Theorem:* The set @@B = \\{b_0,\cdots,b_{\ell-1}\\}@@ of elements in
> @@\FF_{p^n}@@ spans its field iff the set @@B^p =
> \\{b_0^p,\cdots,b_{\ell-1}^p\\}@@ does.

For the "only if" direction, observe that if @@v@@ can be expressed as a linear
combination of basis elements in @@B@@, then
%%\begin{align\*}
    v^p
        &= \left( \sum\_{i=0}^{\ell-1} \alpha_i b_i \right)^p \nl
        &= \sum\_{i=0}^{\ell-1} \alpha_i^p b_i^p \nl
\end{align\*}%%
by Freshman's Dream. Since the Frobenius endomorphism is bijective over finite
fields, one can make any target vector out of elements of @@B^p@@ by making its
preimage using @@B@@ then raising it to the @@p@@-th power.

For the "if" direction, we use a similar argument. To construct a target element
@@v@@, construct @@v^p@@ using elements of @@B^p@@, then construct @@v@@ by
taking the @@p@@-th root of all the coefficients and using them on the basis
@@B@@. Again, doing this is well defined since the Frobenius endomorphism is
bijective over @@\FF_{p^n}@@. □

> *Corollary:* Same as the above theorem, but with the set @@B^{p^k} =
> \\{b_0^{p^k},\cdots,b_{\ell-1}^{p^k}\\}@@ instead of @@B^p@@, where @@k@@ is
> an arbitrary natural number.

Apply the above theorem @@k@@ times. □

The result we set out to prove is this corollary with @@p=2@@, @@k=w@@, and
@@b_i = x^i@@.

##### On *n* Consecutive Powers of Primitive Elements

The result in the previous section was agnostic to our choice of @@b_i@@.
However, our basis is usually quite "nice". For example, in the last section, we
chose the standard basis @@\\{1,x,x^2,\cdots,x^{31}\\}@@. Moreover, since
multiplication by a constant is a linear automorphism, we could have chosen any
32 consecutive powers of @@x@@. These same results hold for other elements too.

In particular, it holds for primitive elements of @@\FF_{2^{32}}@@. This fact
could've been used to prove the result in the last section. Unfortunately, it
has limited utility since it requires consecutive powers of that element, which
might be hard to guarantee for non-powers of two.

> *Lemma:* If the minimal polynomial of @@g \in \FF_{p^n}@@ has degree at least
> (so, exactly) @@n@@, then the set @@\\{1,g,g^2,\cdots,g^{n-1}\\}@@ is linearly
> independent and therefore a basis for @@\FF_{p^n}@@.

I'll prove by contraposition. Suppose there were some constants @@\alpha_i \in
\FF_p@@, not all zero, such that
%%\begin{equation\*}
    \sum\_{i=0}^{n-1} \alpha_i g^i = 0.
\end{equation\*}%%
Then by definition @@g@@ satisfies this polynomial nonzero of degree at most
@@n-1@@, and its minimal polynomial must have degree less than or equal to that.
□

> *Theorem:* If @@g \in \FF_{p^n}@@ is primitive, then its minimal polynomial
> has degree at least @@n@@.

Again, I'll proceed by contraposition. Without loss of generality, suppose @@g@@
satisfies some monic polynomial of degree @@d < n@@. We can move all the lower
degree terms to one side to get
%%\begin{equation\*}
    g^d = \sum\_{i=0}^{d-1} \alpha_i g^i.
\end{equation\*}%%
Then, all subsequent powers of @@g@@ can be expressed as a linear combination of
@@\\{1,g,g^2,\cdots,g^{d-1}\\}@@. Just keep substituting this identity until all
instances of @@g@@ have power at most @@d-1@@. Therefore, the set of elements
@@\langle g\rangle \subseteq \FF_{p^n}^\times@@ that can be reached via powers
of @@g@@ has at most @@p^d - 1@@ elements. We get @@p@@ choices for each
coefficient, minus one because zero can't be reached. This is strictly fewer
elements than are contained in the whole field, so @@g@@ cannot be primitive. □

> *Corollary:* If @@g \in \FF_{p^n}@@ is primitive, any @@n@@ consecutive powers
> of @@g@@ are linearly independent and therefore form a basis.

To show @@\\{1,g,g^2,\cdots,g^n\\}@@ is linearly independent, simply compose the
above theorem and the lemma before it. As for any @@n@@ consecutive powers, with
@@g^d@@ being the lowest power among them, linearly transform this basis via
multiplication with @@g^d@@. □


#### Future Work

Characterizing powers of two and consecutive powers is relatively easy. However,
real-world situations might not afford this structure. Attackers might only be
able to choose bits at irregular positions, and the above guarantees about how
many choices are needed to span might not hold. Future work might focus on
getting a tighter bound on which and how many elements are needed to guarantee a
spanning set.

Additionally, I assumed for simplicity that the attacker would choose once per
byte --- either @@c@@ or @@d@@. They usually have more choices than that though,
and it would be good to take advantage of them. By introducing @@K@@ independent
displacement vectors @@\delta_k@@, it's possible to use an alphabet @@\Sigma@@
that has @@2^K@@ characters. In that case, you need to solve
%%\begin{align\*}
    x^{32} \cdot \sum\_{i=0}^{\ell-1}\sum_{k=1}^K \alpha_{i,k} \cdot x^{8i} \delta_k &= t - p \nl
    \sum\_{i=0}^{\ell-1}\sum_{k=1}^K \alpha_{i,k} \cdot x^{8i} \delta_k &= \frac{t - p}{x^{32}}.
\end{align\*}%%
Additionally, @@\Sigma@@ has to be an affine space over @@\FF_2@@, otherwise it
wouldn't be possible to safely take linear combinations of the vectors
@@\delta_k@@ as we require. Finally, while the bound on @@\ell@@ established
above still technically holds, in the case of multiple displacement vectors,
it's clearly very loose. Intuitively, we'd expect it to be close to
@@\frac{32}{K}@@. Future work could try to relax these restrictions and get a
tighter bound on the number of bytes needed.


#### Worked Example

Suppose I want to find a string that starts with `DC`, only contains the letters
`G` and `T` after that, and whose CRC-32 is the same as the string `the`. I
compute the target CRC to be `0x3C456DE6`, and undoing the post-processing by
reversing the bits and NOTing gives
%%\begin{align\*}
    t =&\,
        1 + x + x^6 + x^7 + x^8 \nl
        &+ x^{10} + x^{11} + x^{12} + x^{14} \nl
        &+ x^{16} + x^{19} + x^{22} \nl
        &+ x^{27} + x^{28} + x^{31}.
\end{align\*}%%
Taking @@\ell=32@@ gives the original message `DCG...G`, and computing its CRC
gives `0xBAAB7C95`, or
%%\begin{align\*}
    p =&\,
        x + x^5 + x^7 + x^9 + x^{11} \nl
        &+ x^{13} + x^{16} + x^{22} + x^{23} \nl
        &+ x^{25} + x^{26} + x^{28} + x^{30}.
\end{align\*}%%
This gives a difference of
%%\begin{align\*}
    t-p =&\,
        1 + x^5 + x^6 + x^8 + x^9 \nl
        &+ x^{10} + x^{12} + x^{13} + x^{14} \nl
        &+ x^{19} + x^{23} + x^{25} + x^{26} \nl
        &+ x^{27} + x^{30} + x^{31}.
\end{align\*}%%
The characters we can use have ASCII codes `0x47` and `0x54` respectively.
Remembering that the bytes will be reflected on the input, the polynomials are
%%\begin{align\*}
    c &= x + x^5 + x^6 + x^7 \nl
    d &= x + x^3 + x^5 \nl
    \delta &= x^3 + x^6 + x^7.
\end{align\*}%%
I then compute
%%\begin{align\*}
    \vect{y} =&\, \frac{t-p}{x^{32}\delta} \nl
        =&\, 1 + x + x^4 + x^6 + x^7 \nl
        &+ x^9 + x^{18} + x^{19} + x^{21} \nl
        &+ x^{22} + x^{24} + x^{25} + x^{26} \nl
        &+ x^{27} + x^{29} + x^{30}.
\end{align\*}%%
Solving gives
%%\begin{align\*}
    \alpha = [\,\,
        &0, 1, 1, 0, 0, 0, 1, 1, \nl
        &1, 1, 1, 1, 1, 1, 0, 1, \nl
        &0, 1, 1, 1, 1, 0, 1, 1, \nl
        &1, 1, 1, 0, 1, 1, 0, 0 \,\,],
\end{align\*}%%
which corresponds to the message `DCGGTTGTTTTTGTTTTGTGTTTTTTTTGGGTTG`.


#### Appendix: Previous Results

This section lists facts I used to prove my main results.

> *Lemma ([Conrad § 1.6][5]):* The multiplicative group @@F^\times@@ of a
> finite field @@F@@ is cyclic.

Remember that, over fields, polynomials can have at most as many roots as their
degree. If it has a root @@r@@, a factor of @@(X-r)@@ can be divided out. This
can be repeated until the degree of the polynomial is reduced to zero. We can
use that fact to show the following: if @@F^\times@@ has at least one element of
order @@d@@, then it has exactly @@\varphi(d)@@ of them. Let @@g@@ be an element
such that @@g^d@@ is the lowest power of @@g@@ equaling the group identity
@@1@@. Every element @@X@@ in the group it generates @@\langle g\rangle@@ will
satisfy @@X^d - 1 = 0@@. There are @@d@@ such elements in this subgroup, so
we've found all the possible roots of that polynomial. To find objects in
@@F^\times@@ of order exactly @@d@@, it suffices to restrict our search to
@@\langle g\rangle@@. By basic number theory, out of the @@d@@ elements in that
cycle with order dividing @@d@@, exactly @@\varphi(d)@@ of them will have order
exactly @@d@@.

Define @@\text{NumElementsOfOrder}(d)@@ to be the number of elements in
@@F^\times@@ such that their @@d@@-th power is their smallest power equaling
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

This result isn't strictly needed, but remembering that the underlying group is
cyclic may make some of the later results more intuitive. Also, the methods used
are just cool, so I wanted to include it.

> *Lemma ([Freshman's Dream][4]):* Over a ring @@R@@ of prime characteristic
> @@p@@, any @@a,b \in R@@ satisfy @@(a+b)^p = a^p+b^p@@.

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

> *Lemma ([Frobenius Endomorphism][8]):* Over the finite field @@\FF_{p^n}@@,
> the map @@X \mapsto X^p@@ is an automorphism --- an isomorphism from
> @@\FF_{p^n}@@ to itself.

It can easily be verified that both the additive and multiplicative identities
are fixed by the function @@X^p@@. In fact, [Fermat's Little Theorem][7] shows
that all of @@\FF_p@@ remains fixed. Freshman's Dream shows that this function
respects addition. Powers trivially respect multiplication, so @@X^p@@ is an
endomorphism --- a homorphism from @@\FF_{p^n}@@ to itself.

All that remains is to show that @@X^p@@ is injective and therefore bijective.
[This MathOverflow post][9] does that in one line, noting that @@\ker X^p =
\\{0\\}@@ since that's the only proper ideal in a finite field. In fact, the
same logic shows that any ring endomorphism over @@\FF_{p^n}@@ is an
automorphism.

I'll do it a different way though. Suppose for the sake of contradiction that
@@X^p@@ is not injective, so it maps two different elements of
@@\FF_{p^n}^\times@@ to the same thing. This is equivalent to saying that it
maps some @@g \neq 1@@ to the identity. That element @@g@@ satisfies @@X^p - 1 =
0@@, as do all the other elements of @@\langle g\rangle@@. Since that subgroup
has @@p@@ elements, we've found all solutions to @@X^p = 1@@, which is @@\ker
X^p@@ by definition. Recall that the size of a subgroup divides the size of the
whole group, so we get @@p@@ divides @@p^n-1@@, which is false. □


[1]: https://github.com/Nautilus-Institute/quals-2022/tree/main/sameold "sameold challenge solution"
[2]: https://math.stackexchange.com/a/132383 "Number of elements of a finite field"
[3]: https://math.stackexchange.com/a/1230045 "Order of finite fields is $p^n$"
[4]: https://en.wikipedia.org/wiki/Freshman%27s_dream "Freshman's dream"
[5]: https://kconrad.math.uconn.edu/blurbs/galoistheory/finitefields.pdf "Finite fields"
[6]: https://en.wikipedia.org/wiki/Euler%27s_totient_function#Divisor_sum "Totient function: Divisor sum"
[7]: https://en.wikipedia.org/wiki/Fermat's_little_theorem "Fermat's little theorem"
[8]: https://en.wikipedia.org/wiki/Frobenius_endomorphism "Frobenius endomorphism"
[9]: https://math.stackexchange.com/a/2485017 "When is the Frobenius endomorphism an automorphism?"
