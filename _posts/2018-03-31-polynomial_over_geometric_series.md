---
title: The Convergence of Infinite Series of a Particular Form
libs: [mathjax]
---

<div class="mathjaxDeclarations">
    @@\newcommand{\qed}{\blacksquare}@@
    @@\newcommand{\nl}{\\}@@
</div>

_This post used to be hosted on my [GitHub](https://github.com/ammrat13),
but I felt it would fit better here. I wrote this when we covered sequences and
series in Calculus BC. I was interested in these particular series since they
weren't covered in class, and I found them to be a good opportunity to practice
the techniques I learned._

Consider the infinite sum 
%%S = \sum_{k=1}^\infty \frac{k^m}{n^k}.%%
We will first establish the convergence criteria for @@S@@, and we will then
find an explicit formula for the @@N@@-th partial sum of @@S@@ and the value
@@S@@ converges to in the case of @@m=1@@.

The convergence criteria for @@S@@ can easily be found with the Ratio Test.
Consider the limit of the absolute value of the ratio of successive terms in the
sum @@S@@. We find that the limit converges to 
\begin{align\*}
\lim_{k\to\infty} \left|\frac{\frac{(k+1)^m}{n^{k+1}}}{\frac{k^m}{n^k}}\right| &= \lim_{k\to\infty} \left|\frac{(k+1)^m}{n^{k+1}} \frac{n^k}{k^m}\right| \nl
	&= \frac{1}{\left|n\right|} \lim_{k\to\infty} \left|\left(\frac{k+1}{k}\right)^m\right| \nl
	&= \frac{1}{\left|n\right|} \, \left|\left(\lim_{k\to\infty}\frac{k+1}{k}\right)^m\right| \nl
	&= \frac{1}{\left|n\right|} \, \left|1^m\right| \nl
	&= \frac{1}{\left|n\right|}
\end{align\*}
since @@\left|x^m\right|@@ is continuous for all @@m@@. Thus, the sum @@S@@
converges if @@\left|n\right| > 1@@ and diverges if @@\left|n\right| < 1@@ by
the Ratio Test. @@\qed@@

We then consider the case @@\left|n\right|=1@@. There are two cases to consider
here: @@n=1@@ and @@n=-1@@. If @@n=1@@, the sum @@S@@ simplifies to
%%S = \sum_{k=1}^\infty \frac{k^m}{1^k} = \sum_{k=1}^\infty k^m,%%
which converges if @@m<-1@@ and diverges otherwise by the @@p@@-Series Test. If
@@n=-1@@, @@S@@ simplifies to 
%%S = \sum_{k=1}^\infty \frac{k^m}{(-1)^k} = \sum_{k=1}^\infty (-1)^k k^m,%%
which converges if @@m<0@@ and diverges otherwise (since only when @@m<0@@ is
@@\lim_{k\to\infty} k^m = 0@@ and is @@(k+1)^m < k^m@@ for @@k@@ positive) by
the Alternating Series Test. @@\qed@@

In summary, the convergence criteria for @@S@@ are as follows: The sum @@S@@
converges if @@\left|n\right| > 1@@ and diverges if @@\left|n\right| < 1@@. If
@@n=1@@, then @@S@@ converges if @@m<-1@@ and diverges otherwise. If @@n=-1@@,
then @@S@@ converges if @@m<0@@ and diverges otherwise.

In the case of @@m=1@@, we can find an explicit formula for the @@N@@-th partial
sum of @@S@@, @@S_N@@, and the value to which @@S@@ converges if
@@\left|n\right|>1@@. First, however, we claim that, for @@f@@ defined on all
positive integers,
%%\sum_{k=1}^N k\,f(k) = \sum_{k=1}^N \sum_{j=k}^N f(j)%%
and we will prove that claim by induction. In our base case of @@N=1@@,
\begin{align\*}
f(1) &= f(1) \nl
1 \cdot f(1) &= \sum_{j=1}^1 f(j) \nl
\sum_{k=1}^1 k\,f(k) &= \sum_{k=1}^1 \sum_{j=k}^1 f(j),
\end{align\*}
as required. So, assume that this claim holds for @@N-1@@. Then 
\begin{align\*}
\sum_{k=1}^N k \, f(k) &= \sum_{k=1}^{N-1} k \, f(k) + N \, f(N) \nl
	&= \sum_{k=1}^{N-1} \sum_{j=k}^{N-1} f(j) + \sum_{k=1}^N f(N) \nl
	&= \sum_{k=1}^{N-1} \sum_{j=k}^{N-1} f(j) + \sum_{k=1}^{N-1} f(N) + \sum_{k=N}^N f(N) \nl
	&= \sum_{k=1}^{N-1} \left( \sum_{j=k}^{N-1} f(j) + \sum_{j=N}^N f(j) \right) + \sum_{k=N}^N f(N) \nl
	&= \sum_{k=1}^{N-1} \sum_{j=k}^N f(j) + \sum_{k=N}^N \sum_{j=k}^N f(j) \nl
\sum_{k=1}^N k \, f(k) &= \sum_{k=1}^N \sum_{j=k}^N f(j)
\end{align\*}
as required. @@\qed@@

We can use the fact above to determine the aforementioned explicit formula for
@@S_N@@ when @@m=1@@ as such:
\begin{align\*}
S_N = \sum_{k=1}^N \frac{k}{n^k} &= \sum_{k=1}^N \sum_{j=k}^N \frac{1}{n^j} \nl
	&= \sum_{k=1}^N \frac{1}{n^k}\left( \frac{1-\frac{1}{n^{N-k+1}}}{1-\frac{1}{n}} \right) \nl
	&= \frac{n}{n-1} \sum_{k=1}^N \left(\frac{1}{n^k} - \frac{1}{n^{N+1}}\right) \nl
	&= \frac{n}{n-1} \left( \frac{1}{n}\left(\frac{1-\frac{1}{n^N}}{1-\frac{1}{n}}\right) - \frac{N}{n^{N+1}} \right) \nl
	&= \frac{n}{n-1} \left( \frac{n^N-1}{n^N\left(n-1\right)} - \frac{N}{n^{N+1}} \right) \nl
S_N &= \frac{n}{\left(n-1\right)^2} \left( \frac{n^N-1}{n^N} - \frac{N\left(n-1\right)}{n^{N+1}} \right). \qed
\end{align\*}

Having found a formula for @@S_N@@, we can now find the value to which @@S =
\lim_{N\to\infty} S_N@@ converges to when @@m=1@@. Using the fact that
@@\left|n\right|>1@@, we see that
\begin{align\*}
S = \lim_{N\to\infty} S_N &= \lim_{N\to\infty} \frac{n}{\left(n-1\right)^2} \left( \frac{n^N-1}{n^N} - \frac{N\left(n-1\right)}{n^{N+1}} \right) \nl
	&= \frac{n}{\left(n-1\right)^2} \left( \lim_{N\to\infty}\frac{n^N-1}{n^N} - \lim_{N\to\infty}\frac{N\left(n-1\right)}{n^{N+1}} \right) \nl
	&= \frac{n}{\left(n-1\right)^2} \cdot \left(1-0\right) \nl
S &= \frac{n}{\left(n-1\right)^2}. \qed
\end{align\*}
