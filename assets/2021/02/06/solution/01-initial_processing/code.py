import struct
import sys

file_name = sys.argv[1]
file_contents = open(file_name, 'rb').read()
float_iter = struct.iter_unpack('<e', file_contents)
for f in float_iter:
    print(f[0])
