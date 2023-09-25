import struct
import sys
 
def rc4(data, key):
    S = [i for i in range(256)]
    j = 0
    out = []
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(char ^ S[(S[i] + S[j]) % 256])
    return bytearray(out)
 
 
KEYMASK = [0xB1, 0x54, 0x45, 0x57, 0xA7, 0xC4, 0x64, 0x2E,
           0x98, 0xD8, 0xB1, 0x1A, 0x0B, 0xAA, 0xD8, 0x8E,
           0x7F, 0x1E, 0x5B, 0x8D, 0x08, 0x67, 0x96, 0xCB,
           0xAA, 0x11, 0x50, 0x84, 0x17, 0x46, 0xA3, 0x30]
 
if len(sys.argv) <= 1:
    print('usage: script.py vgc_X_Y_Z.log')
    exit()
 
DATA = open(sys.argv[1], 'rb').read()
DATA = DATA[4:]
REAL_KEY = [DATA[i] ^ KEYMASK[i] for i in range(32)]
DATA = DATA[32:]
while len(DATA) > 0:
    BLOCK_LEN = struct.unpack('<L', DATA[:4])[0]
    DATA = DATA[4:]
    print(rc4(DATA[:BLOCK_LEN], REAL_KEY).decode('utf-16'))
    DATA = DATA[BLOCK_LEN:]
