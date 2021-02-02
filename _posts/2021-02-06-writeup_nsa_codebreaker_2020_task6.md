---
title: "NSA Codebreaker 2020 Writeup: Proof of Life"
libs: [mathjax]
---

*This post is lifted from a letter I wrote to Mr. Todd Mateer, the designer of
Task 6 for NSA Codebreaker 2020. I was one of the first to solve it, and he
inquired about my approach. The relevant files supporting files can be found on
my [GitHub][1]*

> **Task 6 - Proof of Life (1300 Points)**
>
> Satellite imaging of the location you identified shows a camouflaged building
> within the jungle. The recon team spotted multiple armed individuals as well
> as drones being used for surveillance. Due to this heightened security
> presence, the team was unable to determine whether or not the journalist is
> being held inside the compound. Leadership is reluctant to raid the compound
> without proof that the journalist is there.
>
> The recon team has brought back a signal collected near the compound. They
> suspect it is a security camera video feed, likely encoded with a systematic
> Hamming code. The code may be extended and/or padded as well. We've used BPSK
> demodulation on the raw signal to generate a sequence of half precision
> floating point values. The floats are stored as IEEE 754 binary16 values in
> little-endian byte order within the attached file. Each float is a sample of
> the signal with 1 sample per encoded bit. You should be able to interpret this
> to recover the encoded bit stream, then determine the Hamming code used. Your
> goal for this task is to help us reproduce the original video to provide proof
> that the journalist is alive and being held at this compound.
>
> * [Collected Signal (`signal.ham`)](/assets/2021/02/06/challenge/signal.ham)

---

Mr. Mateer,

Thank you again for reaching out to me about Task 6. I'm fairly new to
college-level CTFs, so it means a lot that you're commending my efforts. As you
suggested, I'll document here my thought process when solving the problem, and
tell you about what little background I have in coding theory.

To start, I wanted to take the signal we were given and make it into something
more readable. So, I wrote a simple Python program to parse each of the 16-bit
floats and print them out. I was worried I'd have to write a parser myself,
based off the Wikipedia article on the [Half-precision Floating-point Format][2]
but thankfully Python's `struct` library supports 16-bit floats
[since Python 3.6][3].

{% highlight python %}
import struct
import sys

file_name = sys.argv[1]
file_contents = open(file_name, 'rb').read()
float_iter = struct.iter_unpack('<e', file_contents)
for f in float_iter:
    print(f[0])
{% endhighlight %}

The result of this was a long list of floats, as expected. I didn't notice that
the task stated the signal had already been demodulated, so I went and tried to
plot the floats as a waveform. I thought the signal was still BPSK encoded and
that I'd have to demodulate it, so I wanted to at least see the data before
working with it.


[1]: <https://github.com/ammrat13/ammrat13.github.io/tree/master/assets/2021/02/06> "My GitHub"
[2]: <https://en.wikipedia.org/wiki/Half-precision_floating-point_format> "Half-precision Floating-point Format"
[3]: <https://bugs.python.org/issue11734> "Python Supports 16-Bit Floats"
