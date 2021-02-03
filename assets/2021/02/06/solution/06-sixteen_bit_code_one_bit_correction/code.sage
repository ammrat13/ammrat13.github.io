import sys


# Matrix space and the matrix itself
HSpace = MatrixSpace(GF(2), 5, 16)
H = HSpace([
    1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0,
    1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0,
    0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0,
    1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0,
    0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1,
])

# Space for message vectors
MessageSpace = VectorSpace(GF(2), 16)


# Open and parse the file
file_name = sys.argv[1]
file_handle = open(file_name, 'r')

# Read everything in the file
while True:
    # Read until we have nothing left
    bit_chars = file_handle.read(17)
    if len(bit_chars) != 17:
        break

    # Convert the file to vectors
    bit_list = list( map(lambda c: int(c) - int(b'0'), bit_chars) )
    message_vec = MessageSpace(bit_list[0:16])
    syndrome_vec = H * message_vec

    # Try to correct
    corrected_message_vec = message_vec
    try:
        synd_idx = H.columns().index(syndrome_vec)
        corrected_message_vec[synd_idx] += 1
    except ValueError:
        # Item not found
        # Either no error or two-bit error
        pass


    # Make sure to strip off parity when we're done
    corrected_data_vec = corrected_message_vec[0:11]

    # Print the result as a bitstring
    # Have to do weird stuff with casts to get it to work
    print(''.join(map(str, list(corrected_data_vec))), end='')
