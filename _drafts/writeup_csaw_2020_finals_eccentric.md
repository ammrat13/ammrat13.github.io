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
    @@\newcommand{\degr}[1]{\deg(#1)}@@
    @@\newcommand{\kernl}[1]{\ker(#1)}@@
    @@\newcommand{\chin}[1]{\Delta #1}@@
    @@\newcommand{\BigO}[1]{\mathcal{O}(#1)}@@
    @@\newcommand{\modulo}[1]{\text{ mod } #1}@@
    @@\newcommand{\modfunc}[2]{\text{mod}(#1,#2)}@@
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
together. So close, in fact, that an 8-bit computer has a hard time telling them
apart. Recall that most arithmetic instructions on an @@n@@-bit computer are
executed modulo @@2^n@@, and both of these numbers are congruent to @@1
\modulo{256}@@.

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
indistinguishable from negative one no matter how many bits of precision we use.
Thus @@-1=\rep{1}@@ under the @@2@@-adic metric. Incidentally, this was the
subject of a [3Blue1Brown video](https://youtu.be/XFDM1ip5HdU). In fact, all the
negative numbers are present, and the trick for negation --- flipping the bits
and adding one --- works as well. Moreover, we get some fractions like
@@\frac{1}{3}=\rep{01}1@@.

Sadly, we don't get everything. We don't get @@\frac{1}{2}@@, @@\frac{1}{4}@@,
@@\frac{1}{6}@@,&nbsp;...&nbsp;. For those, we need the @@2@@-adic rationals
@@\QQ_2@@, which is just like @@\ZZ_2@@ except we allow negative powers of two.
This makes @@\QQ_2@@ a field, unlike @@\ZZ_2@@ which is just a ring. Note that
we can have numbers with expansions stretching infinitely to the left, but not
to the right since they'll just diverge under our new metric. And of course,
what I've said here for @@2@@ can be generalized to any prime number @@p@@. It
doesn't generalize to composites, though, since they lose field structure, in
part because they lack closure. For example, @@\frac{1}{5}\notin\QQ_{10}@@.

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
> it's a member of @@\ZZ_p@@ *not* congruent to zero modulo @@p@@. For example
> in @@\QQ_5@@, @@3@@ and @@-1@@ are units while @@-5@@ and @@\frac{1}{10}@@ are
> not.

> Unofficially, a *@@p@@-adic fraction* is a member of @@\QQ_p\setminus\ZZ_p@@.
> That is, a @@p@@-adic rational which is not an integer. For instance in
> @@\QQ_5@@, @@\frac{1}{5}@@ is a fraction while @@\frac{1}{4}@@ is not.

But, I think the takeaways from this section are two different ways of thinking
about the @@p@@-adics. First, they can be seen as formal power series in the
"variable" @@p@@. Arithmetic is defined in exactly the same way, with carries
being the only exception. Just as two power series are "fairly close" if they
differ by @@\BigO{x^{100}}@@, two @@p@@-adics are "farily close" if they require
@@100@@ digits of precision to distinguish. Many concepts, like degrees and
units, carry over as well. Because of this similarity, the @@p@@-adics actually
play really nicely with formal power series, as we'll see later.

Second and more importantly, @@\ZZ_p@@ can also be thought of as
@@\ZZ/p^\infty\ZZ@@, whatever that's supposed to mean. It contains all the rings
@@\ZZ/p^k\ZZ@@, each embedded in the last @@k@@ digits, so @@\ZZ_p@@ can easily
be used to reason about them. For example, division over @@\ZZ_p@@ (when it
works) looks like inversion modulo @@p@@ when looking at the ones place. In
addition, working over @@\QQ_p@@ often seems to be nicer than working over
finite fields. Thus, one might solve a problem in @@\FF{p}@@ by "lifting" it to
@@\QQ_p@@, solving it there, then "reducing" by taking the result modulo @@p@@
--- by looking at the ones place in the expansion.

---

Let's focus on the reduction step first. Suppose we have some point @@P=(x,y)@@
on the curve @@E\[\QQ_p\]@@, and we'd like to find some corresponding point on
the reduced curve over @@\FF{p}@@. Our first instinct might be to take
everything modulo @@p@@ as described above. I denote this process with an
overbar, abusing notation for points and curves. We get a reduced point
@@\bar{P}=(\bar{x},\bar{y})@@, as well as a reduced curve @@\bar{E}@@ defined by
@@y^2=x^3+\bar{a}x+\bar{b}@@. This'll work as long as all the numbers involved
are @@p@@-adic integers. If @@a@@ or @@b@@ are fractional, we can't do anything
and the process fails. If @@x@@ or @@y@@ are fractional, however, we can
sensibly map @@P@@ to the group identity @@\ecid@@, thus putting it in the
kernel of this reduction homomorphism.

Oh by the way, this mapping @@\rho:E\[\QQ_p\]\to\bar{E}\[\FF{p}\]@@ is a group
homomorphism --- a transformation which respects group addition. It doesn't take
much effort to get the intuition behind this, but the details are somewhat
hairy. We'll use the same notation for elliptic curve operations as
[Wikipedia](https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication).
It's immediately clear that @@\rho@@ respects "most" point additions. As long as
two points (that *don't* map to @@\ecid@@) don't share an @@\bar{x}@@, their
calculation of @@\lambda@@ wouldn't care about this transformation, again since
division in @@\QQ_p@@ when taken modulo @@p@@ looks exactly like division in
@@\FF{p}@@. Even if they do share an @@\bar{x}@@, the computation still works if
they have different @@\bar{y}@@. The numerator in @@\lambda@@ would have degree
zero while the denominator would have degree at least one. The results for
@@\lambda@@, @@x@@, and @@y@@ would be fractional, so the sum would map to
@@\ecid@@, as expected.

Here come the details. Feel free to skip to the last paragraph of this section
if you don't care about them. Otherwise, consider the trickier case when both
points @@P,Q\notin\kernl{\rho}@@ share an @@\bar{x}@@ and a @@\bar{y}@@. We'd
like to show that the resulting @@\lambda@@ is congruent to that of
point-doubling modulo @@p@@. To do this, we'll assume @@x_P-x_Q=p^k\chin{x}@@
and similarly that @@y_P-y_Q=p^k\chin{y}@@, where @@k\geq1@@ and @@\chin{x}@@ is
a unit but @@\chin{y}@@ may not be. However, we do know @@\chin{y}@@ has degree
at least @@-k+1@@ since @@y_P-y_Q@@ has a zero in its ones place. Now we can
solve for @@\chin{y}@@ in
%%
\left(y_Q+p^k\chin{y}\right)^2 = \left(x_Q+p^k\chin{x}\right)^3 + a\left(x_Q+p^k\chin{x}\right) + b.
%%
That looks bad, until we realize we can manipulate it to say
%%
\begin{align\*}
2y_Qp^k\chin{y} &= 3x_Q^2p^k\chin{x} + ap^k\chin{x} + \BigO{p^{k+1}} \nl
2y_Q\chin{y} &= 3x_Q^2\chin{x} + a\chin{x} + \BigO{p} \nl
\chin{y} &= \frac{3x_Q^2 + a}{2y_Q}\chin{x} + \BigO{p}.
\end{align\*}
%%
Finally note that
%%
\begin{align\*}
\lambda &= \frac{p^k\chin{y}}{p^k\chin{x}} = \frac{\chin{y}}{\chin{x}} \nl
&= \frac{3x_Q^2 + a}{2y_Q} + \BigO{p},
\end{align\*}
%%
which, when taken modulo @@p@@, becomes the equation for @@\lambda@@ in
point-doubling, as required.

Now, we just need to handle showing homomorphism in the cases I've been avoiding
up to this point. Namely, those where: 1.&nbsp;exactly one summand is in
@@\kernl{\rho}@@, or 2.&nbsp;both summands are. We can quickly show Case 2 given
Case 1. Suppose @@I,J\in\kernl{\rho}@@, but their sum @@P=I+J@@ is not.
Subtracting @@J@@ from both sides, it follows that @@P-J@@ reduces to @@\ecid@@.
However, using Case 1 and that @@\overline{-J}=-\bar{J}@@ (for all @@J@@ in
fact) we get @@\overline{P-J}=\bar{P}@@ which is not the identity, a
contradiction.

As for Case 1, let @@\bar{I}=\ecid@@ without loss of generality and consider
@@P+I@@. We just need to verify that @@x_{P+I}\equiv x_P\modulo{p}@@ and the
same for @@y@@. To do this, we'll first write down the formula for the
@@x@@-coordinate in point addition:
%%
\begin{align\*}
x_{P+I} &= \lambda^2 - x_I - x_P \nl
&= \left(\frac{y_P-y_I}{x_P-x_I}\right)^2 - x_I - x_P \nl
&= \frac{y_P^2 - 2y_Py_I + y_I^2 - x_P^2x_I + 2x_Px_I^2 - x_I^3}{x_P^2 - 2x_Px_I + x_I^2} - x_P.
\end{align\*}
%%
Again, that looks bad, until we make the following observations: that
@@\degr{x_P}=0@@ and that @@\degr{y_I}=\frac{3}{2}\degr{x_I}@@. The former is
true by the assumption @@P\notin\kernl{\rho}@@. The latter follows directly from
the defining equation of the elliptic curve, combined with the fact @@x_I@@ and
@@y_I@@ are fractional. By considering these degrees, and simplifying @@y_I^2@@,
a lot of the expression vanishes. Letting @@\chin{d}=\degr{y_I}-\degr{x_I}@@, we
get
%%
\begin{align\*}
x_{P+I} &= \frac{-2y_Py_I + 2x_Px_I^2}{x_I^2} - x_P + \BigO{p^{\chin{d}+1}} \nl
&= x_P - \frac{2y_Py_I}{x_I^2} + \BigO{p^{\chin{d}+1}} \nl
&= x_P + \BigO{p}.
\end{align\*}
%%
So the @@x@@-coordinate is correct. What about the @@y@@-coordinate. Again,
we'll write down the formula:
%%
\begin{align\*}
y_{P+I} &= \lambda\cdot(x_P - x_{P+I}) - y_P \nl
&= \frac{y_P-y_I}{x_P-x_I}\cdot\left(\frac{2y_Py_I}{x_I^2} + \BigO{p^{\chin{d}+1}}\right) - y_P \nl
&= \frac{2y_P^2y_I-2y_Py_I^2}{x_Px_I^2-x_I^3} - y_P + \lambda\BigO{p^{\chin{d}+1}}
\end{align\*}
%%
Since @@\degr{\lambda}@@ is just @@\chin{d}@@, we get that
@@\lambda\BigO{p^{\chin{d}+1}}@@ simplifies to @@\BigO{p}@@. Thus
%%
\begin{align\*}
y_{P+I} &= \frac{2y_P^2y_I-2y_Py_I^2}{x_Px_I^2-x_I^3} - y_P + \BigO{p} \nl
&= \frac{2y_Py_I^2}{x_I^3} - y_P + \BigO{p} \nl
&= \frac{2y_Px_I^3}{x_I^3} - y_P + \BigO{p} \nl
&= y_P + \BigO{p}.
\end{align\*}
%%

So we've created a reduction mapping @@\rho:E\[\QQ_p\]\to\bar{E}\[\FF{p}\]@@.
Despite doing so in the most obvious way possible, it turns out this
transformation is quite nice. It's a group homomorphism, which is the most we
can ask for. I guess it goes to show how closely @@\QQ_p@@ is related to
@@\FF{p}@@. Sadly, we won't really use @@\rho@@ in Smart's attack. The most
we'll see is that the points in @@\kernl{\rho}@@ are precisely those with
fractional coordinates, which is true almost by definition. Instead, most of our
time will be spent going the opposite direction. We'll lift our elliptic curve
from @@\FF{p}@@ to @@\QQ_p@@ and do all our math there.

---

So we have some point on a curve @@P\in E\[\FF{p}\]@@ and we'd like to find some
new point @@\hat{P}\in\hat{E}\[\QQ_p\]@@ that reduces to our original point
under the reduction homomorphism described above: @@\rho(\hat{P})=P@@. In some
sense, we'd like to "invert" the reduction by lifting. Of course, there are
(probably) infinitely many @@\hat{P}@@ and @@\hat{E}@@ that'll work --- we just
need to find one. How?

[Hensel's lifting lemma](https://wikipedia.org/wiki/Hensel%27s_lemma) makes this
very easy. Novotney's [paper][2] covers it too. Here's a very roundabout
explanation of what the lemma says, which will hopefully provide some intuition
as to why we're using it. Suppose we have some polynomial @@f@@ and we'd like to
find one of its roots @@n\in\ZZ_p@@. *A priori* we won't know all the digits of
@@n@@, but suppose we know the last @@k@@ digits. Then, Hensel's lemma allows us
to find the next digit in the expansion, so that we now know the last @@k+1@@
digits of @@n@@. This process can then be repeated indefinitely --- we can find
the last @@k+2@@ digits, then @@k+3@@, *ad infinitum*.

How's this useful? Well, by moving everything to the LHS, we can see our
original elliptic curve @@E\[\FF{p}\]@@ as a polynomial @@y^2-x^3-ax-b@@ for
which we know a root @@P=(x,y)@@. Remember that @@\FF{p}@@ is just the ones
place of @@\ZZ_p@@, so we can apply Hensel's lifting lemma here for @@k=1@@. We
can choose one of the variables to treat as a constant, say @@x@@, then
repeatedly lift the other variable to find a root of this polynomial in
@@\ZZ_p\subset\QQ_p@@, and thus a point @@\hat{P}\in\hat{E}\[\QQ_p\]@@.

That's the idea, but there are some details to be mindful of. First, I used
@@a@@ and @@b@@ as the coefficients in the polynomial above. That usually works,
but will cause Smart's attack to fail about @@\frac{1}{p}@@-th of the time. If
the lifted curve defined by @@a@@ and @@b@@ over @@\QQ_p@@ happens to be
isomorphic to that over @@\FF{p}@@, Smart's attack will fail. He actually notes
this in his original [paper][1], and this
[StackExchange thread](https://crypto.stackexchange.com/a/70508) provides a
solution for these "canonical lifts". Note that @@\hat{E}@@ isn't unique --- we
can lift the original curve @@E@@ in infinitely many ways. Before trying to lift
@@P@@ to @@\hat{P}@@, just add a random multiple of @@p@@ to both @@a@@ and
@@b@@. Now, @@\hat{E}@@ will be defined by these new values @@\hat{a}@@ and
@@\hat{b}@@, but will still reduce to our original curve @@E@@ when taken modulo
@@p@@.

Second, I chose to keep @@x@@ constant and lift @@y@@. Usually, either will
work, but not always. As we'll see below, at each iteration of the lift we
require that @@f^\prime@@ is not a multiple of @@p@@. If we iterate with @@x@@
held constant, then @@f^\prime(y)=2y@@ is guaranteed to satisfy that condition
since our initial @@y@@ is not congruent to zero modulo @@p@@. If we hold @@y@@
constant instead, then @@f^\prime(x)=3x^2-\hat{a}@@ which can be a multiple of
@@p@@.

With that out of the way, let's look at the surprisingly simple proof. But
first, we need to clarify what exactly we're trying to prove. The formulation
from three paragraphs ago isn't exactly nice to work with, but we can make it
so. Suppose we have the last @@k@@ digits of @@n@@, a root of @@f@@ in
@@\ZZ_p@@. This is equivalent to saying we have a root @@r@@ of @@f@@ modulo
@@p^k@@. We'd like to find the next digit in the expansion of @@n@@ --- some
root @@s@@ of @@f@@ modulo @@p^{k+1}@@. Moreover, we require that @@s\equiv
r\modulo{p^k}@@. The last @@k@@ digits are set once they're "discovered", and we
never go back and change them.

This formulation is much easier to work with. Now we just need to solve for
@@s@@. Though, we do need one more trick. We start by
[Taylor-expanding](https://en.wikipedia.org/wiki/Taylor_series) @@f@@ about
@@r@@. This is why we require @@f@@ to be a polynomial: they have finite
Taylor series. So we expand
%%
\begin{align\*}
f(s) &\equiv \sum_{i=0}^N \frac{f^{(i)}(r)}{i!} (s-r)^i &\mod p^{k+1} &\nl
&\equiv f(r) + f^\prime(r)\cdot(s-r) + \sum_{i=2}^N \frac{f^{(i)}(s)}{i!}(s-r)^i &\mod p^{k+1} &.
\end{align\*}
%%
Since we require @@s-r\equiv0\modulo{p^k}@@, all the terms in the sum will be
divisible by @@p^{2k}@@ and will thus vanish. We also require that
@@f(s)\equiv0\modulo{p^{k+1}}@@, eliminating the RHS. Now we solve
%%
\begin{align\*}
0 &\equiv f(r) + f^\prime(r)\cdot(s-r) &\mod p^{k+1} &\nl
s &\equiv r + f(r) \cdot f^\prime(r)^{-1} &\mod p^{k+1} &.
\end{align\*}
%%

---



[1]: </assets/2021/01/15/pdf/Smart.pdf> "The Discrete Logarithm Problem on Elliptic Curves of Trace One"
[2]: </assets/2021/01/15/pdf/Novotney.pdf> "Weak Curves In Elliptic Curve Cryptography"
