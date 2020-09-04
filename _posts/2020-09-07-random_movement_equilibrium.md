---
title: Equilibrium in Normal  Random Movement
libs: [mathjax]
---

<div class="mathjaxDeclarations">
    @@\newcommand{\nl}{\\}@@
</div>

In my last post [last post]({{page.previous.url}}), I touched on my efforts to
model how a simple "virus" moves through a population, mainly through the lens
of differential equations. As part of that, I wanted to test my model of how the
population moves over time. Intuitively, we'd expect the dynamics to follow the
[Diffusion Equation](https://en.wikipedia.org/wiki/Diffusion_equation), which
reduces to the [Heat Equation](https://en.wikipedia.org/wiki/Heat_equation) if
the diffusivity is constant throught the domain.

![Equilibrium of my simulated diffusion](/assets/2020/09/07/clip_nofilter.png)
Imagine my surprise, then, when I simulated the population to a steady state and
got the above distribution. It's inconsistent with the heat equation --- we'd be
expecting a uniform equilibrium distribution from that. Instead, we get "clumps"
on the edges of the simulation domain, as well as a "rarefaction" near them.

Granted, the result makes sense. Look at the code that moves people around:
{% highlight python %}
dx = np.random.normal(scale=MOVE_SIGMA, size=(POP_SIZE,))
population += dx
population = np.clip(population, 0.0, 1.0)
{% endhighlight %}
A given person has a non-zero probability of winding up exactly on the boundary,
unlike everywhere else in the domain. Really, the bounaries are accumulating
everyone who overstepped them.

The rarefactions are somewhat harder to explain. The best I can come up with is
to compare it to the "unbounded" case. Imagine the simulation domain streteched
to infinity in both directions. Then, with every person moving according to a
normal distribution, having a constant population density would be an
equilibrium state. When we bound the domain, however, we lose the contribution
of everyone outside. This becomes especially noticible near the edges, where
almost half of the influx would be coming from outside @@[0,1]@@.

Of couse, I find these "clipping artifacts" undesireable, and I looked for ways
to mitigate them. One idea I had was to reroll the positions of people who
overstepped instead of simply clipping them to the edge.
{% highlight python %}
dx = np.random.normal(scale=MOVE_SIGMA, size=(POP_SIZE,))
while True:
    population += dx
    outIdx = (population <= 0.0) | (population >= 1.0)
    numOut = np.sum(outIdx)
    if numOut != 0:
        population[outIdx] -= dx[outIdx]
        dx[~outIdx] = 0.0
        dx[outIdx] = np.random.normal(scale=MOVE_SIGMA, size=(numOut,))
    else:
        break
{% endhighlight %}
This did get rid of the people clumped to the edge, but it still left the
rarefactions. In fact, it actually made them much worse.
![Equilibrium with rerolling](/assets/2020/09/07/reroll.png)

On a side note, decreasing the variance for people's movement seemed to help
significantly. In my simulation, all the people moved according to a normal
distribution, and the above figures were collected with @@\texttt{MOVE_SIGMA} =
\sigma = 0.1@@. This value can be made arbitrarily small --- if, every second,
people move according to a normal distribution with variance @@\sigma^2@@,
simply do @@n@@ "runs" with variance @@\frac{1}{n}\sigma^2@@ to simulate one
second, where @@n@@ can be made arbitrarily large.

That works in theory, but not in practice. If we have a population of size
@@\texttt{POP_SIZE} = K@@ and we simulate for @@t@@ seconds, then simulating
takes @@\mathcal{O}(ntK)@@ time. That's not great, especially since two of those
parameters are being made really large. However, we only really want to see the
equilibrium state for now, and it might be better to calculate it rather than to
simulate it out.

To do this, we can start by formalizing the problem we are trying to solve. I'll
consider the case where we clip the people to the edges of the domain, and the
case where we reroll can be built on top of it. First, notation. I'm using
slightly non-standard names here:
%%\begin{align\*}
\varphi(x \mid \mu) &= \frac{1}{\sqrt{2\pi\sigma^2}} \, \exp\left( -\frac{(x-\mu)^2}{2\sigma^2} \right) \nl
\phi(x \mid \mu) &= \int_{-\infty}^x \varphi(t \mid \mu) dt
\end{align\*}%%
