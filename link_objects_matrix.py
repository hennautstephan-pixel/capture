from pathlib import Path
import struct


data = Path(
    "capture_block_full.bin"
).read_bytes()


objects = {
"Ape Labs": bytes.fromhex(
"82 1c 75 08 be 3d 44 c8 93 0e 82 fc 29 e8 6e 60"
),

"Nanlux": bytes.fromhex(
"f2 db fd 8a 6f 6d 4e 6c be c6 75 0a 9f 24 5b 21"
)
}


for name,guid in objects.items():

    pos=data.find(guid)

    print("\n====",name,pos,"====")

    # recherche de floats/matrices dans les 5000 octets suivants
    start=pos
    end=pos+5000

    found=0

    for i in range(start,end-64,4):

        vals=struct.unpack(
            "<16f",
            data[i:i+64]
        )

        if (
            abs(vals[15]-1)<0.001
            and
            all(abs(v)<1000 for v in vals)
        ):

            print(
                "Matrice",
                i,
                "pos=",
                (
                    round(vals[12],3),
                    round(vals[13],3),
                    round(vals[14],3)
                )
            )

            found+=1

            if found>5:
                break