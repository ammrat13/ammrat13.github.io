EXTRA_DIGITS = 32
TARGET = 0x3C456DE6

K.<x> = GF(2**32, modulus = 0x104C11DB7.digits(2))

TARGET = TARGET.digits(2)
TARGET = TARGET + [0] * (32 - len(TARGET))
TARGET = sum(map(lambda iv: (1-iv[1]) * x**(31-iv[0]), enumerate(TARGET)))


msg = [
    1, 1, 1, 0, 0, 0, 1, 0, # G
    0, 1, 0, 0, 1, 1, 1, 0, # r
    1, 0, 1, 0, 0, 1, 1, 0, # e
    1, 0, 0, 1, 1, 1, 1, 0, # y
    0, 0, 0, 1, 0, 0, 1, 0, # H
    1, 0, 0, 0, 0, 1, 1, 0, # a
    0, 0, 1, 0, 1, 1, 1, 0, # t
    1, 1, 1, 0, 0, 0, 1, 0, # G
    0, 0, 1, 0, 1, 0, 1, 0, # T
] + EXTRA_DIGITS * [
    0, 0, 0, 0, 1, 1, 0, 0, # 0
]
rem = x^30 + x^26 + x^25 + x^23 + x^21 + x^19 + x^18 + x^17 + x^16 + x^14 + x^13 + x^10 + x^6 + x^3 + 1
for (i, d) in enumerate(msg):
    rem *= x
    rem += d
rem *= x**32

m = []
for i in range(EXTRA_DIGITS-1, -1, -1):
    for j in [7]:
        nv = x ** (32 + 8*i + j)
        nc = nv.polynomial().list()
        m.append(nc + [0] * (32 - len(nc)))
M = matrix(GF(2), m).T

delt = TARGET - rem
delt = delt.polynomial().list()
delt += [0] * (32 - len(delt))
delt = vector(GF(2), delt)
print(M \ delt)
