---
title: Algorithms for Fast Cubic Evaluation
tags: ["mathematics", "algorithms"]
libs: ["mathjax", "mermaidjs"]
libs_config:
    mermaidjs:
        flowchart:
            padding: 0
            nodeSpacing: 25
            rankSpacing: 25
---

<div class="mathjaxDeclarations">
    @@\newcommand{\nl}{\\}@@
</div>

It's been a while; a lot's happened. I got accepted to Stanford's MS CS program,
and I even graduated from there last month. During my last quarter there, I took
*EE 372: Design Projects in VLSI Systems II*. In the iteration of the course I
took, [Priyanka][1] essentially gave us the source code for [MINOTAUR][2], and
asked us to improve it however we saw fit. I mainly focused on improving the
vector unit --- the part of the accelerator that handles activations,
element-wise operations, and other low arithmetic-intensity tasks.

I was not the only one working on the vector unit though. Another group looked
at changing the strategy it used to compute activation functions. Ultimately,
they settled on piecewise-cubic activations, with programmable coefficients and
interval bounds. I interacted with them, and I investigated ways to make the
computation of these cubic polynomials more efficient.

Let's say we have some

%% p(x) = c_3 x^3 + c_2 x^2 + c_1 x + c_0. %%

Na&iuml;vely implementing this in hardware, by evaluating all the
multiplications before computing the additions, gives a relatively poor result.
It requires six multipliers and three adders, and its critical path consists of
two multipliers and two adders.

<figure>
<pre class="mermaid">
flowchart TB
    x3["`*x*`"]
    x2["`*x*`"]
    x1["`*x*`"]

    c0["`*c<sub>0</sub>*`"]
    c1["`*c<sub>1</sub>*`"]
    c2["`*c<sub>2</sub>*`"]
    c3["`*c<sub>3</sub>*`"]

    c3m0["`\*`"]
    c3m1["`\*`"]
    c3m2["`\*`"]
    c3 --> c3m0
    x3 --> c3m0
    x3 --> c3m1
    x3 --> c3m1
    c3m0 --> c3m2
    c3m1 --> c3m2

    c2m0["`\*`"]
    c2m1["`\*`"]
    c2 --> c2m0
    x2 --> c2m0
    c2m0 --> c2m1
    x2 --> c2m1

    c1m0["`\*`"]
    c1 --> c1m0
    x1 --> c1m0

    a0["`\+`"]
    a1["`\+`"]
    a2["`\+`"]
    c3m2 --> a0
    c2m1 --> a0
    c1m0 --> a1
    c0 --> a1
    a0 --> a2
    a1 --> a2

    a2 --> Output
</pre>
<figcaption>
Data-flow graph of the na&iuml;ve cubic evaluation algorithm. The "*" nodes
multiply their two inputs, while the "+" nodes add them. Furthermore, the input
@@x@@ is duplicated and used in multiple places.
</figcaption>
</figure>

