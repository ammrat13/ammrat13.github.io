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
# From 01-initial_processing
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

![Plot of Part of the Signal](/assets/2021/02/06/zres_img/signal_time.svg)

It became clear that I wouldn't have to demodulate the signal. There weren't any
smooth sine curves like I'd expect the actual transmission to have. So, I went
on assuming that the transmission was already demodulated, with each float
presumably corresponding to a single bit. That is, the recon team did the first
step of BPSK demodulation for us, then sampled it using a bit-clock, but just
didn't convert it to binary. (Note that I did the task before the clarification
about one bit per float was given.)

To make the rest of the sections easier to follow, I'll diverge a bit from my
process while I was solving the problem. I'll make a file that just contains a
"bitstring" of the data. I use quotes since I'm just going to use the ASCII
characters "0" and "1" to represent the data. Having this makes the following
code much easier to follow. The actual Python code to do this is very much like
the initial decoding step. The inner part of the loop is the only change.
{% highlight python %}
# From 02-to_bitstring
for f in float_iter:
    print(1 if f[0] > 0 else 0, end='')
{% endhighlight %}

Coming back to my actual workflow, at this point it was simply a question of
getting details about the Hamming code the signal used. I'd recently watched
[3Blue1Brown's video on Hamming codes][4]. It introduced the concept very well,
and gave me a few takeaways useful in this task. One was that Hamming codes use
blocks of size @@2^r@@ or @@2^r-1@@. So, if the signal was Hamming encoded, I'd
expect its length to have factors of that form:
{% highlight python %}
sage: divisors(9572547)
[1,
 3,
 17,
 51,
 61,
 ...
{% endhighlight %}

The only factors of @@9\,572\,547@@ that looked promising were @@3=2^2-1@@ and
@@17=2^4+1@@. I first tried @@3@@ since it was the only factor that fit the
required form exactly. A Hamming code on three bits is just the three-bit
repetition code, so I quickly implemented that in Python. The script outputs
ASCII "0"s and "1"s, so I converted it to a sequence of bytes by piping the
result through the Perl command I found on [StackExchange][5].

{% highlight python %}
# From 03-three_bit_code
import sys

file_name = sys.argv[1]
file_handle = open(file_name, 'r')

# While the file has stuff in it
while True:
    # Check if we’re done
    bit_chars = file_handle.read(3)
    if len(bit_chars) != 3:
        break

    # Check which bit is in the majority
    bit_ints = map(lambda c: int(c) - int(b'0'), bit_chars)
    sum_over = sum(bit_ints)
    print(1 if sum_over >= 2 else 0, end='')
{% endhighlight %}

{% highlight bash %}
$ perl -pe 'BEGIN { binmode \*STDOUT } chomp; $_ = pack "B*", $_'
{% endhighlight %}

Unsuprisingly, this didn't work. I just got garbage data out the other end. So,
I reasoned that the data probably came in packets of seventeen, with some extra
padding in each group. To actually see how this might be being done, I took my
"bitstring" and `fold`ed it to seventeen characters.
{% highlight bash %}
$ cat 02-to_bitstring/result.txt | fold -w 17 | head
01010010010110110
01001010001011110
10010001100110110
11000101101111010
00000000101110110
10000000001101000
00000101010101010
11001001001100110
00100000010011000
01100010010100010
{% endhighlight %}

I quickly noticed that the last bit in each group of seventeen was almost always
zero, and I assumed that it was just a padding bit. Using this, I was able to
approximate the error rate in this data. There were @@689@@ lines ending with a
padding bit of one and @@563\,090@@ lines total, giving an error probability of
about @@0.12\%@@ per bit. More importantly, I now had groups of sixteen, a
common size for Hamming codes. I assumed the data was using a @@(15,11)@@
Hamming code with an extra parity bit, backing this by the fact many lines had
even parity, as expected.

Now, I wanted to work out which bits were parity and which were data. I was
given that the code was systematic, and looking up the definition on
[Wikipedia][6] gives that the "plaintext" data appears inside the encoded data
somewhere. So, I made the assumption that the first few groups had no errors,
found an [online Hamming code calculator][7], and started plugging in
consecutive bits of the data.

I had no luck with this method. Counting the expected number of parity ones and
zeros seldom gave consistent matches. Slowly it dawned on me that the data
probably didn't use the "standard" Hamming code, and that I'd have to figure out
what it was using. Granted, this makes sense since the task asks for the
parity-check matrix, which wouldn't be very useful unless it was non-standard.

But before diving head-first into error correction, I wanted to make sure I was
at least on the right track. The Wikipedia article on [Hamming codes][8] gives
systematic code-generation and parity-check matricies for the @@(7,4)@@ case. It
seems that systematic Hamming codes have the left-most minor of @@\mathbf{G}@@
be the identity matrix, meaning the first @@11@@ bits (in our case) would be the
original data, assuming no errors. To test this, I took the first @@11@@ bits in
each group of @@17@@ and wrote the data into a file using the Perl command from
earlier.
{% highlight bash %}
$ cat 02-to_bitstring/result.txt                                        \
    | fold -w 17                                                        \
    | sed -E -e 's/[0-1]{6}$//g'                                        \
    | tr -d '\n'                                                        \
    | perl -pe 'BEGIN { binmode \*STDOUT } chomp; $_ = pack "B*", $_'   \
    > 04-sixteen_bit_code_no_correction/result.avi
{% endhighlight %}

Miraculously, this worked, kind of. It produced a file recognized as an AVI by
`file`. However, VLC complained that the file's index was missing, and trying to
play the video anyway resulted in garbage. Nonetheless, the fact that the magic
bytes were correct gave me the confidence to move forward with this form of
error correction.

To proceed, I first tried to find the code-generation matrix. I read a bit on
them, and most of the material was familar to me.
[3Blue1Brown's aforementioned video][4] mentioned XOR, priming me to think back
to my experience working with @@\mathbb{F}_2@@. Most of the Linear Algebra we
did in Georgia Tech's MATH 1564 was over @@\mathbb{R}@@, but we discussed how
the theory can be extended to an arbitrary field, so working over
@@\mathbb{F}_2@@ wasn't that much of a stretch.


[1]: <https://github.com/ammrat13/ammrat13.github.io/tree/master/assets/2021/02/06> "My GitHub"
[2]: <https://en.wikipedia.org/wiki/Half-precision_floating-point_format> "Half-precision Floating-point Format"
[3]: <https://bugs.python.org/issue11734> "Python Supports 16-Bit Floats"
[4]: <https://youtu.be/X8jsijhllIA> "Hamming Codes and Error Correction"
[5]: <https://unix.stackexchange.com/a/212208> "How can I convert two-valued text data to binary (bit-representation)"
[6]: <https://en.wikipedia.org/wiki/Systematic_code> "Systematic Code"
[7]: <http://www.ecs.umass.edu/ece/koren/FaultTolerantSystems/simulator/Hamming/HammingCodes.html> "Hamming Code"
[8]: <https://en.wikipedia.org/wiki/Hamming_code> "Hamming code"