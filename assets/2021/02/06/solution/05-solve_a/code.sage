import sys


# Arbitrarily set
# Shouldn't be too high to make corruption less likely
N = 20

# Spaces for all our matrices and vectors
DSpace = MatrixSpace(GF(2), N, 11)
ASpace = MatrixSpace(GF(2), 11, 5)
PSpace = MatrixSpace(GF(2), N, 5)
DVecSpace = VectorSpace(GF(2), 11)
PVecSpace = VectorSpace(GF(2), 5)

# Create storage for our matrices and vectors
D = DSpace()
P = PSpace()


# Utility functions to convert a string of ASCII '0' and '1' to vectors
def ascii_to_vec(string, vecType):
    strNumsMap = map(lambda c: int(c) - int(b'0'), string)
    return vecType(list(strNumsMap))

# Parse the data into the matrices
file_name = sys.argv[1]
file_handle = open(sys.argv[1], 'r')
for r in range(N):
    bytes = file_handle.read(17)
    D.set_row(r, ascii_to_vec(bytes[0:11], DVecSpace))
    P.set_row(r, ascii_to_vec(bytes[11:16], PVecSpace))


# Solve
A = D.solve_right(P)
print(A)