A better idea is to use [Horner's Scheme][3], which decomposes @@p@@ as

%% p(x) = ((c_3 \cdot x + c_2) \cdot x + c_1) \cdot x + c_0. %%

It has a longer critical path, at three multipliers and three adders. But, it
uses less area --- just the three multipliers and three adders. Possibly for
that reason, this was the initial scheme used in MINOTAUR. Area is particularly
important for its vector unit. Most of its operations are performed on 32-wide
vectors, pipelined and in parallel. So, any area savings are multiplied by 32.

<figure>
<pre class="mermaid">
flowchart TB
    x3["`*x*`"]
    x2["`*x*`"]
    x1["`*x*`"]

    c0["`*c<sub>0</sub>*`"]
    c1["`*c<sub>1</sub>*`"]
    c2["`*c<sub>2</sub>*`"]
    c3["`*c<sub>3</sub>*`"]

    c3m["`\*`"]
    c2a["`\+`"]
    c3 --> c3m
    x3 --> c3m
    c3m --> c2a
    c2 --> c2a

    c2m["`\*`"]
    c1a["`\+`"]
    c2a --> c2m
    x2 --> c2m
    c2m --> c1a
    c1 --> c1a

    c1m["`\*`"]
    c0a["`\+`"]
    c1a --> c1m
    x1 --> c1m
    c1m --> c0a
    c0 --> c0a

    c0a --> Output
</pre>
<figcaption>
Data-flow graph of Horner's Scheme.
</figcaption>
</figure>

Another improvement over the na&iuml;ve approach is to use [Estrin's Scheme][4],
which instead recursively factorizes @@p@@ as

%% p(x) = x^2 \cdot (c_3 x + c_2) + (c_1 x + c_0). %%

In total, Estrin's Scheme uses four multipliers and three adders. Its critical
path consists of two multipliers and two adders. In other words, for just an
additional multiplier compared to Horner's Scheme, this algorithm improves on
its critical path by a full Multiply-Accumulate (MAC). And in fact, when this
approach was implemented in MINOTAUR, it saved area over Horner's Scheme. Its
shorter critical path allowed the pipeline depth to be reduced by one stage,
eliminating an entire set of pipeline registers.

<figure>
<pre class="mermaid">
flowchart TB
    xsq["`*x*`"]
    xl["`*x*`"]
    xr["`*x*`"]

    sq["`\*`"]
    xsq --> sq
    xsq --> sq

    c3["`*c<sub>3</sub>*`"]
    c2["`*c<sub>2</sub>*`"]
    ml["`\*`"]
    al["`\+`"]
    c3 --> ml
    xl --> ml
    ml --> al
    c2 --> al

    c1["`*c<sub>1</sub>*`"]
    c0["`*c<sub>0</sub>*`"]
    mr["`\*`"]
    ar["`\+`"]
    c1 --> mr
    xr --> mr
    mr --> ar
    c0 --> ar

    mt["`\*`"]
    at["`\+`"]
    sq --> mt
    al --> mt
    mt --> at
    ar --> at

    at --> Output
</pre>
<figcaption>
Data-flow graph of Estrin's Scheme.
</figcaption>
</figure>

The above approaches were actually synthesized in MINOTAUR. It's possible that
they leave performance on the table though. Specifically, note that all the
algorithms given above take the "raw" coefficients @@c_3@@, ..., @@c_0@@ as
input. But, Wikipedia's page on [Polynomial Evaluation][5] points out that
pre-processing these coefficients can decrease the number of multipliers and
adders required. [Knuth's Algorithm][6] provides a concrete way to do that.

Knuth's Algorithm points out that, by applying polynomial long-division, we can
write

%% p(x) = (x^2 + \alpha) (k_1 x + k_0) + \beta x + \gamma, %%

for some set of constants. The only knob we have is @@\alpha@@; once it's fixed,
the divisor @@x^2 + \alpha@@ is set and the rest of the constants can be
determined. The key idea is to judiciously set @@\alpha := \alpha^*@@ such that
@@\beta = 0@@. This can be done by picking

%%
\begin{align\*}
    \alpha^\* &= \frac{c_1}{k_1^\*} \nl
    \gamma^\* &= c_0 - \alpha^\* k_0^\* \nl
    k_1^\* &= c_3 \nl
    k_0^\* &= c_2,
\end{align\*}
%%

which works so long as @@c_3 \neq 0@@. That case can be worked around for
MINOTAUR. A few multiplexers can be used to reconfigure the existing multipliers
and adders for Knuth's Algorithm to implement Horner's Scheme on quadratics. In
the end, Knuth's Algorithm prescribes

{% highlight python %}
def preprocess(c: list[float]):
    cubic = c[3] != 0
    if cubic:
        k1 = c[3]
        k0 = c[2]
        α = c[1] / k1
        ɣ = c[0] - α * k0
    else:
        k1 = c[2]
        k0 = c[1]
        α = float('nan') # Don't care
        ɣ = c[0]
    return (cubic, k1, k0, α, ɣ)

def hardware(
    x: float,
    cubic: bool,
    k1: float, k0: float, α: float, ɣ: float,
) -> float:
    quotient = k1 * x + k0
    divisor = x * x + α
    whole = quotient * divisor if cubic else quotient
    return whole + ɣ

def evaluate(x: float, c: list[float]) -> float:
    return hardware(x, *preprocess(c))
{% endhighlight %}

Ignoring MUX overhead, it requires three multipliers and three adders, and it
has a critical path of two multipliers and two adders. Thus, it is strictly
better than both Horner's and Estrin's Schemes. It does require preprocessing,
but that's okay for MINOTAUR.

<figure>
<pre class="mermaid">
flowchart TB
    xq["`*x*`"]
    xd["`*x*`"]

    k1["`*k<sub>1</sub>*`"]
    k0["`*k<sub>0</sub>*`"]
    mq["`\*`"]
    aq["`\+`"]
    k1 --> mq
    xq --> mq
    mq --> aq
    k0 --> aq

    alpha["`α`"]
    md["`\*`"]
    ad["`\+`"]
    xd --> md
    xd --> md
    md --> ad
    alpha --> ad

    gamma["`ɣ`"]
    mt["`\*`"]
    at["`\+`"]
    aq --> mt
    ad --> mt
    mt --> at
    gamma --> at

    at --> Output
</pre>
<figcaption>
Data-flow graph of Knuth's Algorithm.
</figcaption>
</figure>

To close, even though none of the algorithms described here are entirely new,
they don't seem to be widely known. For instance, I independently rediscovered
Estrin's Scheme, and I came to Knuth's Algorithm myself after seeing a different
algorithm inspired by it in a source I have since lost. Furthermore in my
experience with MINOTAUR, Horner's Scheme is often treated as the "default"
approach for polynomial evaluation in hardware, even when other approaches might
be better. Either way, it was some work to find these algorithms, so hopefully
this post can save someone else from doing redoing it.

Another question that remains is whether Knuth's Algorithm is "optimal".
According to [CS 497][7] at UIUC ([mirrored][8]), it is known that Knuth's
Algorithm uses the lowest possible number of multiplications and additions
(or&nbsp;subtractions). But, it does not show that it achieves the best possible
critical path. As shown by Estrin's Scheme in MINOTAUR, it may be better to
optimize that instead of total area.

[1]: https://priyanka-raina.github.io/ "Priyanka Raina: Assistant Professor, Stanford University"
[2]: https://doi.org/10.1109/VLSITechnologyandCir46783.2024.10631515 "MINOTAUR: An Edge Transformer Inference and Training Accelerator with 12 MBytes On-Chip Resistive RAM and Fine-Grained Spatiotemporal Power Gating"
[3]: https://en.wikipedia.org/w/index.php?title=Horner%27s_method&oldid=1292763330 "Horner's method"
[4]: https://doi.org/10.1145/1460361.1460365 "Organization of computer systems: the fixed plus variable structure computer"
[5]: https://en.wikipedia.org/w/index.php?title=Polynomial_evaluation&oldid=1296426370#Evaluation_with_preprocessing "Polynomial evaluation § Evaluation with preprocessing"
[6]: https://doi.org/10.1145/355580.369074 "Evaluation of polynomials by computer"
[7]: https://jeffe.cs.illinois.edu/teaching/497/08-polynomials.pdf "CS 497: Concrete Models of Computation - Spring 2003 - Evaluating Polynomials (March 10)"
[8]: /assets/2025/07/02/polynomials.pdf "CS 497: Concrete Models of Computation - Spring 2003 - Evaluating Polynomials (March 10)"
