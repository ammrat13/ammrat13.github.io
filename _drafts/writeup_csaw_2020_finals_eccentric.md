---
title: "CSAW CTF 2020 Finals Writeup: Eccentric"
libs: [mathjax]
---

<div class="mathjaxDeclarations">
    @@\newcommand{\nl}{\\}@@
    @@\newcommand{\FF}[1]{\mathbb{F}_{#1}}@@
    @@\newcommand{\ZZ}{\mathbb{Z}}@@
    @@\newcommand{\QQ}{\mathbb{Q}}@@
    @@\newcommand{\RR}{\mathbb{R}}@@
    @@\newcommand{\ecid}{\mathcal{O}}@@
    @@\newcommand{\hex}[1]{\texttt{0x#1}}@@
    @@\newcommand{\rep}[1]{\overline{#1}}@@
    @@\newcommand{\chin}[1]{\Delta #1}@@
    @@\newcommand{\BigO}[1]{\mathcal{O}(#1)}@@
    @@\newcommand{\modulo}[1]{\text{ mod } #1}@@
</div>

I was a finalist for [CSAW CTF 2020](https://csaw.io). I was on the Mad H@tter's
team, and I swept the cryptography challenges. They were all interesting, and I
felt I'd write down some of my thoughts on them. Curiously, the question ranked
the easiest was the one I found most difficult. So, I'm devoting this entire
post to it.

---

> **Eccentric (100 Points)**
>
> 'Don't worry, I'm using ECC.' - every crypto script kiddy ever
>
> * `nc crypto.chal.csaw.io 5002`
> * [`handout.txt`](/assets/2021/01/15/challenge/handout.txt)

The handout specifies a finite field of prime order @@\FF{p}@@, as well as an
elliptic curve @@E@@ over it with the form @@y^2 = x^3 + ax + b@@. It also gives
us two points on the curve @@P = dG@@, and asks us to solve for the integer
@@d@@.

This is a [discrete-log problem](https://wikipedia.org/wiki/Discrete_logarithm),
which is hard to solve in general. In CTFs, however, there is generally some
additional structure in place to make the problem easier. For a challenge like
this, they might use a weak elliptic curve --- a curve in some class for which
there are known attacks. The challenge is often just finding and implementing
that exploit, hence the low point value.

Indeed, that is the case here. Plugging @@E@@ into SageMath gives that the
number of points on the elliptic curve @@\\#E@@ is equal to @@p@@.
[Wikipedia](https://wikipedia.org/wiki/Elliptic-curve_cryptography#Domain_parameters)
lists such curves as insecure, providing some references but sadly not
describing any attacks against them. It does, however, link to [a paper][1] by
Nigel Smart. Moreover, Smart's attack shows up within the first few results of
Googling attacks on this class of curves.

I found a [StackExchange thread](https://crypto.stackexchange.com/q/71525) which
linked to [a paper][2] by Novotney surveying weak elliptic curves. It had some
SageMath code in the back implementing Smart's attack. During the competition, I
just copied the program, and it worked. But, I didn't understand how. The math
is actually pretty involved, and it took me about a month of reading and
re-reading to gain some deeper understanding of it.

---

The first piece of the attack has to do with the @@p@@-adic numbers. I've
thought a lot about how to briefly summarize them, and what follows is my best
attempt.

Consider the numbers @@1=\hex{0001}@@ and @@257=\hex{0101}@@. They're very far
apart in the conventional sense, but in another sense they're very close
together. So close, in fact, that an 8-bit computer can't tell them apart.
Recall that all math on an @@n@@-bit computer is done modulo @@2^n@@, and as
such these numbers would both be congruent to @@1 \modulo{256}@@.

In some sense, eight bits of "precision" isn't enough - you'd need nine to
distinguish the two numbers. But it goes deeper. You'd need thirteen bits of
precision to distinguish @@1@@ and @@4097=\hex{1001}@@. In this sense, @@1@@ is
closer to @@4097@@ than it is to @@257@@, and @@257@@ is just as far away from
@@1@@ as it is from @@4097@@.

What I've just described is the @@2@@-adic metric. Starting from the *least*
significant digit, how many bits of "precision" do we need to distinguish two
numbers? With this metric, we also get the @@2@@-adic integers @@\ZZ_2@@, which
are all the numbers that can be expressed as a sum of *non-negative* integer
powers of two, or all the "binary" integers. Even though @@\ZZ_2@@ contains many
of the expected values --- all natural numbers for instance, it also contains
many unexpected numbers. For example, @@-1\in\ZZ_2@@. How? Note that in two's
complement, we can express @@-1@@ as all ones. If we take ones stretching all
the way to the left: @@\rep{1}=\cdots111@@, we should get a number
indistinguishable from @@-1@@ no matter how many bits of precision we use. Thus
@@-1=\rep{1}@@ under the @@2@@-adic metric. In fact, all the negative numbers
are present, and the trick of flipping the bits and adding one works as well.
Moreover, we get some fractions like @@\frac{1}{3}=\rep{01}1@@. Incidentally,
this was the subject of a [3Blue1Brown video](https://youtu.be/XFDM1ip5HdU).

Sadly, we don't get everything. We don't get @@\frac{1}{2}@@, @@\frac{1}{4}@@,
@@\frac{1}{6}@@,&nbsp;...&nbsp;. For those, we need the @@2@@-adic rationals
@@\QQ_2@@, which is just like @@\ZZ_2@@ except we allow negative powers of
@@2@@. This makes @@\QQ_2@@ a field, unlike @@\ZZ_2@@ which was just a ring.
Note that we can have numbers with expansions stretching infinitely to the left,
but not to the right since they'll just diverge under our new metric. And of
course, what I've said here for @@2@@ can be generalized to any prime number
@@p@@. It doesn't generalize to composites, though, since they lose field
structure, in part because they lack closure. For example,
@@\frac{1}{5}\notin\QQ_{10}@@.

I've glossed over a lot of details here. For instance, the distance between two
numbers is not just how many bits you need to distinguish them @@b@@, but rather
@@p^{-b}@@. Also, I didn't explain in detail how computations work. Addition is
done term-by-term with carries, and we know to negate and thus subtract.
However, multiplication is a bit more complicated, requiring an infinite FOIL as
with power series, and division is reverse-engineering multiplication again like
power series.

I also still need to give some definitions:

> The *degree*, or more commonly *order*, of a @@p@@-adic number is the lowest
> power of @@p@@ that shows up in its expansion. For instance in @@\QQ_5@@, the
> degree of @@3@@ is zero, that of @@5@@ is one, and that of @@\frac{1}{50}@@ is
> negative two.

> A *@@p@@-adic unit* is a @@p@@-adic number with degree zero. Alternatively,
> it's a member of @@\ZZ_p@@ congruent to zero modulo @@p@@.

But, the main takeaway is that @@\ZZ_p@@ can be thought of as
@@\ZZ/p^\infty\ZZ@@, whatever that's supposed to mean. It has all the rings
@@\ZZ/p^k\ZZ@@ inside of it, and thus can be used to reason about them. For
example, division over @@\ZZ_p@@ (when it works) looks like inversion modulo
@@p@@ when looking at the ones place. In addition, working over @@\QQ_p@@ often
seems to be nicer than working over finite fields. Thus, one might solve a
problem in @@\FF{p}@@ by "lifting" it to @@\QQ_p@@, solving it there, then
"reducing" by taking the result modulo @@p@@.

---

Let's focus on the reduction step first. It won't be that important for the
actual attack, so feel free to skip this section. Otherwise, suppose we have
some point @@R=(x,y)@@ on the curve @@E\[\QQ_p\]@@, and we'd like to find some
corresponding point @@\bar{R}@@ over the curve @@\bar{E}\[\FF{p}\]@@. Our first
instinct might be to take everything modulo @@p@@ as described above, just
looking at the ones digit. I denote this process with an overbar. We get a
reduced point @@\bar{R}=(\bar{x},\bar{y})@@, as well as a reduced curve
@@y^2=x^3+\bar{a}x+\bar{b}@@. This'll work as long as all the numbers are
@@p@@-adic integers. If @@a@@ or @@b@@ are fractional, we can't do anything and
the process fails. If @@x@@ or @@y@@ are, however, we can sensibly map the point
to the group identity @@\ecid@@.

It turns out that this mapping is a group homomorphism --- a transformation
which respects group addition. It doesn't take much effort to see this, but
still more than you'd think. We'll use the same notation for elliptic curve
point addition as
[Wikipedia](https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication).
It's immediately clear that this reduction mapping respects "most" point
additions. As long as two points (that don't map to @@\ecid@@) don't share an
@@\bar{x}@@, their calculation of @@\lambda@@ doesn't care about this
transformation, again since division in @@\QQ_p@@ when taken modulo @@p@@ looks
like division in @@\FF{p}@@. Even if they share an @@\bar{x}@@, the computation
still works if they have different @@\bar{y}@@. The numerator in @@\lambda@@
would have degree zero while the denominator would have degree at least one. The
results for @@\lambda@@, @@x@@, and @@y@@ wouldn't be in @@\ZZ_p@@, so the sum
would map to @@\ecid@@, as expected.

Things become trickier when both points @@\bar{R},\bar{S}\neq\ecid@@ share an
@@\bar{x}@@ and a @@\bar{y}@@. We'd like to show that the resulting @@\lambda@@
is congruent to that of point-doubling modulo @@p@@. To do this, we'll assume
@@x_R-x_S=p^k\chin{x}@@ and similarly that @@y_R-y_S=p^k\chin{y}@@, where
@@k\geq1@@ and @@\chin{x}@@ is a unit but @@\chin{y}@@ may not be. However, we
do know @@\chin{y}@@ has degree at least @@-k+1@@ since @@y_R-y_S@@ has a zero
in its ones place. Now we can solve for @@\chin{y}@@ in
%%
\left(y_S+p^k\chin{y}\right)^2 = \left(x_S+p^k\chin{x}\right)^3 + a\left(x_S+p^k\chin{x}\right) + b.
%%
That looks bad, until we realize we can manipulate it to say
%%
\begin{align\*}
2y_Sp^k\chin{y} &= 3x_S^2p^k\chin{x} + ap^k\chin{x} + \BigO{p^{k+1}} \nl
2y_S\chin{y} &= 3x_S^2\chin{x} + a\chin{x} + \BigO{p} \nl
\chin{y} &= \frac{3x_S^2 + a}{2y_S}\chin{x} + \BigO{p}.
\end{align\*}
%%
Finally note that
%%
\begin{align\*}
\lambda &= \frac{p^k\chin{y}}{p^k\chin{x}} = \frac{\chin{y}}{\chin{x}} \nl
&= \frac{3x_S^2 + a}{2y_S} + \BigO{p},
\end{align\*}
%%
which becomes the equation for @@\lambda@@ in point-doubling when taken modulo
@@p@@, as required.

Now, we just need to handle the cases where: 1) exactly one summand maps to the
identity under reduction, and 2) both summands map to @@\ecid@@. We can quickly
show Case 2 given Case 1. Suppose @@\bar{I}=\bar{J}=\ecid@@, but their sum
@@R=I+J@@ does not reduce to the identity. Then it follows that @@R-J@@ reduces
to @@\ecid@@. However, using Case 1 and that @@\overline{-J}=-\bar{J}@@, for all
@@J@@ in fact, we get that @@\overline{R-J}=\bar{R}@@ which is not the identity,
a contradiction.

As for Case 1, let @@\bar{I}=\ecid@@ and consider @@R+I@@.



[1]: </assets/2021/01/15/pdf/Smart.pdf> "The Discrete Logarithm Problem on Elliptic Curves of Trace One"
[2]: </assets/2021/01/15/pdf/Novotney.pdf> "Weak Curves In Elliptic Curve Cryptography"
