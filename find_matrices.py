from pathlib import Path
import struct


data = Path(
    "capture_block_full.bin"
).read_bytes()


guids = {
    "Ape Labs":
    bytes.fromhex(
        "82 1c 75 08 be 3d 44 c8 93 0e 82 fc 29 e8 6e 60"
    ),

    "Nanlux":
    bytes.fromhex(
        "f2 db fd 8a 6f 6d 4e 6c be c6 75 0a 9f 24 5b 21"
    )
}


for name,guid in guids.items():

    pos = data.find(guid)

    print("\n====",name,"GUID",pos,"====")

    start = pos + 16
    end = start + 256

    for off in range(start,end-48,4):

        vals = struct.unpack(
            "<12f",
            data[off:off+48]
        )

        if all(
            abs(v)<1000 for v in vals
        ):

            print(
                off,
                [
                    round(v,3)
                    for v in vals
                ]
            )