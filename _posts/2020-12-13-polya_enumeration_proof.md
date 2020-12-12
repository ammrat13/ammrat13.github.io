---
title: A Proof of Pólya's Enumeration Theorem
libs: [mathjax]
---

<div class="mathjaxDeclarations">
    @@\newcommand{\nl}{\\}@@
</div>

This semester, I took [MATH 3012](http://math.gatech.edu/courses/math/3012), a
discrete math course with Dr. Ernest Croot. It was an interesting class,
especially because discrete structures aren't discussed heavily in high-school
and early college math, despite them being a core part of computer science.

Until now, my main exposure to discrete math had been through math competitions,
and I was kind of bad at them. The counting problems always messed me up (since
I never practiced them). As such, combinatorics has always held a special place
in my heart --- a field of math that's widely applicable, but one that I'm not
good at.

Dr. Croot began the course by showing us a wide variety of problems in the
domain of discrete math. Stuff like simple counting problems, stars and bars,
graph coloring, the travelling salesman problem,&nbsp;&hellip;&nbsp;. One
problem he mentioned was counting colorings in the presence of symmetry. He gave
the example of a necklace and counting the distinct colorings on it with
rotational symmetry. I think he did an example with @@k@@ colors and @@3@@
beads, deriving the formula:

%% \frac{k^3 - k}{3} + k. %%

The first term counts the colorings where all the beads aren't the same color,
each generating three equivalent arrangements. The second term enumerates those
colorings where all beads are the same, where the coloring is thus invariant
under rotation.

Dr. Croot then asked us to think about the equivalent formulas for non-prime
numbers of beads, or when we allow for reflection. If the derivation in this
simple case was so complicated, just imagine how bad those would be! Just look
at the example below: four beads and two colors with a flip along the vertical
as symmetry. The case of just one bead is particularly ugly.
![The case of four beads and two colors under reflection](/assets/2020/12/13/colorings_reflection.svg)

My professor mentioned Pólya's Enumeration Theorem as an easier way. I noticed a
chapter of the same name in the textbook as well, though it was quite late in
the book and we wouldn't get around to it.

My gut reaction for finding a plan of attack. I read through Nathan Carter's
[Visual Group Theory](http://books.google.com?id=F_H3DwAAQBAJ) last semester,
and I was surprised as to how ubiquitous groups really are. Since they, in some
sense, represent the symmetry of a system, it felt intuitive to look at this
problem through the lens of group theory.

In particular, it felt like a good idea to look at all the subgroups of the
relevant symmetry group @@G@@. For a particular subgroup @@H@@, we might color
all the elements of a particular coset the same color, ensuring that not all
cosets share the same color. We would thus count (for @@k@@ colors)
%% \frac{k^{[G:H]} - k}{[G:H]} %%
distinct colorings for @@H \neq G@@, and @@1@@ otherwise.

There are several problems with this. First, we'd require that @@H \triangleleft
G@@ for this to work. We'd also have to somehow sum over all the normal
subgroups of @@G@@, which becomes difficult when subgroups contain each other.
But worst of all, it's not even counting the right thing! We need to count with
respect to the objects @@G@@ acts on, not @@G@@ itself!
