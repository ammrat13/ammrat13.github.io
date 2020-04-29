---
title: Solving a Problem from Reddit
libs: [mathjax]
---

<div class="mathjaxDeclarations">
    @@\newcommand{\nl}{\\}@@
</div>

_This post used to be hosted at [ammrat13/proofs](https://github.com/ammrat13/proofs),
but I felt it would fit better here. I was intrigued by this problem because it
tied into what I learned in Calculus BC. Only now do I know I didn't have the
techniques I needed to tackle this problem. I can't quite put my finger on why,
but my proof seems wrong to me. For instance, I prove an integral converges by
bounding it between two values, which I can't immediately say is true. I'm not
proud of this work, but I thought I'd put it here for completeness._

### The Problem
Reddit user `u/Poliorcetyks` posed the following question on `r/learnmath` in
his post titled *Integrals with parameter, problem proving continuity*. Given a
function
%% f(x) = \int_0^1 \frac{\ln\left(\frac{1}{t}\right)^x}{t+1}\,dt, %%
find the domain of @@f@@ and show that it is continuous on its domain.

### Domain
We begin by bounding @@f@@ between two other functions. Note that for all @@0
\leq t \leq 1@@ that
%% \frac{1}{2} \leq \frac{1}{t+1} \leq 1 %%
%% \frac{1}{2} \int_0^1 \ln\left(\frac{1}{t}\right)^x dt \leq f(x) \leq \int_0^1 \ln\left(\frac{1}{t}\right)^x dt, %%
multiplying all sides of the inequality by the positive number
@@\ln\left(1/t\right)^x@@ then integrating all sides from @@0@@ to @@1@@. Thus,
we see that @@f@@ converges --- and @@x@@ is in the domain of @@f@@ --- if and
only if the above integral also converges.

We can transform that integral by a @@u@@-substitution with 
\begin{align\*}
u &= \ln\left(\frac{1}{t}\right) = -\ln(t) \nl
t &= e^{-u} \nl
dt &= -e^{-u} du
\end{align\*}
to get
%% \int_0^1 \ln\left(\frac{1}{t}\right)^x dt = \int_0^\infty u^x e^{-u} du = \Pi(x). %%
Thus, the above inequality simplifies to 
%% \frac{\Pi(x)}{2} \leq f(x) \leq \Pi(x) %%
which is certainly less intimidating. All that remains is to determine the
domain of @@\Pi@@, and we know that @@f@@ has the same domain.

It is clear that both @@0@@ and @@1@@ are in the domain of @@\Pi@@ as
\begin{align\*}
\Pi(0) &= \int_0^\infty e^{-u} du = 1 \nl
\Pi(1) &= \int_0^\infty ue^{-u} \nl
	&= \left[ -ue^{-u} + \int e^{-u} du \right]_0^\infty \nl
	&= 0 - 0 + 1 = 1.
\end{align\*}
We will thus begin by showing that all @@0 < x < 1@@ are in the domain of
@@\Pi@@. For those values of @@x@@, note that for @@0 \leq u \leq 1@@ that @@u^x
\leq 1@@ and that for @@u > 1@@ that @@u^x < u@@. We can therefore, for @@0 < x
< 1@@, split then bound @@\Pi@@ as 
\begin{align\*}
\Pi(x) &= \int_0^1 u^xe^{-u} du + \int_1^\infty u^xe^{-u} du \nl
	&\leq \int_0^1 e^{-u} du + \int_1^\infty ue^{-u} du \nl
	&\leq 1 + \frac{1}{e}.
\end{align\*}
Since the integrand for @@\Pi@@ is always positive and since @@\Pi@@ is bounded
for @@0 < x < 1@@, those values of @@x@@ are in the domain of @@\Pi@@ (and thus
that of @@f@@).

We will now show by induction that all positive real numbers are in the domain
of @@\Pi@@. We have already shown our base case that all positive real numbers
less than @@1@@ are in the domain of @@\Pi@@. Now, assume that all positive real
numbers less than @@n@@ are in the domain of @@\Pi@@. For any number @@n \leq x
< n+1@@ we find that
\begin{align\*}
\Pi(x) &= \left[ -u^xe^{-u} + \int xu^{x-1}e^{-u} \right]\_0^\infty \nl
	&= 0 - 0 + x\,\Pi(x-1) = x\,\Pi(x-1)
\end{align\*}
since @@x@@ is positive. Since @@x-1 < n@@ is in the domain of @@\Pi@@, all
positive real numbers less than @@n+1@@ are in the domain of @@\Pi@@, proving by
induction that all positive real numbers are in the domain of @@\Pi@@ and thus
in the domain of @@f@@.

We will next show that all real numbers @@-1 < x < 0@@ are in the domain of
@@\Pi@@. We perform an integration by parts on the definition of @@\Pi@@ as
\begin{align\*}
\Pi(x) &= \left[ \frac{1}{x+1}\,u^{x+1}e^{-u} + \int \frac{1}{x+1}\,u^{x+1}e^{-u} \right]\_0^\infty \nl
    &= 0 - 0 + \frac{\Pi(x+1)}{x+1} = \frac{\Pi(x+1)}{x+1}
\end{align\*}
since @@x+1 > 0@@ and since @@x+1@@ is in the domain of @@\Pi@@ --- and thus
@@f@@ --- as a result.

Note that @@x = -1@@ is not in the domain of @@\Pi@@. Attempting the integration
by parts leads to 
\begin{align\*}
\Pi(-1) &= \left[ \ln(u)e^{-u} + \int \ln(u)e^{-u} du \right]\_0^\infty \nl
	&= 0 + \infty + \int_0^\infty \ln(u)e^{-u} du \nl
	&= \infty
\end{align\*}
since the integral in the last term is a convergent integral. There are similar
results for all @@x < -1@@, as attempting the integration by parts gives
%% \Pi(x) = \left[ \frac{1}{x+1}\,u^{x+1}e^{-u} + \int \frac{1}{x+1}\,u^{x+1}e^{-u} \right]\_0^\infty %%
which results in a division by zero since @@x + 1 < 0@@. (And of course, the
integration by parts can continue upward until a convergent integral is reached.
The result, however, is still the same.) Thus, no real numbers less than or
equal to @@-1@@ are in the domain of @@\Pi@@, and are thus not in the domain of
@@f@@ either.

In summary, we conclude that the domain of @@\Pi@@, and thus of @@f@@, is the
set of all real numbers strictly greater than @@-1@@.

### Continuity
To show that @@f@@ is continuous on its domain, we must show that @@\lim_{h \to
0} f(x+h) = f(x)@@. To show that, we first note two facts. First, that 
%% f(x) = \lim_{a \to 0^+} \int_a^{1-a} \frac{\ln\left(\frac{1}{t}\right)^x}{t+1}\,dt, %%
since the integrand may go to infinity on either end --- on the lower end if @@x
< 0@@ and on the higher end if @@x > 0@@. And of course, it is the limit from
the positive side since the integrand may not be defined outside the interval
@@[0,1]@@. Second, that for all @@0 < t < 1@@ that
%% \lim_{h \to 0} \ln\left(\frac{1}{t}\right)^h = 1. %%

With both of these facts in hand, the proof of continuity is remarkably simple.
Note that 
%% \lim_{h \to 0} f(x+h) = \lim_{h \to 0} \int_0^1 \ln\left(\frac{1}{t}\right)^h \,\frac{\ln\left(\frac{1}{t}\right)^x}{t+1}\,dt. %%
This limit exists if and only if for all @@\epsilon > 0@@ there exists a
@@\delta > 0@@ such that when @@h@@ is within @@\delta@@ of @@0@@, @@f(x+h)@@ is
within @@\epsilon@@ of @@f(x)@@. We use our first fact to see that there is an
@@a > 0@@ such that
%% \left| \int_a^{1-a} \frac{\ln\left(\frac{1}{t}\right)^x}{t+1}\,dt - f(x) \right| < \frac{\epsilon}{2}. %%
We then use our second fact to show that for all @@h@@ within some distance
@@\delta@@ of @@0@@,
%% \left| \ln\left(\frac{1}{t}\right)^h - 1 \right| < \frac{\epsilon}{2 \left| \int_a^{1-a} \frac{\ln\left(\frac{1}{u}\right)^x}{u+1} \,du \right|} %%
for all @@a < t < 1-a@@.  Thus, we find that 
\begin{align\*}
\left| \int_a^{1-a} \ln\left(\frac{1}{t}\right)^h
\frac{\ln\left(\frac{1}{t}\right)^x}{t+1}\,dt - \int_a^{1-a} \frac{\ln\left(\frac{1}{t}\right)^x}{t+1}\,dt \right| &= \left| \int_a^{1-a} \frac{\ln\left(\frac{1}{t}\right)^x}{t+1} \left( \ln\left(\frac{1}{t}\right)^h - 1 \right) \,dt \right| \nl
	&< \left|\frac{\epsilon}{2 \left| \int_a^{1-a} \frac{\ln\left(\frac{1}{u}\right)^x}{u+1} \,du \right|}\right| \left| \int_a^{1-a} \frac{\ln\left(\frac{1}{t}\right)^x}{t+1} \,dt \right| \nl
	&< \frac{\epsilon}{2}.
\end{align\*}
Since it is possible to approximate @@f(x)@@, by choosing some @@a > 0@@ to cut
our approximation off at, to within @@\epsilon/2@@, and since it is possible to
choose an @@h@@ within @@\delta@@ of @@0@@ such that the first integral above is
within @@\epsilon/2@@ of our approximation of @@f(x)@@, it follows that that
integral is within @@\epsilon@@ of @@f(x)@@ as required. Thus, @@\lim_{h \to 0}
f(x+h) = f(x)@@ and @@f@@ is continuous on its domain.
