from pathlib import Path
import struct
import json
import math


data = Path(
    "capture_block_full.bin"
).read_bytes()


print("Taille :", len(data))


# ==========================================
# Lecture matrice
# ==========================================

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


    # matrice Capture
    if abs(m[15]-1.0) > 0.001:
        return None


    return m



# ==========================================
# Recherche GUID candidats
# GUID = 16 octets
# matrice = GUID +18
# ==========================================

instances=[]


print()
print("========== SCAN INSTANCES ==========")



for pos in range(
    0,
    len(data)-82
):


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



    # éviter les blocs vides

    if guid.count(0) > 8:
        continue



    x,y,z = (
        m[12],
        m[13],
        m[14]
    )


    # élimination valeurs absurdes

    if (
        abs(x)>500 or
        abs(y)>500 or
        abs(z)>500
    ):
        continue



    item = {

        "guid_offset":hex(pos),

        "matrix_offset":hex(matrix_offset),

        "guid":guid.hex(),

        "position":[
            round(x,4),
            round(y,4),
            round(z,4)
        ]

    }


    # éviter doublons

    if item not in instances:

        instances.append(item)



print(
    "Instances trouvées :",
    len(instances)
)



# ==========================================
# Affichage
# ==========================================

for i in instances:

    print()
    print(
        i["guid_offset"],
        i["guid"]
    )

    print(
        "matrice",
        i["matrix_offset"]
    )

    print(
        "XYZ",
        i["position"]
    )



# ==========================================
# Export
# ==========================================

with open(
    "capture_instances_v5.json",
    "w",
    encoding="utf8"
) as f:

    json.dump(
        instances,
        f,
        indent=4
    )


print()
print(
"Export : capture_instances_v5.json"
)