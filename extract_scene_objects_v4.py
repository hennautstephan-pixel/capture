from pathlib import Path
import struct
import json
import math


# ==================================================
# Chargement fichier
# ==================================================

data = Path(
    "capture_block_full.bin"
).read_bytes()


print()
print("Fichier : capture_block_full.bin")
print("Taille :", len(data))


# ==================================================
# GUID instances connus
# (trouvés dans le fichier Capture)
# ==================================================

objects = {

    "Ape Labs Neon Tube":
        bytes.fromhex(
            "5fb40e612ab74b58a00fc75047ec4bae"
        ),

    "Nanlux":
        bytes.fromhex(
            "8ed0691bb3d24d0ba99c57303d3010ab"
        )

}



# ==================================================
# Recherche GUID
# ==================================================

def find_guid(guid):

    positions=[]

    start=0

    while True:

        p=data.find(
            guid,
            start
        )

        if p==-1:
            break

        positions.append(p)

        start=p+1


    return positions



# ==================================================
# Lecture matrice Capture
# GUID +18
# ==================================================

def read_matrix(guid_offset):

    matrix_offset = guid_offset + 18


    if matrix_offset+64 > len(data):
        return None,None



    values=struct.unpack_from(
        "<16f",
        data,
        matrix_offset
    )



    # contrôle matrice

    if abs(values[15]-1.0)>0.001:

        return None,None



    if any(
        math.isnan(x) or math.isinf(x)
        for x in values
    ):

        return None,None



    return matrix_offset, values



# ==================================================
# Extraction
# ==================================================

scene=[]


print()
print("========== EXTRACTION SCENE ==========")



for name,guid in objects.items():


    print()
    print("-----------------------------")
    print(name)



    positions=find_guid(guid)



    if not positions:

        print("GUID non trouvé")
        continue



    for guid_offset in positions:


        matrix_offset,matrix = read_matrix(
            guid_offset
        )


        if matrix is None:

            print(
                "GUID trouvé mais matrice invalide :",
                hex(guid_offset)
            )

            continue



        position=[

            round(matrix[12],4),
            round(matrix[13],4),
            round(matrix[14],4)

        ]



        rotation=[

            round(x,4)
            for x in matrix[:12]

        ]



        print(
            "GUID offset :",
            hex(guid_offset)
        )

        print(
            "Matrice offset :",
            hex(matrix_offset)
        )

        print(
            "Position :",
            position
        )



        scene.append({

            "name":name,

            "guid_offset":
                hex(guid_offset),

            "matrix_offset":
                hex(matrix_offset),

            "position":
                position,

            "rotation":
                rotation

        })



# ==================================================
# Export JSON
# ==================================================

with open(
    "capture_scene_full.json",
    "w",
    encoding="utf8"
) as f:


    json.dump(
        scene,
        f,
        indent=4,
        ensure_ascii=False
    )



print()
print("==============================")
print("Export terminé")
print(
    "Objets extraits :",
    len(scene)
)

print(
    "Fichier : capture_scene_full.json"
)
print("==============================")