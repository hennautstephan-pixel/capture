from pathlib import Path
import re
import struct


data = Path("capture_block_full.bin").read_bytes()

start = 0x2D20
end = 0x2E00


print("ASCII :")

for m in re.finditer(rb'[\x20-\x7E]{4,}', data[start:end]):
    print(
        hex(start+m.start()),
        m.group().decode(errors="ignore")
    )


print("\nFLOATS :")

for i in range(start,end-4,4):
    v=struct.unpack("<f",data[i:i+4])[0]

    if abs(v)<1000 and v!=0:
        print(hex(i),round(v,4))