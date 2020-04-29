---
title: Some Thoughts on Fundamental Groups
libs: [mathjax]
---

<div class="mathjaxDeclarations">
    @@\newcommand{\nl}{\\}@@
</div>

During a Multivariable Calculus review session, we were talking about simply
connected sets. That is, sets where loops can be continuously "contracted" down
to a point without stepping outside the set itself. For instance, in the image
below, the set on the left is not simply connected, while the set on the right
is.
![A non-simply connected set and a simply connected set](/assets/2020/04/27/simply_connected.svg)
In the context of Multivariable Calculus, whether or not a set is simply
connected has consequences for vector fields defined on it. For instance, a
conservative vector field is only guaranteed to be curl-less on a simply
connected domain.

During the review session, my TA offhandedly mentioned that simply connected
spaces have trivial fundamental group. Of course, I didn't know what that meant,
so I read the [Wikipedia article](https://en.wikipedia.org/wiki/Fundamental_group).
It starts by defining loop homotopy --- intuitively, whether one continuous loop
can itself be continuously deformed into another. It claims homotopy is an
equivalence relation, and its not hard to see why. Any loop @@\gamma@@ is
homotopic to itself under @@h(r,t) = \gamma(r)@@ for all @@t@@. If @@\gamma_1@@
is homotopic to @@\gamma_2@@ under @@h(r,t)@@, then the reverse is true under
@@h(r,1-t)@@.  Finally, if @@\gamma_1@@ is homotopic to @@\gamma_2@@ under
@@h@@, and @@\gamma_2@@ is homotopic to @@\gamma_3@@ under @@g@@, then we may
define a homotopy between @@\gamma_1@@ and @@\gamma_3@@ as 
%% f(r,t) = \begin{cases}
    h(r,2t) & t \leq \frac{1}{2} \nl
    g(r,2t-1) & t \geq \frac{1}{2} 
\end{cases}, %%
which is continuous despite being peicewise.

The article goes on to consider the equivalence classes under this relation. It
then defines a group on those classes, where the operation is concatenating
loops. Checking that the group law is well defined is fairly straightforward ---
just consider arbitrary representatives from each class, then construct
peicewise the required homotopy between their products. More interesting,
however, is that the article notes that the choice of the point on which to
"base" the loops doesn't matter when the space is path connected. Why?  If we
have a loop @@\gamma_0@@ with endpoint @@x_0@@, and there is a path @@C@@
starting at @@x@@ and going to @@x_0@@, then we can "pull out" @@C@@ from
@@\gamma_0@@ to construct a homotopy, as shown below.
!["Rebasing" a loop](/assets/2020/04/27/rebasing_loop.svg)
We might formally write down this function between @@\gamma_0@@ and our new loop
@@\gamma@@ (though its somewhat messy)
%% h(r,t) = \begin{cases} 
    C\left( 3\left(r - \frac{t}{3}\right) + 1 \right) & r \leq \frac{t}{3} \nl
    C\left( -3\left(r - \left(1 - \frac{t}{3}\right)\right) + 1 \right) & r \geq 1 - \frac{t}{3} \nl
    \gamma_0\left( \frac{1}{1-\frac{2t}{3}}\left(r - \frac{t}{3}\right) \right) & \text{otherwise}
\end{cases}. %%
This shows @@[\gamma_0] \subseteq [\gamma]@@, implying equality.

Given this structure, what my TA was saying makes sense. Simply connected spaces
have only one homotopy equivalence class! Every loop is homotopic to the
constant loop --- the one that starts at a point and stays there for all @@t@@.
The choice of point doesn't matter either since simply connected spaces are path
connected by assumption. However, the fact every loop can be "contracted" in
some way doesn't necessarily guarantee it can be done in a "natural" way. It
might be worth looking at exactly how exotic these homotopies can get.
