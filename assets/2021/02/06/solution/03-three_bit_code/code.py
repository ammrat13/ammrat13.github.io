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
