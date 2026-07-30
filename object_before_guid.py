from pathlib import Path
import struct


data = Path("capture_block_full.bin").read_bytes()


for name,pos in [
    ("OBJ1",0x2D8A),
    ("OBJ2",0x314E)
]:

    print("\n====",name,"====")

    start = pos-120

    for i in range(start,pos,4):
        v = struct.unpack("<I",data[i:i+4])[0]

        print(
            hex(i),
            v,
            hex(v)
        )