---
title: L'H&ocirc;pital's Rule in Higher Dimensions
libs: [mathjax]
---

<div class="mathjaxDeclarations">
    @@\newcommand{\nl}{\\}@@
</div>

*This post is taken from an email I wrote to Dr. Shuenn Siang Ng and (now) Dr.
Santana Afton. They were my professor and my TA respectively for MATH 2551:
Multivariable Calculus at Georgia Tech.*

---

Dr. Shuenn Siang Ng and TA Santana Afton,

I was talking to you about finding the limits of ratios in higher dimensions
where L'H&ocirc;pital's rule is not available. I did some thinking, and I would
like to hear what you have to say. First, however, I would like to just consider
limits toward the origin. Shifts by a constant are continuous functions, so we
should be able to restrict our view without loss of generality.

The idea behind L'H&ocirc;pital's rule is to approximate the functions whose
values vanish with their tangent lines. The obvious extension would be to do the
same with planes. However, first we need to understand how the limits of the
ratios of planes work. Thus, consider two planes through the origin written in
@@z@@-equals form with coefficients @@\mathbf{a} = \langle a_1, \cdots, a_n
\rangle@@ and @@\mathbf{b} = \langle b_1, \cdots, b_n \rangle@@. We wish to
consider the limit

%% \lim_{\left(r_1,\cdots, r_n\right) \to \mathbf{0}} \frac{\sum_{i=1}^n a_i r_i}{\sum_{i=1}^n b_i r_i} = \lim_{\mathbf{r} \to \mathbf{0}} \frac{\mathbf{a}\cdot\mathbf{r}}{\mathbf{b}\cdot\mathbf{r}}. %%

We can make the following observation. If the limit exists and equals
@@\lambda@@, then in particular the limit converges to @@\lambda@@ for all lines
going through the origin. Consider an arbitrary line in the direction of
@@\mathbf{v}@@ and note that

%%
\begin{align\*}
    \lim_{t \to 0} \frac{\left(\mathbf{a}\cdot\mathbf{v}\right) t}{\left(\mathbf{b}\cdot\mathbf{v}\right) t} &= \lambda \nl
    \frac{\mathbf{a}\cdot\mathbf{v}}{\mathbf{b}\cdot\mathbf{v}} &= \lambda \nl
    \mathbf{a}\cdot\mathbf{v} &= \lambda\mathbf{b}\cdot\mathbf{v}
\end{align*}
%%

for all @@\mathbf{v}@@. From here, we may deduce that if the limit of the ratio
of these planes exists and converges to @@\lambda@@, then @@\mathbf{a} =
\lambda\mathbf{b}@@. On a sidenote, the reverse can easily be shown true as long
as @@\mathbf{b} \neq \mathbf{0}@@.

What now? Well, we can approximate a function @@f@@ around the origin as

%%
\begin{align\*}
    f(\mathbf{r}) &\approx f(\mathbf{0}) + \sum_{i=1}^n \frac{\partial f}{\partial x_i} \, r_i \nl
        &\approx f(\mathbf{0}) + \nabla f \cdot \mathbf{r}.
\end{align\*}
%%

Thus, if two functions @@f@@ and @@g@@ pass through the origin and the limit of
their ratios converges to @@\lambda@@, by the previous paragraph it makes sense
to believe @@\nabla f = \lambda \nabla g@@ at the origin. Indeed, if we further
assume @@\nabla f@@ and @@\nabla g@@ are continuous at the origin, we may
evaluate the limit along an arbitrary line in the direction of @@\mathbf{v}@@ as

%% \lambda = \lim_{t\to 0} \frac{f\left(\mathbf{v} t\right)}{g\left(\mathbf{v} t\right)} = \lim_{t\to 0} \frac{\sum_{i=1}^n f_{x_i}(\mathbf{v} t) \, v_i}{\sum_{i=1}^n g_{x_i}(\mathbf{v} t) \, v_i} = \lim_{t\to 0} \frac{\nabla f(\mathbf{v} t) \cdot \mathbf{v}}{\nabla g(\mathbf{v} t) \cdot \mathbf{v}} = \frac{\nabla f \cdot \mathbf{v}}{\nabla g \cdot \mathbf{v}}. %%

Note that we used L'H&ocirc;pital's rule for one variable in the second step. By
the same argument as in the last paragraph, we have @@\nabla f = \lambda \nabla
g@@ at the origin. However, note that the reverse is not true. If we consider

%%\lim_{\left(x,y\right) \to \mathbf{0}} \frac{y^2}{x},%%

we get @@\nabla f = \langle 0, 2y\rangle@@ and @@\nabla g = \langle 1,0
\rangle@@. At the origin, the equality holds with @@\lambda = 0@@, but the limit
does not exist as substituting @@x \mapsto y^2@@ shows.

Can we extend this argument? Well, maybe. Suppose @@f@@ and @@g@@ are both @@m@@
times continuously differentiable and that the first @@m-1@@ partial derivatives
of both @@f@@ and @@g@@ vanish at the origin. Then, like before, we may consider
an arbitrary line through the origin in the direction of @@\mathbf{v}@@ and
apply L'H&ocirc;pital's rule to get

