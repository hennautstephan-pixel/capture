from pathlib import Path
import struct
import json
import math


# =====================================================
# Chargement
# =====================================================

data = Path(
    "capture_block_full.bin"
).read_bytes()


print()
print("Fichier : capture_block_full.bin")
print("Taille :", len(data))


# =====================================================
# Signature Capture trouvée dans les instances
# =====================================================

SIGNATURES = [

    bytes.fromhex(
        "00 01 00 01 01 01"
    ),

    bytes.fromhex(
        "01 00 01 01 01"
    )

]



# =====================================================
# Lecture matrice
# =====================================================

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



    # valeurs invalides

    for x in m:

        if math.isnan(x) or math.isinf(x):

            return None



    # matrice homogène

    if abs(m[15]-1.0) > 0.001:

        return None



    # colonnes translation

    if abs(m[3]) > 0.001:
        return None

    if abs(m[7]) > 0.001:
        return None

    if abs(m[11]) > 0.001:
        return None



    # position réaliste

    if abs(m[12]) > 500:
        return None

    if abs(m[13]) > 500:
        return None

    if abs(m[14]) > 500:
        return None



    return m



# =====================================================
# Recherche instances
# =====================================================

instances=[]


print()
print("========== SCAN INSTANCES V6 ==========")



for sig in SIGNATURES:


    start = 0


    while True:


        p = data.find(
            sig,
            start
        )


        if p == -1:
            break



        # GUID après signature

        guid_offset = p + len(sig)



        guid = data[
            guid_offset:
            guid_offset+16
        ]



        # matrice après GUID + padding Capture

        matrix_offset = guid_offset + 18



        matrix = read_matrix(
            matrix_offset
        )



        if matrix:


            obj = {

                "signature_offset":
                    hex(p),

                "guid_offset":
                    hex(guid_offset),

                "matrix_offset":
                    hex(matrix_offset),


                "guid":
                    guid.hex(),


                "position":[

                    round(matrix[12],4),
                    round(matrix[13],4),
                    round(matrix[14],4)

                ],


                "matrix":[

                    round(x,4)
                    for x in matrix

                ]

            }



            # suppression doublons

            if not any(
                x["guid_offset"] ==
                obj["guid_offset"]
                for x in instances
            ):

                instances.append(obj)



        start = p + 1



# =====================================================
# Nettoyage GUID proches
# =====================================================

instances.sort(
    key=lambda x:
    int(x["guid_offset"],16)
)



clean=[]


for obj in instances:


    offset=int(
        obj["guid_offset"],
        16
    )


    if clean:

        last=int(
            clean[-1]["guid_offset"],
            16
        )


        if offset-last < 32:

            continue



    clean.append(obj)



instances=clean



# =====================================================
# Résultat
# =====================================================

print()
print(
    "Instances valides :",
    len(instances)
)



for i in instances:

    print()
    print(
        "GUID",
        i["guid_offset"],
        i["guid"]
    )

    print(
        "Matrice",
        i["matrix_offset"]
    )

    print(
        "XYZ",
        i["position"]
    )



# =====================================================
# Export
# =====================================================

with open(
    "capture_instances_v6.json",
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
    "Export : capture_instances_v6.json"
)