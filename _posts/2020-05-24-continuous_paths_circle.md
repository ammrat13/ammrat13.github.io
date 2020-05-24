---
title: Parametrizing Continuous Paths on a Circle
libs: [mathjax]
---

I've been meaning to write this post for some time now, partially as a follow up
to my [last post]({{page.previous.url}}). I mentioned that winding numbers can
be thought of as the homotopy classes for loops around a point. I also said that
the fact winding numbers exist at all is not entirely obvious. Why? Well, how
might we define what a winding number is? We might parametrize a continuous path
@@\gamma: [0,1] \to \mathbb{R}^2\setminus\\{\mathbf{0}\\}@@ in polar
coordinates, then define the winding number of that path to be @@\frac{1}{2\pi}
\left(\theta(1) - \theta(0)\right)@@. That works, and that's the approach the
[Wikipedia article](https://en.wikipedia.org/wiki/Winding_number) uses, but it
also points out that, in order for this to work, @@\theta: [0,1] \to
\mathbb{R}@@ must be continuous.  To me, it's clear we _should_ be able to
construct a continuous @@\theta@@ for every path, but not entirely obvious _how_
exactly.

We'll start by "collapsing" the arbitrary path we're given down onto the unit
circle. Essentially, we ignore the path's radius @@r@@ since it doesn't matter
for its winding number's calculation. Thus, we want to find a way to
continuously (in @@\mathbb{R}@@) parametrize continuous paths on a circle (in
@@\mathbb{R}/2\pi\mathbb{Z}@@).

Perhaps the most straightforward way to do this would be as follows. Take a
continuous path on the unit circle @@\gamma@@ and consider @@f_0@@ the "natural"
map from the circle to @@[-\pi, \pi]@@, shown below. Obviously, just taking
@@f_0(\gamma)@@ would break continuity as soon as @@\gamma@@ "wraps around" the
far side of the circle. There would be a discontinuous jump from @@\pi@@ to
@@-\pi@@. To "patch" this, we can switch to using a different map at the point
of discontinuity. For instance, at a point where @@\gamma@@ wraps around the
circle and @@f_0@@ switches from positive to negative, we switch to using @@f_1
= f_0 + 2\pi@@. Similarly, if @@\gamma@@ wraps off the circle going down, switch
to @@f_{-1} = f_0 - 2\pi@@. In general, if you are using @@f_n = f_0 + 2n\pi@@
as your current map and @@\gamma@@ "wraps around," switch to using @@f_{n+1}@@
if it wraps going up or @@f_{n-1}@@ if it wraps going down.

That approach kind of works. One drawback is that @@f_0@@ maps the far side of
the circle to both @@\pi@@ and @@-\pi@@. We'd have to arbitrarily choose one
then carefully define what exactly it means to wrap going up or wrap going down.
We wouldn't be able to use the same definition in both cases. Perhaps more
pressing is that this approach requires us to step through all the map
transitions. It's very possible for there to be infinitely many such
transitions. For example, consider a path that behaves somewhat like the
function @@x\sin(x^{-1})@@, graphed below. A calculation that relies on stepping
through all of the transitions would likely be ill-defined.

After some thinking, you might realize that we don't necessarily need to map one
point on the circle to _just_ one point in @@\mathbb{R}@@. We could instead
"double cover" some parts of the unit circle, as shown below. I'll say that the
ends of the cover are open -- that we don't include @@\pi+D@@ and @@-(\pi+D)@@
-- but I'm sure the following arguments would be very similar if I'd made it
closed. This double cover is nice, but we still need create an @@f_0@@ to
unambiguously map points on @@\gamma@@ to real numbers, and we resolve as
follows. In order for the path to enter the "ambiguous zone," it must've at some
prior time had @@f_0 = \pm(\pi-D)@@.  If it entered through the positive side,
use the positive "branch" of the map, otherwise use the negative branch.

That works in the absence of map transitions, and with careful definitions, we
can get it to work in their presence as well. We define a map transition upward
as the path exiting the ambiguous zone with @@f_0@@ arbitrarily close to
@@\pi+D@@, and a map transition downward as exiting arbitrarily close to
@@-(\pi+D)@@. Clearly, these are the only two ways for a continuous path to exit
the ambiguous zone to introduce a discontinuity into @@f_0@@. Moreover, on exit
we attain @@f_0 = \pm(\pi-D)@@, which allows the definition from the last
paragraph to work through transitions.

Again, we keep a counter in @@n@@ and use @@f_n = f_0 + 2n\pi@@, incrementing
@@n@@ on a transition upward and decrementing on a transition downward. With the
new definition for map transitions, we are guaranteed to have only finitely many
of them. Why? Suppose we had infinitely many transitions, and thus a point about
which map transitions are "dense." Consider a point just after a transition,
where @@f_0(\gamma(t)) = \pm(\pi-D)@@. In order for another transition to
happen, we must have at some time @@s@@ in the future @@f_0(\gamma(s)) =
\mp(\pi-D)@@, exactly @@2D@@ away on the circle. However, this can never happen
infinitely often since @@\gamma@@ is continuous.

Thus, we can, in a well-defined manner, create a continuous function in
@@\mathbb{R}@@ to parametrize a continuous path on a circle. At least, I think
we can. I used IVT and other properties of continuous functions without
explicitly mentioning them in the above argument. Indeed, I may have glossed
over too much and, for instance, accidentally ignored a condition or an edge
case. Nonetheless, I'm fairly sure this approach can be made into a more formal
proof.

Here more than ever, I feel that I'm missing a lot of machinery. For instance,
my idea of covering the unit circle seems at least superficially to the idea of
an [atlas](https://en.wikipedia.org/wiki/Atlas_(topology)), though I can't say
for sure because I don't yet know much about it. Again, I look forward to
learning higher math, though I don't know if I'll ever be able to.
