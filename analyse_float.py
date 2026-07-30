from pathlib import Path
import struct

inner = Path("decompressed_block.bin").read_bytes()

for name,pos in [
    ("Ape Labs",1986),
    ("Nanlux",2098)
]:
    print("\n====", name, "====")

    start = pos - 80

    for i in range(start,pos,4):
        value = struct.unpack("<f", inner[i:i+4])[0]

        if abs(value) < 1000:
            print(i, round(value,4))