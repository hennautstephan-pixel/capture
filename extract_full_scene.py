from pathlib import Path
import struct
import json


# =====================================================
# Chargement fichier Capture
# =====================================================

data = Path("capture_block_full.bin").read_bytes()


# =====================================================
# Objets connus + GUID instance
# (GUID validés par analyse du fichier)
# =====================================================

objects = {

    "Ape Labs Neon Tube":
    {
        "guid":
        "5fb40e612ab74b58a00fc75047ec4bae"
    },


    "Nanlux":
    {
        "guid":
        "8ed0691bb3d24d0ba99c57303d3010ab"
    },

}


# =====================================================
# Lecture matrice Capture
# =====================================================

def read_matrix(offset):

    return struct.unpack(
        "<16f",
        data[offset:offset+64]
    )



# =====================================================
# Recherche matrice après GUID
# =====================================================

def find_matrix(guid_offset):

    start = guid_offset + 16


    for pos in range(
        start,
        start + 500
    ):

        try:
            m = read_matrix(pos)

        except:
            continue


        # matrice homogène 4x4
        if abs(m[15]-1.0) < 0.01:


            x,y,z = m[12:15]


            if (
                abs(x)<1000
                and abs(y)<1000
                and abs(z)<1000
            ):

                return pos,m


    return None,None



# =====================================================
# Extraction
# =====================================================

scene=[]


print()
print("========== EXTRACTION SCENE ==========")


for name,obj in objects.items():


    guid = bytes.fromhex(
        obj["guid"]
    )


    guid_pos = data.find(guid)


    print()
    print("----------------------------")
    print(name)


    if guid_pos == -1:

        print(
            "GUID non trouvé"
        )

        continue



    print(
        "GUID offset :",
        hex(guid_pos)
    )


    matrix_pos,matrix = find_matrix(
        guid_pos
    )


    if matrix is None:

        print(
            "Matrice non trouvée"
        )

        continue



    print(
        "Matrice offset :",
        hex(matrix_pos)
    )


    position = [
        round(matrix[12],4),
        round(matrix[13],4),
        round(matrix[14],4)
    ]


    rotation = [
        round(v,4)
        for v in matrix[:12]
    ]


    print(
        "Position :",
        position
    )


    print(
        "Rotation :",
        rotation
    )



    scene.append(
        {
            "name": name,
            "guid_instance": obj["guid"],
            "guid_offset": hex(guid_pos),
            "matrix_offset": hex(matrix_pos),
            "position": position,
            "rotation": rotation
        }
    )



# =====================================================
# Export JSON
# =====================================================

with open(
    "capture_scene.json",
    "w",
    encoding="utf-8"
) as f:


    json.dump(
        scene,
        f,
        indent=4,
        ensure_ascii=False
    )



print()
print(
    "Export terminé : capture_scene.json"
)

print(
    "Objets extraits :",
    len(scene)
)