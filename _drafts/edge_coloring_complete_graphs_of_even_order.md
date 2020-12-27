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

I started as I usually do, taking small examples and trying to find some
pattern. One of the first things I noticed was that a greedy algorithm wouldn't
always work. In the case above, for example, a greedy approach fails on the
second row. After taking @@\\{1,3\\}@@, the algoritm takes @@\\{2,4\\}@@ then is
forced to repeat @@\\{5,6\\}@@. There might've been some ordering with which
this approach would work, and we see later that this is the case, but I decided
to look elsewhere.

Another pattern I noticed had to do with the first and last lines in the
arrangement above. It's not immediately obvious from the figure, so consider the
"re-arrangement" below.

%%
\begin{align\*}
\\{1,2\\} \, \\{3,4\\} \, \\{5,6\\} \nl
\\{2,3\\} \, \\{4,5\\} \, \\{1,6\\}
\end{align\*}
%%

The first row contains subsets of adjacent numbers starting at @@1@@ and going
up. The same is true for the last row, except it starts at @@2@@ (and wraps
around). Another way see this arrangement is to start by taking the sets with
adjacent elements in the "natural" order --- @@\\{1,2\\}@@, @@\\{2,3\\}@@, all
the way up to @@\\{6,1\\}@@ --- then to, place all these sets, alternating the
rows as we go. This was a nice observation, but I couldn't immediately elaborate
on it. But, I would later use it in a different form.

Most of my effort focused on looking for some recursive pattern --- some way to
create the case of @@n+2@@ from that of @@n@@. Initially, the problem would seem
to lend itself to induction. The structure above, with the subsets @@\\{1,x\\}@@
along the right side, looked convenient to work with, and I tried inducting with
that. I put the sets @@\\{1,2\\}@@ along the first @@n-3@@ rows, then worked to
"swap" the @@2@@ with some other number, using the remaining @@2@@ rows to put
the "destroyed" sets in. I spent a lot of time here, but couldn't quite get it
to work.

---

<figure>
%%
\begin{align*}
\begin{pmatrix} 2 & 1 & 4 & 3 & 6 & 5 \end{pmatrix} \nl
\begin{pmatrix} 3 & 5 & 1 & 6 & 2 & 4 \end{pmatrix} \nl
\begin{pmatrix} 4 & 6 & 5 & 1 & 3 & 2 \end{pmatrix} \nl
\begin{pmatrix} 5 & 4 & 6 & 2 & 1 & 3 \end{pmatrix} \nl
\begin{pmatrix} 6 & 3 & 2 & 5 & 4 & 1 \end{pmatrix} \nl
\end{align*}
%%
<figcaption>
The same arrangement as the last figure, but framed in terms of permutations
</figcaption>
</figure>

That's not to say I didn't make progress, though. One effective way I found to
think about this problem was to think of each set as a permutation, specifically
a two-cycle. Each day (row), then, is a product of two-cycles, and we're given
the constraint that each column must be a permutation as well. This process
gives a nice table, which I find easier to think about.

One observation I made soon after was the existence of "three-cycles". In the
example above, we have the two-cycle @@\begin{pmatrix}1&2\end{pmatrix}@@ on day
one, and @@\begin{pmatrix}1&3\end{pmatrix}@@ on day two. This implies that
@@\begin{pmatrix}2&3\end{pmatrix}@@ cannot be on days one or two, and must be on
some other day (five in this case). I thought this could be made into some
algorithm to arrange the cycles with. But, I gave up on it after realizing how
much overlap there would be between different three-cycles. Again, I would see
this observation later, but in a different form.

Another observation arising from this framing, one which I found quite powerful
even though it didn't necessarily mean anything, was the idea of "pointing". For
example, in the above arrangement, the @@1@@ on the first row is paired with
@@2@@ (the first column of the first row has a @@2@@), so it can be seen as
pointing to the @@2@@ (the second column) on the *second* row. Similarly, the
@@2@@ on the second row points to the @@5@@ on the *third* row, and so on until
we hit the last day. Repeatedly following these pointers gives "paths",
@@(1,2,5,3,6)@@ in this case. This path is "good" since it didn't repeat any
numbers. That's good since the recursive construction from the last section, the
one involving @@\\{1,x\\}@@ sets, could probably be made to work with it.

<figure>
<img src="/assets/2020/12/31/pointing_paths.svg">
<figcaption>
    A visualization of the two paths from the example above. The red arrows show
    a good path, and the blue arrows show a bad one
</figcaption>
</figure>

Of course, the days can be reordered as needed to give favorable results.
Nonetheless, I couldn't quite get this approach to work. I couldn't prove the
existence of some day-ordering and some initial number which would give a good
path. I also tried shoe-horning new-days into existing paths, regardless of
whether they were good or bad, but I didn't have much luck with that either.

---
