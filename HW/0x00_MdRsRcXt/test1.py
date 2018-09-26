import hashlib
import sys
import binascii
import struct

if len(sys.argv) != 2:
    print('Usage: python3 task.py <password>')
    exit(255)


def md5(s):
    return hashlib.md5(s.encode('ascii')).hexdigest()


hashs = ''.join(map(md5, sys.argv[1]))
def split_by_n( seq, n ):
    """A generator to divide a sequence into chunks of n units."""
    while seq:
        yield seq[:n]
        seq = seq[n:]
print(list(split_by_n(hashs,32)))
