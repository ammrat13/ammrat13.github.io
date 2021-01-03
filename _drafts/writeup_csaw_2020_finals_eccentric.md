---
title: "CSAW CTF 2020 Finals Writeup: Eccentric"
libs: [mathjax]
---

<div class="mathjaxDeclarations">
    @@\newcommand{\FF}[1]{\mathbb{F}_{#1}}@@
    @@\newcommand{\ZZ}{\mathbb{Z}}@@
    @@\newcommand{\QQ}{\mathbb{Q}}@@
    @@\newcommand{\RR}{\mathbb{R}}@@
    @@\newcommand{\hex}[1]{\texttt{0x#1}}@@
    @@\newcommand{\rep}[1]{\overline{#1}}@@
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

But, the main takeaway is that @@\ZZ_p@@ can be thought of as
@@\ZZ/p^\infty\ZZ@@, whatever that's supposed to mean. It has all the rings
@@\ZZ/p^k\ZZ@@ inside of it, and thus can be used to reason about them. For
example, division over @@\ZZ_p@@ (when it works) looks like inversion modulo
@@p@@ when looking at the ones place. In addition, working over @@\QQ_p@@ often
seems to be nicer than working over finite fields. Thus, one might solve a
problem in @@\FF{p}@@ by "lifting" it to @@\QQ_p@@, solving it there, then
transfering back by looking at the ones place --- taking the result it modulo
@@p@@.

It's also worth noting that the @@p@@-adics can be thought of as formal power
series in the "variable" @@p@@. Their addition, multiplication, and division
laws are very similar, with the @@p@@-adics just having to deal with carries. We
even see that @@\frac{1}{p}\notin\ZZ_p@@, just as @@\frac{1}{x}@@ can't be
expressed as a formal power series and must be treated separately. This
similarity means they sometimes play nicely with each other, which we'll see
later.



[1]: </assets/2021/01/15/pdf/Smart.pdf> "The Discrete Logarithm Problem on Elliptic Curves of Trace One"
[2]: </assets/2021/01/15/pdf/Novotney.pdf> "Weak Curves In Elliptic Curve Cryptography"
