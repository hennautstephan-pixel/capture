from pathlib import Path
import struct


data = Path("capture_block_full.bin").read_bytes()


objects = {
    "OBJ1":0x2D8A,
    "OBJ2":0x314E
}


for name,pos in objects.items():

    print("\n====",name,"====")

    for i in range(pos-60,pos,4):

        v=struct.unpack("<I",data[i:i+4])[0]

        if v < 20:
            print(hex(i),v)