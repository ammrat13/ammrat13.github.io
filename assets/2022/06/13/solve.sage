# CONFIGURATION VARIABLES: -----------------------------------------------------
# I was too lazy to implement command-line argument parsing, so you have to
# supply options through these variables.

# The modulus for the CRC
# Should be expressed in hexadecimal in the normal ordering, so bit 0 should
# correspond to the 1s place. The most significant digit should be left off.
MODULUS_RAW = 0x04c11db7

# Initial value of the CRC
# It turns out that this value is not reflected first. Keep that in mind.
INIT = 0xffffffff
# Whether the CRC reflects each input byte
REF_IN = True
# Whether the CRC reflects the output
REF_OUT = True
# What the CRC XORs the output by
XOR_OUT = 0xffffffff

# The target CRC
# This should be the output of the CRC algorithm, with REF_OUT and XOR_OUT
# applied if needed. Those transformations will be undone.
TARGET_RAW = 0x3c456de6

# What the output should start with
OUTPUT_START = b'DC'
# The two possible characters the output can have after OUTPUT_START
OUTPUT_CHARS_RAW = (b'G', b'T')


# ALGORITHM: -------------------------------------------------------------------

# The field over which we'll work
F.<x> = GF(2**32, modulus = (MODULUS_RAW | 2**32).digits(2))

# Utility function
def pad_to_length(to_pad, pad_with = 0, length = 32, left_side = False):
    padding = [pad_with] * (length - len(to_pad))
    return (padding + to_pad) if left_side else (to_pad + padding)

# Utility function
# Handling reflections is a bit counterintuitive. After the calls to digits and
# enumerate, the x**i term's coefficient is at index i. We reflect if needed by
# mapping index i -> length - 1 - i.
def word_to_polynomial(word, length = 32, reflect = False):
    dig_list = pad_to_length(Integer(word).digits(2), length = length)
    return sum(map(
        lambda iv: iv[1] * x**(iv[0] if not reflect else length-1-iv[0]),
        enumerate(dig_list)
    ))

# Compute the target as a polynomial over F
# Undo the post-processing to the output too.
target = word_to_polynomial(TARGET_RAW ^^ XOR_OUT, reflect = REF_OUT)

# Compute the CRC of the original message
# This takes several steps. First, we initialize the remainder according to
# INIT. It's shifted right 32 places to counter the left shifts that will happen
# later. Then, we shift in the starting characters, reflecting if needed.
# Remember that digits will reverse. Finally, we shift in the "extra"
# characters, again reflecting if needed. Lastly, we shift left 32 times.
plaintext = x**-32 * word_to_polynomial(INIT)
for c in OUTPUT_START + OUTPUT_CHARS_RAW[0] * 32:
    c_bits = pad_to_length(Integer(c).digits(2), length = 8)
    if not REF_IN:
        c_bits.reverse()
    for b in c_bits:
        plaintext *= x
        plaintext += b
plaintext *= x**32

# Compute the characters as polynomials
output_chars = tuple(map(
    lambda c: word_to_polynomial(c[0], length = 8, reflect = REF_IN),
    OUTPUT_CHARS_RAW
))

# Compute the RHS
# To do the linear algebra later, we have to convert it to a vector
y = (target - plaintext) / (x**32 * (output_chars[1] - output_chars[0]))
y_vec = vector(GF(2), pad_to_length(y.polynomial().list()))

# Compute the matrix of all the x**(8*i)
# We populate it row-wise, so we have to transpose
V_mat = matrix(GF(2), [
    pad_to_length((x**(8*i)).polynomial().list()) for i in range(32)
]).T

# Solve
a_vec = V_mat \ y_vec

# Pretty print the output
# Remember that index zero is the right-most character. We have to reverse it.
print(OUTPUT_START + b''.join(
    [OUTPUT_CHARS_RAW[v] for v in reversed(a_vec)]
))
