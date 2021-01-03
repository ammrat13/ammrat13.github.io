---
title: "CSAW CTF 2020 Finals Writeup: Eccentric"
libs: [mathjax]
---

<div class="mathjaxDeclarations">
    @@\newcommand{\FF}[1]{\mathbb{F}_{#1}}@@
</div>

I was a finalist for [CSAW CTF 2020](https://csaw.io). I was on the Mad H@tter's
team, and I swept the cryptography challenges. They were all interesting, and I
felt I'd write down some of my thoughts on them. Curiously, the challenge I
found most difficult was ranked the easiest. Thus, I'm devoting this entire post
to it.

> **Eccentric (100 Points)**
>
> 'Don't worry, I'm using ECC.' - every crypto script kiddy ever
>
> * `nc crypto.chal.csaw.io 5002`
> * [`handout.txt`](/assets/2021/01/15/challenge/handout.txt)

The handout specifies a finite field of prime order @@\FF{p}@@, as well as an
elliptic curve @@E@@ over it with the form @@y^2 = x^3 + ax + b@@. It also gives
us two points on the curve @@P = dG@@, and asks us to solve for the integer
@@d@@.

This is a [discrete-log problem](https://wikipedia.org/wiki/Discrete_logarithm),
which is hard to solve in general. In CTFs, however, there is generally some
additional structure in place to make the problem easier. For a challenge like
this, they might use a weak elliptic curve --- a curve in some class for which
there are known attacks. The challenge is often just finding and implementing
that exploit, hence the low point value.

Indeed, that is the case here. Plugging @@E@@ into SageMath gives that the
number of points on the elliptic curve @@\\#E@@ is equal to @@p@@.
[Wikipedia](https://wikipedia.org/wiki/Elliptic-curve_cryptography#Domain_parameters)
lists such curves as insecure, providing some references but sadly not
describing any attacks against them. It does, however, reference [a paper][1] by
Nigel Smart. Moreover, Smart's Attack shows up within the first few results of
Googling attacks on this class of curves.


[1]: </assets/2021/01/15/pdf/Smart.pdf> "The Discrete Logarithm Problem on Elliptic Curves of Trace One"
