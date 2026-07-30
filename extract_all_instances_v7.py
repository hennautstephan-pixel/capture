from pathlib import Path
import struct
import json
import math


data = Path(
    "capture_block_full.bin"
).read_bytes()


print("Taille :", len(data))


def read_matrix(offset):

    if offset + 64 > len(data):
        return None

    try:
        m = struct.unpack_from(
            "<16f",
            data,
            offset
        )
    except:
        return None


    if any(
        math.isnan(x) or math.isinf(x)
        for x in m
    ):
        return None


    # matrice homogène Capture
    if abs(m[15]-1.0) > 0.01:
        return None


    # éviter les blocs aléatoires
    if (
        abs(m[12]) > 1000 or
        abs(m[13]) > 1000 or
        abs(m[14]) > 1000
    ):
        return None


    return m



instances=[]


print()
print("========== SCAN V7 ==========")


for pos in range(len(data)-82):


    matrix_offset = pos + 18


    m = read_matrix(
        matrix_offset
    )


    if not m:
        continue


    guid = data[
        pos:
        pos+16
    ]


    if guid.count(0) > 6:
        continue


    # éliminer GUID dans les floats
    before = data[pos-6:pos] if pos >= 6 else b""


    obj={

        "guid_offset":hex(pos),

        "matrix_offset":hex(matrix_offset),

        "guid":guid.hex(),

        "position":[
            round(m[12],4),
            round(m[13],4),
            round(m[14],4)
        ]

    }


    instances.append(obj)



# supprimer chevauchements
instances.sort(
    key=lambda x:int(x["guid_offset"],16)
)


clean=[]


for obj in instances:

    off=int(
        obj["guid_offset"],
        16
    )

    if clean:

        last=int(
            clean[-1]["guid_offset"],
            16
        )

        if off-last < 16:
            continue


    clean.append(obj)



print(
    "Instances trouvées :",
    len(clean)
)


for x in clean:

    print()
    print(
        x["guid_offset"],
        x["guid"]
    )

    print(
        "Matrice",
        x["matrix_offset"]
    )

    print(
        "XYZ",
        x["position"]
    )


with open(
    "capture_instances_v7.json",
    "w"
) as f:

    json.dump(
        clean,
        f,
        indent=4
    )


print()
print(
    "Export : capture_instances_v7.json"
)