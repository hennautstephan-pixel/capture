from pathlib import Path
import struct

data = Path("capture_block_full.bin").read_bytes()

start = 0x2D34

for i in range(start,start+80,4):
    v = struct.unpack("<I",data[i:i+4])[0]
    print(hex(i), v, hex(v))