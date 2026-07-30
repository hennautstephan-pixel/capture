from pathlib import Path
import struct
import re
import json


data = Path(
    "capture_block_full.bin"
).read_bytes()



def read_matrix(pos):

    return struct.unpack(
        "<16f",
        data[pos:pos+64]
    )



def valid_matrix(m):

    return (
        abs(m[3]) < 0.001 and
        abs(m[7]) < 0.001 and
        abs(m[11]) < 0.001 and
        abs(m[15]-1.0) < 0.001
    )



names = [
    b"Ape Labs Neon Tube",
    b"Plancher",
    b"Nanlux",
    b"Plancher SKP",
    b"Piano",
    b"Mandarine",
    b"Ampoule",
    b"Pendrillons",
    b"Trussxxx",
    b"Table",
    b"Perche",
    b"PC face"
]



results=[]



print()
print("========== SCAN MATRICES ==========")



# scan complet

for pos in range(
    0,
    len(data)-64,
    4
):

    try:

        m = read_matrix(pos)

    except:

        continue


    if not valid_matrix(m):

        continue


    x,y,z=m[12:15]


    # élimine les faux blocs

    if (
        abs(x)>500 or
        abs(y)>500 or
        abs(z)>500
    ):

        continue



    context=data[
        max(0,pos-200):
        pos
    ]



    found=None


    for n in names:

        if n in context:

            found=n.decode(
                "utf8",
                errors="ignore"
            )

            break



    if found:


        print()
        print(
            found
        )

        print(
            "Matrice:",
            hex(pos)
        )

        print(
            "XYZ:",
            [
                round(x,3),
                round(y,3),
                round(z,3)
            ]
        )


        results.append({

            "name":found,

            "matrix_offset":hex(pos),

            "position":[
                x,y,z
            ],

            "rotation":[
                *m[:12]
            ]

        })



print()
print(
"Trouvés :",
len(results)
)



with open(
    "scene_instances_scan.json",
    "w",
    encoding="utf8"
) as f:

    json.dump(
        results,
        f,
        indent=4,
        ensure_ascii=False
    )