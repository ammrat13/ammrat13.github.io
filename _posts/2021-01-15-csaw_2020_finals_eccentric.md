---
title: "CSAW CTF 2020 Finals: Eccentric"
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

I was a finalist for [CSAW CTF 2020](https://csaw.io). I was on the Mad H@tters'
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
elliptic curve @@E@@ over it of the form @@y^2 = x^3 + ax + b@@. It also gives
us two points on the curve @@P = dG@@, and asks us to solve for the integer
@@d@@.

This is a [discrete-log problem](https://wikipedia.org/wiki/Discrete_logarithm),
which is hard to solve in general. In CTFs, however, there's generally some
additional structure in place to make the problem easier. For a challenge like
this, they might use a weak elliptic curve --- a curve in some class for which
there are known attacks. The challenge is often just finding the exploit, hence
the low point value.

Indeed, that is the case here. Plugging @@E@@ into SageMath gives that the
number of points on the elliptic curve @@\\#E@@ is equal to @@p@@.
[Wikipedia](https://wikipedia.org/wiki/Elliptic-curve_cryptography#Domain_parameters)
lists such curves as insecure, providing some references but sadly not
describing any attacks against them. It does, however, link to [a paper][1] by
Nigel Smart. Moreover, Smart's attack shows up within the first few results of
Googling attacks on this class of curves.

I found a [StackExchange thread](https://crypto.stackexchange.com/q/71525) which
linked to [a paper][2] by Novotney surveying weak elliptic curves. It had some
SageMath code at the back implementing Smart's attack. During the competition, I
just copied the program, and it worked. But I didn't understand how. The math
is actually pretty involved, and it took me about a month of reading and
re-reading to gain some deeper understanding of it.

---

The first piece of the attack has to do with @@p@@-adic numbers. I've thought a
lot about how to briefly summarize them, and what follows is my best attempt.

Consider the numbers @@1=\hex{0001}@@ and @@257=\hex{0101}@@. They're far apart
in the conventional sense, but in another sense they're very close together. So
close, in fact, that an 8-bit computer has a hard time telling them apart.
Recall that most arithmetic instructions on an @@n@@-bit computer are executed
modulo @@2^n@@, and both of these numbers are congruent to @@1\modulo{256}@@.

In some sense, eight bits of "precision" isn't enough - you'd need nine to
distinguish the two numbers. But it goes deeper. You'd need thirteen bits of
precision to distinguish @@1@@ and @@4097=\hex{1001}@@. In this sense, @@1@@ is
closer to @@4097@@ than it is to @@257@@, and @@257@@ is just as far away from
@@1@@ as it is from @@4097@@.

What I've just described is the @@2@@-adic metric. Starting from the *least*
significant digit, how many bits of "precision" do we need to distinguish two
numbers? With this metric, we also get the @@2@@-adic integers @@\ZZ_2@@, which
are all the numbers that can be expressed as a sum of *non-negative* powers of
two, or all the "binary" integers. Even though @@\ZZ_2@@ contains many of the
expected values --- all the natural numbers for instance, it also contains many
unexpected numbers. For example, @@-1\in\ZZ_2@@. How? Note that in two's
complement, we can express @@-1@@ as all ones. If we take ones stretching all
the way to the left: @@\rep{1}=\cdots111@@, we should get a number
indistinguishable from negative one no matter how many bits of precision we use.
Thus @@-1=\rep{1}@@ under the @@2@@-adic metric. Incidentally, this was the
subject of a [3Blue1Brown video](https://youtu.be/XFDM1ip5HdU). In fact, all the
negative numbers are present, and the trick for negation --- flipping the bits
and adding one --- works as well. We even get some fractions like
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
However, multiplication is a bit more complicated, needing an infinite FOIL as
with power series, and division requires reverse-engineering multiplication
again like power series.

I also still need to give some definitions:

> The *degree*, or more commonly *order*, of a @@p@@-adic number is the lowest
> power of @@p@@ that shows up in its expansion. For instance in @@\QQ_5@@, the
> degree of @@3@@ is zero, that of @@5@@ is one, and that of @@\frac{1}{50}@@ is
> negative two.

> A *@@p@@-adic unit* is a @@p@@-adic number with degree zero. Alternatively,
> it's a member of @@\ZZ_p@@ not congruent to zero modulo @@p@@. For example in
> @@\QQ_5@@, @@3@@ and @@-1@@ are units while @@-5@@ and @@\frac{1}{10}@@ are
> not.

> Unofficially, a *@@p@@-adic fraction* is a member of @@\QQ_p\setminus\ZZ_p@@.
> That is, a @@p@@-adic rational which is not an integer. For instance in
> @@\QQ_5@@, @@\frac{1}{5}@@ is a fraction while @@\frac{1}{4}@@ is not.

But, I think the main takeaways from this section are two different ways of
thinking about the @@p@@-adics. First, they can be seen as formal power series
in the "variable" @@p@@. Arithmetic is defined in exactly the same way, with
carries being the only exception. Just as two power series are "fairly close" if
they differ by @@\BigO{x^{100}}@@, two @@p@@-adics are "farily close" if they
require @@100@@ digits of precision to distinguish. Many concepts, like degrees
and units, carry over as well. Because of this similarity, the @@p@@-adics
actually play really nicely with formal power series, as we'll see later.

Second and more importantly, @@\ZZ_p@@ can be thought of as @@\ZZ/p^\infty\ZZ@@,
whatever that's supposed to mean. It contains all the rings @@\ZZ/p^k\ZZ@@, each
embedded in the last @@k@@ digits, so @@\ZZ_p@@ can easily be used to reason
about them. For example, division over @@\ZZ_p@@ (when it works) looks like
inversion modulo @@p@@ when looking at the ones digit. In addition, working over
@@\QQ_p@@ is often nicer than working over finite fields. Thus, one might solve
a problem in @@\FF{p}@@ by "lifting" it to @@\QQ_p@@, solving it there, then
"reducing" by taking the result modulo @@p@@ --- by looking at the ones place in
the expansion.

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
hairy. We'll use the same notation as
[Wikipedia](https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication)
for elliptic curve operations. It's immediately clear that @@\rho@@ respects
"most" point additions. As long as two points (that *don't* map to @@\ecid@@)
don't share an @@\bar{x}@@, their calculation of @@\lambda@@ wouldn't care about
this transformation, again since division in @@\QQ_p@@ when taken modulo @@p@@
looks exactly like division in @@\FF{p}@@. Even if they do share an @@\bar{x}@@,
the computation still works if they have different @@\bar{y}@@. The numerator in
@@\lambda@@ would have degree zero while the denominator would have degree at
least one. The results for @@\lambda@@, @@x@@, and @@y@@ would be fractional, so
the sum would map to @@\ecid@@, as expected.

Now for the details. Feel free to skip to the last paragraph of this section if
you don't care about them. Otherwise, consider the trickier case when both
points @@P,Q\notin\kernl{\rho}@@ share an @@\bar{x}@@ and a @@\bar{y}@@. We'd
like to show that the resulting @@\lambda@@ is congruent modulo @@p@@ to that of
point-doubling. To do this, we'll assume @@x_P-x_Q=p^k\chin{x}@@ and similarly
that @@y_P-y_Q=p^k\chin{y}@@, where @@\chin{x}@@ is a unit but @@\chin{y}@@ may
not be. However, we do know @@\chin{y}@@ has degree at least @@-k+1@@ since
@@y_P-y_Q@@ has a zero in its ones place. Now we can solve for @@\chin{y}@@ in
%%
\begin{align\*}
\left(y_Q+p^k\chin{y}\right)^2 &= \left(x_Q+p^k\chin{x}\right)^3 + a\left(x_Q+p^k\chin{x}\right) + b \nl
y_Q^2 + 2y_Qp^k\chin{y} + p^{2k}\chin{y}^2 &= x_Q^3 + 3x_Q^2p^k\chin{x} + 3x_Qp^{2k}\chin{x}^2 + p^{3k}\chin{x}^3 + ax_Q + ap^k\chin{x} + b.
\end{align\*}
%%
That looks bad, until we realize we can simplify it as
%%
\begin{align\*}
2y_Qp^k\chin{y} &= 3x_Q^2p^k\chin{x} + ap^k\chin{x} + \BigO{p^{k+1}} \nl
2y_Q\chin{y} &= 3x_Q^2\chin{x} + a\chin{x} + \BigO{p} \nl
\chin{y} &= \frac{3x_Q^2 + a}{2y_Q}\chin{x} + \BigO{p}.
\end{align\*}
%%
Finally see that
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

As for Case 1, let @@\bar{I}=\ecid@@ and consider @@P+I@@. We just need to
verify that @@x_{P+I}\equiv x_P\modulo{p}@@ and the same for @@y@@. To do this,
we'll first write down the formula for the @@x@@-coordinate in point addition:
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
a lot of the expression vanishes. Letting @@\chin{d}=\degr{x_I}-\degr{y_I}@@, we
get
%%
\begin{align\*}
x_{P+I} &= \frac{-2y_Py_I + 2x_Px_I^2}{x_I^2} - x_P + \BigO{p^{\chin{d}+1}} \nl
&= x_P - \frac{2y_Py_I}{x_I^2} + \BigO{p^{\chin{d}+1}} \nl
&= x_P + \BigO{p}.
\end{align\*}
%%
So the @@x@@-coordinate is correct. What about the @@y@@-coordinate? Again,
we'll write down the formula:
%%
\begin{align\*}
y_{P+I} &= \lambda\cdot(x_P - x_{P+I}) - y_P \nl
&= \frac{y_P-y_I}{x_P-x_I}\cdot\left(\frac{2y_Py_I}{x_I^2} + \BigO{p^{\chin{d}+1}}\right) - y_P \nl
&= \frac{2y_P^2y_I-2y_Py_I^2}{x_Px_I^2-x_I^3} - y_P + \lambda\BigO{p^{\chin{d}+1}}
\end{align\*}
%%
Since @@\degr{\lambda}@@ is just @@-\chin{d}@@, we get that
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
fractional coordinates, which is true almost by definition. Instead, we'll spend
most of our time going the opposite direction. We'll lift our elliptic curve
from @@\FF{p}@@ to @@\QQ_p@@ and do all our math there.

---

So we have some point on a curve @@P\in E\[\FF{p}\]@@ and we'd like to find some
new point @@P^\*\in E^\*\[\QQ_p\]@@ that reduces to our original point under the
reduction homomorphism described above: @@\rho(P^\*)=P@@. In some sense, we'd
like to "invert" the reduction by lifting. Of course, there are (probably)
infinitely many @@P^\*@@ and @@E^\*@@ that'll work --- we just need to find one.
How?

[Hensel's lifting lemma](https://wikipedia.org/wiki/Hensel%27s_lemma) makes this
very easy. Novotney's [paper][2] covers it. Here's a very roundabout explanation
of what the lemma says, which will hopefully provide some intuition as to why
we're using it. Suppose we have some polynomial @@f@@ and we'd like to find one
of its roots @@n\in\ZZ_p@@. *A priori* we won't know all the digits of @@n@@,
but suppose we know the last @@k@@ digits. Then, Hensel's lemma allows us to
find the next digit in the expansion, so that we know the last @@k+1@@ digits of
@@n@@. This process can then be repeated indefinitely --- we can find the last
@@k+2@@ digits, then @@k+3@@, *ad infinitum*.

How's this useful? Well, by moving everything to the LHS, we can see our
original elliptic curve @@E@@ as a polynomial @@y^2-x^3-ax-b@@ for which we know
a root @@P=(x,y)@@ in @@\FF{p}@@. Remember that @@\FF{p}@@ is just the ones
place of @@\ZZ_p@@, so we can apply Hensel's lifting lemma with @@k=1@@. We can
choose one of the variables to treat as a constant, say @@x@@, then repeatedly
lift the other to find a root of this polynomial in @@\ZZ_p\subset\QQ_p@@, and
thus find a point @@P^\*\in E^\*\[\QQ_p\]@@.

That's the idea, but there are some details to be mindful of. First, I used
@@a@@ and @@b@@ as the coefficients in the polynomial above. That usually works,
but will cause Smart's attack to fail about @@\frac{1}{p}@@-th of the time. It
fails when the lifted curve, defined by @@a@@ and @@b@@ over @@\QQ_p@@, happens
to be isomorphic to that over @@\FF{p}@@. Smart actually notes this in his
[paper][1], and this
[StackExchange thread](https://crypto.stackexchange.com/a/70508) provides a
solution for these "canonical lifts". Note that @@E^\*@@ isn't unique --- we can
lift the original curve @@E@@ in infinitely many ways. So, before trying to lift
@@P@@ to @@P^\*@@, just add a random multiple of @@p@@ to both @@a@@ and @@b@@.
Now, @@E^\*@@ will be defined by these new values @@a^\*@@ and @@b^\*@@, but
will still reduce to our original curve @@E@@ when taken modulo @@p@@.

Second, I chose to keep @@x@@ constant and lift @@y@@. Usually, either will
work, but not always. As we'll see below, at each iteration of the lift we
require that @@f^\prime@@ is not a multiple of @@p@@. If we iterate with @@x@@
held constant, then @@f^\prime(y)=2y@@ is guaranteed to satisfy that condition
since our initial @@y@@ is not congruent to zero modulo @@p@@. If we hold @@y@@
constant instead, then @@f^\prime(x)=3x^2-a^\*@@ which can be a multiple of
@@p@@.

With that out of the way, let's look at the surprisingly simple proof. But
first, we need to clarify what exactly we're trying to prove. The formulation
from three paragraphs ago isn't exactly easy to work with, but we can make it
so. Suppose we have the last @@k@@ digits of @@n@@, a root of @@f@@ in
@@\ZZ_p@@. This is equivalent to saying we have a root @@r@@ of @@f@@ modulo
@@p^k@@. We'd like to find the next digit in the expansion of @@n@@ --- some
root @@s@@ of @@f@@ modulo @@p^{k+1}@@. Moreover, we require that @@s\equiv
r\modulo{p^k}@@. The last @@k@@ digits are set once they're "discovered", and we
never go back to change them.

This formulation is much nicer. Now we just need to solve for @@s@@! Though, we
do need one more trick. We start by
[Taylor-expanding](https://en.wikipedia.org/wiki/Taylor_series) @@f@@ about
@@r@@. This is why we require @@f@@ to be a polynomial: they have finite Taylor
series. So we expand
%%
\begin{align\*}
f(s) &\equiv \sum_{i=0}^N \frac{f^{(i)}(r)}{i!} (s-r)^i &\mod p^{k+1} &\nl
&\equiv f(r) + f^\prime(r)\cdot(s-r) + \sum_{i=2}^N \frac{f^{(i)}(s)}{i!}(s-r)^i &\mod p^{k+1} &.
\end{align\*}
%%
Since we require @@s-r\equiv0\modulo{p^k}@@, all the terms in the sum will be
divisible by @@p^{2k}@@ and thus vanish. We also require that
@@f(s)\equiv0\modulo{p^{k+1}}@@, eliminating the RHS. Now we solve
%%
\begin{align\*}
0 &\equiv f(r) + f^\prime(r)\cdot(s-r) &\mod p^{k+1} &\nl
s &\equiv r - f(r) \cdot f^\prime(r)^{-1} &\mod p^{k+1} &.
\end{align\*}
%%

As an aside, the actual statement of Hensel's lemma is much more general than
what I've given here. We just don't need the extra power.

---

So we can lift @@P\in E\[\FF{p}\]@@ to another point @@P^\*\in E^\*\[\QQ_p\]@@,
as well as convert back by reducing modulo @@p@@. But what does this get us? I
said that working over @@\QQ_p@@ is much nicer than working over a finite field,
but how so? We need one more transformation before we can understand Smart's
attack. It's breifly discussed in Leprevost's [paper][3], but it's covered in
much more detail in Chapter IV.1 of Silverman's [book][4].

Suppose we have some elliptic curve @@E\[\QQ_p\]@@ with domain parameters @@a@@
and @@b@@. Silverman makes the following change of variables (which I denote as
the function @@\theta@@):
%%
\begin{align\*}
z &= -\frac{x}{y} \nl
w &= -\frac{1}{y}.
\end{align\*}
%%
I'm honestly not sure what motivated this choice. He mentions that it brings
@@\ecid@@ to the origin in the @@z@@-@@w@@-plane, which is in line with his
investigation of points in the "neighborhood" around @@\ecid@@. He also talks
about uniformizers, but I don't have the background to understand what he's
saying.

What he does next is even stranger. He first rewrites the equation of @@E@@ in
terms of @@z@@ and @@w@@ as
%%
w = z^3 + azw^2 + bw^3,
%%
then recursively substitutes it into itself over and over again! This process
"converges" to a power series in @@z@@. This seems surprising at first, but it's
actually quite easy to see this. Note that, every time we recursively substitute
@@w@@, the minimum possible degree of any term containing a @@w@@ increases by
at least one. That is, every substitution "determines" at least one more
coefficient in the power series. Another way to see this, and the way Silverman
presents it, is through Hensel's lemma. We repeatedly lift modulo powers of
@@z@@.

So we have this power series
%%
w = \sum_{i=0}^\infty A_i z^{3+i}
%%
which describes some of the points on our original elliptic curve @@E@@. It
doesn't describe all of them, though --- only those whose value of @@z@@ causes
this series to converge. Convergence over @@\RR@@ is tricky, and that over
@@\FF{p}@@ is impossible, but it's fairly simple to show over @@\QQ_p@@. Under
the @@p@@-adic metric, this power series converges when @@\degr{z}\geq1@@. That
happens when @@\degr{x}>\degr{y}@@, which is true if and only if both @@x@@ and
@@y@@ are fractional. That is, this series converges for and only for points in
the kernel of the reduction homomorphism described two sections ago:
@@P\in\kernl{\rho}@@.

Thus we can think of some of the points on @@E@@ in terms of their @@z@@-value,
from which we can derive @@w@@. But that doesn't really help us unless we can do
math with @@z@@ alone. Luckily, our choice of @@\theta@@ makes point arithmetic
easy. Ultimately, this is because it maps lines to lines, with vertical lines
mapping to lines through the origin. As a result, three points that are colinear
in @@x@@-@@y@@-space will be colinear in @@z@@-@@w@@-space, and vice-versa since
@@\theta@@ is invertible.

Because of this line-preservation property, we can derive the formula for point
addition in terms of @@z@@. Recall that we define three colinear points
@@P@@,@@Q@@,@@R@@ as summing to @@\ecid@@. Suppose we know @@P@@ and @@Q@@ and
wish to find @@R@@. We'll do so much the same way we would for any other
elliptic curve. We start by finding the line between @@P@@ and @@Q@@ --- the one
with slope
%%
\begin{align\*}
\lambda &= \frac{w_P - w_Q}{z_P - z_Q} \nl
&= \sum_{i=0}^\infty A_i \frac{z_P^{3+i} - z_Q^{3+i}}{z_P - z_Q} \nl
&= \sum_{i=0}^\infty \left( A_i \sum_{j=0}^{i+2} z_P^j z_Q^{i+2-j} \right) \nl
&= \BigO{z^2}
\end{align\*}
%%
and @@w@@-intercept
%%
\nu = w_P - \lambda z_P = w_Q - \lambda z_Q.
%%
We then substitute @@w=\lambda z + \nu@@ and solve for @@z_R@@ in
%%
c(z-z_P)(z-z_Q)(z-z_R) = z^3 + azw^2 + bw^3 - w.
%%
Expanding then equating the cubic and quadratic coefficients gives
%%
\begin{align\*}
c &= 1 + a\lambda^2 + b\lambda^3 \nl
-c\cdot(z_P + z_Q + z_R) &= 2a\lambda\nu + 3b\lambda^2\nu,
\end{align\*}
%%
from which we get
%%
z_R = -z_P - z_Q - \frac{2a\lambda\nu+3b\lambda^2\nu}{1+a\lambda^2+b\lambda^3}.
%%
However, this isn't the formula for point addition. We defined @@P+Q+R@@ to
equal @@\ecid@@ since they're colinear. Thus, @@P+Q=-R@@. We invert a point in
@@x@@-@@y@@-space by negating its @@y@@-coordinate. So in @@z@@-@@w@@-space, we
invert a point by negating both its @@z@@- and @@w@@-values. Thus
%%
z_{P+Q} = z_P + z_Q + \frac{2a\lambda\nu+3b\lambda^2\nu}{1+a\lambda^2+b\lambda^3}.
%%

That fraction looks nasty to work with. Thankfully, we don't need to. Note that
@@\lambda@@ only contains terms of degree two or higher, and the same is thus
true for the numerator in that last term. The denominator is a unit power series
--- a formal power series with a nonzero constant term. So, it's invertible as a
power series in @@z_P@@ and @@z_Q@@, and more importantly it won't change the
degree of the numerator after division. Therefore
%%
z_{P+Q} = z_P + z_Q + \BigO{z^2},
%%
which simplifies things greatly.

So we have this very simple addition law when we view points in @@E\[\QQ_p\]@@
in terms of their @@z@@-coordinates after transforming with @@\theta@@. We
define this new space of @@z@@-values @@\hat{E}\[p\ZZ_p\]@@ as the set
@@p\ZZ_p@@ endowed with this group operation, denoted @@\oplus@@ to distinguish
it from regular addition. Note that @@\theta:\kernl{\rho}\to\hat{E}@@ is a group
homomorphism by construction. More importantly however, note the structure in
the lower digits of @@\hat{E}@@. The ones place of any number in that set is
zero by definition, but the @@p@@s digit is more interesting. Under @@\oplus@@,
it looks exactly like @@\FF{p}@@ under addition, which makes sense since it's
the least significant non-zero digit and since none of the higher order terms in
the addition law affect it.

We know how to solve the discrete-log problem in @@\FF{p}^+@@ --- it's just
inversion modulo @@p@@. So, we can take advantage of this structure to construct
an attack. Of course, we have to be mindful of the fact @@\theta@@ is only
defined for points that reduce to @@\ecid@@ modulo @@p@@, but we can work around
that.

---

After covering all that background material, we're finally ready to see Smart's
attack. Let's look back at the CTF problem that started this whole post. We have
some elliptic curve @@E\[\FF{p}\]@@, defined by @@a@@ and @@b@@, with order
@@\\#E=p@@. Furthermore, we're given two points on the curve related by
@@P-dG=\ecid@@, and we're asked to solve for @@d@@.

Smart's attack starts by lifting @@E@@ and its points to a curve over @@\QQ_p@@.
We get that
%%
P^\* - dG^\* \in \kernl{\rho}
%%
since reduction modulo @@p@@ is a group homomorphism. Now, we'd like to use the
mapping @@\theta@@, described in the last section, to exploit that simple
addition law. We know
%%
\theta(P^\* - dG^\*) = k p + \BigO{p^2},
%%
and we'd like to say something along the lines of
%%
\theta(P^\*) - d\cdot\theta(G^\*) \equiv k p \mod p^2,
%%
since from there, solving for @@d@@ is straightforward. But, we run into two
issues. First, @@P^\*,G^\*\notin\kernl{\rho}@@, so passing them to @@\theta@@ is
ill-defined. Second, since we don't know what @@d@@ is, we don't know @@k@@
either, and solving in terms of it is kind of useless.

To fix both of these problems at once, we require @@\\#E=p@@. Why? We're going
to multiply both sides of the equation by @@p@@. On the LHS, note that
@@pG=\ecid@@, so @@pG^\*\in\kernl{\rho}@@ and taking @@\theta@@ of it is
well-defined. Likewise for @@P@@. Meanwhile, multiplying the RHS by @@p@@ will
cause it to vanish modulo @@p^2@@. We can see this either as the @@p@@s digit of
the RHS operating in @@\FF{p}^+@@ or as multiplication by @@p@@ corresponding to
a "shift" in a number's @@p@@-adic expansion.

Thus we get
%%
\begin{align\*}
p \cdot \theta( P^\* - dG^\* ) &= k p^2 + \BigO{p^3} \nl
\theta( pP^\* - d \cdot pG^\* ) &= \BigO{p^2} \nl
\theta(pP^\*) - d \cdot \theta(pG^\*) &= \BigO{p^2},
\end{align\*}
%%
from which it's easy to solve for @@d@@ as
%%
d = \frac{\theta(pP^\*)}{\theta(pG^\*)} + \BigO{p}.
%%
Of course, we only care about @@d@@ modulo @@\\#E@@, so we can drop the
@@\BigO{p}@@ term and simply look at the ones place of the result.

This method allows us to find @@d@@ for the curve given in `handout.txt`. We can
give it to the challenge server and get the flag:
{% highlight plaintext %}
flag{wh0_sa1d_e11ipt1c_curv3z_r_s3cur3??}
{% endhighlight %}

---

### Resources

This post may or may not have helped you understand Smart's attack. Ultimately,
there's no substitute for practice --- for struggling through the material
yourself. I've linked a few resources below, some which I've mirrored on my site
in case the original link breaks. I found Koc's and Novotney's papers
particularly helpful.
* [Koc, C. K. (2002). A Tutorial on p-adic Arithmetic. *Electrical and Computer
  Engineering*, *Oregon State University*, *Corvallis*, *Oregon*, *97331*.
  `http://www.cryptocode.net/docs/r09.pdf`][5]
* [Smart, N. P. (1999). The discrete logarithm problem on elliptic curves of
  trace one. *Journal of cryptology*, *12*(3), 193-196.
  `https://link.springer.com/content/pdf/10.1007/s001459900052.pdf`][1]
* [Silverman, J. H. (2009). *The arithmetic of elliptic curves* (Vol. 106).
  Springer Science & Business Media.
  `https://link.springer.com/book/10.1007/978-0-387-09494-6`][4]
* [Leprevost, F., Monnerat, J., Varrette, S., & Vaudenay, S. (2005). Generating
  anomalous elliptic curves. *Information processing letters*, *93*(5), 225-230.
  `http://www.monnerat.info/publications/anomalous.pdf`][3]
* [Novotney, P. (2010). Weak Curves In Elliptic Curve Cryptography.
  `https://www.wstein.org/edu/2010/414/projects/novotney.pdf`][2]



[1]: </assets/2021/01/15/pdf/Smart.pdf> "The Discrete Logarithm Problem on Elliptic Curves of Trace One"
[2]: </assets/2021/01/15/pdf/Novotney.pdf> "Weak Curves In Elliptic Curve Cryptography"
[3]: </assets/2021/01/15/pdf/Leprevost.pdf> "Generating Anomalous Elliptic Curves"
[4]: <https://link.springer.com/book/10.1007/978-0-387-09494-6> "The Arithmetic of Elliptic Curves"
[5]: </assets/2021/01/15/pdf/Koc.pdf> "A Tutorial on p-adic Arithmetic"
