---
title: The Sums of Random Numbers on [0,1]
libs: [mathjax]
---

<div class="mathjaxDeclarations">
    @@\newcommand{\Ex}{\text{Ex}}@@
    @@\newcommand{\C}{\text{C}}@@
    @@\newcommand{\nl}{\\}@@
</div>

_This post used to be hosted on my [GitHub](https://github.com/ammrat13),
but I felt it would fit better here. I found this fact online somewhere, and I
wanted to try and prove it myself. The way I did so is far from elegant. In
particular, I didn't see the connection between uniformly choosing then summing
real numbers and higher-dimensional right tetrahedra. Nonetheless, it works (I
think) and I'm quite proud of it._

A rather famous question in probability goes as follows. Suppose you pick a real
number @@X_1@@ uniformly at random on @@[0,1]@@, then pick another real number
@@X_2@@ uniformly at random on the same interval, and continue to pick these
random numbers until the sum of the @@n@@ numbers you picked @@\sum_{i=1}^n
X_i@@ becomes strictly greater than @@1@@. On average, how many numbers will you
have to pick for their sum to exceed @@1@@?

Surprisingly, on average you will require @@e@@ numbers. What follows is an
inelegant but functional proof of that fact.

First, we will work out the probability of choosing @@n@@ numbers @@X_1, X_2,
\dots, X_n@@ uniformly at random on @@[0,d]@@ for arbitrary @@d@@ and having
their sum less than or equal to @@d@@, which we designate @@\Pr[S(n,d)]@@. We
claim that 
%% \Pr[S(n,d)] = \frac{1}{n!} %% 
regardless of @@d@@, and we will prove that claim by induction. First, it is
clear that 
%% \Pr[S(1,d)] = 1 = \frac{1}{1!} %% 
as the one number chosen, because it was chosen on @@[0,d]@@, cannot be greater
than @@d@@, thus establishing our base case.

We then assume that the claim holds for @@n-1@@ and lower as our induction
hypothesis. We then look at 
%% \Pr[S(n,d)] = \int_0^d \frac{1}{d} \Pr[S(n,d) \mid X_1 = x] dx %% 
(with @@1/d@@ being used as the numbers picked have a uniform distribution on an
interval of length @@d@@). Intuitively, this can be seen as iterating over all
the possible values @@X_1@@ could take and taking their weighted average, just
as we may do in the discrete case. We then observe that 
\\begin{align\*}
\Pr[S(n,d) \mid X_1 = x] &= \Pr\left[(X_2,\dots,X_n \leq d-x) \cap \left(\sum_{i=2}^n X_i \leq d-x \right) \right] \\\\ 
    &= \Pr[(X_2,\dots,X_n \leq d-x)] \cdot \Pr[S(n-1,d-x)].
\\end{align\*}
In other words, we observe that the probability that the sum of all the @@n@@
numbers chosen being less than @@d@@ given the first number was @@x@@ is the
probability that the remaining numbers chosen are each less than @@d-x@@ (as if
even one was over, the total sum would be greater than @@d@@) and that the sum
of the remaining @@n-1@@ numbers is less than @@d-x@@ given they are all
individually being chosen on @@[0,d-x]@@ (for a similar reason to before). We
then see that
%% \Pr[S(n,d) \mid X_1 = x] = \left(\frac{d-x}{d}\right)^{n-1}\frac{1}{(n-1)!}, %%
with the first term coming from our @@n-1@@ remaining numbers all having to fall
on @@[0,d-x]@@ when chosen on @@[0,d]@@, and the second term coming from our
induction hypothesis. Substituting that back into the integral, we get
\\begin{align\*}
\Pr[S(n,d)] &= \frac{1}{d^n(n-1)!}\int_0^d (d-x)^{n-1} dx \nl
	&= \frac{1}{d^n(n-1)!}\cdot\frac{d^n}{n} \nl
	&= \frac{1}{n!}
\\end{align\*}
as required.

Now that we have found the probability choosing @@n@@ numbers uniformly at
random on @@[0,d]@@ and having their sum not exceed @@d@@, we are ready to
calculate the expected number of numbers required to have their sum exceed
@@d=1@@. We designate @@N@@ to be the number of numbers chosen on @@[0,1]@@
required for their sum to exceed @@1@@, and we see that 
%% \Ex[N] = \sum_{i=1}^\infty i \cdot \Pr[N=i]. %%
We then observe that @@\Pr[N=i]@@ is the probability that the sum of  @@i-1@@
random numbers on @@[0,1]@@ does not exceed @@1@@, but the sum of @@i@@ numbers
does. In other words
\\begin{align\*}
\Pr[N=i] &= \Pr\left[S(i-1,1) \cap S(i,1)^\C\right] \nl
	&= \Pr[S(i-1,1)] \cdot \Pr\left[S(i,1)^\C \mid S(i-1,1)\right] \nl
	&= \Pr[S(i-1,1)] \cdot \left(1-\Pr\left[S(i,1) \mid S(i-1,1)\right]\right) \nl
	&= \Pr[S(i-1,1)] \cdot \left(1-\frac{\Pr[S(i,1) \cap S(i-1,1)]}{\Pr[S(i-1,1)]}\right)
\end{align\*}
We then see that @@S(i,1)@@ implies @@S(i-1,1)@@. It is impossible to pick @@i@@
numbers on @@[0,1]@@ and have their sum not exceed @@1@@ without first picking
@@i-1@@ numbers and having their sum not exceed @@1@@. Thus @@\Pr[S(i,1) \cap
S(i-1,1)]=\Pr[S(i,1)]@@ and
\\begin{align\*}
\Pr[N=i] &= \Pr[S(i-1,1)] \cdot \left(1-\frac{\Pr[S(i,1)]}{\Pr[S(i-1,1)]}\right) \nl
	&= \frac{1}{(i-1)!} \cdot \left(1 - \frac{\frac{1}{i!}}{\frac{1}{(i-1)!}}\right) \nl
	&= \frac{1}{(i-1)!} \cdot \left(1-\frac{1}{i}\right) \nl
	&= \frac{i-1}{i!}.
\\end{align\*}
Substituting this back into our sum then manipulating it shows that 
\\begin{align\*}
\Ex[N] &= \sum_{i=1}^\infty i \cdot \frac{i-1}{i!} \nl 
	&= 0 + \sum_{i=2}^\infty i \cdot \frac{i-1}{i!} \nl
	&= \sum_{i=2}^\infty \frac{1}{(i-2)!} \nl
	&= \sum_{i=0}^\infty \frac{1}{i!} \nl
\Ex[N] &= e
\\end{align\*}
as required. It should be noted that there is nothing special about @@1@@. It
would, on average, require @@e@@ numbers picked uniformly at random on @@[0,d]@@
for their sum to exceed @@d@@, regardless of @@d@@. This proof works for all
@@d@@, albeit with some slight modifications, namely replacing all the @@1@@'s
with @@d@@'s.
