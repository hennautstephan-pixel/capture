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

    pos=data.find(guid)

    print("\n====",name,pos,"====")

    for i in range(pos-64,pos,4):

        if i>=0:

            v=struct.unpack(
                "<I",
                data[i:i+4]
            )[0]

            print(
                i,
                v
            )