from pathlib import Path
import struct


data = Path("capture_block_full.bin").read_bytes()


for i in range(0,len(data)-64,4):

    vals = struct.unpack(
        "<16f",
        data[i:i+64]
    )

    # matrice homogène possible
    if (
        abs(vals[15]-1)<0.001 and
        abs(vals[3])<0.001 and
        abs(vals[7])<0.001 and
        abs(vals[11])<0.001
    ):
        print(
            "Matrice possible",
            i,
            [
                round(v,3)
                for v in vals
            ]
        )