%%
\begin{align\*}
    \lim_{t\to 0} \frac{f(\mathbf{v} t)}{g(\mathbf{v} t)} &= \lim_{t\to 0} \frac{\sum_{i=1}^n f_{x_i}(\mathbf{v} t) \, v_i}{\sum_{i=1}^n g_{x_i}(\mathbf{v} t) \, v_i} \nl
        &= \lim_{t\to 0} \frac{\sum_{i=1}^n \sum_{j=1}^n f_{x_ix_j}(\mathbf{v} t) \, v_iv_j}{\sum_{i=1}^n \sum_{j=1}^n g_{x_ix_j}(\mathbf{v} t) \, v_iv_j} \nl
        &= \cdots \nl
        &= \lim_{t\to 0} \frac{\sum_{\left|\alpha\right| = m} \frac{m!}{\alpha!} \left( \partial^\alpha f(\mathbf{v}t) \,\, \mathbf{v}^\alpha \right)}{\sum_{\left|\alpha\right| = m} \frac{m!}{\alpha!} \left( \partial^\alpha g(\mathbf{v}t) \,\, \mathbf{v}^\alpha \right)},
\end{align\*}
%%

using multi-index notation to keep the math clean. Further assuming the limit
exists and converges to @@\lambda@@,

%%
\begin{align\*}
    \frac{\sum_{\left|\alpha\right|=m} \frac{1}{\alpha!}\partial^\alpha f \,\, \mathbf{v}^\alpha}{\sum_{\left|\alpha\right|=m} \frac{1}{\alpha!}\partial^\alpha g \,\, \mathbf{v}^\alpha} &= \lambda \nl
    \sum_{\left|\alpha\right|=m} \frac{1}{\alpha!}\partial^\alpha f \,\, \mathbf{v}^\alpha &= \sum_{\left|\alpha\right|=m} \frac{\lambda}{\alpha!}\partial^\alpha g \,\, \mathbf{v}^\alpha
\end{align\*}
%%

for all @@\mathbf{v}@@. The left- and right-hand sides are both polynomials in
@@v_1,\cdots,v_n@@, and for the equality to hold regardless of the values those
variables take, we must have for all @@\left|\alpha\right| = m@@

%% \partial^\alpha f = \lambda\,\partial^\alpha g. %%

That is, all the @@m@@-th order partial derivatives of @@f@@ and @@g@@ must be
proportional at the origin.

How useful is this? You would think not very, and you are probably right.
However, note that while I focused on limits toward the origin, the above
observations generalize without change to arbitrary points. Differential
operators "do not care" about shifts, as long as the point they are being
evaluated at is shifted as well. Moreover, the proportionality constant
@@\lambda@@ is always the value of the limit, so it could be useful for
evaluating limits given they exist.

But perhaps most useful is the possibility of another test for determining
whether the limit of a ratio exists at a point. First, find the least @@m@@ such
that not all of the @@m@@-th order partial derivatives of @@f@@ and @@g@@
vanish. Then, check if all the @@m@@-th order partial derivatives of @@f@@ and
@@g@@ are proportional with the same proportionality constant. If they are not,
the limit does not exist. If they are, the limit may exist and is equal to the
proportionality constant if it does.

Note that no power is gained from this test. It is essentially just testing all
possible lines through the point the limit is being taken at. However, it might
be useful since it may be easier and faster to execute. What do you think? Is my
work correct? If it is, can I use this on quizzes and tests? I expect both
answers to be "no", but it is worth asking.

Thank you,

\- Ammar Ratnani

---

Dr. Shuenn Siang Ng and TA Santana Afton,

It occured to me in class today that, when I consider an arbitrary line in the
direction of @@\mathbf{v}@@, I have to consider whether the values
@@\mathbf{v}t@@ are in the domain of @@f/g@@. That is, whether @@g(\mathbf{v}t)
\neq 0@@ for at least some neighborhood around the origin.

However, looking over my arguments again, it seems this should be a non-issue.
Why? Because the crux of my argument relies on determining the coefficients of a
polynomial. In my original justification, I stated we can equate the
coefficients since the two polynomials

%%
\sum_{\left|\alpha\right|=m} \frac{1}{\alpha!}\partial^\alpha f \,
\mathbf{v}^\alpha = \sum_{\left|\alpha\right|=m}
\frac{\lambda}{\alpha!}\partial^\alpha g \, \mathbf{v}^\alpha
%%

are equal for all possible @@\mathbf{v}^\alpha@@. However, we can also say the
coefficients are equal if we know they agree on any region with "volume". Why?
Well, pick a point "inside" that region and compute all the partial derivatives
of the two relevant polynomoials up to order @@m@@. Those will all be equal
since the polynomial's values are equal in a neighborhood around the point, and
from there we can reason all the coefficients are equal. My argument here is
very similar to
[https://math.stackexchange.com/a/1354872](https://math.stackexchange.com/a/1354872).

Let us assume there is at least one direction that ensures @@g(\mathbf{v}t) \neq
0@@ for some neighborhood around @@t=0@@. Since @@g@@ is continuously
differentiably sufficiently many times, we should be able to find some
@@\epsilon > 0@@ such that all @@\left|\left|\mathbf{u}-\mathbf{v}\right|\right|
< \epsilon@@ have @@g(\mathbf{u}t) \neq 0@@ in some neighborhood around @@t=0@@.
We can then use all of these @@\mathbf{u}@@ in the formula above then equate the
coefficients as I had originally planned.

How exactly I would go about formalizing this argument, I don't know. Again,
what do you think? Can you think of any counterexamples? I know I use
L'Hôpital's rule and that it has a restriction that the limit of @@f^\prime /
g^\prime@@ must exist, but that might just be for limits to infinity to prevent
cases with infinitely many oscillations. However, I might be misinterpreting
that. If I am, can you find a counterexample based on that?

Thank you,

\- Ammar Ratnani
