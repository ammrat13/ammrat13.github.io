---
title: Faster Cubic Evaluation
tags: ["mathematics", "algorithms"]
libs: ["mathjax", "mermaidjs"]
libs_config:
    mermaidjs:
        flowchart:
            padding: 0
            nodeSpacing: 25
            rankSpacing: 25
---

It's been a while; a lot's happened. I got accepted to Stanford's MS CS program,
and I even graduated from there last month. During my last quarter there, I took
*EE 372: Design Projects in VLSI Systems II*. In the iteration of the course I
took, [Priyanka][1] essentially gave us the source code for [MINOTAUR][2], and
asked us to improve it in whatever way we saw fit. I mainly focused on improving
the vector unit --- the part of the accelerator that handles activations,
element-wise operations, and other low arithmetic-intensity tasks.

I was not the only one working on the vector unit though. Another group looked
at changing the strategy it used to evaluate activation functions. Ultimately,
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
eliminating one set of pipeline registers.

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

    c3["`*c<sub>3</sub>*`"]
    c2["`*c<sub>2</sub>*`"]
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
algorithms given above take in the "raw" coefficients @@c_3@@, ..., @@c_0@@ as
input. But, Wikipedia's page on [Polynomial Evaluation][5] points out that
pre-processing these coefficients can decrease the number of multipliers and
adders required.

[1]: https://priyanka-raina.github.io/ "Priyanka Raina: Assistant Professor, Stanford University"
[2]: https://doi.org/10.1109/VLSITechnologyandCir46783.2024.10631515 "MINOTAUR: An Edge Transformer Inference and Training Accelerator with 12 MBytes On-Chip Resistive RAM and Fine-Grained Spatiotemporal Power Gating"
[3]: https://en.wikipedia.org/w/index.php?title=Horner%27s_method&oldid=1292763330 "Horner's method"
[4]: https://doi.org/10.1145/1460361.1460365 "Organization of computer systems: the fixed plus variable structure computer"
[5]: https://en.wikipedia.org/w/index.php?title=Polynomial_evaluation&oldid=1296426370#Evaluation_with_preprocessing "Polynomial evaluation § Evaluation with preprocessing"
