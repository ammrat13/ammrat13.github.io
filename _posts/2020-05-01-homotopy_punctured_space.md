---
title: Fundamental Groups in Punctured Space
libs: [mathjax]
---

When learning concepts in math, I often find it helpful to look at "toy"
examples. They help me more intuitively see facts about the objects I'm looking
at. All of this is true for Fundamental Groups, which is what my [last
post]({{page.previous.url}}) was about. I found a simple example to be the
plane with some points removed from it --- as if I'd come along with a dart and
poked holes in @@\mathbb{R}^2@@.

It's actually a lot more useful than it might initially seem. Suppose we have
some region that's simply connected save for some "sufficiently nice" holes. We
can pick one of the holes and deform the set such that the hole becomes a disk.
This is guarunteed to be possible if the border of the hole can be parameterized
by [Jordan-Schoenflies](https://en.wikipedia.org/wiki/Schoenflies_problem).
Then, we might contract the hole down to a point if it's open, or contract it
arbitrarily small if it's closed. We could finally repeat this process on all
the other holes, ending up with some subset of a "punctured plane."
![Contracting holes in a set](/assets/2020/05/01/contracting_holes.svg)

At least, that's the intuition. It's far from complete --- there's still work to
do in the case of a closed hole. Perhaps to make our efforts more concrete, we
can focus on @@\mathbb{R}^2@@ with some disk (either open or closed and possibly
of zero radius) removed. It's clear the fundamental group of this space is
@@\mathbb{Z}@@. Why? Since a loop never goes through the origin, we can write
all its points in terms of polar coordinates @@\gamma(s) = (r,\theta)@@, then
collapse them all to a fixed @@R@@ as
%% h(s,t) = (Rt + r(1-t), \theta).  %%
Thus, the every loop is homotopic to one on a fixed circle, whose fundamental
group is known to be @@\mathbb{Z}^+@@. Indeed, that's where we get the concept
of [winding numbers](https://en.wikipedia.org/wiki/Winding_number).  However, it
may not be obvious that this is true (it certainly wasn't to me). I might try to
prove it formally in a later post.

So that's the case of one hole, but what if there's multiple holes? I don't know
how to do this formally, but here's a possible approach. We might start by
segmenting the plane into "sectors," each containing one hole. If they're are
all isolated points, this is always possible since there are only finitely many
of them. If not, you might have to argue based off the fact the holes can be
made arbitrarily small.

![Contracting a loop](/assets/2020/05/01/contracting_loop.svg)
We might then take an arbitrary loop and "contract" it along the sector division
lines, as shown above. The end result of this homotopy will be a loop @@\gamma@@
that only crosses sectors at the sectors' "base point" @@B@@. This clearly gives
rise to the same "winding" structure as earlier. If that's not obvious, do the
following.  In each sector pick a loop @@\ell_i@@ homeomorphic to a circle that
stays entirely in the sector and that goes through @@B@@. Then, similar to what
we did above, project each of @@\gamma@@'s "segments" onto their relevant
sector's loop @@\ell_i@@.

Looking at this construction, we may guess at the fundamental group for a
punctured plane with @@n@@ holes. You might start with @@\mathbb{Z}^n@@, but
then I'd point out that the order we wrap in would matter. For instance, in the
image above, wrapping around the bottom hole, then the top, then the bottom is
clearly different from wrapping around the bottom, then the bottom again, then
the top. Thus, we might conjecture that the fundamental group of this punctured
space is the [free group](https://en.wikipedia.org/wiki/Free_group) on @@n@@
elements.

How correct this reasoning is? How easy it is to formalize? How well it extends
to closed holes? I don't know. Fundamental groups are quite interesting, though,
and they raise a lot of questions. For instance, are all fundamental groups
free? What about on non-planar spaces, like tori or mobius strips? What if you
have an infinite number of "holes," as in @@\mathbb{R} \setminus \mathbb{Q}@@? I
don't have the machinery to answer these questions. I know nothing about
Topology, but I look forward to studying it in the future if I can.
