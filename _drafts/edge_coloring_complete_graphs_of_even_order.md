---
title: Edge Coloring Complete Graphs of Even Order
libs: [mathjax]
---

<div class="mathjaxDeclarations">
    @@\newcommand{\nl}{\\}@@
</div>

Recently, I rediscovered a special case of [Baranyani's
Theorem](https://en.wikipedia.org/wiki/Baranyai%27s_theorem). Specifically, I
found the case of @@r=2@@, a result which has apparently been known since the
1800s. It states that every complete graph with an even number of vertices @@n@@
has a proper [edge coloring](https://en.wikipedia.org/wiki/Edge_coloring) with
@@n-1@@ colors. Alternatively, it is possible to partition the edges of @@K_n@@
into @@n-1@@ sets (colors) such that no two edges in the same set share an
endpoint. Clearly, this is the least possible number of colors --- each vertex
has @@n-1@@ distinct edges going out of it. The theorem states that, for even
@@n@@, it is possible to attain this minimum.

---

I actually discovered this fact in a context completely separate from graph
theory. This semester, I served as a TA for [CS
2110](http://www.icc.gatech.edu/files/syllabus/undergrad/CS-2110_Syllabus.pdf)
at Georgia Tech. It was fun, though time consuming, and I thought a lot about
how to best teach struggling students. I remembered that pair programming is a
common technique used to teach new developers, but it could never be implemented
in the course. Nonetheless, I went on a tangent thinking about how one could
implement pair programming in a class. Ideally, the same students wouldn't work
together all the time --- usually the teacher would mix students around. How
long it would take before we're forced to repeat, and a student is paired with
someone they've already worked with?

I assumed the number of students @@n@@ was even for simplicity. Each day, we
take @@\frac{1}{2}n@@ subsets of size two, making sure none of them share an
element. We want to never repeat subsets. In that case, the longest we can
sustain this process is clearly

%%
\frac{\text{# Total Subsets}}{\text{# Subsets per Day}}
= \frac{\binom{n}{2}}{\frac{1}{2}n}
= n-1
%%

days. I still had to show that it can't be shorter, though, and that's what I
then set out to do.

---

<figure>
%%
\begin{align*}
\{1,2\} \, \{3,4\} \, \{5,6\} \nl
\{1,3\} \, \{2,5\} \, \{4,6\} \nl
\{1,4\} \, \{2,6\} \, \{3,5\} \nl
\{1,5\} \, \{2,4\} \, \{3,6\} \nl
\{1,6\} \, \{2,3\} \, \{4,5\}
\end{align*}
%%
<figcaption>
Grouping six people into distinct pairs over five days
</figcaption>
</figure>
