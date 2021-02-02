import struct
import sys

file_name = sys.argv[1]
file_contents = open(file_name, 'rb').read()
float_iter = struct.iter_unpack('<e', file_contents)
for f in float_iter:
    print(1 if f[0] > 0 else 0, end='')
